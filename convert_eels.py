import argparse
import re
import sys

parser = argparse.ArgumentParser(
    description="取得したい情報をオプションで指定してください。"
)
parser.add_argument(
    "-c",
    "--columnname",
    type=str,
    help="（必須）カラムの名前を指定してください。グラフで凡例として使用します。 例) reference",
)
parser.add_argument(
    "-f", "--filename", type=str, help="出力ファイル名を指定してください。\n 例) eels"
)
# 引数を解析
args = parser.parse_args()
column_name = args.columnname if args.columnname is not None else ""
filename = args.filename if args.filename is not None else ""

if len(column_name) == 0:
    print("データのカラムの名前を指定してください。グラフで凡例として使用します。")
    sys.exit(1)
if len(filename) == 0:
    filename = "eels.txt"
elif "." in filename:
    filename = filename.split(".")[0] + ".txt"
else:
    filename = filename + ".txt"

# OUTCARファイルを読み込む
with open("OUTCAR", "r") as file:
    lines = file.readlines()

# IMAGINARYとREALのデータをそれぞれ格納する変数
imaginary_data = []
real_data = []

# データの抽出
imaginary_flag = False
real_flag = False
for line in lines:
    # IMAGINARY DIELECTRIC FUNCTIONの始まりを検出
    if (
        "frequency dependent IMAGINARY DIELECTRIC FUNCTION (independent particle, no local field effects) density-density"
        in line
    ):
        imaginary_flag = True
        real_flag = False
        continue
    # REAL DIELECTRIC FUNCTIONの始まりを検出
    elif (
        "frequency dependent      REAL DIELECTRIC FUNCTION (independent particle, no local field effects) density-density"
        in line
    ):
        real_flag = True
        imaginary_flag = False
        continue

    # データの終了判定
    if re.match(r"^-{10,}", line):
        imaginary_flag = False
        real_flag = False
        continue

    # IMAGINARY DIELECTRIC FUNCTIONのデータを格納
    if imaginary_flag:
        imaginary_data.append(line.strip())
    # REAL DIELECTRIC FUNCTIONのデータを格納
    elif real_flag:
        real_data.append(line.strip())

# 1行目と2行目を削除
if len(imaginary_data) > 2:
    imaginary_data = imaginary_data[2:]
if len(real_data) > 2:
    real_data = real_data[2:]

# 出力用テキストファイルに書き込む
with open("eels.txt", "w") as output_file:
    # ヘッダ行の書き込み
    headers = "energies   " + column_name
    output_file.write(headers + "\n")
    output_file.write("-" * (len(headers) + 30) + "\n")

    min_length = min(len(imaginary_data), len(real_data))
    for i in range(min_length):
        im_columns = imaginary_data[i].split()
        re_columns = real_data[i].split()
        if len(im_columns) >= 4 and len(re_columns) >= 4:
            try:
                energy = float(im_columns[0])
                intensity = float(im_columns[3]) / (
                    float(re_columns[3]) ** 2 + float(im_columns[3]) ** 2
                )
                output_file.write(f"{energy} {intensity}\n")
            except (ValueError, ZeroDivisionError) as e:
                print(f"Error processing line {i}: {e}")
                continue
print(f"処理が完了しました。出力は '{filename}' に保存されました。")
