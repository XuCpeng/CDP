# -*- coding: utf-8 -*-

class Strings(object):
    def __init__(self, i):
        self.select_method = ['2.Please select the method and metric (distance) \nof hierarchical clustering',
                              '2.请选择层次聚类的method和distance',
                              '2.Please select method for calculating the \ndistance between the newly formed '
                              'cluster，\ndefault is average'][i]
        self.help_doc = [
            '1. The file is xlsx or xls format.\n'
            '2. The first row should be the element name.\n'
            '3. The first column should be the sample number.\n'
            '4. The second column (i.e. the first column of the data) should be \'Ash\'.\n'
            '5. The column immediately following \'Ash\' is oxide elements, followed by non-oxide elements.\n\n'
            'The paper\'s raw data is in \n the RawCoalGeochemistryData folder',
            '1. 输入的原始数据文件应该是 xlsx 或 xls 格式。\n'
            '2. 数据表的第一行为元素名称.\n'
            '3. 数据表的第一列为样本编号.\n'
            '4. 数据表的第二列(也就是数据的第一列)应该是灰分。\n'
            '5. 紧跟在灰分之后的列是连续的氧化物数据,再后面是非氧化物元素\n\n'
            '你可以在 RawCoalGeochemistryData 文件夹中找到论文中的源数据。'
        ][i]
        self.transform_select = ['\n1.Please select Transformation algorithm:', '\n1.请选择转换算法:'][i]
        self.ialr_help = ['3.Please input column numbers(e.g. C):',
                          '3.Improved-alr 需要额外的信息\n请填写?处的列号(例如:C):',
                          '3.Improved-alr need additional information\nplease input column numbers(e.g. C):'][i]
        self.oxides_end = ['Columns C to ? are oxides:',
                           '从列C到列 ? 是氧化物:'][i]
        self.al2o3 = ['Column ? is Al2O3:',
                      '第 ? 列是Al2O3:'][i]
        self.zr = ['Column ? is Zr:',
                   '第 ? 列是Zr:'][i]
        self.fig_format = ['\n4.Please select figures format:',
                           '\n4.请选择要生成的图片格式:'][i]
        self.raw_data = ['5.Please select Raw Data files:',
                         '5.请选择原始数据文件:'][i]
        self.hidden_label = [
            'The paper\'s raw data is in \n the RawCoalGeochemistryData folder',
            '论文中的源数据在 \n RawCoalGeochemistryData 文件夹中'][i]
        self.help = ['Help', '帮助'][i]
        self.exit = ['Quit', '退出'][i]
        self.file_selected = ['$num file(s) have been selected',
                              '选择了 $num 个文件'][i]
        self.file_select_but = ['Click here to select file(s)', '点击此处选择文件'][i]
        self.ready = ['Wait a few minutes after you start, the generated file will be saved to the '
                      '\'out\' directory.\nClick Yes to start!',
                      '开始处理之后请稍等几分钟, 生成的文件将会保存在out目录\n点击\'Yes\'开始处理！'][i]
        self.processed = ['$num file(s) have been processed',
                          '$num 个文件处理完成'][i]
        self.finished = ['Finished, $num file(s) have been processed',
                         '完成, 成功处理了 $num 个文件'][i]
        self.font_family = ['apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Ubuntu,Helvetica Neue,Helvetica,Arial',
                            'PingFang SC,Hiragino Sans GB,Microsoft YaHei UI,Microsoft YaHei,Source Han Sans CN,'
                            'sans-serif'][i]
