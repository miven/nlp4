##
import  pandas as pd
import os

'''
产业链名称	产业分类	产业名称	企业分类	企业名称
人工智能	应用层	机械臂及机器人	A股公司(主营业务)	埃斯顿(002747)

update xxxx set       industry_type='机械臂及机器人' where                     ent_name ='埃斯顿(002747)' 
and industry_type is null





'''








'''



这个是最后的写入数据库脚本,做update
'''

'''
数据库读写要注意操作系统,
从linux里面的表往windows里面放回有bug,数据会变少.
所以从linux里面的数据还是要往linux主机里面放.操作永远在云上操作.本地不操作.因为操作系统不一样会有bug.
'''


import os
import pandas as pd
import numpy as np
from sqlalchemy import create_engine



engine = create_engine('mysql+pymysql://aioc:i8NnFvh6t@mysql-cn-north-1-4fda8775bfcc4f32.public.jcloud.com:3306/city_aioc?charset=utf8', encoding="utf-8")


'''
D:\zhangbo340\Desktop
'''
import pymysql

# 创建连接
conn = pymysql.connect(host='mysql-cn-north-1-4fda8775bfcc4f32.public.jcloud.com', port=3306, user='aioc', passwd='i8NnFvh6t', db='city_aioc')
# 创建游标
cursor = conn.cursor()

##


##
import pickle



import pandas as pd
df=pd.read_sql(sql="SELECT	* FROM	`ent_basic_info` WHERE op_scope like '%新能源汽车%'",con=conn)

##

for i in range(len(df)):
    tmp=df.iloc[i]
    if tmp['param2']==None:
        df.loc[i,'param2']='轨道交通及能源汽车'
    elif tmp['industry_type']==None:
        df.loc[i,'industry_type'] = '轨道交通及能源汽车'
    else:
        df.loc[i,'industry_type'] = '轨道交通及能源汽车'
#注意2个key值要同时写,避免修改的只是临时变量!!!!!!!!!!

##

print(df.iloc[0])
print(111111111111111111111111)
print(df.loc[0])
print(df.columns)
print(len(df.columns))
df.drop(['id'],axis=1,inplace=True)

print(df.iloc[0])
##
df.to_sql('ent_basic_info',engine,if_exists='append', index=False)






##












if 1:

    path='C:/政策云/nlp/这个文件夹用来存一个相关的项目包可以作为工具来使用/处理数据/sfxq全国企业搜索-大健康.xlsx'
    now=pd.read_excel(path,sheet_name='大健康')
    print(now['企业名称'])
    all1=now['企业名称']
    qiye=all1
    import requests
    tmp = requests.post('http://aioc-jinan.xjoycity.com/bi/ent/basicQuery?queryString=' + all1[0])
    tmp = (tmp.json())
    tmp = dict(tmp)
    print(tmp['result']['basicInfo'])
    #完美逻辑的爬取
    for ii in range(len(qiye)):


        print(ii)
        i = qiye[ii]
        tmp = requests.post('http://aioc-jinan.xjoycity.com/bi/ent/basicQuery?queryString=' + str(i))
        tmp = (tmp.json())

        tmp = dict(tmp)
        #带市字的查询
        if 'result' in tmp:

            tmp = tmp['result']['basicInfo']

            for j in jieshou:

                try:
                    jieshou[j].append(tmp[j])
                except:
                    jieshou[j].append(None)
        #  #不带市字的查询
        else:
            i = i.replace('市', '')
            tmp = requests.post('http://aioc-jinan.xjoycity.com/bi/ent/basicQuery?queryString=' + str(i))
            tmp = (tmp.json())

            tmp = dict(tmp)
            if 'result' in tmp:

                tmp = tmp['result']['basicInfo']

                for j in jieshou:

                    try:
                        jieshou[j].append(tmp[j])
                    except:
                        jieshou[j].append(None)
    import pickle
    jieshou=pd.DataFrame(jieshou)
    jieshou['industryType']='大健康'
    print(jieshou)

    #dump 东西.
    pickle.dump(jieshou, open("p.pkl","wb"))
    print(jieshou)

##
tmp=pickle.load(open("p.pkl",'rb'))
print(tmp)
tmp.to_csv("2312.csv")

tmp['industryType']='生物医药健康'
print(tmp['industryType'])
# print(tmp)

print(tmp.columns)
print(len(tmp.columns))


