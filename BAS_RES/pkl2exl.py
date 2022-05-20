#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@author: HG
@contact: 18165271995@163.com
@file: pkl2exl.py
@time: 2019/11/2 21:04
'''
import _pickle as pickle
import xlrd
from xlutils.copy import copy
import os
import xlwt



def read(pkl_file):
    features = pickle.load(open(pkl_file, 'rb'))
    xls_path = split(pkl_file)
    j = 0
    book = xlrd.open_workbook(xls_path, formatting_info=True)
    newb = copy(book)
    new_sheet = newb.get_sheet(0)
    for image, feature in features.items():
        (img_filepath, tempfilename) = os.path.split(image)
        (img_filename, extension) = os.path.splitext(tempfilename)
        vector = feature.reshape(feature.shape[1])
        new_sheet.write(0, j, img_filename)
        MAX, MIN = norm(vector)
        for i in range(vector.shape[0]):
            new_vector = (vector[i] - MIN) / (MAX - MIN)
            new_sheet.write(i + 1, j, str(new_vector))

        # save(xls_path,img_filename,feature,j)
        j += 1
        print("%s转化成功" % (img_filename))
    newb.save(xls_path)


def save(xls_path,img_filename,vector,j):
    book = xlrd.open_workbook(xls_path, formatting_info=True)
    newb = copy(book)
    new_sheet = newb.get_sheet(0)
    vector = vector.reshape(vector.shape[1])
    new_sheet.write(0, j, img_filename)
    MAX,MIN=norm(vector)
    for i in range(vector.shape[0]):
        new_vector=(vector[i]-MIN)/(MAX-MIN)
        new_sheet.write(i + 1, j, str(new_vector))

    newb.save(xls_path)
    print("%s转化成功"%(img_filename))
def norm(vector):
    MAX=max(vector)
    MIN=min(vector)
    return MAX,MIN

def split(pkl_file):
    (filepath, tempfilename) = os.path.split(pkl_file)
    (filename, extension) = os.path.splitext(tempfilename)

    try:
        workbook = xlwt.Workbook(encoding='utf-8')  # 新建工作簿
        sheet1 = workbook.add_sheet("sheet1")  # 新建sheet
        workbook.save(filepath+"/"+filename+".xls")
    except:
        pass
    path=os.path.join(filepath,filename+".xls")
    return path



if __name__ == '__main__':
    pkl_file = r"./features/my_model_18_features.pkl"
    read(pkl_file)