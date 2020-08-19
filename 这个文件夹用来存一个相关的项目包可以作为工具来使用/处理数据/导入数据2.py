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
path='产业链数据-整理后v1.xlsx'
tmp=pd.ExcelFile('产业链数据-整理后v1.xlsx')

'''
D:\zhangbo340\Desktop
'''
import pymysql

# 创建连接
conn = pymysql.connect(host='mysql-cn-north-1-4fda8775bfcc4f32.public.jcloud.com', port=3306, user='aioc', passwd='i8NnFvh6t', db='city_aioc')
# 创建游标
cursor = conn.cursor()



for i in tmp.sheet_names:

    now=pd.read_excel(path,sheet_name=i)


    '''
    更新数据库
    '''
    #要写成一句,逐行for循环太慢了.
    tmp2=list(now['企业名称'])
    tmp4=[]#
    for j in tmp2:

        if type(j)==str and 'datetime' not in j and '/' not in j:
            tmp4.append(j)
    tmp2=tmp4

    tmp2=str(tmp2)[1:-1]
    tmp2='('+tmp2+')'

    #注意转移
    #注意是isNull不是=''
    #
    tmp3="update ent_basic_info set industry_type= " +'\''+str(i) +'\''+" where ent_name in "+tmp2+"and industry_type is null"



    cursor.execute(tmp3)



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