tmp.columns=[     'uuid',
  'credit_code',
  'reg_no',
  'org_codes',
  'ent_status',
  'reg_cap' ,
  'fr_name',
  'industry_phy_name' ,
  'es_date',
  'op_from' ,
  'op_to' ,
  'reg_org_province',
  'reg_org' ,
  'ent_type' ,
  'ent_name' ,
  'dom' ,
  'op_scope' ,
  'approved_time',
  'phone_number' ,
  'email' ,
  'old_name' ,
  'valid_time',
  'industry_large_name' ,
  'industry_middle_name' ,
  'county' ,
                  'industry_type',
  'create_time' ,
  'update_time' ,
  'is_deleted',
  'state' ,
                  'city',
                  'website'

  ]













tmp.to_sql('ent_basic_info',engine,if_exists='append', index=False)










#用pickle读取.


##
import pickle
tmp=pickle.load(open("p.pkl",'rb'))
print(tmp)
all1=tmp['entName']
print(all1)
out=[]
cursor.execute("select ent_name from ent_basic_info")

import pandas as pd
df=pd.read_sql(sql="select ent_name from ent_basic_info",con=conn)
print(df)
##
out=df[df['ent_name'].isin(all1)]
print(out)







##








##




















##
'''
更新数据库
'''
    #要写成一句,逐行for循环太慢了.
if 1:
    for j in range(len(now)) :
        if type(now.iloc[j]['企业名称']) == str  :
            tmp =now.iloc[j]

            tmp3 = "update ent_basic_info set industry_type= " + '\''+ tmp['产业名称'] + '\'' \
                   +",param2= " + '\'' + tmp['产业链名称'] + '\'' \
                   +",param3= " + '\'' + tmp['产业分类'] + '\'' \
                   +",param4= " + '\'' + tmp['企业分类'] + '\'' \
                   + " where ent_name = " + '\''+tmp['企业名称'] +  '\'' +"and industry_type is null"

            cursor.execute(tmp3)
            conn.commit()

    #     raise
    #
    #
    #
    # raise
    #
    # tmp2=list(now['企业名称'])
    # tmp4=[]
    # for j in tmp2:
    #
    #     if type(j)==str and 'datetime' not in j and '/' not in j:
    #         tmp4.append(j)
    # tmp2=tmp4
    #
    #
    #
    # #注意转移
    # #注意是isNull不是=''
    # #
    # tmp3="update ent_basic_info set industry_type= " +'\''+str(i) +'\''+" where ent_name in "+tmp2+"and industry_type is null"
    #
    #
    #
    # cursor.execute(tmp3)
    # conn.commit()



conn.commit()
cursor.close()
conn.close()


'''
项目总结:
1.sql一定要一次写很多,用where xxx in ()语法,这个速度快.逐条太慢了!!!!!!!!!!
2. 注意空是is null语法不是=''
'''
























raise
tmp.drop('Unnamed: 0',axis=1,inplace=True)




tmp.columns=[     'uuid',
  'credit_code',
  'reg_no',
  'org_codes',
  'ent_status',
  'reg_cap' ,
  'fr_name',
  'industry_phy_name' ,
  'es_date',
  'op_from' ,
  'op_to' ,
  'reg_org_province',
  'reg_org' ,
  'ent_type' ,
  'ent_name' ,
  'dom' ,
  'op_scope' ,
  'approved_time',
  'phone_number' ,
  'email' ,
  'old_name' ,
  'valid_time',
  'industry_large_name' ,
  'industry_middle_name' ,
  'county' ,
  'create_time' ,
  'update_time' ,
  'is_deleted',
  'state' ,
                  'city',
                  'website'

  ]



# tmp.rename(columns={'regNo' : 'reg_no', 'orgCodes' : 'org_codes', '产业名称' : 'entStatus','产业分类':'param2','企业分类':'stock_type'}, inplace=True)
# # tmp.drop(column=0)



    #第一个参数是tablename第二个是engine



tmp.to_sql('ent_basic_info',engine,if_exists='append', index=False)




# data_dict = pd.read_excel(path,sheet_name=["国家代码", "包装种类"], encoding="UTF-8")
# data_dict2 = pd.read_excel(path,sheet_name=["币种代码", "货物通关代码", "联系人方式"], header=None, encoding="UTF-8")
# country = pd.DataFrame(data_dict.get("国家代码"))
# wraptype = pd.DataFrame(data_dict.get("包装种类"))
# currcode = pd.DataFrame(data_dict2.get("币种代码"))
# carnetcode = pd.DataFrame(data_dict2.get("货物通关代码"))
# communication = pd.DataFrame(data_dict2.get("联系人方式"))




