import torch
import numpy as np
a=[[1,2],[3,4]]
b=a[:1]
b[0][0]=1.898989
print(a)       #普通数组里面也是传地址.