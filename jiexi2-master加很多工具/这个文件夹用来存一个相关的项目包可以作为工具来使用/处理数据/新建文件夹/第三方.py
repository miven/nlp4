import  pandas as pd
tmp=pd.read_csv('chaxunqiye.csv')




'''
掉jinan接口
'''
import requests

url='http://aioc-jinan.xjoycity.com/bi/ent/fuzzyQuery'

tmp=requests.post(url=url+'?queryString=发的')
tmp=(tmp.json())
tmp=dict(tmp)


import pandas as pd

qiye=pd.read_csv('chaxunqiye.csv')['企业名称']



'''
jianli接收字典


海高仙自动化科技发展有限公司

http://aioc-jinan.xjoycity.com/bi/ent/basicQuery?queryString=海高仙自动化科技发展有限公司


'''

tmp = requests.post('http://aioc-jinan.xjoycity.com/bi/ent/basicQuery?queryString='+'海南阿凡题科技有限公司')
tmp = (tmp.json())
tmp = dict(tmp)
tmp=tmp['result']['basicInfo']


# tmp=[tmp]

outputlist=tmp

for i in outputlist:
    outputlist[i]=[]



feiwu=[]





# t=requests.post('http://aioc-jinan.xjoycity.com/bi/ent/basicQuery?queryString='+'哈工大机器人集团有限公司')
# t=t.json()

# raise




for i in qiye :

        tmp = requests.post('http://aioc-jinan.xjoycity.com/bi/ent/basicQuery?queryString='+str(i))
        tmp = (tmp.json())

        tmp = dict(tmp)
        if len(tmp)>20:

            tmp=tmp['result']['basicInfo']


            for j in tmp:

                outputlist[j].append(tmp[j])


del outputlist['id']
out=pd.DataFrame(outputlist)
out.to_csv('final.csv')









