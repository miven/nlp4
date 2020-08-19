
import collections
tmp = collections.Counter()
tmp[1]=3
tmp[2]=3
tmp2 = collections.Counter()
tmp2[2]=3
tmp2[3]=3
tmp3 = collections.Counter()

tmp3[3]=20
for i in [tmp,tmp2]:
    tmp=tmp|i

