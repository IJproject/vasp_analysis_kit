import argparse

parser = argparse.ArgumentParser(
    description="取得したい情報をオプションで指定してください。"
)
parser.add_argument(
    "-f", "--filename", type=str, help="出力ファイル名を指定してください。\n 例) band"
)

# 引数を解析
args = parser.parse_args()
filename = args.filename if args.filename is not None else ""

if len(filename) == 0:
    filename = "band.txt"
elif "." in filename:
    filename = filename.split(".")[0] + ".txt"
else:
    filename = filename + ".txt"

with open("KPOINTS", "r") as input_file:
    kpoints = input_file.readlines()[4:]

# KPOINTSから特定のK点の情報を重複なく抽出
points = set()
for kpoint in kpoints:
    if kpoint == "\n":
        continue
    else:
        a_axis, b_axis, c_axis = kpoint.split()[:3]
        label = kpoint.split()[-1]
        try:
            label = float(label)
        except ValueError:
            point = {
                "a_axis": float(a_axis),
                "b_axis": float(b_axis),
                "c_axis": float(c_axis),
                "label": label,
            }
            points.add(tuple(point.items()))
unique_kpoints = [dict(point) for point in points]

with open("EIGENVAL", "r") as input_file:
    content = input_file.readlines()
    number_of_bands = int(content[5].split()[2])
    eigenvalues = content[7:]

# EIGENVALからバンドの情報を抽出
kpoints_index = 0
kpoints_diff_index = 50
kpoints_label = []
bands = [''] * number_of_bands
for eigenvalue in eigenvalues:
    if eigenvalue == "\n":
        continue
    else:
        value = eigenvalue.split()
        if len(value) >= 4:
            kpoints_diff_index += 1
            target_coords = [float(eigen) for eigen in eigenvalue.split()[:-1]]
            for kpoint in unique_kpoints:
                kpoint_coords = [kpoint['a_axis'], kpoint['b_axis'], kpoint['c_axis']]
                if all(abs(tc - kc) < 1e-6 for tc, kc in zip(target_coords, kpoint_coords)) and kpoints_diff_index > 10:
                    kpoints_label.append({
                        "index": kpoints_index,
                        "label": kpoint["label"]
                    })
                    kpoints_diff_index = 0
                    break
            kpoints_index += 1
        elif len(value) == 3:
            band_number = int(value[0])
            band_energy = float(value[1])
            bands[band_number - 1] += f"{band_number} {kpoints_index-1} {band_energy}\n"

# # データの書き出し
with open(filename, "w") as output_file:
    # kpointsの書き出し
    kpoints_header = "x_axis   labels"  # indexは0からスタート
    output_file.write(kpoints_header + "\n")
    output_file.write("-" * (len(kpoints_header) + 30) + "\n")
    for item in kpoints_label:
        output_file.write(f"{item['index']} {item['label']}\n")
    output_file.write("\n")

    # バンドの書き出し
    bands_header = "band_numbers   x_axis   energies"
    output_file.write(bands_header + "\n")
    output_file.write("-" * (len(bands_header) + 30) + "\n")
    output_file.write("\n".join(bands) + "\n")

print(f"処理が完了しました。出力は '{filename}' に保存されました。")
