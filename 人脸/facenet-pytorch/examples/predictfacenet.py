#%% md

# Face detection and recognition inference pipeline

#%%

from facenet_pytorch import MTCNN, InceptionResnetV1
import torch
from torch.utils.data import DataLoader
from torchvision import datasets
import numpy as np
import pandas as pd
import os

workers = 0 if os.name == 'nt' else 4

#%% md

#### Determine if an nvidia GPU is available

#%%

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
print('Running on device: {}'.format(device))

#%% md

#### Define MTCNN module


#%%

mtcnn = MTCNN(
    image_size=160, margin=0, min_face_size=20,
    thresholds=[0.6, 0.7, 0.7], factor=0.709, post_process=True,
    device=device
)

#%% md

#### Define Inception Resnet V1 module

# 直接就会自动下载权重.         # 是facenet的网络.
resnet = InceptionResnetV1(pretrained='vggface2').eval().to(device)       #把一张图片变成高维的一个点坐标.

#%% md



def collate_fn(x):
    return x[0]  # 因为他外面包了一层,所以退掉即可.

dataset = datasets.ImageFolder('../data/test_images')
dataset.idx_to_class = {i:c for c, i in dataset.class_to_idx.items()}
loader = DataLoader(dataset, collate_fn=collate_fn, num_workers=workers)

#%% md

#### Perfom MTCNN facial detection

#%%

aligned = []
names = []
for x, y in loader:
    x_aligned, prob = mtcnn(x, return_prob=True)
    if x_aligned is not None:
        print('Face detected with probability: {:8f}'.format(prob))
        aligned.append(x_aligned)
        names.append(dataset.idx_to_class[y])

#%% md

#### Calculate image embeddings

#%%

aligned = torch.stack(aligned).to(device)  # 按照0维度进行摞起来.   也就是把list 变成batch_size ,.... 然后就可以批量扔网络里面跑一次出来了.
embeddings = resnet(aligned).detach().cpu()

#%% md

#### Print distance matrix for classes

#%%

dists = [[(e1 - e2).norm().item() for e2 in embeddings] for e1 in embeddings] # 就是L2范数. 欧几里得长度.
print(pd.DataFrame(dists, columns=names, index=names))
