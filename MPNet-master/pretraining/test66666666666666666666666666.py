from fairseq.models.masked_permutation_net import MPNet
mpnet = MPNet.from_pretrained('/mpnet.base', 'mpnet.pt', '', bpe='bert')
import torch
assert isinstance(mpnet.model, torch.nn.Module)