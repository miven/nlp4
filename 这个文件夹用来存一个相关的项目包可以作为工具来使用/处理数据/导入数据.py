import  pandas as pd
import os
'''



这个是最后的写入数据库脚本
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

tmp=pd.read_csv('final2.csv')



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




