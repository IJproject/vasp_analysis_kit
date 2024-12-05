import py4vasp
import argparse

parser = argparse.ArgumentParser(
    description="取得したい情報をオプションで指定してください。"
)
parser.add_argument(
    "-s",
    "--selection",
    type=str,
    help="原子や軌道を指定してください。\n 例) total, Bi, s(Bi), p(Bi,Se) etc.",
)
parser.add_argument(
    "-f", "--filename", type=str, help="出力ファイル名を指定してください。\n 例) dos"
)

# 引数を解析
args = parser.parse_args()
selection = args.selection if args.selection is not None else ""
filename = args.filename if args.filename is not None else ""

if len(selection) == 0:
    selection = "total"

if len(filename) == 0:
    filename = "dos.txt"
elif "." in filename:
    filename = filename.split(".")[0] + ".txt"
else:
    filename = filename + ".txt"

# py4vaspでデータの解析
calc = py4vasp.Calculation.from_path(".")
all_data = calc.dos.to_dict(selection=selection)
data = {key: value for key, value in all_data.items() if key not in ["fermi_energy"]}

# # データの書き出し
with open(filename, "w") as file:
    # ヘッダ行の書き込み
    headers = "   ".join(data.keys())
    file.write(headers + "\n")
    file.write("-" * (len(headers) + 30) + "\n")

    # データ行の書き込み
    max_length = max(len(value) for value in data.values())
    for i in range(max_length):
        row = []
        for key in data.keys():
            if i < len(data[key]):
                row.append(str(data[key][i]))
            else:
                row.append("")  # データがない場合は空白を挿入
        file.write(" ".join(row) + "\n")

print(f"処理が完了しました。出力は '{filename}' に保存されました。")
