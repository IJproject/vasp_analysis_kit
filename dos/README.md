## List of Scripts

### Generating Text File

#### Example

```
  python convert_dos.py

  python convert_dos.py -f <output_file_name>
  # python convert_dos.py -f dos.txt

  python convert_dos.py -s <DOS_option>
  # python convert_dos.py -s total,Bi,Se
  # python convert_dos.py -s s(Bi,Se),p(Bi,Se)
  # You can see more options from this link. (https://www.vasp.at/py4vasp/latest/calculation/dos/)
```

### Plotting Graph

#### Example

```
  python plot_dos.py -i <text_data_file_name>
  # python plot_dos.py -i dos.txt

  python plot_dos.py -i <text_data_file_name> -o <output_file_name>
  # python plot_dos.py -i dos.txt -o dos.png

  python plot_dos.py -i <text_data_file_name> -x <energy_range(min, max)>
  # python plot_dos.py -i dos.txt -x -1 1

  python plot_dos.py -i <text_data_file_name> -y <density_state_range(min, max)>
  # python plot_dos.py -i dos.txt -y 0 20
```

### Sample

用意したファイルの説明
実行方法
得られた結果を表示
