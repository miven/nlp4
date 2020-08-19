from pymongo import MongoClient
from pymongo import InsertOne
import time

def insert():
    #连接数据库
    myclient = MongoClient("mongodb://localhost:27017/")
    mydb = myclient["d1"]
    my_collection = mydb['c6']
    i = 0
    t0 = time.time()
    data =[]

    
    
    dex=0
    jilu=0
    f=open('/data/zb/Embedding.txt',encoding='utf-8') 
    for i in f:
    
        hanzi=i.split(' ')[0]
        if '.' in hanzi or '$' in hanzi:
            continue

        bianma=i.split(' ')[1:]
    #'_id'为主键，循环时递增，全部添加到data列表内
    
        data.append(InsertOne({"hanzi":hanzi,"bianma":bianma}))
        dex+=1
        if dex==10000 and jilu<8000000:


            my_collection.bulk_write(data)
            data=[]
            dex=0
        jilu+=1
        if jilu>=8000000:
            my_collection.insert({"hanzi":hanzi,"bianma":bianma})
            


      #判断i等于1亿时停止循环


if __name__ == '__main__':
    insert()
