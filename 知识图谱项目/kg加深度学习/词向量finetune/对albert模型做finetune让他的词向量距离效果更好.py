'''
找同义词表,然后让他们cosin值趋近于1, 这样参数保存之后,起码能保证经过训练的词语能表现距离了.

'''






'''
看看bert词向量的用法:



https://github.com/hanxiao/bert-as-service/tree/master/server/bert_serving/server/bert







'''








from bert4keras.backend import keras
from bert4keras.models import build_transformer_model
from bert4keras.tokenizers import Tokenizer
from bert4keras.snippets import to_array
import numpy as np

# config_path = '/mnt/chinese_L-12_H-768_A-12/bert_config.json'
# checkpoint_path = '/mnt/chinese_L-12_H-768_A-12/bert_model.ckpt'
# dict_path = '/mnt/chinese_L-12_H-768_A-12/vocab.txt'

# tokenizer = Tokenizer(dict_path, do_lower_case=True)  # 建立分词器
# model = build_transformer_model(config_path, checkpoint_path)  # 建立模型，加载权重

from transformers import *
import torch
from torch.nn.functional import softmax

from transformers import *
from albertForVec import  AlbertModelForVec
pretrained = 'voidful/albert_chinese_tiny'          # 这次我们使用小模型,加速训练侧效果.
tokenizer = BertTokenizer.from_pretrained(pretrained)  # 主要这里面的tokenizer是bert的.
model = AlbertModelForVec.from_pretrained(pretrained)



'''
---------------------------------
那么问题来了,如何构造我们需要的同义词表呢?
首先我们拿到所有kg里面的边,也就是关系.
    然后我们把关系的词输入中文近义词工具包Synonyms 中,搜索相关关键词,就构建了词表.
'''



def finetune():


    class A():
        pass
    args=A()
    args.learning_rate=3e-5
    args.adam_epsilon=1e-8
    args.weight_decay=0
    no_decay = ["bias", "LayerNorm.weight"]
    optimizer_grouped_parameters = [
        {
            "params": [p for n, p in model.named_parameters() if not any(nd in n for nd in no_decay)],
            "weight_decay": args.weight_decay,
        },
        {"params": [p for n, p in model.named_parameters() if any(nd in n for nd in no_decay)], "weight_decay": 0.0},
    ]
    optimizer = AdamW(optimizer_grouped_parameters, lr=args.learning_rate, eps=args.adam_epsilon)
    #开启finetune模式 ,,,,,,,C:\Users\Administrator\.PyCharm2019.3\system\remote_sources\-456540730\-337502517\transformers\data\processors\squad.py 从这个里面进行抄代码即可.
    model.zero_grad()

    model.train()
    tongyicibiao={'老婆':'妻子'}

    for epoch in range(10):
      for i in tongyicibiao:
        left=i
        right=tongyicibiao[i]
        left=torch.tensor(tokenizer.encode(left, add_special_tokens=True)).unsqueeze(0)
        right=torch.tensor(tokenizer.encode(right, add_special_tokens=True)).unsqueeze(0)  # 注意这个地方要拓展一维batch_size
        outputs1 = model(left, )
        outputs2 = model(right, )
        tmp=torch.cosine_similarity(outputs1,outputs2)
        loss=1-tmp
        print(loss)
        loss.backward()
        optimizer.step()

        model.zero_grad()


    return "over"



finetune()

print("finetune结束")
model.eval()















def search128(tex):# 返回维度128的向量.
    inputtext = tex  # 编码后第一个位置是cls,所以msk的索引是3
    # 看看这个函数怎么用
    input_ids = torch.tensor(tokenizer.encode(inputtext, add_special_tokens=True)).unsqueeze(0)



    list1=[]
    list1.append(torch.tensor(tokenizer.encode(tex, add_special_tokens=True)))
    tmp=torch.stack(list1,0)





    outputs = model(tmp, )
    tmp2=outputs[:,:]
    return tmp2



import os, re, json
import json
import nmslib
import torch
import random
import pandas as pd
from tqdm import tqdm
import numpy as np
#import tensorflow_hub as hub
from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer
from joblib import dump, load
from string import punctuation
from operator import itemgetter
from functools import wraps
from pytorch_pretrained_bert import BertModel, BertTokenizer, BertConfig
from sklearn.metrics.pairwise import cosine_similarity
from rusenttokenize import ru_sent_tokenize





























def vec2(tex):

    # 编码测试
    # token_ids, segment_ids = tokenizer.encode(tex)
    # token_ids, segment_ids = to_array([token_ids], [segment_ids])
    global tmp
    # tmp=model.predict([token_ids, segment_ids])[:,0,:] # 0代表取[CLS]
    # tmp3=tmp(tex)
    tmp3=search128(tex) #返回一个768维向量.
    # print(tmp)
    return tmp3









from ltp import LTP

ltp = LTP()
# text='我现在在天津,我想知道这里的大学都有什么学校.'






