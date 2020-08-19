# 测试代码可用性: 提取特征
##


'''
构建知识图谱的逻辑.

'''
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

    tmp=model.predict([token_ids, segment_ids])[:,0,:]
    # print(tmp)
    return tmp









from ltp import LTP

ltp = LTP()
# text='我现在在天津,我想知道这里的大学都有什么学校.'






def searchKG(kglist,text):
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
text='泰坦尼克号的演员是谁演的'



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
print(dep)
for i in dep:

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
if len(luxian)==1:
    #kglist = luxian[0] 这个东西的所有的边.
    tiaozhuan = searchKG(kglist=['地点', '地址', '大小', '颜色', '老婆', '丈夫'], text=text)
    # 利用距离小于一个阈值,我们就使用这个tiaozhuan,目前只支持bert算法的一次跳转,多次跳转没想到.








