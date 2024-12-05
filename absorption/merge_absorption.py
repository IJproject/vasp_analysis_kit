import py4vasp
import argparse
import sys

parser = argparse.ArgumentParser(
    description="取得したい情報をオプションで指定してください。"
)
parser.add_argument(
    "-m",
    "--mergefiles",
    type=str,
    nargs="*",
    help="（必須）結合したいファイルを全て選択してください。例) absorption1.txt absorption2.txt ...",
)
parser.add_argument(
    "-f", "--filename", type=str, help="出力ファイル名を指定してください。\n 例) absorption.txt"
)

# 引数を解析
args = parser.parse_args()
mergefiles = args.mergefiles if args.mergefiles is not None else []
filename = args.filename if args.filename is not None else ""

if len(mergefiles) == 0:
    print("結合するテキストファイル名を全て列挙してください")
    sys.exit(1)

if len(filename) == 0:
    filename = "absorption.txt"
elif "." in filename:
    filename = filename.split(".")[0] + ".txt"
else:
    filename = filename + ".txt"

# 書き出しファイルの初期化
with open(filename, "w") as outputfile:
    pass

# データの書き出し
for i in range(0, len(mergefiles)):
    with open(mergefiles[i], "r") as inputfile:
        lines = inputfile.readlines()

    with open(filename, "a") as outputfile:
        outputfile.write("".join(lines) + "\n")

print(f"処理が完了しました。出力は '{filename}' に保存されました。")
