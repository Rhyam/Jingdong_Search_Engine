import numpy as np
import torch
import torchvision.transforms as transforms
from torchvision.datasets.folder import default_loader
import heapq

model = torch.hub.load('pytorch/vision', 'resnet50', pretrained=True)

normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225])
trans = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    normalize,
])

def features(x):
    x = model.conv1(x)
    x = model.bn1(x)
    x = model.relu(x)
    x = model.maxpool(x)
    x = model.layer1(x)
    x = model.layer2(x)
    x = model.layer3(x)
    x = model.layer4(x)
    x = model.avgpool(x)

    return x

def imgorder(keyword):
    search_image = default_loader('image/%s.jpg' % keyword)
    input_image = trans(search_image)
    input_image = torch.unsqueeze(input_image, 0)
    search_feature_tmp = features(input_image)
    search_feature_tmp = search_feature_tmp.detach().numpy()
    search_feature = []
    for i in range(2048):
        search_feature.append(search_feature_tmp[0][i][0][0])
    search_hash = 0
    for i in range(2048):
        search_hash = (search_hash*13 + search_feature[i]) % 2048

    image_features = np.load('./dataset/img_hash_in_Docker.npy', allow_pickle=True).item()

    for key, value in image_features.items():
        image_features[key] = abs(value - search_hash)

    order_list = sorted(image_features.items(), key=lambda x: x[1])
    return order_list

def logo_shop(keyword):
    search_image = default_loader('image/%s.jpg' % keyword)
    input_image = trans(search_image)
    input_image = torch.unsqueeze(input_image, 0)
    search_feature_tmp = features(input_image)
    search_feature_tmp = search_feature_tmp.detach().numpy()
    search_feature = []
    for i in range(2048):
        search_feature.append(search_feature_tmp[0][i][0][0])
    search_hash = 0
    for i in range(2048):
        search_hash = (search_hash*13 + search_feature[i]) % 2048
    
    shops = np.load('./dataset/logo_hash_in_Docker.npy', allow_pickle=True).item()
    for key, value in shops.items():    
        shops[key] = abs(value - search_hash)
    
    key = min(shops, key=lambda x: shops[x])
    return key
