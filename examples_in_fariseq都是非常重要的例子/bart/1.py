import torch

bart = torch.hub.load('pytorch/fairseq', 'bart.large')
bart.eval()  # disable dropout (or leave in train mode to finetune)
tokens = bart.encode('Hello world!')
print(tokens)
tmp=bart.decode(tokens)
print(tmp)












