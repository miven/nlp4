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


path = '11/产业链数据-整理后2.xlsx'  # excel的存放路径




x= pd.ExcelFile(path)



'''



kong=pd.read_excel(path,sheet_name=x.sheet_names[0])

for index in range(len(x.sheet_names)):
    if index ==0:
        continue
    tmp=pd.read_excel(path,sheet_name=x.sheet_names[index])
    kong=pd.concat([kong,tmp],axis=0) #0是数据按行合并.行变多了.




kong.to_csv('output222.csv')




raise
'''
tmp=pd.read_csv('output222.csv')













'''
merge需要看这个函数
https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.merge.html


str字段处理方法:
    https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.str.html
'''

data = pd.read_excel('11/产业链数据-整理后2.xlsx')

data=tmp

data2 = pd.read_csv('2.csv',encoding='utf-8')
# data2.to_csv('2.csv',encoding='utf-8')
# data2 = pd.read_csv('11/hua.csv')























tmp=pd.merge(data, data2, left_on='企业名称' ,
             right_on='CompanyName',
             how='left')


tmp.to_csv("output.csv")


