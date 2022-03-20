# CDP

Composition Data Process with GUI

This program contains four Composition data transformation algorithms：

- Improved-alr
- Clr
- ilr
- Stability based on Geboy's approach

It can also generate hierarchical clustering graphs based on these transformation.(The methods for calculating the distance between the
    newly formed cluster: **average**, distance metric: **correlation**)

## Usage

### 1. Run with Python environment (recommend)

1. install **Python-3.7**，click [here](https://www.python.org/downloads/) to download python. **Note**: Select `Add Python 3.x to PATH`
2. Run `pip install -r requirements.txt`
3. Run `python Composition_data_process_gui.py` or Double-click the startup script

默认显示语言为英文，若使用简体中文需在启动时加上参数`1`：`python Composition_data_process_gui.py 1`。 如果使用脚本启动，用记事本之类的打开修改一下即可。

### 2. Executable File

I will provide an executable File, for windows only. You can download from [releases](https://github.com/XuCpeng/CDP/releases)

### methods and metrics

Click: [scipy.cluster.hierarchy.linkage](https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.hierarchy.linkage.html)

Note: average=UPGMA, weighted=WPGMA, median=WPGMC

## Input File

Raw Composition Data Excel File(s)

### Raw Data Format

1. The file is **xlsx** or **xls** format.
2. The first row should be the element name.
3. The first column should be the sample number.
4. The second column should be **Ash**.
5. The column immediately following Ash is oxide elements, followed by non-oxide elements.

The paper's raw data is in the RawCoalGeochemistryData folder.

## Output Files

- Data for Clr transformation
- Data for Improved Alr transformation
- Data for Ilr transformation
- Stability using Geboy's approach
- Correlation between element based on improved alr
- Correlation between element based on Clr approach
- Correlation between element based on ilr approach
- Hierarchical cluster graph between element based on Improved-alr, Clr, Ilr, Stability. Support eps, png, svg, pdf, ps
