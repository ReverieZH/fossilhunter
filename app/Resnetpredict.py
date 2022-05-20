import torch
from PIL import Image
import requests as req
from io import BytesIO
from torchvision import transforms
import torchvision.models as models

class Resnetpredict:
    def __init__(self):
        self.filepath = ''
    def setfilepath(self, filepath):
        self.filepath = filepath
    def predict(self):

        transform = transforms.Compose([
            transforms.Resize(512),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225])
        ])
        device = torch.device("cpu")
        model_path = 'D:/best.pt'
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        model_ft = models.resnet50(pretrained=False)
        num_ftrs = model_ft.fc.in_features
        model_ft.fc = torch.nn.Linear(num_ftrs, 5)
        checkpoint = torch.load(model_path, map_location=device)
        model_ft.load_state_dict(checkpoint['model_state_dict'])
        model_ft = model_ft.to(device)

        label = []
        img_path = self.filepath
        tags = {
            "0":"三叶虫",
            "1":"奇虾",
            "2":"曳鳃动物",
            "3":"异虫类",
            "4":"真节肢动物",
                }
        model_ft.eval()

        torch.no_grad()
        response = req.get(self.filepath)
        img = Image.open(BytesIO(response.content))
        inputs = transform(img).unsqueeze(0)
        inputs = inputs.to(device)
        outputs = model_ft(inputs)
        value, preds = torch.max(outputs, 1)
        preds = tags[str(preds.item())]

        return preds