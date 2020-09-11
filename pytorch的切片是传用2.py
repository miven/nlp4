import torch
import numpy as np
a=np.array([[1,2],[3,4]])
b=a[:1,:1]
b[0][0]=1.898989
print(a)       # numpy 就不是传引用.