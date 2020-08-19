from pymongo import MongoClient
from pymongo import InsertOne
import time
import time
def search():
    time1=time.time()
    #连接数据库
    myclient = MongoClient("mongodb://localhost:27017/")
    mydb = myclient["d1"]
    my_collection = mydb['c6']
    i = 0
    t0 = time.time()
    data =[]

    
    
    dex=0
    jilu=0
    f=open('/data/zb/888.txt',encoding='utf-8')
    for i in f:
    

            my_collection.find_one({"hanzi":i})
            

    time2 = time.time()

      #判断i等于1亿时停止循环
    '''
    (zb) [root@ai new]# python mongodb速度测试.py 
dasfasd
over
1.384486198425293
(zb) [root@ai new]# 



(zb) [root@ai new]# python mongodb速度测试.py 
dasfasd
over
5.956268787384033


2万一个词,里面有很多重复.



    '''


if __name__ == '__main__':
    search()
