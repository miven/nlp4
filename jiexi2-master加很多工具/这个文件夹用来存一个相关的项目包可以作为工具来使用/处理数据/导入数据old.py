import  pandas as pd
import os

'''
数据库读写要注意操作系统,
从linux里面的表往windows里面放回有bug,数据会变少.
所以从linux里面的数据还是要往linux主机里面放.操作永远在云上操作.本地不操作.因为操作系统不一样会有bug.
'''


import os
import pandas as pd
import numpy as np
from sqlalchemy import create_engine


path = os.path.join( '产业链数据-整理后(1).xlsx')  # excel的存放路径
engine = create_engine('mysql+pymysql://aioc:i8NnFvh6t@mysql-cn-north-1-4fda8775bfcc4f32.public.jcloud.com:3306/city_aioc?charset=utf8', encoding="utf-8")

tmp=pd.read_excel(path)

x= pd.ExcelFile(path)






for i in x.sheet_names:
    tmp=pd.read_excel(path,sheet_name=i)
    tmp['uuid']='20190813'
    tmp['create_time']='20190813'
    tmp['update_time']='20190813'
    # tmp['industry_type']=i
    #改变列的名字
    tmp.rename(columns={'企业名称' : 'ent_name', '产业链名称' : 'industry_type', '产业名称' : 'op_scope','产业分类':'param2','企业分类':'stock_type'}, inplace=True)
    # tmp.drop(column=0)



    #第一个参数是tablename第二个是engine
    tmp.to_sql('ent_basic_info',engine,if_exists='append', index=False)




# data_dict = pd.read_excel(path,sheet_name=["国家代码", "包装种类"], encoding="UTF-8")
# data_dict2 = pd.read_excel(path,sheet_name=["币种代码", "货物通关代码", "联系人方式"], header=None, encoding="UTF-8")
# country = pd.DataFrame(data_dict.get("国家代码"))
# wraptype = pd.DataFrame(data_dict.get("包装种类"))
# currcode = pd.DataFrame(data_dict2.get("币种代码"))
# carnetcode = pd.DataFrame(data_dict2.get("货物通关代码"))
# communication = pd.DataFrame(data_dict2.get("联系人方式"))




