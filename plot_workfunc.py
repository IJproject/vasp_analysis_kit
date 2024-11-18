# legend設定と、格子ベクトルでの規格化はできていない

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
    help="（必須）読み込むファイル名を指定してください。 例) workfunc.txt",
)
parser.add_argument(
    "-o",
    "--outputfile",
    type=str,
    help="出力するファイル名を指定してください。 例) workfunc.png",
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
    outputfile = "workfunc.png"
elif "." in outputfile:
    outputfile = outputfile.split(".")[0] + ".png"
else:
    outputfile = outputfile + ".png"

# フェルミエネルギー
fermi_energy = 100
with open("OUTCAR", "r") as file:
    for line in file:
        if "E-fermi" in line:
            fermi_energy = float(line.split()[2])

# x軸のスケール合わせ
with open("POSCAR", "r") as file:
    POSCAR_lines = file.readlines()
    lattice_constant = float(POSCAR_lines[1].split()[0])
    lattice_c_length = float(POSCAR_lines[4].split()[2])

# ファイルの読み込み
with open(inputfile, "r") as file:
    lines = file.readlines()

# データの整形
data = np.loadtxt(lines[1:], unpack=True)
y = data[1] - fermi_energy
x = data[0] * lattice_constant * lattice_c_length / len(y)

if xrange is None:
    xrange = [0, max(x)]

# プロット
gp.plot(
    (x, y),
    xrange=xrange,
    yrange=yrange,
    terminal=f"png size 1200,900",
    output=outputfile,
    _with="lines lw 3 lc rgb 'blue'",
    _set=[
        "xtics font 'Times New Roman,20' offset 0,-1",
        "ytics font 'Times New Roman,20'",
        "xlabel 'z  (\305)' font 'Times New Roman,24' offset 0,-2",
        "ylabel 'V_z - E_f   (eV)' font 'Times New Roman,24' offset -1,0",
        "lmargin 12",
        "rmargin 4",
        "tmargin 2",
        "bmargin 6",
        f"ytics add ({max(y)})"
    ],
)

print(f"処理が完了しました。出力は '{outputfile}' に保存されました。")
