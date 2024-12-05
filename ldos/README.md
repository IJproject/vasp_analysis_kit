# List of Scripts

These programs uses DENSITYTOOL(https://github.com/llodeiro/DensityTool).

| File Name                 | Function                 |
| :------------------------ | :----------------------- |
| plot_ldos.py              | Ploting the LDOS         |
| plot_partial_mean_ldos.py | Ploting the partial LDOS |

※ These programs have been created for layered materials. (perpendicular to c-axis direction)

## Plotting LDOS Graph

### Required files

- (folder)/LDOS.R3.*.dat
- (folder)/DENSITYTOOL.IN
- POSCAR

### Example

```shell
python plot_ldos.py -d <folder_name>
# python plot_ldos.py -d ldos-data

python plot_ldos.py -d <folder_name> -o <output_file_name>
#  python plot_ldos.py -d ldos-data -o ldos.txt
```

## Plotting partial LDOS Graph

### Required files

- (folder)/LDOS.R3.*.dat
- (folder)/DENSITYTOOL.IN
- POSCAR

### Example

```shell
python plot_partial_mean_ldos.py -d <folder_name>
# python plot_partial_mean_ldos.py -d ldos-data

python plot_partial_mean_ldos.py -d <folder_name> -l <layer_number_list>
#  python plot_partial_mean_ldos.py -d ldos-data -l 4 5 6

python plot_partial_mean_ldos.py -d <folder_name> -o <output_file_name>
#  python plot_partial_mean_ldos.py -d ldos-data -o ldos.png
```

## Sample

用意したファイルの説明
実行方法
得られた結果を表示
