## List of Scripts

| File Name            | Function                                                               |
| :------------------- | :--------------------------------------------------------------------- |
| convert_workfunc.py  | Generating a text file for plotting work function                      |
| plot_workfunc.py     | Ploting the work function                                              |

※ These programs have been created for layered materials. (perpendicular to c-axis direction)

### Generating Text File

Not yet created.

### Plotting Graph

#### Required files

- textfile made by `convert_workfunc.py`
- OUTCAR
- POSCAR

#### Example

```shell
  python plot_workfunc.py -i <text_data_file_name>
  # python plot_workfunc.py -i workfunc.txt

  python plot_workfunc.py -i <text_data_file_name> -o <output_file_name>
  # python plot_workfunc.py -i workfunc.txt -o workfunc.png

  python plot_workfunc.py -i <text_data_file_name> -x <z_range(min, max)>
  # python plot_workfunc.py -i workfunc.txt -x 0 100

  python plot_workfunc.py -i <text_data_file_name> -y <energy_range(min, max)>
  # python plot_workfunc.py -i workfunc.txt -y -5 5
```

### Sample

用意したファイルの説明
実行方法
得られた結果を表示
