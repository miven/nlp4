b=(1  for h in [1,1,1,1])
a=sum(1  for h in [1,1,1,1])
import  torch
mask=torch.tensor([1,0,1,0,1]).view(-1).contiguous().eq(1)
tmp=torch.arange(len(mask))[mask]
print(a)
