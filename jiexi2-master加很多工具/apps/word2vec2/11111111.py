import numpy as np
tmp=np.linalg.norm([1,1,1,1,1])


import re
i='啊啊啊鲁政发〔2016〕50号'
tmp = re.search(r'[\u4e00-\u9fa5]{2,3}发.*[1970-2080].*[1-9999]*号', i)



import pandas as pd

tmp=pd.read_csv(open(r'2.csv'))




tmp=tmp.drop(columns=['MainBusinessIncome','TotalBusinessIncome','NetProfit'])

tmp=tmp[tmp.CompanyName.notna()]

tmp.to_csv('1.csv',encoding='utf-8')
import datetime
import time
# i=datetime.time.fromisoformat('/Date(670608000000)/')








tmp=pd.read_csv(open(r'1.csv',encoding='utf-8'))

