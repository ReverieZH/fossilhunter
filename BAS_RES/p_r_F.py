
import numpy as np
def precison(feature):#precison
    nrow = len(feature)
    ncol = len(feature[0])
    num_top = []
    for i in range(nrow):
        num_pre = 0
        top = []
        for j in range(ncol):
            num_pre+=feature[i][j]
            pre = num_pre/(j+1)
            top.append(pre)
        num_top.append(top)
    num_top = np.array(num_top)
    pre_top = np.mean(num_top,axis=0)

    return pre_top
def recall(feature,n):#precison
    nrow = len(feature)
    ncol = len(feature[0])
    num_top = []
    for i in range(nrow):
        num_recall = 0
        top = []
        for j in range(ncol):
            num_recall+=feature[i][j]
            recall = num_recall/n
            top.append(recall)
        num_top.append(top)
    num_top = np.array(num_top)
    pre_top = np.mean(num_top,axis=0)

    return pre_top
def F(pre,recall):
    F_score = np.zeros(shape=len(pre))
    for i in range(len(pre)):
        F_score[i] = 2*pre[i]*recall[i]/(pre[i]+recall[i])

    return F_score
if __name__ == '__main__':
    #Drag_gills
    # n_list = [
    #     [1  ,  1 ,   1  ,  1  ,  1  ,  1   , 1  ,  1  ,  0  ,  1],
    #     [1  ,  1  ,  1 ,   1 ,   0   , 1  ,  1  ,  0  ,  1  ,  1],
    #     [1  ,  1  ,  1   , 1   , 1  ,  1  ,  1   , 1   , 1  ,  1],
    #     [1  ,  1   , 1  ,  1   , 1  ,  1  ,  1  ,  1 ,   1  ,  1],
    #     [1  ,  1  ,  1  ,  1   , 1  ,  1  ,  1 ,   1  ,  1  ,  1],
    #     [1  ,  1   , 1  ,  1   , 1  ,  1   , 1  ,  1  ,  1  ,  1],
    #     [1  ,  1   , 1  ,  1   , 1  ,  1   , 1  ,  1  ,  1  ,  1],
    #     [1  ,  1   , 1  ,  1   , 0  ,  1  ,  0  ,  1  ,  1  ,  1],
    #     [1  ,  1   , 1  ,  1  ,  1   , 1  ,  1  ,  1  ,  1  ,  1],
    #     [1  ,  1   , 1  ,  1  ,  1  ,  1   , 1  ,  1   , 1  ,  1],
    #     [1  ,  1  ,  1  ,  1  ,  1   , 1  ,  1  ,  1  ,  1  ,  1],
    #
    # ]
    #Different_insect
    # n_list = [
    #     [1 ,   1 ,   1   , 1  ,  1  ,  1  ,  1  ,  1 ,   1  ,  1],
    #     [1  ,  1  ,  1   , 1  ,  1  ,  1  ,  1  ,  1  ,  1  ,  1],
    #     [1   , 1 ,   1  ,  1  ,  1   , 1  ,  1  ,  1 ,   1  ,  1],
    #     [1    ,1  ,  1  ,  1  ,  1   , 1  ,  1  ,  1 ,   0  ,  1],
    #     [1    ,1,    1  ,  1   , 1  ,  1  ,  1 ,   1  ,  1 ,   1]
    #
    # ]
    #Euarthropods
    # n_list = [
    #     [0  ,  0   , 1  ,  0 ,   0,    0    ,0,    0   , 0,    0],
    #     [1  ,  0   , 0  ,  0,    0 ,   0    ,0 ,   0  ,  0 ,   0],
    #     [1  ,  1  ,  0  ,  0    ,0  ,  0   , 0  ,  0 ,   0  ,  0],
    #     [1  ,  1  ,  1  ,  1   , 1   , 1  ,  1   , 1 ,   1   , 1],
    #     [1   , 1  ,  1  ,  1  ,  1 ,   1  ,  1    ,1 ,   1    ,1],
    #     [1  ,  0   , 0  ,  0 ,   0    ,0  ,  0,    0,    0 ,   0],
    #     [1  ,  1  ,  1  ,  0,    0,    0,    0,    0    ,0,    0],
    #     [1  ,  1  ,  1   , 1    ,1 ,   1    ,1 ,   1   , 1  ,  1],
    #     [1  ,  1  ,  1   , 1    ,1  ,  1   , 1  ,  1  ,  1 ,   1],
    #     [1  ,  1  ,  1   , 1   , 1   , 1  ,  1   , 1 ,   1   , 1],
    #     [1  ,  0  ,  0   , 0  ,  0    ,0 ,   0    ,0 ,   0   , 0],
    #     [1  ,  1  ,  1  ,  1 ,   1    ,1,    1    ,1,    1    ,1]
    #
    # ]
    #shrimp
    # n_list = [
    #     [1,    1    ,0,    0    ,0   , 1,    1,    1    ,1,    1],
    #     [1 ,   1   , 1 ,   1   , 1  ,  1 ,   1 ,   1   , 1 ,   1],
    #     [1  ,  1  ,  0  ,  0  ,  1  ,  1    ,0  ,  0  ,  1  ,  1],
    #     [1   , 1 ,   0   , 0  ,  0 ,   0  ,  0   , 0 ,   0    ,0],
    #     [1    ,1,    1   , 1,    1,    1   , 1    ,1,    1   , 1]
    #
    # ]
    #trilobites
    # n_list = [
    #     [1,    1  ,  1,    1  ,  1,    1  ,  1,    1  ,  1,    1],
    #     [1 ,   1 ,   1 ,   1 ,   1 ,   1 ,   1 ,   1 ,   1 ,   1],
    #     [1  ,  1    ,1  ,  1,    1  ,  1,    1  ,  1,    1  ,  1],
    #     [1   , 1   , 1   , 1    ,1   , 0   ,1   , 1    ,1   , 1],
    #     [1    ,1  ,  1    ,1  ,  1    ,1   , 1    ,1   , 1,    1],
    #     [1,    0   , 1,    1   , 1,    1  ,  1,    1  ,  1 ,   1],
    #     [1 ,   1 ,   1 ,   1 ,   1 ,   1 ,   1 ,   1 ,   1  ,  1],
    #     [1  ,  1,    1   , 1,    1  ,  1,    1  ,  1,    1   , 1],
    #     [1   , 1    ,1  ,  1    ,1   , 1    ,1   , 1    ,1    ,1],
    #     [1    ,0   , 0   , 1   , 0    ,0   , 1   ,0   , 0,    1],
    #     [1,    1  ,  1    ,1  ,  1,    1  ,  1,    1  ,  1 ,   1],
    #     [1 ,   1 ,   1 ,   1 ,   1 ,   1 ,   1 ,   0 ,   1  ,  1],
    #     [1  ,  1,    0  ,  1,    1  ,  1,    1  ,  1,    1   , 1],
    #
    # ]
    # pre_top = precison(n_list)
    # print(pre_top)
    # print("*"*40)
    # recall_top = recall(n_list,32)
    # print(recall_top)
    # print("*" * 40)
    # F_score = F(pre_top, recall_top)
    # print(F_score)
    import torch
    import torch.nn as nn

    # x = np.exp(0.114) + np.exp(0.009) + np.exp(0.1488) + \
    #     np.exp(0.1029) + np.exp(0.0318)
    # x = np.log2(x)
    #
    # print(x)
    x_input = torch.tensor([[0.324,0.019,0.1488,0.1029,0.0318]])  # ??????????????????
    print('x_input:\n', x_input)
    y_target = torch.tensor([0])  # ????????????????????? print('y_target\n',y_target)

    # ????????????softmax??????????????????????????????????????????????????????1
    softmax_func = nn.Softmax(dim=1)
    soft_output = softmax_func(x_input)
    print('soft_output:\n', soft_output)

    # ???softmax???????????????log
    log_output = torch.log(soft_output)
    print('log_output:\n', log_output)

    # ??????softmax???log????????????nn.LogSoftmaxloss(?????????????????????)?????????????????????????????????????????????
    logsoftmax_func = nn.LogSoftmax(dim=1)
    logsoftmax_output = logsoftmax_func(x_input)
    print('logsoftmax_output:\n', logsoftmax_output)

    # pytorch?????????NLLLoss???????????????????????????reducetion=True???size_average=True
    nllloss_func = nn.NLLLoss()
    nlloss_output = nllloss_func(logsoftmax_output, y_target)
    print('nlloss_output:\n', nlloss_output)

    # ????????????pytorch??????loss_func=nn.CrossEntropyLoss()????????????NLLLoss????????????????????????
    crossentropyloss = nn.CrossEntropyLoss()
    crossentropyloss_output = crossentropyloss(x_input, y_target)
    print('crossentropyloss_output:\n', crossentropyloss_output)

