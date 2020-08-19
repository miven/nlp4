'''
接口
:


http://116.196.87.166:8000/word2vector?word=%E7%89%9B%E9%80%BC




zhagnbo284  2019-08-02,21点39
'''








import  time



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




from gensim.models import Word2Vec
import gensim.models.word2vec as w2v























import numpy as np

import os

import pandas as pd
'''
超参数写这里:
'''
#训练集
dirname="policy_files/test"
#被提取keyword的文本
tex='policy_files/txt/2012年市场开拓工作的主要任务.txt'
#



from pyhanlp import *
# 第一个demo




HanLP.Config.ShowTermNature = False

CRFnewSegment = HanLP.newSegment("crf")




import jieba.posseg as pseg
tmp=(dirname+'/'+i for i in os.listdir(dirname))
tmp=list(tmp)
tmp.append(tex)
texts=[]


'''
对于关键词,只留名词和动词,去掉数量词
'''
for fn in tmp:


    with open(fn,encoding='utf-8') as file:

        #读取停用词表:
        stopwords = [line.strip() for line in open('chineseStopWord',encoding='UTF-8').readlines()]
        stopwords.append('\n')#去掉回车字符
        stopwords.append('\u00A0')#去掉回车字符
        stopwords.append('\u0020')#去掉回车字符
        stopwords.append('\u3000')#去掉回车字符
        stopwords.append('万')#去掉回车字符
        stopwords.append('元')#去掉回车字符



#

        # seg_list=jieba._lcut("大事发生大放")
        out=[]
        for line in file:
            # seg_list = jieba._lcut(line)
            seg_list=HanLP.segment(line)



            tmp2=[]
            for ii in seg_list:
                tmp2.append(str(ii))
            seg_list=tmp2


            seg_list=list(seg_list)
            for i in seg_list:
                if i in stopwords:
                    continue
                out.append(i)
        texts.append(out)




#去掉只出现一次的
# freq=defaultdict(int)

# for text in texts:
#     for i in text:
#         freq[i]+=1
#










def word_freq(text,freq=2):
    wordlist = pd.DataFrame({'word': text, 'freq': 1})
    wordcount = wordlist.groupby('word').sum()

    wordcount = wordcount.sort_values(by='freq', ascending=False)
    tmp = pd.DataFrame({'word': wordcount.index}, index=wordcount.index)
    wordcount = pd.concat([tmp, wordcount], axis=1)



    wordcount = wordcount[wordcount['freq'] >= freq]
    wordcount = wordcount[wordcount['word'] != '']
    wordcount = pd.DataFrame.reset_index(wordcount, drop=True)#index改成数字

    freq_p=[0.]*len(wordcount)
    for i in range(len(wordcount)):
        freq_p[i]= round(float(wordcount['freq'][i])/float(sum(wordcount['freq'])),5)
    wordcount= pd.concat([wordcount, pd.DataFrame({'tf':freq_p})], axis=1)
    return wordcount











'''
corpus:表示所有文件,就是用的上面的超参数texts
tex:表示需要计算的tex,
fanhui:这个tex的keyword
'''






def tf_idf(corpus,topk=5):


    kws=[]
    for text in corpus:
        word_tfidf = word_freq(text,2)
        t1,t2=[],[]
        for i in range(len(word_tfidf)):
            t1.append(word_tfidf['word'][i])
            t2.append(word_tfidf['tf'][i])
        kws.append(t1)
        kws.append(t2)

    tf_idf= pd.DataFrame(columns=['kw','tf','idf','tf_idf'])
    for i in range(len(kws)-2,len(kws),2):
        idf1,tfidf=[],[]
        for j in range(0,len(kws[i])):
            idf = 0
            #d对每一个单词统计数量
            for k in range(0,len(kws),2):
                if kws[i][j] in kws[k]:
                    idf=idf+1
            idf1.append(round(np.log(float(len(corpus))/float(idf)),5))
            tfidf.append(round(kws[i+1][j]*idf1[-1],5))

        idf_df= pd.DataFrame({'kw':kws[i],'tf':kws[i+1],'idf':idf1,'tf_idf':tfidf})
        idf_df= idf_df.sort_values(by='tf_idf', ascending=False)

        idf_df= idf_df.iloc[:topk,:]
        # 加上标识
        tf_idf= pd.concat([tf_idf,idf_df],axis=0,ignore_index=True)
    return (tf_idf)
    # tf_idf.to_csv('./out.csv')

#看一下自带的tfidfus算法


'''
算了还是用自带的
'''


import jieba.analyse.tfidf as tf
out2=  jieba.analyse.tfidf(''.join(texts[-1]))



# TextRankKeyword = JClass("com.hankcs.hanlp.summary.TextRankKeyword")
# out3=HanLP.extractKeyword(''.join(texts[-1]),5)
# out3=HanLP.extractKeyword(''.join([i for  i in open(tex,encoding='utf-8').readlines()]),5)

'''
根据词性去掉
'''
# out2=HanLP.segment(''.join((out2)))
out3=[]
for i in out2:

    if str((HanLP.segment(i))[0].nature) in ['a','ad','m']:
        continue
    else:
        out3.append(i)





'''
根据标题赛选
'''
if '/'in tex :
    biaoti=tex.split('/')[-1]
else:
    biaoti=tex
out4=[]
out44=[]
for i in out3:
    if i in biaoti:
        out4.append(i)
    else:
       out44.append(i)
out5=out4+out44






