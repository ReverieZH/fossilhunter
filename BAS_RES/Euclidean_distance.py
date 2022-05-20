#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@author: HG
@contact: 18165271995@163.com
@file: Euclidean_distance.py
@time: 2019/11/4 20:37
'''
import matplotlib.pyplot as plt
import xlrd
import numpy as np

def read_excel(path):
    data = xlrd.open_workbook(path)
    sheet = data.sheet_by_index(0)
    rows = sheet.nrows
    cows = sheet.ncols
    name_list = []
    feature_list = []
    for i in range(cows):#列
        name = sheet.row(0)[i].value
        feature = np.zeros((1024, 1))
        for j in range(1,rows):
            feature[j-1, 0] = np.array(sheet.row(j)[i].value)
        name_list.append(name)
        feature_list.append(feature)

    return name_list,feature_list
if __name__ == '__main__':

    use_path=r"./features/best_my18_best_test_features.xls"
    sum_path=r"./features/best_my18_best_train_features.xls"

    use_name,use_feature = read_excel(use_path)
    sum_name,sum_feature = read_excel(sum_path)


    for i in range(len(use_feature)):
        print("*"*100)
        print("检索图片为：%s"%use_name[i])
        # sum_distance = []
        d = {}
        for j in range(len(sum_feature)):
            distance = np.sqrt(np.sum(np.square(sum_feature[j] - use_feature[i]))) #单个度量
            # sum_distance.append(distance)
            d[sum_name[j]]=distance
        sort_sum_distance = sorted(d.items(), key=lambda x: x[1], reverse=False)
        ten_sum_distance=sort_sum_distance[:10]
        print("%s欧氏距离排序整体是：\n" % (use_name[i]))
        print(sort_sum_distance)
        print("%s欧氏距离最短前十个是：\n" % (use_name[i]))
        print(ten_sum_distance)
        # A=[]
        # for i in range(len(sort_sum_distance)):
        #     # plt.hist(sort_sum_distance[i][1],bins=i)
        # #     plt.show()
        #     A.append(sort_sum_distance[i][1])
        #     # print(sort_sum_distance[i][1])
        # plt.hist(A,bins=195)
        # plt.show()
