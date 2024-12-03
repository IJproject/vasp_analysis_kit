import argparse
import gnuplotlib as gp
import numpy as np
import os
import sys
import glob

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
    "-o",
    "--outputfile",
    type=str,
    help="出力するファイル名を指定してください。 例) band.png",
)
# 引数を解析
args = parser.parse_args()
directory = args.directory if args.directory is not None else ""
outputfile = args.outputfile if args.outputfile is not None else ""

if len(directory) == 0:
    print("フォルダ名をオプションで指定してください。")
    sys.exit(1)
if not os.path.exists(directory):
    print(f"指定されたフォルダ '{directory}' が見つかりません。")
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

for file in files:
    with open(file, "r") as f:
        lines = f.readlines()
        line_count = len(lines)
        for line in lines:
            x, y, intensity = line.split()
            max_intensity = max(max_intensity, float(intensity))
            tmp_data.append((float(x), float(y), float(intensity)))

# プロット用データに変換
data = np.array(tmp_data)
x = data[:, 0] * lattice_c_length / line_count
y = data[:, 1] - fermi_energy
intensity = data[:, 2] / max_intensity

# プロット
gp3 = gp.gnuplotlib(
    _3d=True,
    terminal="png size 1200,900",
    output=outputfile,
)
gp3.plot(
    (x, y, intensity, {"with": "points palette", "using": "1:2:3"}),
    xrange=[0, lattice_c_length],
    yrange=[emin, emax],
    zrange=[0, 1],
    _set=[
        "xtics font 'Times New Roman,20' offset 0,-1",
        "ytics font 'Times New Roman,20'",
        "xlabel 'z (\305)' font 'Times New Roman,24' offset 0,-2.5",
        "ylabel 'E - E_F  (eV)' font 'Times New Roman,24' offset -4,0",
        "lmargin 12",
        "rmargin 4",
        "tmargin 2",
        "bmargin 4",
        # "nogrid",
        "palette defined (0 '0xffffff', 1 '0xff0000')",
        "view map",
        "cbrange [0:1]",
        "cblabel 'Intensity' font 'Times New Roman,24' offset 3,0",
    ],
)
