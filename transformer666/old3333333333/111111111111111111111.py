import torch
a=torch.tensor([1,2,5,6])
b=torch.tensor([3,2,5,6])
non_pad_mask= torch.tensor([True,False]).ne(0)
print(non_pad_mask)