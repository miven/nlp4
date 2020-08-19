'''
1111111111111
#


使用前pip 一下transformers 保证版本最新.
'''

# https://www.ctolib.com/amp/brightmart-albert_zh.html


##
# 先引入句向量.
from transformers import *
import torch
from torch.nn.functional import softmax

from transformers import *
from albertForVec import  AlbertModelForVec
pretrained = 'voidful/albert_chinese_xxlarge'
tokenizer = BertTokenizer.from_pretrained(pretrained)  # 主要这里面的tokenizer是bert的.
model = AlbertModel.from_pretrained(pretrained)




##   以后把需要编码的句子写到这里面即可.
def search128(tex):# 返回维度128的向量.
    inputtext = [tex]  # 编码后第一个位置是cls,所以msk的索引是3
    # 看看这个函数怎么用
    input_ids = torch.tensor(tokenizer.encode(inputtext, add_special_tokens=True)).unsqueeze(0)



    list1=[]
    for i in inputtext:
        list1.append(torch.tensor(tokenizer.encode(i, add_special_tokens=True)))
    tmp=torch.stack(list1,0)





    outputs = model(tmp, )
    tmp2=outputs[0][:,0,:]
    return tmp2

# print(search128("今天"))
print(1)
print(1)
print(1)
print(1)

tmp=torch.cosine_similarity(search128("今天"),search128("明天"))
print(tmp)

print(11111111)





##



# 下面玩kg!!!!!!!!!!!!!!!!











from ltp import LTP

ltp = LTP()
text='我现在在天津,我想知道这里的大学都有什么学校.'
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



