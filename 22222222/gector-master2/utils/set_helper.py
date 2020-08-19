# 输入句子, 修补里面空格.里面还有,逻辑和数字逻辑.
import re
from pathlib import Path

VOCAB_DIR = Path(__file__).resolve().parent / "puc_word"  # 获取绝对路径的方法

tmp={i.strip('\n').lower() for i in open(VOCAB_DIR).readlines()} #并且忽略大小写.
def correct(set):
    setp=set.split(' ')
    t=[]
    for i in setp:
        if i.lower() in tmp or (re.findall(r'[0-9]',i) and ('.' in i)) or re.findall(r',[0-9]',i):
            tmp2=i

            t.append(tmp2)
        #对每一个i进行切分 biru :  apple.i          cat        cat.     cat,   i . Am
        else:
            tmp2 = re.sub(r'\.', r' . ', i).rstrip() # 先替换.
            tmp2 = re.sub(r',', r' , ', tmp2).rstrip() # 先替换.
            tmp2 = re.sub(r' +', r' ', tmp2).rstrip() # 再替换多余空格, 删除末尾空格.
            if '.' in tmp2:
                t+=tmp2.split(' ')
            else:
                t.append(tmp2)


    #补大小写:
    for i in range(len(t)):
        if i==0:
            t[i]=t[i].capitalize()
        elif t[i-1] and t[i-1][-1]=='.':
            t[i]=t[i].capitalize()
    #多余空格删除掉:
    k=' '.join(t)
    k = re.sub(r' +', r' ', k).rstrip()  # 再替换多余空格, 删除末尾空格.
    return k





#print(correct('Barack Obama was born in U.S.A. he was elected president in 2008.'))














