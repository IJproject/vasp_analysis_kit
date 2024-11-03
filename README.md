# Python scripts for analysing the results of VASP calculations

## Prerequisites

## List of Scripts

### Generating Text File

| File Name            | Required Files        | Function                                                               |
| :------------------- | :-------------------- | :--------------------------------------------------------------------- |
| convert_band.py      | EIGENVAL <br> KPOINTS | Generating a text file for plotting band structure                     |
| convert_dos.py       | vaspout.h5            | Generating a text file for plotting DOS                                |
| convert_workfunc.py  | vaspout.h5            | Generating a text file for plotting work function                      |
| convert_eels.py      | OUTCAR                | Generating a text file for plotting EELS (optical absorption) spectrum |

### Merging Text File

| File Name     | Script (Generating Text File) | Function                                        |
| :------------ | :---------------------------- | :---------------------------------------------- |
| merge_eels.py | convert_eels                  | Merging text files to display on the same graph |

### Plotting Graphs

| File Name        | Script (Generating Text File) | Function                                       |
| :--------------- | :---------------------------- | :--------------------------------------------- |
| plot_band.py     | convert_band.py               | Ploting the band structure                     |
| plot_dos.py      | convert_dos.py                | Ploting the DOS                                |
| plot_workfunc.py | convert_workfunc.py           | Ploting the work function                      |
| plot_eels.py     | convert_eels.py               | Ploting the EELS (optical absorption) spectrum |
