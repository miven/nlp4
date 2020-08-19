##
import  pandas as pd
import os

'''
产业链名称	产业分类	产业名称	企业分类	企业名称
人工智能	应用层	机械臂及机器人	A股公司(主营业务)	埃斯顿(002747)

update xxxx set       industry_type='机械臂及机器人' where                     ent_name ='埃斯顿(002747)' 
and industry_type is null


全国企业搜索20190917.xlsx

滁州产业链企业清单—2019年9月16日.xlsx
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



engine = create_engine('mysql+pymysql://aioc:i8NnFvh6t@mysql-cn-north-1-4fda8775bfcc4f32.public.jcloud.com:3306/bi?charset=utf8', encoding="utf-8")


'''
D:\zhangbo340\Desktop
'''
import pymysql

# 创建连接
conn = pymysql.connect(host='mysql-cn-north-1-4fda8775bfcc4f32.public.jcloud.com', port=3306, user='aioc', passwd='i8NnFvh6t', db='city_aioc')
# 创建游标
cursor = conn.cursor()



#注意使用cell 模式 pycharm 的使用问题.所有文件的默认路径都是当前项目的根目录!!!!!!!





##
jieshou={}
keys=[     'uuid',
  'creditCode',
  'regNo',
  'orgCodes',
  'entStatus',
  'regCap' ,
  'frName',
  'industryPhyName' ,
  'esDate',
  'opFrom' ,
  'opTo' ,
  'regOrgProvince',
  'regOrg' ,
  'entType' ,
  'entName' ,
  'dom' ,
  'opScope' ,
  'approvedTime',
  'phoneNumber' ,
  'email' ,
  'oldName' ,
  'validTime',
  'industryLargeName' ,
  'industryMiddleName' ,
  'county' ,
           'industryType',
  'createTime' ,
  'updateTime' ,
  'isDeleted',
  'state' ,
                  'city',
                  'website'
                  ,'param1'
                  ,'param2'
                  ,'param3'
                  ,'param4'


  ]

for i in keys:
    jieshou[i]=[]




path='滁州产业链企业清单—2019年9月16日.xlsx'
now=pd.read_excel(path)
print(now['企业名称'])
all1=now['企业名称']
qiye=all1
import requests
tmp = requests.post('http://aioc-jinan.xjoycity.com/bi/ent/basicQuery?queryString=' + all1[0])
tmp = (tmp.json())
tmp = dict(tmp)
print(tmp['result']['basicInfo'])



indus_type=now['industry_type']
param3=now['param3']
param4=now['param4']

print(indus_type,param3,param4)

##
#完美逻辑的爬取
print(indus_type)
print(indus_type[1])
for ii in range(len(qiye)):


    print(ii)
    i = qiye[ii]
    tmp = requests.post('http://aioc-jinan.xjoycity.com/bi/ent/basicQuery?queryString=' + str(i))
    tmp = (tmp.json())

    tmp = dict(tmp)


    #带市字的查询
    if 'result' in tmp:

        tmp = tmp['result']['basicInfo']

        tmp['industryType'] = indus_type[ii]
        tmp['param3'] = param3[ii]
        tmp['param4'] = param4[ii]

        for j in jieshou:

            try:
                jieshou[j].append(tmp[j])
            except:
                jieshou[j].append(None)
    # #  #不带市字的查询
    # else:
    #     i = i.replace('市', '')
    #     tmp = requests.post('http://aioc-jinan.xjoycity.com/bi/ent/basicQuery?queryString=' + str(i))
    #     tmp = (tmp.json())
    #
    #     tmp = dict(tmp)
    #     if 'result' in tmp:
    #
    #         tmp = tmp['result']['basicInfo']
    #         tmp['industryType'] = indus_type[ii]
    #         tmp['param3'] = param3[ii]
    #         tmp['param4'] = param4[ii]
    #         for j in jieshou:
    #
    #             try:
    #                 jieshou[j].append(tmp[j])
    #             except:
    #                 jieshou[j].append(None)
import pickle
jieshou=pd.DataFrame(jieshou)


try:
    jieshou.drop(['id'],axis=1,inplace=True)
except:
    pass
#dump 东西.  pickle 方便多了,万一出错也不用重新爬取了.
pickle.dump(jieshou, open("p.pkl","wb"))
# print(jieshou)


##
tmp=pickle.load(open("p.pkl",'rb'))
print(tmp)
tmp.to_csv("2313.csv")
##

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
    , 'param1'
    , 'param2'
    , 'param3'
    , 'param4'

  ]













tmp.to_sql('ent_basic_info',engine,if_exists='append', index=False)





