import torch
a=torch.rand(3,4,5)
b=a[:1,:1]
b[0][0]=1.898989
print(a)