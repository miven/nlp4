









'''
接口
:
            重要的操作:一定要在mongodb中加索引,提高搜索速度.

http://116.196.87.166:8000/word2vector?word=%E7%89%9B%E9%80%BC



from pymongo import MongoClient,Connection

zhagnbo284  2019-08-02,21点39
'''
import http
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



from pymongo import MongoClient
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
'''
http://116.196.87.166:5050/enterprisePolicyMatch/word2Vector?word=
'''
url = "http://116.196.87.166:8000/word2vector?word="
url = "http://116.196.87.166:5050/service/index.html?word=%E6%89%B6%E6%8C%81"
url = "http://116.196.87.166:5050/enterprisePolicyMatch/word2Vector"


# vec1=urllib.request.urlopen(url).read()





fn="policy_files/txt/青岛西海岸新区关于加快建设四大基地促进先进制造业高质量发展的意见.txt"
# fn="policy_files/txt/全国人大常委会决定修改外资企业法等四部法律.txt"
# fn="policy_files/txt/2015山东国家级示范企业名单.txt"
# fn="policy_files/txt/2018年1-5月外商投资企业进出口简况.txt"
fn="policy_files/txt/青岛软件园入园企业优惠政策.txt"
fn="policy_files/txt/2014年泰安市服务业发展引导资金项目安排情况公示.txt"
# fn="1_abs.txt"

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
out3=out








#
#
#

# score1=[]
# score2=[]
# score3=[]
#
# start=time.time()
# vec1=urllib.request.urlopen(url,data=bytes(urllib.parse.urlencode({"word":"政策"}),encoding='utf-8')).read()
# vec1=urllib.request.urlopen(url,data=bytes(urllib.parse.urlencode({"word": r"扶持 我"}),encoding='utf-8')).read()
#

#
# vec11=urllib.request.urlopen(url+quote("文件",encoding='utf-8')).read()
# vec22=urllib.request.urlopen(url+quote("法律",encoding='utf-8')).read()
# vec2=urllib.request.urlopen(url+quote("法规",encoding='utf-8')).read()
# vec3=urllib.request.urlopen(url+quote("公告",encoding='utf-8')).read()
# vec33=urllib.request.urlopen(url+quote("通知",encoding='utf-8')).read()




from pymongo import MongoClient
from pymongo import InsertOne
import time



#尽量降低链接次数,一次链接就都find到结果.




start=time.time()


myclient = MongoClient("mongodb://localhost:27017/",maxPoolSize=30000,minPoolSize=8,connectTimeoutMS=30000)
# myclient = Connection("mongodb://localhost:27017/")
mydb = myclient["d1"]
my_collection = mydb['c6']


# 得到的东西是一个数组,之后是一个字典.
time5=time.time()
vec1 = my_collection.find_one({'hanzi': '政策'})['bianma']
vec11 = my_collection.find_one({'hanzi': '政策'})['bianma']
vec2 = my_collection.find_one({'hanzi': '法律'})['bianma']
vec22 = my_collection.find_one({'hanzi': '法规'})['bianma']
vec3 = my_collection.find_one({'hanzi': '公告'})['bianma']
vec33 = my_collection.find_one({'hanzi': '通知'})['bianma']







# vec300003 = my_collection.find_one({'hanzi': '%17'})['bianma']
time6=time.time()

#测试如果数据库没有,返回的是什么
# test99 = my_collection.find_one({'hanzi': '通知234'})['bianma']

# rsesafl






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




    vec1=np.fromstring(vec1, dtype=float, sep=',')


    return vec1






vec1=process(vec1)




vec11=process(vec11)
vec2=process(vec2)
vec22=process(vec22)
vec3=process(vec3)
vec33=process(vec33)









'''
用字典去重加速
'''

outdict=defaultdict(int)
for i in out:
    outdict[i]+=1



time3=time.time()


score1=[]
score2=[]
score3=[]



for i in outdict:
    try :
        tmp=my_collection.find_one({'hanzi': i})['bianma']

    except:
        continue
    tmp=process(tmp)




    for j in range(outdict[i]):



        #ju
        # score1.append(np.dot(tmp,vec1))
        # score1.append(np.dot(tmp,vec11))
        # score2.append(np.dot(tmp,vec2))
        # score2.append(np.dot(tmp,vec22))
        # score3.append(np.dot(tmp,vec3))
        # score3.append(np.dot(tmp,vec33))


        #查了gensim源码,上面用的距离是cosin余弦函数.结果总感觉奇怪.
                score1.append(np.dot(tmp,vec1)/(np.linalg.norm(tmp)*np.linalg.norm(vec1)))
                score1.append(np.dot(tmp,vec11)/(np.linalg.norm(tmp)*np.linalg.norm(vec11)))
                score2.append(np.dot(tmp,vec2)/(np.linalg.norm(tmp)*np.linalg.norm(vec2)))
                score2.append(np.dot(tmp,vec22)/(np.linalg.norm(tmp)*np.linalg.norm(vec22)))
                score3.append(np.dot(tmp,vec3)/(np.linalg.norm(tmp)*np.linalg.norm(vec3)))
                score3.append(np.dot(tmp,vec33)/(np.linalg.norm(tmp)*np.linalg.norm(vec33)))













time4=time.time()
score1=sum(score1)
score2=sum(score2)
score3=sum(score3)

















outname={0:'政策',1:'法律',2:'公告'}
tmp=(score1,score2,score3)

tmp=np.array(tmp)

out=outname[tmp.argmax()]


end=time.time()























#