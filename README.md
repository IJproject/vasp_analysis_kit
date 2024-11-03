# VASPでの計算結果解析用Pythonスクリプト

## 前提条件

## スクリプト一覧

### テキストファイルの生成

| ファイル名 | 使用ファイル | 機能 |
| :--- | :--- | :--- |
| convert_band.py | EIGENVAL <br> KPOINTS | バンド図作成用のテキストファイルを生成 |
| convert_dos.py | vaspout.h5 | DOS図作成用のテキストファイルを生成 |
| convert_eels.py | OUTCAR | EELS（光吸収）スペクトル図作成用のテキストファイルを生成 |

### テキストファイルの統合

| ファイル名 | 使用ファイルの作成スクリプト | 機能 |
| :--- | :--- | :--- |
| merge_eels.py | convert_eels | gnuplotで複数の結果を重ねて描画させるため、テキストファイルを結合 |

### グラフのプロット

| ファイル名 | 使用ファイルの作成スクリプト | 機能 |
| :--- | :--- | :--- |
| plot_band.py | convert_band.py | バンド図を作成 |
| plot_dos.py | convert_dos.py | DOS図を作成 |
| plot_workfunc.py | 根性.py | 仕事関数図を作成 |
| plot_eels.py | convert_eels.py | EELS（光吸収）スペクトル図を作成 |
