# 测试代码可用性: 提取特征
##
from bert4keras.backend import keras
from bert4keras.models import build_transformer_model
from bert4keras.tokenizers import Tokenizer
from bert4keras.snippets import to_array
import numpy as np

config_path = '/mnt/chinese_L-12_H-768_A-12/bert_config.json'
checkpoint_path = '/mnt/chinese_L-12_H-768_A-12/bert_model.ckpt'
dict_path = '/mnt/chinese_L-12_H-768_A-12/vocab.txt'

tokenizer = Tokenizer(dict_path, do_lower_case=True)  # 建立分词器
model = build_transformer_model(config_path, checkpoint_path)  # 建立模型，加载权重
def vec2(tex):

    # 编码测试
    token_ids, segment_ids = tokenizer.encode(tex)
    token_ids, segment_ids = to_array([token_ids], [segment_ids])

    print('\n ===== predicting =====\n')
    tmp=model.predict([token_ids, segment_ids])[:,0,:]
    # print(tmp)
    return tmp









from ltp import LTP

ltp = LTP()
text='我现在在天津,我想知道这里的大学都有什么学校.'


##







import numpy as np
def cosine_distance(a, b):  # fanwei 0---2
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
import torch

kglist=['天津的大学','天津的人口','天津的面积']

tmp3=[]
for i in kglist:
     t=(cosine_distance(vec2(i),vec2(text)))
     tmp3.append(t)
tmp3=np.array(tmp3)

# 查询到的最近kg 3元组是!!!!!!!!!!!!!!!!
dix=np.argmin(tmp3)
print('最近的3元组是',kglist[dix])


print(33333333333333)


##







seg, hidden = ltp.seg([text])
sdp = ltp.sdp(hidden, graph=False)

print(seg,"seg")
pos = ltp.pos(hidden)
ner = ltp.ner(hidden)
print("ner",ner)
srl = ltp.srl(hidden)
dep = ltp.dep(hidden)
sdp = ltp.sdp(hidden)



seg=seg[0]
for i in sdp[0]:

    print(i, seg[i[0]-1], seg[i[1]-1]) # 注意下标会多一个, 箭1后为真正下标.














