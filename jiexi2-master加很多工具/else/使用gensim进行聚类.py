import gensim
import jieba
from collections import defaultdict

'''
超参数:
'''
num_topics=3
dirname="policy_files/test"



'''
第一步做分词和停用词去除操作
'''
'''
下面对test文件夹里面的text进行处理,总的text用texts变量表示.
'''
import os

tmp=(dirname+'/'+i for i in os.listdir(dirname))
tmp=list(tmp)
texts=[]
for fn in tmp:


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
        texts.append(out)
#去掉只出现一次的
freq=defaultdict(int)

for text in texts:
    for i in text:
        freq[i]+=1


texts = [
    [token for token in text if freq[token] > 1]
    for text in texts
]



'''
下面用texts作为数据进行下面的处理.
'''
from gensim import corpora
dictionary = corpora.Dictionary(texts)
dictionary.save('test.dict')



#下面把文字替换成id,可以加速运算.

corpus = [dictionary.doc2bow(text) for text in texts]


#下面是编码之后的texts   编码字典是dictionary



#继续进行tfidf编码
from gensim import models
tfidf = models.TfidfModel(corpus)

corpus_tfidf = tfidf[corpus]

for doc in corpus_tfidf:








#扔分类器里
lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=num_topics)  # initialize an LSI transformation
corpus_lsi = lsi[corpus_tfidf]  # create a double wrapper over the original corpus: bow->tfidf->fold-in-lsi








for doc in corpus_lsi:  # both bow->tfidf and tfidf->lsi transformations are actually executed here, on the fly



#只保留最大概率对应的类别





# tmp=[(0, 0.1), (1, -0.1), (2, -0.1), (3, 0.2), (4, -0.3)]
#

# a=max( tmp,  key=lambda x:abs(x[1])    )[0]   #max key中的参数是前面可迭代里面的元素,所以跟索引无关.


out=[]
mapout=defaultdict(list) #创建默认值是shuizu的字典mapout

for i in ((corpus_lsi)):

    out.append(max( i,  key=lambda x:abs(x[1])    )[0])


'''
拼出最后结果
'''#注意生成器,遍历一次就没了
tmp=(dirname+'/'+i for i in os.listdir(dirname))

tmp=list(tmp)

for i in range(len(out)):
    mapout[out[i]].append(tmp[i])





listout=[0]*(num_topics)
for i in mapout:
    listout[i]=mapout[i]


for i in range(len(listout)):








