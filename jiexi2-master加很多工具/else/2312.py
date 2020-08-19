import json 
data = {'username':'李华','sex':'male','age':16}
data=["地方拉三32423等奖","大大32423"]
json_dic2 = json.dumps(data,sort_keys=True,indent=4,ensure_ascii=False)


