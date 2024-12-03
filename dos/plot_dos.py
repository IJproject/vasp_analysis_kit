import argparse
import gnuplotlib as gp
import numpy as np
import os
import sys

parser = argparse.ArgumentParser(
    description="取得したい情報をオプションで指定してください。"
)
parser.add_argument(
    "-i",
    "--inputfile",
    type=str,
    help="（必須）読み込むファイル名を指定してください。 例) dos.txt",
)
parser.add_argument(
    "-o",
    "--outputfile",
    type=str,
    help="出力するファイル名を指定してください。 例) dos.png",
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
xrange = [args.xrange[0], args.xrange[1]] if args.xrange is not None else None
yrange = [args.yrange[0], args.yrange[1]] if args.yrange is not None else None

if len(inputfile) == 0:
    print("ファイル名をオプションで指定してください。")
    sys.exit(1)
if not os.path.exists(inputfile):
    print(f"指定されたファイル '{inputfile}' が見つかりません。")
    sys.exit(1)

if len(outputfile) == 0:
    outputfile = "dos.png"
elif "." in outputfile:
    outputfile = outputfile.split(".")[0] + ".png"
else:
    outputfile = outputfile + ".png"

# ファイルの読み込み
with open(inputfile, "r") as f:
    lines = f.readlines()

# データの整形
labels = lines[0].strip().split()
data = np.loadtxt(lines[2:], unpack=True)
x = data[0]
y_values = data[1:]

# プロット
plots = []
for i, y in enumerate(y_values):
    if i + 1 < len(labels):
        plots.append((x, y, {"legend": labels[i + 1]}))
    else:
        plots.append((x, y, {"legend": f"Data {i+1}"}))

gp.plot(
    *plots,
    xrange=xrange,
    yrange=yrange,
    terminal="png size 1200,900",
    output=outputfile,
    _with="lines",
    _set=[
        "xtics font 'Times New Roman,20' offset 0,-1",
        "noytics",
        "xlabel 'E - E_{VBM}  (eV)' font 'Times New Roman,24' offset 0,-2",
        "ylabel 'DOS  (eV^{-1})' font 'Times New Roman,24' offset -1,0",
        "lmargin 8",
        "rmargin 4",
        "tmargin 2",
        "bmargin 6",
    ],
)

print(f"処理が完了しました。出力は '{outputfile}' に保存されました。")
