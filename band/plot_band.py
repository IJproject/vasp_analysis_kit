import argparse
import os
import sys
import gnuplotlib as gp
import numpy as np

parser = argparse.ArgumentParser(
    description="取得したい情報をオプションで指定してください。"
)
parser.add_argument(
    "-i",
    "--inputfile",
    type=str,
    help="（必須）読み込むファイル名を指定してください。 例) band.txt",
)
parser.add_argument(
    "-o",
    "--outputfile",
    type=str,
    help="出力するファイル名を指定してください。 例) band.png",
)
parser.add_argument(
    "-b",
    "--band",
    type=int,
    nargs="*",
    help="バンドの番号を指定してください。例: 13 14",
)
parser.add_argument(
    "-x",
    "--xrange",
    type=float,
    nargs=2,
    help="x軸の変域を指定してください。 例: xmin xmax",
)
parser.add_argument(
    "-y",
    "--yrange",
    type=float,
    nargs=2,
    help="y軸の値域を指定してください。例: ymin ymax",
)


# 引数を解析
args = parser.parse_args()
inputfile = args.inputfile if args.inputfile is not None else ""
outputfile = args.outputfile if args.outputfile is not None else ""
band = args.band if args.band is not None else []
xrange = [args.xrange[0], args.xrange[1]] if args.xrange is not None else None
yrange = [args.yrange[0], args.yrange[1]] if args.yrange is not None else None

if len(inputfile) == 0:
    print("ファイル名をオプションで指定してください。")
    sys.exit(1)
if not os.path.exists(inputfile):
    print(f"指定されたファイル '{inputfile}' が見つかりません。")
    sys.exit(1)

if len(outputfile) == 0:
    outputfile = "band.png"
elif "." in outputfile:
    outputfile = outputfile.split(".")[0] + ".png"
else:
    outputfile = outputfile + ".png"

# ファイルの読み込み
with open(inputfile, "r") as f:
    lines = f.readlines()
    border_index = [i for i, line in enumerate(lines) if line == "\n"][0]
    kpoints_label = lines[2:border_index]
    eigenvalues = lines[border_index + 3 :]

# X軸方向のラベルの作成
xtics_labels = []
for label in kpoints_label:
    index, symbol = label.split()
    xtics_labels.append(f"'{symbol.strip()}' {index}")

# フェルミエネルギー
fermi_energy = 100
with open("OUTCAR", "r") as file:
    for line in file:
        if "E-fermi" in line:
            fermi_energy = float(line.split()[2])

all_lines_data = []
x_data = []
y_data = []

# データの処理
for line in eigenvalues:
    if line.strip() == "":
        if x_data and y_data:
            all_lines_data.append((np.array(x_data), np.array(y_data)))
            x_data = []
            y_data = []
    elif band:
        values = line.split()
        if len(values) >= 3 and int(values[0]) in band:
            x_data.append(float(values[1]))
            y_data.append(float(values[2]) - fermi_energy)
    else:
        values = line.split()
        if len(values) >= 3:
            x_data.append(float(values[1]))
            y_data.append(float(values[2]) - fermi_energy)

if x_data and y_data:
    all_lines_data.append((np.array(x_data), np.array(y_data)))

# gnuplotlibでプロット
gp.plot(
    *[(x, y, {"with": 'lines lw 3 lc rgb "blue"'}) for x, y in all_lines_data],
    xrange=xrange,
    yrange=yrange,
    terminal="png size 1200,900",
    output=outputfile,
    legend=None,
    _set=[
        f"xtics ({', '.join(xtics_labels)}) font 'Times New Roman,20' offset 0,-1",
        "ytics font 'Times New Roman,20'",
        "ylabel 'E - E_f  (eV)' font 'Times New Roman,24' offset -1,0",
        "lmargin 12",
        "rmargin 4",
        "tmargin 2",
        "bmargin 4",
    ],
)

print(f"処理が完了しました。出力は '{outputfile}' に保存されました。")
