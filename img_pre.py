import json
import os
import sys
import time
import random
import string
import threading

import pymysql
import requests
from lxml import etree

import time
import os
import numpy as np
import torch
import torchvision.transforms as transforms
from torchvision.datasets.folder import default_loader

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

def img_prepro():    #图片下载并预处理
    count = 0
    data = {}

    if not os.path.exists('data'):
        os.mkdir('data')
    if not os.path.exists('dataset'):
        os.mkdir('dataset')

    for root, dirnames, filenames in os.walk('html'):
        for filename in filenames:
            if not filename.endswith('.txt'):
                continue
            try:
                path = os.path.join(root, filename)
                file = open(path, encoding='gbk')
                line = file.readlines()
                imgurl = "http:" + line[1].strip()
                img_con = requests.get(imgurl)
                url = line[5].strip()
                order = url[20:32]
                file.close()

                print("Downloading %s.jpg" % order)
                f = open('./data/tmp.jpg','wb')
                f.write(img_con.content)
                f.close()
            except Exception as e:
                print("Failed in downloading:", e)
            
            try:
                image = default_loader("data/tmp.jpg")
                input_image = trans(image)
                input_image = torch.unsqueeze(input_image, 0)
                print('Extract features of %s.jpg!' % order)
                image_feature = features(input_image)
                image_feature = image_feature.detach().numpy()
                image_feature_vector = []
                for i in range(2048):
                    image_feature_vector.append(image_feature[0][i][0][0])

                hash = 0
                for i in range(2048):
                    hash = (hash*13 + image_feature_vector[i]) % 2048
                print("The hash value:", hash)
                data[order] = hash
                count += 1
            except Exception as e:
                print("Failed in preprocessing:", e)

    np.save('./dataset/img_hash_in_Docker.npy', data)

    print(count, "images downloaded!")

def logo_prepro():    #logo下载并预处理
    count = 0
    logo = {}
    
    if not os.path.exists('data'):
        os.mkdir('data')
    if not os.path.exists('dataset'):
        os.mkdir('dataset')

    for root, dirnames, filenames in os.walk('html'):
        for filename in filenames:
            if not filename.endswith('.txt'):
                continue
            try:
                path = os.path.join(root, filename)
                file = open(path, encoding='gbk')
                line = file.readlines()
                shop = line[6].strip()
                if shop in logo.keys():
                    continue
                logo_url = line[8].strip()
                if logo_url == 'NONE':
                    continue
                else:
                    logo_url = 'http:' + logo_url
                logo_con = requests.get(logo_url)
                file.close()

                print("Downloading %s.jpg" % shop)
                f = open('./data/tmp.jpg','wb')
                f.write(logo_con.content)
                f.close()
            except Exception as e:
                print("Failed in downloading:", e)
            
            try:
                logo_pic = default_loader("data/tmp.jpg")
                input_image = trans(logo_pic)
                input_image = torch.unsqueeze(input_image, 0)
                print('Extract features of %s.jpg' % shop)
                image_feature = features(input_image)
                image_feature = image_feature.detach().numpy()
                image_feature_vector = []
                for i in range(2048):
                    image_feature_vector.append(image_feature[0][i][0][0])

                hash = 0
                for i in range(2048):
                    hash = (hash*13 + image_feature_vector[i]) % 2048
                print("The hash value:", hash)
                logo[shop] = hash
                count += 1
            except Exception as e:
                print("Failed in preprocessing:", e)

    np.save('./dataset/logo_hash_in_Docker.npy', logo)
    print(count, "logos downloaded!")

if __name__ == '__main__':
    print('Load model: ResNet50')
    model = torch.hub.load('pytorch/vision', 'resnet50', pretrained=True)

    normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                     std=[0.229, 0.224, 0.225])
    trans = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        normalize,
    ])

    img_prepro()
    logo_prepro()