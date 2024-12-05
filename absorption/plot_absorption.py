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
    help="（必須）読み込むファイル名を指定してください。 例) absorption.txt",
)
parser.add_argument(
    "-o",
    "--outputfile",
    type=str,
    help="出力するファイル名を指定してください。 例) absorption.png",
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
    outputfile = "absorption.png"
elif "." in outputfile:
    outputfile = outputfile.split(".")[0] + ".png"
else:
    outputfile = outputfile + ".png"

# ファイルの読み込み
with open(inputfile, "r") as file:
    lines = file.readlines()
    empty_line_count = sum(1 for line in lines if line == "\n")

    # データの書き出し
    label = ""
    plots = []
    x = []
    y = []
    for line in lines:
        line = line.split()
        if line == []:
            print(1)
            plots.append(
                (
                    np.array(x),
                    np.array(y) / max(y),
                    {"with": "lines lw 3", "legend": label},
                )
            )
            x = []
            y = []
        elif len(line) == 1:
            continue
        elif len(line) == 2 and line[0] == "energies":
            label = line[1]
        else:
            x.append(float(line[0]))
            y.append(float(line[1]))

print(plots)

gp.plot(
    *[(x, y, setting) for x, y, setting in plots],
    xrange=xrange,
    yrange=yrange,
    terminal=f"png size 1200,900",
    output=outputfile,
    _set=[
        "xtics font 'Times New Roman,20' offset 0,-1",
        "noytics",
        "xlabel 'Energy Loss  (eV)' font 'Times New Roman,24' offset 0,-2",
        "ylabel 'Intensity (percentage of maximum intensity)' font 'Times New Roman,24' offset -1,0",
        "lmargin 8",
        "rmargin 4",
        "tmargin 2",
        "bmargin 6",
        "key left top",
        "key reverse",
        "key font 'Times New Roman,18'",
        "key Left",
        "key spacing 1.4",
        "nogrid",
    ],
)

print(f"処理が完了しました。出力は '{outputfile}' に保存されました。")
