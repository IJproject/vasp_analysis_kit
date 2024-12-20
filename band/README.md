# List of Scripts

| File Name            | Function                                                               |
| :------------------- | :--------------------------------------------------------------------- |
| convert_band.py      | Generating a text file for plotting band structure                     |
| plot_band.py         | Ploting the band structure                                             |

## Generating Text File

### Required files

- EIGENVAL
- KPOINTS

### Example

```shell
  python convert_band.py

  python convert_band.py -f <output_file_name>
  # python convert_band.py -f band.txt
```

## Plotting Graph

### Required files

- textfile made by `convert_band.py`

### Example

```shell
  python plot_band.py -i <text_data_file_name>
  # python plot_band.py -i band.txt

  python plot_band.py -i <text_data_file_name> -o <output_file_name>
  # python plot_band.py -i band.txt -o band.png

  python plot_band.py -i <text_data_file_name> -b <band_number_list(refer to EIGENVAL)>
  # python plot_band.py -i band.txt -b 15 16 17 18

  python plot_band.py -i <text_data_file_name> -x <k_point_range(min, max)>
  # python plot_band.py -i band.txt -x 0 100

  python plot_band.py -i <text_data_file_name> -y <energy_range(min, max)>
  # python plot_band.py -i band.txt -y -1 1
```

## Sample

用意したファイルの説明
実行方法
得られた結果を表示
