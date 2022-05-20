from __future__ import print_function, division
import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler
from torchvision import transforms
import time
import os
from torch.utils.data import DataLoader
from dataload import ToTensorLab, SalObjDataset,RandomCrop,RescaleT
from BAS_RES_net import MYnet
tags = {"trilobites": 0,#三叶虫
                "shrimp": 1,#虾
                "Drag_gills": 2,    #曳鳃动物
                "Different_insect": 3,#异虫类
                "Euarthropods": 4,#真节肢动物
                }
def train_model(model, criterion, optimizer, scheduler,model_name, num_epochs=25,lambdaL1=0.00001):
    since = time.time()
    best_acc = 0.0
    current_dir1 = os.path.dirname(__file__)
    weights = os.path.join(current_dir1, 'result/{}/'.format(model_name))
    if not os.path.exists(weights):
        os.makedirs(weights)
    last = os.path.join(weights,'last.pt')
    best = os.path.join(weights,'best.pt')
    print("最终模型保存地址：\t",last)
    train_len = len(dataloader)
    epoch_loss_acc=os.path.join(weights,"result.txt")
    f=open(epoch_loss_acc,'w')
    loss = 0
    epoch = 0
    for epoch in range(1,num_epochs+1):
        scheduler.step()
        model.train()
        running_loss = 0.0
        running_corrects = 0
        for i, data_test in enumerate(dataloader):
            path = data_test["path"]
            inputs = data_test["image"]
            labels = data_test["label"]
            inputs = inputs.type(torch.FloatTensor)
            labels = labels.type(torch.FloatTensor)
            inputs = inputs.to(device)
            labels = labels.to(device)
            optimizer.zero_grad()
            with torch.set_grad_enabled(True):
                # regularization_loss = 0
                # for param in model.parameters():
                #     regularization_loss += torch.sum(abs(param))

                outputs = model(inputs)
                _, preds = torch.max(outputs, 1)
                loss = criterion(outputs, labels.long())
                loss.backward()
                optimizer.step()
                # 统计
            running_loss += loss.item() * inputs.size(0)
            running_corrects += torch.sum(preds == labels.data.long())

            print('Epoch: [{:3d}/{:3d}] || iters: [{:3d}/ {:3d}] || loss: {:.4f} || lr : {}'
                .format(epoch, num_epochs, i, train_len, loss.data.item(),optimizer_ft.param_groups[0]['lr']))
        torch.cuda.empty_cache()
        epoch_loss = running_loss / len(dataset)
        epoch_acc = running_corrects.double() / len(dataset)
        torch.save({
            'epoch': epoch,
            'model_state_dict': model.state_dict(),
            'optimizer_state_dict': optimizer.state_dict(),
            'loss': loss,
        }, os.path.join(weights,'epoch_%d.pt'%epoch))
        print('-' * 100)
        print('Epoch: [{:3d}/{:3d}] ||  epoch_loss: {:.4f} || epoch_acc: {:.4f} || lr : {}'
              .format(epoch, num_epochs, epoch_loss,epoch_acc,optimizer_ft.param_groups[0]['lr']))
        f.write('Epoch: [{:3d}/{:3d}] ||  epoch_loss: {:.4f} || epoch_acc: {:.4f} || lr : {} \n'
              .format(epoch, num_epochs, epoch_loss,epoch_acc,optimizer_ft.param_groups[0]['lr']))
        print('-' * 100)
        # deep copy the model
        if  epoch_acc > best_acc:
            best_acc = epoch_acc
            torch.save({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'loss': loss,
            }, best)
        print()
    time_elapsed = time.time() - since
    print('Training complete in {:.0f}m {:.0f}s'.format(
        time_elapsed // 60, time_elapsed % 60))
    f.write('Training complete in {:.0f}m {:.0f}s\n'.format(
        time_elapsed // 60, time_elapsed % 60))
    print('Best val Acc: {:4f}'.format(best_acc))
    f.write('Best val Acc: {:4f}\n'.format(best_acc))
    torch.save({
        'epoch': epoch,
        'model_state_dict': model.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
        'loss': loss,
         }, last)
    f.close()

#读取图片列表，以文件名作为label
def x_y_list(img_path):
    img_list = []
    label_list = []
    for child_dir in os.listdir(img_path):
        child_path = os.path.join(img_path, child_dir)
        for dir_image in os.listdir(child_path):
            img = os.path.join(child_path, dir_image)
            img_list.append(img)
            label_list.append(tags[child_dir])
    return img_list, label_list

if __name__ == '__main__':
    img_path = r"..\..\dataset\new_train\new_expand1"#总文件夹，分类是小文件夹
    model_name = "my_50_exp_softmax1"
    train_x_list, train_y_list = x_y_list(img_path)
    dataset = SalObjDataset(train_x_list,
                            train_y_list,
                            transform=transforms.Compose([
                                RescaleT(256),
                                RandomCrop(224),
                                ToTensorLab(flag=0)]))
    dataloader = DataLoader(dataset,
                            batch_size=16,
                            num_workers=0,
                            shuffle=True,
                            pin_memory=True,
                            )
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    my_model = MYnet(num_classes=5)
    my_model.to(device)
    criterion = nn.CrossEntropyLoss()

    optimizer_ft = optim.Adam(my_model.parameters(), lr=0.00001)
    # 设置学习率每7个epoch衰减0.1
    exp_lr_scheduler = lr_scheduler.StepLR(optimizer_ft, step_size=5, gamma=0.1)
    train_model(my_model, criterion, optimizer_ft, exp_lr_scheduler,model_name=model_name,
                           num_epochs=10,lambdaL1=0)

