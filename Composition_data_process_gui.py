# -*- coding: utf-8 -*-
# @Time    : 2019/12/22 12:07 下午
# @Author  : Xu Chuanpeng
# @FileName: CompositionDataProcess_gui.py
# @Software: PyCharm
# @Blog    ：https://x.medemede.cn


import platform
import sys
import tkinter.font as tk_font
from string import Template
from tkinter import Frame, Label, Button, Checkbutton, filedialog, X, messagebox, Entry, StringVar, LEFT

from Composition_data_processing import CompositionDataProcess
from strings import Strings


# Convert the alphabetic number of excel to a numeric number
def char_to_num(s):
    rec = 0
    s = s.upper()
    for i in range(len(s)):
        rec *= 26
        rec += (ord(s[i]) - ord('A') + 1)
    return rec


class Application(Frame):
    def __init__(self, language=0, master=None):
        Frame.__init__(self, master)

        self.text_str = Strings(language)
        if platform.system() == "Windows":
            self.set_win_center(700, 710)
        else:
            self.set_win_center(555, 680)
        self.pack()
        self.ft = tk_font.Font(
            family=self.text_str.font_family, size=14)

        # transform algorithm checkbox
        self.algorithms = [StringVar(), StringVar(), StringVar(), StringVar(), StringVar()]
        Label(self, text=self.text_str.transform_select, font=self.ft).pack()
        algorithms_check_box = Frame(self)
        Checkbutton(algorithms_check_box,
                    text='None',
                    onvalue='none',
                    offvalue='',
                    font=self.ft,
                    variable=self.algorithms[0]
                    ).pack(side=LEFT, pady=8)
        Checkbutton(algorithms_check_box,
                    text='Improved-alr',
                    onvalue='ialr',
                    offvalue='',
                    font=self.ft,
                    variable=self.algorithms[1]
                    ).pack(side=LEFT, pady=8)
        Checkbutton(algorithms_check_box,
                    text='clr',
                    onvalue='clr',
                    offvalue='',
                    font=self.ft,
                    variable=self.algorithms[2]
                    ).pack(side=LEFT, pady=8)
        Checkbutton(algorithms_check_box,
                    text='ilr',
                    onvalue='ilr',
                    offvalue='',
                    font=self.ft,
                    variable=self.algorithms[3]
                    ).pack(side=LEFT, pady=8)
        Checkbutton(algorithms_check_box,
                    text='stab',
                    onvalue='stab',
                    offvalue='',
                    font=self.ft,
                    variable=self.algorithms[4]
                    ).pack(side=LEFT, pady=8)
        algorithms_check_box.pack()

        # methods checkbox
        self.methods = [StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar()]
        Label(self, text=self.text_str.select_method, font=self.ft).pack()
        methods_check_box = Frame(self)
        Checkbutton(methods_check_box,
                    text='single',
                    onvalue='single',
                    offvalue='',
                    font=self.ft,
                    variable=self.methods[0]
                    ).pack(side=LEFT, pady=8)
        Checkbutton(methods_check_box,
                    text='complete',
                    onvalue='complete',
                    offvalue='',
                    font=self.ft,
                    variable=self.methods[1]
                    ).pack(side=LEFT, pady=8)
        Checkbutton(methods_check_box,
                    text='average',
                    onvalue='average',
                    offvalue='',
                    font=self.ft,
                    variable=self.methods[2]
                    ).pack(side=LEFT, pady=8)
        Checkbutton(methods_check_box,
                    text='centroid',
                    onvalue='centroid',
                    offvalue='',
                    font=self.ft,
                    variable=self.methods[3]
                    ).pack(side=LEFT, pady=8)
        Checkbutton(methods_check_box,
                    text='ward',
                    onvalue='ward',
                    offvalue='',
                    font=self.ft,
                    variable=self.methods[4]
                    ).pack(side=LEFT, pady=8)
        Checkbutton(methods_check_box,
                    text='weighted',
                    onvalue='weighted',
                    offvalue='',
                    font=self.ft,
                    variable=self.methods[5]
                    ).pack(side=LEFT, pady=8)
        Checkbutton(methods_check_box,
                    text='median',
                    onvalue='median',
                    offvalue='',
                    font=self.ft,
                    variable=self.methods[6]
                    ).pack(side=LEFT, pady=8)
        methods_check_box.pack()

        # distances checkbox
        self.distances = [StringVar(), StringVar(), StringVar(), StringVar()]
        distances_check_box = Frame(self)
        Checkbutton(distances_check_box,
                    text='correlation',
                    onvalue='correlation',
                    offvalue='',
                    font=self.ft,
                    variable=self.distances[0]
                    ).pack(side=LEFT, pady=8)
        Checkbutton(distances_check_box,
                    text='euclidean',
                    onvalue='euclidean',
                    offvalue='',
                    font=self.ft,
                    variable=self.distances[1]
                    ).pack(side=LEFT, pady=8)
        Checkbutton(distances_check_box,
                    text='minkowski',
                    onvalue='minkowski',
                    offvalue='',
                    font=self.ft,
                    variable=self.distances[2]
                    ).pack(side=LEFT, pady=8)
        Checkbutton(distances_check_box,
                    text='chebyshev',
                    onvalue='chebyshev',
                    offvalue='',
                    font=self.ft,
                    variable=self.distances[3]
                    ).pack(side=LEFT, pady=8)

        distances_check_box.pack()

        # improved-alr need more inputs
        self.end_o = StringVar()
        self.o_x_j = StringVar()
        self.e_x_j = StringVar()
        Label(self, text=self.text_str.ialr_help,
              font=self.ft).pack()
        Label(self, text=self.text_str.oxides_end, font=self.ft).pack()
        Entry(self, textvariable=self.end_o).pack()
        Label(self, text=self.text_str.al2o3, font=self.ft).pack()
        Entry(self, textvariable=self.o_x_j).pack()
        Label(self, text=self.text_str.zr, font=self.ft).pack()
        Entry(self, textvariable=self.e_x_j).pack()
        self.end_o.set('L')  # default
        self.o_x_j.set('C')  # default
        self.e_x_j.set('AE')  # default

        # select the format when saving pictures
        self.figs = [StringVar(), StringVar(), StringVar(), StringVar(), StringVar()]
        Label(self, text=self.text_str.fig_format, font=self.ft).pack()
        check_box = Frame(self)
        Checkbutton(check_box, text='png', onvalue='png', offvalue='', font=self.ft, variable=self.figs[0]).pack(
            side=LEFT, pady=8)
        Checkbutton(check_box, text='eps', onvalue='eps', offvalue='', font=self.ft, variable=self.figs[1]).pack(
            side=LEFT, pady=8)
        Checkbutton(check_box, text='pdf', onvalue='pdf', offvalue='', font=self.ft, variable=self.figs[2]).pack(
            side=LEFT, pady=8)
        Checkbutton(check_box, text='svg', onvalue='svg', offvalue='', font=self.ft, variable=self.figs[3]).pack(
            side=LEFT, pady=8)
        Checkbutton(check_box, text='ps', onvalue='ps', offvalue='', font=self.ft, variable=self.figs[4]).pack(
            side=LEFT, pady=8)
        check_box.pack()

        # file selection button
        Label(self, text=self.text_str.raw_data, font=self.ft).pack()
        select_button = Button(self, text=self.text_str.file_select_but, font=self.ft, command=self.select_files)
        select_button.pack(fill=X, pady=8)

        # variable prompt label
        self.hidden_label = StringVar()
        self.hidden_label.set(self.text_str.hidden_label)
        Label(self, textvariable=self.hidden_label, font=self.ft).pack()

        # help button
        Button(self, text=self.text_str.help, font=self.ft, command=self.help_doc_box).pack(fill=X, pady=8)

        quit_button = Button(self, text=self.text_str.exit, font=self.ft, command=self.quit)
        quit_button.pack(pady=8)

    # windows centered
    def set_win_center(self, cur_width, cur_height):
        if not cur_width:
            cur_width = self.master.winfo_width()
        if not cur_height:
            cur_height = self.master.winfo_height()
        scn_w, scn_h = self.master.maxsize()
        cen_x = (scn_w - cur_width) / 2
        cen_y = (scn_h - cur_height) / 2
        size_xy = '%dx%d+%d+%d' % (cur_width, cur_height, cen_x, cen_y)
        self.master.geometry(size_xy)

    # perform file selection
    def select_files(self):
        filenames = filedialog.askopenfilenames()
        messagebox.showinfo('select files', Template(self.text_str.file_selected).substitute(num=len(filenames)))

        if len(filenames) > 0:
            flag = messagebox.askquestion('Ready to process',
                                          self.text_str.ready)
            if flag == messagebox.YES:
                k = 0  # processed file counter

                # improved alr parameters
                end_o = char_to_num(self.end_o.get()) - 2
                o_x_j = char_to_num(self.o_x_j.get()) - 3
                e_x_j = char_to_num(self.e_x_j.get()) - 3

                for filename in filenames:
                    methods = [x.get() for x in self.methods if not x.get() == '']
                    distances = [x.get() for x in self.distances if not x.get() == '']
                    algorithms = [x.get() for x in self.algorithms if not x.get() == '']
                    figs = [x.get() for x in self.figs if not x.get() == '']
                    process = CompositionDataProcess(filename, end_o, o_x_j, e_x_j, methods, distances, algorithms,
                                                     figs)
                    process.save_data()
                    k += 1

                self.hidden_label.set(Template(self.text_str.processed).substitute(num=k))
                messagebox.showinfo('Finished', Template(self.text_str.finished).substitute(num=k))

    def help_doc_box(self):
        messagebox.showinfo(self.text_str.help, self.text_str.help_doc)


def main(argv):
    # language:
    # 0 -> English, 1 -> 简体中文
    language = 0

    if len(argv) > 1 and argv[1] == '1':
        language = 1

    app = Application(language)
    app.master.title('Composition data process GUI')
    app.mainloop()


if __name__ == '__main__':
    main(sys.argv)
