# -*- coding: utf-8 -*-
# @Time    : 2019/12/22 12:07 下午
# @Author  : Xu Chuanpeng
# @FileName: Composition_data_processing.py
# @Software: PyCharm
# @Blog    ：https://x.medemede.cn

# https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.hierarchy.linkage.html
# average=UPGMA, weighted=WPGMA, median=WPGMC

import os
import sys

import numpy as np
import xlrd
import xlsxwriter
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import cophenet, dendrogram, linkage
from scipy.spatial.distance import pdist
from scipy.spatial.distance import squareform
from scipy.stats import gmean
from sklearn.cluster import AgglomerativeClustering


class CompositionDataProcess:

    def __init__(self, filepath, end_o=10, o_x_j=0, e_x_j=28, methods=None, distances=None, algorithms=None, figs=None):
        """
        :param filepath: Absolute path to raw data file, supports xlsx and xls;
        :param end_o: [0:end_o-1] is Oxide,[end_o:] is not Oxide;
        :param o_x_j: the index of x_j in X, when x_i is Oxide;
        :param e_x_j: the index of x_j in X, when x_i is not Oxide;
        :param methods: linkage methods, supports ’single’, ’complete’, ’average’, ’weighted’, ’centroid’, ’median’, ’ward’;
        :param distances: See the 'scipy.spatial.distance.pdist' function for a list of valid distance metrics;
        :param algorithms: Data Transformation Algorithms, supports 'none', 'ialr', 'clr', 'ilr', 'stab'.
        :param figs: See the 'matplotlib.pyplot.savefig' function for a list of valid figure format.
        """

        if figs is None:
            figs = []
        if algorithms is None:
            algorithms = []
        if distances is None:
            distances = []
        if methods is None:
            methods = []
        self.data_path = filepath
        self.sheet_name = 'Sheet1'
        self.end_o = end_o
        self.o_x_j = o_x_j
        self.e_x_j = e_x_j
        self.file_name = self.data_path.split('.')[-2].split('/')[-1]
        if len(self.file_name) > 42:
            self.file_name = self.file_name[:42]
        self.data_all, self.data_ash, self.data_features, self.data_serial = self.read_excel(self.data_path,
                                                                                             self.sheet_name)
        self.data_no_ash = self.data_all[:, 1:]
        self.methods = methods
        self.distances = distances
        self.algorithms = algorithms
        self.figs = figs

        self.out_path = os.path.join(self.get_app_path(), 'out/')
        if not os.path.exists(self.out_path):
            os.mkdir(self.out_path)
        plt.rc('font', family='Times New Roman')

    @staticmethod
    def get_app_path():
        if getattr(sys, 'frozen', False):
            application_path = os.path.dirname(sys.executable)
            # running_mode = 'Frozen/executable'
        else:
            try:
                app_full_path = os.path.realpath(__file__)
                application_path = os.path.dirname(app_full_path)
                # running_mode = "Non-interactive (e.g. 'python myapp.py')"
            except NameError:
                application_path = os.getcwd()
                # running_mode = 'Interactive'
        return application_path  # , running_mode

    # X:All_data but no ash
    @staticmethod
    def clr(x):
        d = x.shape[1]
        ln_x = np.log(x)
        e_sum_x = np.exp(np.sum(ln_x, 1) / d)
        return np.log(x.T / e_sum_x).T

    # ------------------ improved-alr ----------------------
    # X:All_data but no ash
    # end_o: [0:end_o-1] is Oxide,[end_o:] is not Oxide
    # o_x_j: the index of x_j in X, when x_i is Oxide
    # e_x_j: the index of x_j in X, when x_i is not Oxide
    @staticmethod
    def ialr(x, features, end_o, o_x_j, e_x_j):
        rec = np.zeros(shape=x.shape)
        rec[:, :end_o] = np.log(x[:, :end_o].T / x[:, o_x_j]).T
        rec[:, end_o:] = np.log(x[:, end_o:].T / x[:, e_x_j]).T
        rec = np.delete(rec, [o_x_j, e_x_j], axis=1)
        features = np.delete(features, [o_x_j, e_x_j])
        return rec, features

    # X:All_data but no ash
    @staticmethod
    def ilr(x, features):
        m, d = x.shape
        rec = np.zeros((m, d - 1))

        for j in range(1, d):
            g = gmean(x[:, :j], axis=1)
            rec[:, j - 1] = np.sqrt(j / (j + 1)) * np.log(g / x[:, j])
        return rec, np.delete(features, [d - 1])

    # X:All_data but no ash
    @staticmethod
    def stab(x):
        d = x.shape[1]
        rec = np.zeros(shape=(d, d))
        for i in range(d):
            for j in range(i, d):
                ilr_i_j = (1 / np.sqrt(2)) * np.log(x[:, i] / x[:, j])
                var_i_j = np.var(ilr_i_j)
                stab_i_j = np.exp(-var_i_j)
                rec[i, j] = stab_i_j
                rec[j, i] = stab_i_j
        return rec

    # read excel Raw data
    @staticmethod
    def read_excel(excel_path, sheet_name='Sheet1'):
        wb = xlrd.open_workbook(excel_path)
        sheet = wb.sheet_by_name(sheet_name)
        x_rows = sheet.nrows - 1
        x_cols = sheet.ncols - 1
        x = np.zeros((x_rows, x_cols))
        x_features = sheet.row_values(0)[1:]
        x_serial = sheet.col_values(0)
        ash = sheet.col_values(1, start_rowx=1)
        for i in range(x_rows):
            x[i] = sheet.row_values(i + 1, start_colx=1)
        return x, ash, x_features, x_serial

    # read data at the specified position in excel
    @staticmethod
    def read_data(excel_path, sheet_name, start_row, start_col, end_row, end_col):
        sheet = xlrd.open_workbook(excel_path).sheet_by_name(sheet_name)
        m, d = end_row - start_row + 1, end_col - start_col + 1
        data = np.zeros(shape=(m, d))
        for i in range(start_row - 1, end_row):
            data[i - start_row + 1, :] = sheet.row_values(i, start_colx=start_col - 1, end_colx=end_col)
        return data

    def all_evolution(self, y, f_all, f_all_f, method, elements_l=None, transform=None, dataset_name=None, metric=None):
        for clusters_n in range(elements_l, 1, -1):
            clusters = AgglomerativeClustering(affinity='precomputed', n_clusters=clusters_n,
                                               linkage=method).fit_predict(squareform(y))

            for f_all_f_i, f_all_f_v in enumerate(f_all_f):
                if f_all_f_v:
                    tmp_f = f_all[f_all_f_i].copy()
                    for index, cc in enumerate(clusters):
                        if cc == clusters[f_all[f_all_f_i][0]]:
                            if index in tmp_f:
                                tmp_f.remove(index)
                            else:
                                f_all_f[f_all_f_i] = False
                                if tmp_f:
                                    print(dataset_name + '-' + transform + '-' + method + '-' + metric + '-' + str(
                                        f_all_f_i) + ": false")
                                break
                    if not tmp_f:
                        f_all_f[f_all_f_i] = False
                        print(dataset_name + '-' + transform + '-' + method + '-' + metric + '-' + str(
                            f_all_f_i) + ": true")
        for f_all_f_i, f_all_f_v in enumerate(f_all_f):
            if f_all_f_v:
                print(dataset_name + '-' + transform + '-' + method + '-' + metric + '-' + str(f_all_f_i) + ": false")

    def save_none(self, wb, figs):
        no_ash_features = np.delete(self.data_features, [0])

        for method in self.methods:
            for distance in self.distances:
                y = pdist(self.data_no_ash.T, distance)
                # ===============Adaohai=====================
                # f_a = [2, 5, 6, 8]
                # f_b = [29, 52]
                # f_c = [28, 51]
                # f_d = [36, 26]
                # f_e = [20, 31]
                # f_f = [27, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50]
                # f_g = [0, 1]
                # f_h = [33, 55]
                # f_all = [f_a, f_b, f_c, f_d, f_e, f_f, f_g, f_h]
                # f_all_f = [True, True, True, True, True, True, True, True]

                # self.all_evolution(y, f_all, f_all_f, method, len(no_ash_features), 'none', self.file_name, distance)
                # ====================================

                # ================Datanhao====================
                # f_a = [5, 4, 6, 3]
                # f_b = [27, 36]
                # f_c = [26, 35]
                # f_d = [34, 25]
                # f_e = [19, 29]
                # f_f = [43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57]
                # f_g = [2, 0]
                # f_h = [31, 37]
                # f_all = [f_a, f_b, f_c, f_d, f_e, f_f, f_g, f_h]
                # f_all_f = [True, True, True, True, True, True, True, True]

                # self.all_evolution(y, f_all, f_all_f, method, len(no_ash_features), 'none', self.file_name, distance)
                # ====================================

                z = linkage(y, method=method)
                c, _ = cophenet(z, y)
                print(self.file_name + '-none-' + method + '-' + distance + ': ' + str(c))
                plt.figure(figsize=(15, 8))
                dendrogram(z, labels=no_ash_features, leaf_font_size=12)
                plt.title(self.file_name + ' ' + method + ' ' + distance + ' ', fontdict={'size': 20})
                plt.ylabel("Distance cluster combine", fontdict={'size': 18})
                for fig in figs:
                    plt.savefig(self.out_path + self.file_name + '_' +
                                method + '_' + distance + '_None.' + fig, bbox_inches='tight', dpi=600)
                plt.close()

    def save_clr(self, wb, figs):
        clr_features = np.delete(self.data_features, [0])
        data_clr = self.clr(self.data_no_ash)
        data_clr_corr = np.corrcoef(data_clr, rowvar=False)

        sheet = wb.add_worksheet('Data for Clr Transform')
        sheet.write_row('B1', clr_features)
        sheet.write_column('A1', self.data_serial)
        for i in range(data_clr.shape[0]):
            sheet.write_row(i + 1, 1, data_clr[i, :])

        sheet = wb.add_worksheet('Correlation using Clr approach')
        sheet.write_row('B1', clr_features)
        sheet.write_column('A2', clr_features)
        for i in range(data_clr_corr.shape[0]):
            sheet.write_row(i + 1, 1, data_clr_corr[i, :])

        for method in self.methods:
            for distance in self.distances:
                y = pdist(data_clr.T, distance)
                z = linkage(y, method=method)
                c, _ = cophenet(z, y)
                plt.figure(figsize=(15, 8))
                dendrogram(z, labels=clr_features, leaf_font_size=12)
                plt.title(self.file_name + ' ' + method + ' ' + distance + ' Clr', fontdict={'size': 20})
                plt.ylabel("Distance cluster combine", fontdict={'size': 18})
                for fig in figs:
                    plt.savefig(self.out_path + self.file_name + '_' +
                                method + '_' + distance + '_Clr.' + fig, bbox_inches='tight', dpi=600)
                plt.close()

    def save_ialr(self, wb, figs):
        ialr_features = np.delete(self.data_features, [0])
        data_ialr, ialr_features = self.ialr(
            self.data_no_ash, ialr_features, self.end_o, self.o_x_j, self.e_x_j)
        data_ialr_corr = np.corrcoef(data_ialr, rowvar=False)

        sheet = wb.add_worksheet('Data for Improved-Alr Transform')
        sheet.write_row('B1', ialr_features)
        sheet.write_column('A1', self.data_serial)
        for i in range(data_ialr.shape[0]):
            sheet.write_row(i + 1, 1, data_ialr[i, :])

        sheet = wb.add_worksheet('Correlation using improved-alr')
        sheet.write_row('B1', ialr_features)
        sheet.write_column('A2', ialr_features)
        for i in range(data_ialr_corr.shape[0]):
            sheet.write_row(i + 1, 1, data_ialr_corr[i, :])

        for method in self.methods:
            for distance in self.distances:
                y = pdist(data_ialr.T, distance)

                # =================== Adaohai ======================
                # f_a = [1, 4, 5, 7]
                # f_b = [27, 50]
                # f_c = []
                # f_d = [25, 34]
                # f_e = [19, 29]
                # f_f = [26, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48]
                # f_g = []
                # f_h = [31, 53]
                # f_all = [f_a, f_b, f_c, f_d, f_e, f_f, f_g, f_h]
                # f_all_f = [True, True, False, True, True, True, False, True]

                # self.all_evolution(y, f_all, f_all_f, method, len(ialr_features), 'ialr', self.file_name, distance)
                # =========================================

                # ================= Datanhao ========================
                # f_a = [4, 3, 5, 2]
                # f_b = [25, 34]
                # f_c = []
                # f_d = [32, 24]
                # f_e = [18, 27]
                # f_f = [41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55]
                # f_g = []
                # f_h = [29, 35]
                # f_all = [f_a, f_b, f_c, f_d, f_e, f_f, f_g, f_h]
                # f_all_f = [True, True, False, True, True, True, False, True]

                # self.all_evolution(y, f_all, f_all_f, method, len(ialr_features), 'ialr', self.file_name, distance)
                # =========================================

                z = linkage(y, method=method)
                c, _ = cophenet(z, y)
                print(self.file_name + '-ialr-' + method + '-' + distance + ': ' + str(c))
                plt.figure(figsize=(15, 8))
                dendrogram(z, labels=ialr_features, leaf_font_size=12)
                plt.title(self.file_name + ' ' + method + ' ' + distance + ' Improved-alr',
                          fontdict={'size': 20})
                plt.ylabel("Distance cluster combine", fontdict={'size': 18})
                for fig in figs:
                    plt.savefig(self.out_path + self.file_name + '_' +
                                method + '_' + distance +
                                '_Improved-alr.' + fig, bbox_inches='tight', dpi=600)
                plt.close()

    def save_ilr(self, wb, figs):
        ilr_features = np.delete(self.data_features, [0])
        data_ilr, ilr_features = self.ilr(self.data_no_ash, ilr_features)
        data_ilr_corr = np.corrcoef(data_ilr, rowvar=False)

        sheet = wb.add_worksheet('Data for Ilr Transform')
        sheet.write_row('B1', ilr_features)
        sheet.write_column('A1', self.data_serial)
        for i in range(data_ilr.shape[0]):
            sheet.write_row(i + 1, 1, data_ilr[i, :])

        sheet = wb.add_worksheet('Correlation using ilr approach')
        sheet.write_row('B1', ilr_features)
        sheet.write_column('A2', ilr_features)
        for i in range(data_ilr_corr.shape[0]):
            sheet.write_row(i + 1, 1, data_ilr_corr[i, :])

        for method in self.methods:
            for distance in self.distances:
                y = pdist(data_ilr.T, distance)

                # ====================================
                # f_a = [2, 5, 6, 8]
                # f_b = [29, 52]
                # f_c = [28, 51]
                # f_d = [36, 26]
                # f_e = [20, 31]
                # f_f = [27, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50]
                # f_g = [0, 1]
                # f_h = [33, 55]
                # f_all = [f_a, f_b, f_c, f_d, f_e, f_f, f_g, f_h]
                # f_all_f = [True, True, True, True, True, True, True, True]

                # self.all_evolution(y, f_all, f_all_f, method, len(ilr_features), 'ilr', self.file_name, distance)
                # ====================================

                # ================Datanhao====================
                # f_a = [5, 4, 6, 3]
                # f_b = [27, 36]
                # f_c = [26, 35]
                # f_d = [34, 25]
                # f_e = [19, 29]
                # f_f = [43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56]
                # f_g = [2, 0]
                # f_h = [31, 37]
                # f_all = [f_a, f_b, f_c, f_d, f_e, f_f, f_g, f_h]
                # f_all_f = [True, True, True, True, True, True, True, True]

                # self.all_evolution(y, f_all, f_all_f, method, len(ilr_features), 'ilr', self.file_name, distance)
                # ====================================

                z = linkage(y, method=method)
                c, _ = cophenet(z, y)
                print(self.file_name + '-ilr-' + method + '-' + distance + ': ' + str(c))
                plt.figure(figsize=(15, 8))
                dendrogram(z, labels=ilr_features, leaf_font_size=12)
                plt.yticks(fontsize=12, )
                plt.title(self.file_name + ' ' + method + ' ' + distance + ' Ilr', fontdict={'size': 20})
                plt.ylabel("Distance cluster combine", fontdict={'size': 18})
                for fig in figs:
                    plt.savefig(self.out_path + self.file_name + '_' +
                                method + '_' + distance + '_Ilr.' + fig, bbox_inches='tight', dpi=600)
                plt.close()

    def save_stab(self, wb, figs):

        stab_features = np.delete(self.data_features, [0])
        data_stab = self.stab(self.data_no_ash)

        sheet = wb.add_worksheet('Stability using Geboy approach')
        sheet.write_row('B1', stab_features)
        sheet.write_column('A2', stab_features)
        for i in range(data_stab.shape[0]):
            sheet.write_row(i + 1, 1, data_stab[i, :])

        for method in self.methods:
            data_stab_dis = 1 - data_stab
            y = squareform(data_stab_dis)
            z = linkage(y, method=method)
            c, _ = cophenet(z, y)
            plt.figure(figsize=(15, 8))
            dendrogram(z, labels=stab_features, leaf_font_size=12)
            plt.title(self.file_name + ' ' + method + ' Geboy\'s approach',
                      fontdict={'size': 20})
            plt.ylabel("Distance cluster combine", fontdict={'size': 18})
            for fig in figs:
                plt.savefig(self.out_path + self.file_name + '_' +
                            method + '_' +
                            '_Geboy\'s approach.' + fig, bbox_inches='tight', dpi=600)
            plt.close()

    def dispatch(self, value, wb, figs):
        method_name = 'save_' + value
        method = getattr(self, method_name)
        method(wb, figs)

    def save_data(self):
        wb = xlsxwriter.Workbook(self.out_path + self.file_name + '_processed.xlsx')
        sheet = wb.add_worksheet('Raw data')
        sheet.write_row('B1', self.data_features)
        sheet.write_column('A1', self.data_serial)
        for i in range(self.data_all.shape[0]):
            sheet.write_row(i + 1, 1, self.data_all[i, :])
        for algorithm in self.algorithms:
            self.dispatch(algorithm, wb, self.figs)
        wb.close()
