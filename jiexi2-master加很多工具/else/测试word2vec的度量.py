'''
zhangbo284

'''
import time
import urllib.request

import urllib.request
#

# danci="答复"
#
#
# from urllib.parse import quote
#
#

# response1 = urllib.request.urlopen(url+quote(danci,encoding='utf-8'))
#
# # 打印请求的状态码

# # 打印请求的网页内容的长度







from urllib.parse import quote



'''
政策文件
法律法规
通知公告
'''




'''
用内积来算差别.
'''












import gensim
import jieba
from collections import defaultdict

'''
超参数:
'''

url = "http://116.196.87.166:8000/word2vector?word="

fn="policy_files/txt/“营业税改增值税”不会增加缴税负担.txt"
# fn="policy_files/txt/1月份山东省利用外资快速增长.txt"
# fn="policy_files/txt/2015山东国家级示范企业名单.txt"
fn="policy_files/txt/沂源县招商引资优惠政策.txt"

from gensim.models import Word2Vec
import gensim.models.word2vec as w2v

























'''
第一步做分词和停用词去除操作
'''
'''
下面对test文件夹里面的text进行处理,总的text用texts变量表示.
'''
import os

text=[]


with open(fn,encoding='utf-8') as file:

        #读取停用词表:
        stopwords = [line.strip() for line in open('chineseStopWord',encoding='UTF-8').readlines()]
        stopwords.append('\n')#去掉回车字符
        stopwords.append('\u00A0')#去掉回车字符
        stopwords.append('\u0020')#去掉回车字符
        stopwords.append('\u3000')#去掉回车字符





        # seg_list=jieba._lcut("大事发生大放")
        out=[]
        for line in file:
            seg_list = jieba._lcut(line)

            for i in seg_list:
                if i in stopwords:
                    continue
                out.append(i)







score1=[]
score2=[]
score3=[]

start=time.time()
vec1=urllib.request.urlopen(url+quote("中国",encoding='utf-8')).read()
vec2=urllib.request.urlopen(url+quote("鸭梨",encoding='utf-8')).read()
vec3=urllib.request.urlopen(url+quote("人",encoding='utf-8')).read()
import numpy as np
import re
def process(vec1):
    vec1 = str(vec1)
    vec1 = vec1.replace(r'\n', '')
    vec1 = vec1.replace('[', '')
    vec1 = vec1.replace(']', '')
    vec1 = vec1.replace('\'', '')

    vec1=re.sub('\s+',' ',vec1)
    vec1 = vec1[1:]
    vec1=np.fromstring(vec1, dtype=float, sep=' ')
    return vec1
vec1=process(vec1)
vec2=process(vec2)
vec3=process(vec3)








#用cosin来度量相似度



'''
测一测模唱是不是都是1

,说明模长不是1.
'''







a=np.array([1,2])
b=np.array([1,2])


