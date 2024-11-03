import py4vasp
import argparse

parser = argparse.ArgumentParser(
    description="取得したい情報をオプションで指定してください。"
)
parser.add_argument(
    "-b",
    "--band",
    type=int,
    nargs="*",
    help="バンドの番号を指定してください。例: 13 14",
)
parser.add_argument(
    "-f", "--filename", type=str, help="出力ファイル名を指定してください。\n 例) band"
)

# 引数を解析
args = parser.parse_args()
band = args.band if args.band is not None else []
filename = args.filename if args.filename is not None else ""

if len(filename) == 0:
    filename = "band.txt"
elif "." in filename:
    filename = filename.split(".")[0] + ".txt"
else:
    filename = filename + ".txt"

with open("KPOINTS", "r") as input_file:
    kpoints = input_file.readline()[4:]

with open("EIGENVAL", "r") as input_file:
    eigenvalues = input_file.readlines()[7:]

# データの書き出し
with open(filename, "w") as output_file:
    # kpointsの書き出し
    kpoints_header = "kpoints_index   labels"  # indexは0からスタート
    output_file.write(kpoints_header + "\n")
    output_file.write("-" * (len(kpoints_header) + 30) + "\n")

    # バンドの書き出し
    bands_header = "band_numbers   energies_per_kpoints"
    output_file.write(bands_header + "\n")
    output_file.write("-" * (len(bands_header) + 30) + "\n")

print(f"処理が完了しました。出力は '{filename}' に保存されました。")
