from __future__ import print_function, division
from res_net.resnet import *
import torch.nn as nn

import os
from skimage import io
import torch
# import torch.nn as nn
# import torch.nn.functional as F
from torch.utils.data import DataLoader
from torchvision import transforms#, utils
# import torch.optim as optim
# import matplotlib.pyplot as plt
# import numpy as np
from PIL import Image
from res_net.dataload import RescaleT, ToTensorLab,SalObjDataset
from BAS_net.model import BASNet
from BAS_RES.BAS_RES_net import MYnet

def test(my_model):
    label = []
    imgpath = []
    tags = {
        "0":"trilobites",
        "1":"shrimp",
        "2":"Drag_gills",
        "3":"Different_insect",
        "4":"Euarthropods",
            }
    my_model.eval()
    dic_feature = {}
    for i, data_test in enumerate(dataloader):

        path = data_test["path"]
        # print(path)
        inputs = data_test["image"]
        inputs = inputs.type(torch.FloatTensor)
        inputs = inputs.to(device)
        inputs = inputs.to(device)
        outputs,feature = my_model(inputs)
        # value, preds = torch.max(outputs, 1)
        # preds = tags[str(preds.item())]
        clss_name = path[0].split("\\")[-2]
        img_name = path[0].split("\\")[-1]
        img_name = clss_name+"_"+img_name
        dic_feature[img_name] = feature.cpu().detach().numpy()
        # label.append(preds)
    return  dic_feature

def x_y_list(img_path):
    img_list = []
    label_list = []
    for child_dir in os.listdir(img_path):
        child_path = os.path.join(img_path, child_dir)
        for dir_image in os.listdir(child_path):
            img = os.path.join(child_path, dir_image)
            img_list.append(img)
            label_list.append(child_dir)
    return img_list, label_list

if __name__ == '__main__':
    test_data_path = r"..\..\dataset\new_test\111"
    my_model_path = r"./result/my_model18_No_expand_74%/best.pt"
    model_name = "my18_No_exp"
    img_list, label_list = x_y_list(test_data_path)
    datasets = SalObjDataset(img_name_list=img_list, lbl_name_list=label_list,
                             transform=transforms.Compose([RescaleT(256), ToTensorLab(flag=0)]))
    dataloader = DataLoader(datasets, batch_size=1, shuffle=False, num_workers=0)
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    #resnet
    # print("...load resnet...")
    # my_model = resnet18(pretrained=False)
    # num_ftrs = my_model.fc.in_features
    # my_model.fc = nn.Linear(num_ftrs, 5)

    #------------mynet
    print("...load mynet...")
    my_model = MYnet(num_classes=5)
    #---------------------
    checkpoint = torch.load(my_model_path)
    my_model.load_state_dict(checkpoint['model_state_dict'])
    my_model = my_model.to(device)
    dic_feature = test(my_model)
    try:
        os.makedirs('new_features/')
    except:
        pass
    import _pickle as pickle
    exp_pkl = open('./new_features/' + model_name + '_features.pkl', 'wb')
    data = pickle.dumps(dic_feature)
    exp_pkl.write(data)
    exp_pkl.close()

