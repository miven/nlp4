import urllib
from urllib.request import quote
from urllib.request import quote,unquote

import requests

ff = '//list.51test.net/w/?nclassid=69&key=&search_key=双语&search_key2=新闻&page=4'
ff = quote(ff,safe=";/?:@&=+$ ,",encoding="utf-8")
print(33333333333,ff)

'''
https://list.51test.net/w/?nclassid=69&key=&search_key=%E5%8F%8C%E8%AF%AD&search_key2=%E6%96%B0%E9%97%BB&page=4
'''


ff='https://list.51test.net/w/?nclassid=69&key=&search_key=%CB%AB%D3%EF&search_key2=%D0%C2%CE%C5&page=3'
ff = unquote(ff,encoding="utf-8")



print(ff)


aaa=urllib.parse.quote("新闻", safe='/', encoding='GBK', errors=None)
print(aaa)


html='https://list.51test.net/w/?nclassid=69&key=&search_key=%CB%AB%D3%EF&search_key2=%D0%C2%CE%C5&page=47 '

tmp=requests.get(html)
tmp.encoding = 'gb18030'
print(tmp.text)



