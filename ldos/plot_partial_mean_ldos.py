import argparse
import gnuplotlib as gp
import numpy as np
import os
import sys
import glob

# マジックナンバー
layer_thickness = 9.5466667
layer_count = 6

parser = argparse.ArgumentParser(
    description="取得したい情報をオプションで指定してください。"
)
parser.add_argument(
    "-d",
    "--directory",
    type=str,
    help="（必須）データが入ったフォルダ名を指定してください。 例) ldos_data",
)
parser.add_argument(
    "-l",
    "--layers",
    type=int,
    nargs="*",
    help="（必須）何番目の層のLDOSを取得したいのかを指定してください。 例) 4",
)
parser.add_argument(
    "-o",
    "--outputfile",
    type=str,
    help="出力するファイル名を指定してください。 例) ldos.png",
)
# 引数を解析
args = parser.parse_args()
directory = args.directory if args.directory is not None else ""
layers = args.layers if args.layers is not None else []
outputfile = args.outputfile if args.outputfile is not None else ""

if len(directory) == 0:
    print("フォルダ名をオプションで指定してください。")
    sys.exit(1)
if not os.path.exists(directory):
    print(f"指定されたフォルダ '{directory}' が見つかりません。")
    sys.exit(1)

if layers == []:
    print("層番号をオプションで指定してください。")
    sys.exit(1)

if len(outputfile) == 0:
    outputfile = "ldos.png"
elif "." in outputfile:
    outputfile = outputfile.split(".")[0] + ".png"
else:
    outputfile = outputfile + ".png"

# x軸のスケール合わせ
with open("POSCAR", "r") as file:
    POSCAR_lines = file.readlines()
    lattice_c_length = float(POSCAR_lines[4].split()[2])

# フェルミエネルギー
# fermi_energy = 100
# with open("OUTCAR", "r") as file:
#     for line in file:
#         if "E-fermi" in line:
#             fermi_energy = float(line.split()[2])
fermi_energy = 2.619

# プロット設定を読み込む
with open(directory + "/DENSITYTOOL.IN", "r") as file:
    setup_lines = file.readlines()
    emin = float(setup_lines[1].split()[0]) - fermi_energy
    emax = float(setup_lines[2].split()[0]) - fermi_energy
    nen = int(setup_lines[3].split()[0])

file_pattern = directory + "/LDOS.R3.*.dat"
files = sorted(glob.glob(file_pattern))

# データを読み込む
tmp_data = []
max_intensity = 0
tmp_data = [[] for _ in layers]
data = []

for file in files:
    with open(file, "r") as f:
        lines = f.readlines()
        line_count = len(lines)
        for layer_index, layer in enumerate(layers):
            min_layer_count = int(
                line_count * layer_thickness * (layer - 1) / lattice_c_length
            )
            max_layer_count = int(
                line_count * layer_thickness * layer / lattice_c_length
            )
            sum_intensity = 0
            for index, line in enumerate(lines):
                position, energy, intensity = line.split()
                if min_layer_count <= index and index <= max_layer_count:
                    sum_intensity += float(intensity)
                elif index == max_layer_count + 1:
                    tmp_data[layer_index].append((float(energy), float(sum_intensity)))
                    max_intensity = max(max_intensity, float(sum_intensity))
                    sum_intensity = 0

# データの処理
for index, item in enumerate(tmp_data):
    processed_tmp_data = np.array(item)
    energy = processed_tmp_data[:, 0] - fermi_energy
    intensity = (
        processed_tmp_data[:, 1] / max_intensity
        if max_intensity != 0
        else 0
    )
    data.append((energy, intensity))

gp.plot(
    *[
        (energy, intensity, {"with": "lines lw 3", "legend": f"Layer {layers[i]}"})
        for i, (energy, intensity) in enumerate(data)
    ],
    terminal="png size 1200,900",
    output=outputfile,
    yrange=[0, 1],
    xrange=[emin, emax],
    _with="lines",
    _set=[
        "xtics font 'Times New Roman,20' offset 0,-1",
        "noytics",
        "xlabel 'E - E_{F}  (eV)' font 'Times New Roman,24' offset 0,-2",
        "ylabel 'Intensity' font 'Times New Roman,24' offset -1,0",
        "lmargin 8",
        "rmargin 4",
        "tmargin 2",
        "bmargin 6",
        "key font 'Times New Roman,18'",
        "key spacing 1.4",
    ],
)

print(f"処理が完了しました。出力は '{outputfile}' に保存されました。")
