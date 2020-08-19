from html.parser import HTMLParser
import os

os.mkdir('policy_txt')
tmp=os.listdir('policy_html')
from bs4 import BeautifulSoup
for i in tmp:
    dangqian='policy_html/'+i
    with open(dangqian,encoding='utf-8') as f:
        bs = BeautifulSoup(f, "html.parser").get_text()


    with open('policy_txt/'+i[:-5]+'.txt','w',encoding='utf-8') as f :
        f.write(bs)





