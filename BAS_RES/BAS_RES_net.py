from BAS_RES.BASNet import BASNet
from BAS_RES.my_resnet import *
import torch
import torch.nn as nn
from torch.nn import functional as F
class ronghe(nn.Module):
    def __init__(self):
        super(ronghe, self).__init__()
        self.fc1 = nn.Linear(512 , 256)
        self.relu1 = nn.ReLU(inplace=True)
        self.fc2 = nn.Linear(256, 256)
        self.relu2 = nn.ReLU(inplace=True)
        self.fc3 = nn.Linear(256, 512)
        self.relu3 = nn.ReLU(inplace=True)

    def forward(self, x):
        hx = self.fc1(x)
        hx = self.relu1(hx)

        hx = self.fc2(hx)
        hx = self.relu2(hx)

        hx = self.fc3(hx)
        hx = self.relu3(hx)

        return hx

class MYnet(nn.Module):
    def __init__(self,num_classes):
        super(MYnet,self).__init__()
        print("...load resnet...")
        res_model_path = r"D:\PycharmProjects\fossilhunter\BAS_RES\save_model\resnet50.pt" #在imgnet上训练好的模型
        pretrained_dict = torch.load(res_model_path, map_location=torch.device('cpu'))['model_state_dict']
        # pretrained_dict = torch.load(res_model_path)
        resnet = resnet50(pretrained=False)
        model_dict = resnet.state_dict()
        pretrained_dict = {k: v for k, v in pretrained_dict.items() if k in model_dict}
        model_dict.update(pretrained_dict)
        resnet.load_state_dict(model_dict)
        for param in resnet.named_parameters():
            # if param[0].split(".")[0]!="layer4" and param[0].split(".")[0]!="layer3":
            param[1].requires_grad = False
        # num_ftrs = resnet.fc.in_features
        # resnet.fc = nn.Linear(num_ftrs, 5)


        #-------------1.26_0:33修改
        # for param in resnet.named_parameters():
        #     param[1].requires_grad = False
        # -------------1.26_0:33修改
        self.resnet = resnet

        print("...load BASNet...")
        bas_model_path = r"D:\PycharmProjects\fossilhunter\BAS_RES\save_model\basnet.pth"#训练好的分割模型
        basnet = BASNet(3, 1)
        basnet.load_state_dict(torch.load(bas_model_path))
        for param in basnet.named_parameters():
            param[1].requires_grad = False

        self.basnet = basnet
        #resnet50-----------------

        self.conv1 = nn.Conv2d(512, 512, kernel_size=3, padding=1) #对basnet输出卷积
        self.bn1 = nn.BatchNorm2d(512)

        self.conv2 = nn.Conv2d(2048, 512, kernel_size=1) #对resnet输出卷积
        self.bn2 = nn.BatchNorm2d(512)

        self.conv3 = nn.Conv2d(1024, 512, kernel_size=3,padding=1)#对拼接后的卷积 原来是1
        self.bn3 = nn.BatchNorm2d(512)
        self.relu = nn.ReLU(inplace=True)
        # self.relu = nn.PReLU(512)
        # self.relu = nn.Softmax(dim=1)
        #----------------------res18
        # self.conv1 = nn.Conv2d(512, 512, kernel_size=1)
        # self.bn = nn.BatchNorm2d(512)
        # self.relu = nn.ReLU(inplace=True)
        #------------------------
        self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc = nn.Linear(512 , num_classes)
        ## -------------Encoder--------------
        # self.ronghe = ronghe()


    def forward(self,x):
        basx = self.basnet(x)
        basx = self.conv1(basx)
        basx = self.bn1(basx)
        basx = F.relu(basx)

        resx = self.resnet(x)
        hx = self.conv2(resx)
        hx = self.bn2(hx)
        hx = F.relu(hx)


        #-------------1.26_0:33修改
        # hx = self.bn(hx)
        # hx = self.relu(hx)
        # -------------1.26_0:33修改
        #加
        # hx1 = torch.add(hx,basx)
        # hx = self.bn(hx1)
        # hx = self.relu(hx)
        # hx1 = torch.sigmoid(hx1)
        # hx1 = torch.softmax(hx1,dim=1)
        #乘
        # x1 = torch.sigmoid(hx)
        # y1 = torch.sigmoid(basx)
        # hx1 = torch.matmul(hx,basx)
        # hx1 = x1 * y1

        # cat
        hx1 = torch.cat((hx,basx),dim=1)
        hx = self.conv3(hx1)
        hx = self.bn3(hx)
        hx = self.relu(hx)

        hx = self.avgpool(hx)
        hx = hx.reshape(hx.size(0), -1)
        # feature = hx
        hx = self.fc(hx)
        hx = F.softmax(hx,dim=1)
        return hx

