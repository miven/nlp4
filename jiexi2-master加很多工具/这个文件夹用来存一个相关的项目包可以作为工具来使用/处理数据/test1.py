#这个就是最后使用的爬取脚本!!!!!!!!!!!!!!!!!!!!!!
'''
这个脚本会,查询企业信息,然后写入一个csv文件中.

'''

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
#补上第一条缺的字段
outputlist['county']=[]
outputlist['city']=[]
outputlist['website']=[]



feiwu=[]





# t=requests.post('http://aioc-jinan.xjoycity.com/bi/ent/basicQuery?queryString='+'哈工大机器人集团有限公司')
# t=t.json()

# raise




for ii in range(len(qiye)):


        i=qiye[ii]
        tmp = requests.post('http://aioc-jinan.xjoycity.com/bi/ent/basicQuery?queryString='+str(i))
        tmp = (tmp.json())

        tmp = dict(tmp)
        if 'result' in tmp:

            tmp=tmp['result']['basicInfo']

            for j in outputlist:


                try:
                    outputlist[j].append(tmp[j])
                except:
                    outputlist[j].append(None)

        else:
            i=i.replace('市','')
            tmp = requests.post('http://aioc-jinan.xjoycity.com/bi/ent/basicQuery?queryString=' + str(i))
            tmp = (tmp.json())

            tmp = dict(tmp)
            if 'result' in tmp:

                tmp=tmp['result']['basicInfo']


                for j in outputlist :

                    try :
                        outputlist[j].append(tmp[j])
                    except :
                        outputlist[j].append(None)


del outputlist['id']

for i in outputlist.values():

out=pd.DataFrame(outputlist)

out.to_csv('final.csv')









