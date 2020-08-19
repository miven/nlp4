# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd





'''
合并sheets
'''



import os
import pandas as pd
import numpy as np
from sqlalchemy import create_engine

'''
新加入的数据
'''
path = 'out2.csv'  # excel的存放路径

'''
就的数据
'''
pathold='binzhouold.csv'


tmp=pd.read_csv(path)

tmp8=tmp
tmp2=pd.read_csv(pathold)


'''
找出在tmp中有,在tmp2中没有的企业

pandas in 查询

https://blog.csdn.net/xiebin6163/article/details/95460414
'''

io=tmp[-tmp['企业名称'].isin(tmp2['ent_name'])]



'''
这样我们就得到了,需要去数科查询的数据. 的所有企业名称.

下面进行去重.
'''

data=io.drop_duplicates(subset=['企业名称'],keep='first',inplace=True)





'''
现在io就是要找的企业
'''




io.to_csv('chaxunqiye.csv')

'''
下面掉数科,找这个1万条数据.
'''



