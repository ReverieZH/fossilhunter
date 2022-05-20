import numpy as np
import matplotlib.pyplot as plt
import json
from sklearn import manifold
import xlrd

import pandas as pd

def excel_one_line_to_list(path):
    df = pd.read_excel(path, names=None)  # 读取项目名称和行业领域两列，并不要列名
    df_li = df.values.tolist()
    labels = list(df.columns.values)
    labels = [x.split("_")[0] for x in labels]
    return df_li ,labels

def draw_tsne(Y,X):
    tags = {"trilobites": 0,  # 三叶虫
            "shrimp": 1,  # 虾
            "Drag": 2,  # 曳鳃动物
            "Different": 3,  # 异虫类
            "Euarthropods": 4,  # 真节肢动物
            }
    '''t-SNE'''
    tsne = manifold.TSNE(n_components=2, init='pca', random_state=501)
    X = np.array(X).T
    y = np.array(Y)
    X_tsne = tsne.fit_transform(X)
    print(X.shape)
    print(X_tsne.shape)
    print(y.shape)
    print("Org data dimension is {}.Embedded data dimension is {}".format(X.shape[-1], X_tsne.shape[-1]))

    '''嵌入空间可视化'''
    x_min, x_max = X_tsne.min(0), X_tsne.max(0)
    X_norm = (X_tsne - x_min) / (x_max - x_min)  # 归一化
    plt.figure(figsize=(4, 4))
    for i in range(X_norm.shape[0]):
        plt.text(X_norm[i, 0], X_norm[i, 1], '*', color=plt.cm.Set1(tags[Y[i]]),
                 fontdict={'weight': 'bold', 'size': 10})
    plt.xticks([])
    plt.yticks([])
    plt.show()

if __name__ == '__main__':
    sum_path = r"./new_features/my50_No_exp_features.xls"
    use_feature,use_name = excel_one_line_to_list(sum_path)
    # use_name, use_feature = read_excel(sum_path)
    draw_tsne(use_name,use_feature)
