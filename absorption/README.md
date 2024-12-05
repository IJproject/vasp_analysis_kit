# List of Scripts

| File Name             | Function                                                        |
| :-------------------- | :-------------------------------------------------------------- |
| convert_absorption.py | Generating a text file for plotting optical absorption spectrum |
| merge_absorption.py   | Merging text files to display on the same graph                 |
| plot_absorption.py    | Ploting the optical absorption spectrum                         |

## Generating Text File

### Required files

- OUTCAR

### Example

```shell
  python convert_absorption.py -c <column_name>
  # python convert_absorption.py -c reference

  python convert_absorption.py -c <column_name> -f <output_file_name>
  # python convert_absorption.py -c reference -f absorption_reference.txt
```

## Merging Text File

### Required files

- textfile made by `convert_absorption.py`

### Example

```shell
  python merge_absorption.py -m <files>
  # python merge_absorption.py -m absorption_reference.txt absorption_data.txt

  python merge_absorption.py -m <files> -f <output_file_name>
  # python merge_absorption.py -m absorption_reference.txt absorption_data.txt -f absorption.txt
```

## Plotting Graph

### Required files

- textfile made by `merge_absorption.py` or `convert_absorption`

### Example

```shell
  python plot_absorption.py -i <text_data_file_name>
  # python plot_absorption.py -i absorption.txt

  python plot_absorption.py -i <text_data_file_name> -o <output_file_name>
  # python plot_absorption.py -i absorption.txt -o absorption.png

  python plot_absorption.py -i <text_data_file_name> -x <energy_loss_range(min, max)>
  # python plot_absorption.py -i absorption.txt -x 0 30

  python plot_absorption.py -i <text_data_file_name> -y <intensity_range(min, max)>
  # python plot_absorption.py -i absorption.txt -y 0 1
```

## Sample

用意したファイルの説明
実行方法
得られた結果を表示

