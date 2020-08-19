import re
old='dsl .kfjksl . adjfa. sdf.dfjlasdlkfjas.'
tmp=re.sub(r'\.',r' . ',old).rstrip()
tmp=re.sub(r' +',r' ',tmp).rstrip()
old=tmp
tmp=re.finditer(r'\. .',tmp)
tmp=list(tmp)
list3=[]
for i in tmp:
    list3.append(i.span()[-1]-1)
# print(list(tmp))
#
# print(list3)
# print(old)
out=''
for i in range(len(old)):
    if i not in list3 :
        out += old[i]
    else:
        out+=str.upper(old[i])
# print(out)