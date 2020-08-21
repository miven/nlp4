from flask import Flask
import json
# import gevent.monkey
# gevent.monkey.patch_all()  #开着2个时候没法debug
from flask_wtf import FlaskForm
from wtforms import SubmitField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask import send_from_directory, request, send_file, jsonify

app=Flask(__name__) #变量app是Flask的一个实例并且必须传入一个参数，__name__对应的值是__main，即当前的py文件的文件名作为Flask的程序名称，这个也可以自定义，比如，取，'MY_ZHH_APP'                          #__name__是固定写法，主要是方便flask框架去寻找资源 ，也方便flask插件出现错误时，去定位问题

# 初始化写这里.

import os





import random


# curl localhost:5000/upload -F "file=@/computer.txt"




def main_mini(lujing):

    print('jinrule ','main_mini')
    data=[i for i in open(lujing,encoding='utf-8').readlines()]

    out=[]
    for i in data:
        for j in i.split(';'):
            j=j.strip("\n")
            j=j.strip(' ')
            out.append(j)
    # print(out[:10])
    # print(len(out))
    print('jinrule ', 'main_mini2')
    from collections import defaultdict

    dict1 = defaultdict(int)
    print('jinrule ', 'main_mini3')
    for i in out:
        dict1[i]+=1
    print('jinrule ', 'main_mini4')
    # print(len(dict1))

    a=[]
    for i in dict1:
        a.append((i,dict1[i]))
    a=sorted(a,key=lambda x:x[1])
    a=a[::-1]
    print('jinrule ', 'main_mini5')
    # print(a[:1000])

    # 我们只处理最大前1千个词语
    a=a[:100] ####################################################################################
    print(778, a)




    # 计算文本相似度.
    from bert_serving.client import BertClient
    import numpy as np
    bc = BertClient()
    print(32432423473947,a)
    shuju=[i[0] for i in a]
    def cosine(a, b):
        return a.dot(b) / (np.linalg.norm(a) * np.linalg.norm(b))
    print('jinrule ',shuju)
    emb = np.array(bc.encode(shuju))
    # print('new',emb)
    # print(['First do it', 'then do it right'], ":", cosine(emb[0], emb[1]))
    # return 99999999999999
    # 下面调用这个函数即可vec_route



    # b里面放的是词语,词频,词向量

    b=[]
    for i in range(len(a)):
        b.append([a[i][0],a[i][1],emb[i]])
    # print(b,333333333333333333333333)





    # 下面进行降维
    from matplotlib.font_manager import _rebuild

    _rebuild() #reload一下
    import numpy as np
    from sklearn.manifold import TSNE
    import matplotlib.pyplot as plt

    import matplotlib as mpl



    label=[]
    for i in b:
        label.append(i[0])
    vectors=[]
    for i in b:
        vectors.append(i[2])
    cipin=[]
    for i in b:
        cipin.append(i[1])

    print(112)

    tsne = TSNE(perplexity=30, n_components=2, init='pca', n_iter=5000, method='exact')

    low_dim_embs = tsne.fit_transform(vectors) # 需要显示的词向量，一般比原有词向量文件中的词向量个数少，不然点太多，显示效果不好

    print(113)
    for i in range(len(b)):
        b[i][2]=low_dim_embs[i]

    uuuuu=str(b)

    print(11233333333)

    import json
    #chuanshu22288.json  这个数据就是给前端用的!!!!!!!!!!!!!!!!!1
    bb=b
    for i in range(len(bb)):
        bb[i][2]=list(bb[i][2])

    print(11255555555)
    import json

    print(1127777777777)
    # define A.class
    class node:
        def __init__(self, id,label,x,y,size,color):
            self.id = id
            self.label = label
            self.x = x
            self.y = y
            self.size = size
            self.cluster=color  # cluster




    ##








    import matplotlib.pyplot as plt
    from sklearn.datasets.samples_generator import make_blobs
    from sklearn.cluster import KMeans
    from sklearn import metrics

    print(11299999999)

    #选择聚类数K=2  聚类小于=8,因为颜色就写了8个
    final2=[]
    for i4 in range(3,11):
        n_clusters=i4
        y_pred=KMeans(n_clusters=n_clusters).fit_predict(low_dim_embs)
        colorlist=['red','black','yellow','greenyellow','blue','brown','coral','cyan','deeppink','orange']








        list1=[]
        for i,j in enumerate(bb):
            list1.append(node(i,j[0],float((float(j[2][0]))),float((float(j[2][1]))),float(j[1]**0.5),colorlist[y_pred[i]]).__dict__)




        nodes={}
        # 接口:https://github.com/xukuanzhuo/xukuanzhuo.github.io/issues/8
        #下面把每一个聚类里面的距离算一下.
        #similarity


        class edge:
            def __init__(self, sourceID,targetID,size):
                self.source = sourceID
                self.target = targetID

                self.size = size

        print(112000000000)
        print(bb,'lookupu234')
        list3=[]
        for i in range(n_clusters):
            dexlist=[]
            for j in range(len(y_pred)):
                 if y_pred[j]==i:
                     dexlist.append(j)
            for i1 in range(len(dexlist)):
                for i2 in range(i1+1,len(dexlist)):
                        left=dexlist[i1]  # 得到索引.
                        right=dexlist[i2]
                        similar=cosine(np.array(bb[left][2]),np.array(bb[right][2]))+1
                        list3.append(edge(bb[left][0],bb[right][0],similar).__dict__)

        print(list3,"list3")
        all3={"clusterNum":n_clusters ,"nodes":list1,"edges":list3}
        final2.append(all3)

    print('final2',final2)
    tmp2=json.dumps(final2,ensure_ascii=False)

    with open("chuanshuFinal.json",mode='w',encoding='utf-8') as f:
        print("最终json放在chuanshuFinal.json")
        f.write(tmp2)
    return tmp2















import time

@app.route('/upload', methods=['POST', 'GET'])

def upload():


    if request.method == 'POST':
        f = request.files
        print(f)
        for i in f.values():
            # print(i)
            # print(type(i))
            basepath = os.path.dirname(__file__)  # 当前文件所在路径
            tmp=random.random()+time.time()
            tmp=r"lastfile"+str(tmp).replace('.','_')
            i.save(tmp)   # 带字符串的一定要前面写上r.这样少了很多转义字符,方便多了!!!!!!!!!!!!!11
            tmp222=main_mini('/8/'+tmp)
        return tmp222
    return r'请改成post方法'
@app.route('/')      #相当于一个装饰器，视图映射，路由系统生成 视图对应url，这边没有指定method .默认使用get
def first_flask():    #视图函数
    from bert_serving.client import BertClient
    bc = BertClient()
    tmp=(bc.encode(['中国人是天才', '美国']))
    print("获得了")  # 启用多线程,如果没有服务响应的时候会自动等待,还是符合需求的!!!!!!!!!

    return jsonify(tmp.tolist())  #response，最终给浏览器返回的内容
@app.route('/test')      #相当于一个装饰器，视图映射，路由系统生成 视图对应url，这边没有指定method .默认使用get
def first_flask2():    #视图函数
     #response，最终给浏览器返回的内容
    return jsonify('test success')


if __name__ == '__main__':
    app.run(host='0.0.0.0',port='5000',debug=True)              #启动这个应用服务器，并开启debug,才能定位问题