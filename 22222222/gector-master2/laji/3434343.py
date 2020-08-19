import re

tmp=re.sub(r'\.',r' . ','dsl .kfjksl . adjfa. sdf.dfjlasdlkfjas.').rstrip()
tmp=re.sub(r' +',r' ',tmp).rstrip()

print(tmp)