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
    help="（必須）読み込むファイル名を指定してください。 例) eels.txt",
)
parser.add_argument(
    "-o",
    "--outputfile",
    type=str,
    help="出力するファイル名を指定してください。 例) eels.png",
)
parser.add_argument(
    "-r",
    "--reference",
    type=str,
    help="文献値を含むファイル名を指定してください。 例) eels-ref.txt",
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
reference = args.reference if args.reference is not None else ""
xrange = [args.xrange[0], args.xrange[1]] if args.xrange is not None else None
yrange = [args.yrange[0], args.yrange[1]] if args.yrange is not None else None

if len(inputfile) == 0:
    print("ファイル名をオプションで指定してください。")
    sys.exit(1)
if not os.path.exists(inputfile):
    print(f"指定されたファイル '{inputfile}' が見つかりません。")
    sys.exit(1)

if len(outputfile) == 0:
    outputfile = "eels.png"
elif "." in outputfile:
    outputfile = outputfile.split(".")[0] + ".png"
else:
    outputfile = outputfile + ".png"

if len(reference) == 0:
    reference = "eels-ref.txt"
elif "." in reference:
    reference = reference.split(".")[0] + ".txt"
else:
    reference = reference + ".txt"

# ファイルの読み込み
with open(inputfile, "r") as f:
    input_lines = f.readlines()
with open(reference, "r") as f:
    ref_lines = f.readlines()

# データの整形
labels = input_lines[0].strip().split()
input_data = np.loadtxt(input_lines[2:], unpack=True)
input_x = input_data[0]
input_y = input_data[1:]
input_y = np.array([y / np.max(y) if np.max(y) != 0 else y for y in input_y])
input_plots = [
    (
        input_x,
        y,
        {
            "with": "lines",
            "legend": labels[i + 1] if i + 1 < len(labels) else f"Data {i+1}",
        },
    )
    for i, y in enumerate(input_y)
]

ref_data = np.loadtxt(ref_lines[0:], unpack=True)
ref_x = ref_data[0]
ref_y = ref_data[1]
ref_plots = [ref_x, ref_y]

gp.plot(
    *input_plots,
    (*ref_plots, {"with": "lines", "legend": "Experiment(reference)"}),
    xlabel="Energy loss (eV)",
    ylabel="Intensit (percentage of maximum intensity)",
    xrange=xrange,
    yrange=yrange,
    terminal=f"png size 800,600",
    output=outputfile,
    _set=[
        "key left top",
        "key box",
        "key reverse",
        "key Left",
        "key spacing 1.7",
        "nogrid",
    ],
)
