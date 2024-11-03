import py4vasp
import argparse

parser = argparse.ArgumentParser(
    description="取得したい情報をオプションで指定してください。"
)
parser.add_argument(
    "-m",
    "--merge",
    type=str,
    nargs="*",
    help="結合したいファイルを全て選択してください。例) eels1.txt eels2.txt ...",
)
parser.add_argument(
    "-f", "--filename", type=str, help="出力ファイル名を指定してください。\n 例) eels"
)

# 引数を解析
args = parser.parse_args()
merge = args.merge if args.merge is not None else []
filename = args.filename if args.filename is not None else ""

if len(filename) == 0:
    filename = "eels.txt"
elif "." in filename:
    filename = filename.split(".")[0] + ".txt"
else:
    filename = filename + ".txt"

output_content = ""

# 書き出しデータの作成
with open(merge[0], "r") as file:
    lines = file.readlines()
    output_content = [line.strip() for line in lines]
    print(output_content)

for j in range(1, len(merge)):
    with open(merge[j], "r") as file:
        lines = file.readlines()
        output_content[0] += '   ' + lines[0].split('   ')[1].strip()
        content = lines[2:]  # データ部分だけを取得

        for i in range(len(content)):
            value_to_add = content[i].split()[1]
            output_content[i + 2] += " " + value_to_add

# データの書き出し
with open(filename, "w") as file:
    file.write("\n".join(output_content) + "\n")

print(f"処理が完了しました。出力は '{filename}' に保存されました。")
