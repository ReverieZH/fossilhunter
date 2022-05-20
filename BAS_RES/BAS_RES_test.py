from __future__ import print_function, division
from torch.nn import functional as F
import numpy as np
import matplotlib.pyplot as plt
import cv2
import os
import requests as req
from io import BytesIO
from skimage import io
import torch
from torchvision import transforms
from PIL import Image
from BAS_RES.dataload import RescaleT, ToTensorLab, SalObjDataset
import BAS_RES.BASNet
from BAS_RES.BAS_RES_net import MYnet

class BASRESpredict:
    def __init__(self):
        self.filepath = ''
        self.my_model = None
    def setfilepath(self, filepath):
        self.filepath = filepath
    def normPRED(self, d):
        ma = torch.max(d)
        mi = torch.min(d)
        dn = (d-mi)/(ma-mi)
        return dn

    def heat_map(self, feature_map):
        feature = torch.squeeze(feature_map, dim=1)

        feature = torch.sum(feature,dim=1)
        feature = feature.data.cpu().numpy()  # 得到的cuda加速的输出不能直接转变成numpy格式的，当时根据报错的信息首先将变量转换为cpu的，然后转换为numpy的格式
        feature = feature.reshape(feature.shape[1],feature.shape[2]).astype(np.uint8)
        feature = feature / feature.max()
        plt.imshow(feature)
        plt.show()
        return feature
    #--------------------------------------------------------------------------------
    def returnCAM(self, feature_conv, weight_softmax, class_idx):
        # generate the class activation maps upsample to 256x256
        size_upsample = (224, 224)
        bz, nc, h, w = feature_conv.shape
        output_cam = []
        for idx in class_idx:
            feature_conv = feature_conv.reshape((nc, h*w))
            feature_conv = np.squeeze(feature_conv.data.cpu().numpy())
            weight_softmax = weight_softmax[idx]
            weight_softmax = weight_softmax.reshape((1,weight_softmax.size))
            print(feature_conv.shape)
            print(weight_softmax.shape)
            cam = weight_softmax.dot(feature_conv)
            cam = cam.reshape(h, w)
            cam = cam - np.min(cam)
            cam_img = cam / np.max(cam)
            cam_img = np.uint8(255 * cam_img)
            output_cam.append(cv2.resize(cam_img, size_upsample))
        return output_cam

    def CAM(self, model,outputs,features_map,img):
        img = np.squeeze(img.data.cpu().numpy())
        img = img.transpose([1,2,0])
        params = list(model.parameters())
        # get the last and second last weights, like [classes, hiden nodes]
        weight_softmax = np.squeeze(params[-2].data.cpu().numpy())
        classes = {
            "0": "trilobites",
            "1": "shrimp",
            "2": "Drag_gills",
            "3": "Different_insect",
            "4": "Euarthropods",
        }
        h_x = F.softmax(outputs, dim=1).data.squeeze()  # softmax
        probs, idx = h_x.sort(0, True)  # probabilities of classes

        probs = probs.cpu().numpy()
        idx = idx.cpu().numpy()
        # output: the prediction
        for i in range(0, 4):
            print('{:.3f} -> {}'.format(probs[i], classes[str(idx[i])]))
        CAMs = self.returnCAM(features_map, weight_softmax, [idx[0].item()])
        height,width,_ = img.shape
        CAM = cv2.resize(CAMs[0], (width, height))
        heatmap = cv2.applyColorMap(CAM, cv2.COLORMAP_JET)
        result = heatmap * 0.3 + img * 0.5
        plt.imshow(result)
        plt.show()
        # cv2.imwrite('cam.jpg', result)

    #---------------------------------------------------------------------------------

    def BAS_main(self, model_path):
        print("...load BASNet...")
        net = BAS_RES.BASNet(3, 1)
        net.load_state_dict(torch.load(model_path))
        if torch.cuda.is_available():
            net.cuda()
        net.eval()
        return net

    def save_output(self, image_name,pred,d_dir):
        predict = pred
        predict = predict.squeeze()
        predict_np = predict.cpu().data.numpy()

        im = Image.fromarray(predict_np * 255).convert('RGB')
        img_name = image_name.split("\\")[-1]
        image = io.imread(image_name)
        imo = im.resize((image.shape[1], image.shape[0]), resample=Image.BILINEAR)

        pb_np = np.array(imo)

        aaa = img_name.split(".")
        bbb = aaa[0:-1]
        imidx = bbb[0]
        for i in range(1, len(bbb)):
            imidx = imidx + "." + bbb[i]

        imo.save(os.path.join(d_dir, imidx + '.png'))
    def test(self, my_model):
        label = []
        imgpath = []
        tags = {
            "0":"三叶虫",
            "1":"奇虾",
            "2":"曳鳃动物",
            "3":"异虫类",
            "4":"真节肢动物",
                }
        my_model.eval()
        loader = transforms.Compose([transforms.ToTensor()])
        filepath = self.filepath
        response = req.get(filepath)
        # print("识别图像:", response.content)
        img = Image.open(BytesIO(response.content))
        inputs = loader(img).unsqueeze(0)
        inputs = inputs.type(torch.FloatTensor)
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        inputs = inputs.to(device)
        inputs = inputs.to(device)
        outputs = my_model(inputs)
        value, preds = torch.max(outputs, 1)
        preds = tags[str(preds.item())]
        return preds

    def x_y_list(self, img_path):
        img_list = []
        label_list = []
        for child_dir in os.listdir(img_path):
            child_path = os.path.join(img_path, child_dir)
            for dir_image in os.listdir(child_path):
                img = os.path.join(child_path, dir_image)
                img_list.append(img)
                label_list.append(child_dir)
        return img_list, label_list

    def loadmodel(self):
        my_model_path = r"D:\PycharmProjects\fossilhunter\BAS_RES\save_model\best.pt"
        device = torch.device("cpu")
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        #------------resnet
        print("...load mynet...")
        self.my_model = MYnet(num_classes=5)
        checkpoint = torch.load(my_model_path, map_location=torch.device('cpu'))
        self.my_model.load_state_dict(checkpoint['model_state_dict'])
        self.my_model = self.my_model.to(device)
        #---------------------

    def predict(self):
        pre_labels = self.test(self.my_model)
        print(pre_labels)
        return pre_labels