def searchKG(kglist,text): # 用bert来算距离的
    tmp3 = []
    for i in kglist:
        t = (cosine_distance(vec2(i), vec2(text)))
        tmp3.append(t)
    tmp3 = np.array(tmp3)
    print('所有的距离为',tmp3)
    # 查询到的最近kg 3元组是!!!!!!!!!!!!!!!!
    dix = np.argmin(tmp3)
    print('最近的3元组是', kglist[dix], '对应的阈值是', tmp3[dix])


    return kglist[dix]


import numpy as np
def cosine_distance(a, b):  # fanwei 0---2
    if type(a)!='numpy.array':
        a=a.detach().numpy()
        b=b.detach().numpy()
    if a.shape != b.shape:
        raise RuntimeError("array {} shape not match {}".format(a.shape, b.shape))
    if a.ndim==1:
        a_norm = np.linalg.norm(a)
        b_norm = np.linalg.norm(b)
    elif a.ndim==2:
        a_norm = np.linalg.norm(a, axis=1, keepdims=True)
        b_norm = np.linalg.norm(b, axis=1, keepdims=True)
    else:
        raise RuntimeError("array dimensions {} not right".format(a.ndim))
    similiarity = np.dot(a, b.T)/(a_norm * b_norm)
    dist = 1. - similiarity
    return dist







'''
下面我们进行bert计算距离:
kg里面:
天津的大学
天津的人口
天津的面积
'''





#---------------下面开始调用!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
import torch

kglist=['大学','人口','面积']
text='姚明的妻子的丈夫的妻子'
text='我现在在天津,这里有什么大学?'
# text='姚明的妻子'



##
#--------从测试看出来,ner本身对问题有干扰,所以在kglist里面要去除.







# tiaozhuan=searchKG(kglist=['地点','地址','大小','颜色','老婆','丈夫'],text='我家住在和平区哪个地方')








# print(tiaozhuan,"jieguo shi !!!!!!!!!!!!!!!!")
##






# 加入句子成分跳转.
seg, hidden = ltp.seg([text])
# sdp = ltp.sdp(hidden, graph=False)

print(seg,"seg")
pos = ltp.pos(hidden)
ner = ltp.ner(hidden)
print("ner",ner)
srl = ltp.srl(hidden)
dep = ltp.dep(hidden)
sdp = ltp.sdp(hidden)

print(ner,"ner结果")
seg=seg[0]
dep=dep[0]
sdp=sdp[0]
print(sdp,"语义分析!!!!!!!!!!!!!!!!!!!") # 太难用了.
print(dep)
for i in dep: #dep算法目前识别不出来老婆的跳转.

    print(i, seg[i[0]-1], seg[i[1]-1]) # 注意下标会多一个, 箭1后为真正下标.

'''
下面我们根据跳跃图简历bfs算法
'''

#dep 就是我们需要的图
# 从Ner出发,进行遍历图.找到他到root的一个路线.
tiaozhuanlist={'ATT','SBV'} # 正序表
tiaozhuanlist2={'VOB'} # 范旭表
ner=ner[0]
luxian=[]
for ner_sample in ner:
    # 然后对ner_sample进行跳跃搜索.

    ner_sample_index=ner_sample[1]+1 # 变成dep图的索引类型.
    luxian = [ner_sample_index]
    def search_new_node():
        ner_sample_index=luxian[-1]
        for i in dep:
            if i[0]==ner_sample_index and i[2] in tiaozhuanlist and i[1] not in luxian: # 进行的字跳转.并且防止循环.
                luxian.append(i[1])
                ner_sample_index=i[1]
                return 1
            if i[0]==ner_sample_index and i[2] in tiaozhuanlist2 and i[1] not in luxian: # 进行的字跳转.并且防止循环.
                luxian.append(i[1])
                ner_sample_index=i[1]
                return 1
            if i[1]==ner_sample_index and i[2] in tiaozhuanlist2 and i[0] not in luxian: # 进行的字跳转.并且防止循环. vob可能会反.也要考虑
                luxian.append(i[0])
                ner_sample_index=i[0]
                return 1
        return 0 # 说明找不到新跳跃了.
    while search_new_node():
        print("running")
    print(luxian,"bfs方法找到的路线!!!!!!!!!!!!!!!")
    # 根据luxian 跳转即可,原则是能跳转就跳转,跳转不了就停下,直接返回当前结果.


#--------------上面拿到路线了luxian, 在kg里面进行跳转即可.# 可以做词向量距离,来进行模糊跳转.


# 如果luxian里面长度是1,说明没有找到跳转.只有ner.那么我们就用luxian里面这个.进入词向量.搜索算法即可.
if 1:
    print("下面用bert做辅助判断")
    #kglist = luxian[0] 这个东西的所有的边.
    tiaozhuan = searchKG(kglist=['地点','地址','大小','老婆','丈夫'], text='妻子')
    # 利用距离小于一个阈值,我们就使用这个tiaozhuan,目前只支持bert算法的一次跳转,多次跳转没想到.

if len(luxian)==0:
    print("ner没有")




