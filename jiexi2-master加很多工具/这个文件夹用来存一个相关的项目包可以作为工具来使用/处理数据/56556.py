
import time
start=time.time()
a=[1,2,4,5,6,7]*999
a=[i for i in a if i!=2]



start=time.time()
a=[1,2,4,5,6,7]*999
a=filter(lambda x:x!=2   , a)
a=list(a)








