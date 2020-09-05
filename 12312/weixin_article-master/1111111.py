import torch
seq_ids = torch.arange(12, )
causal_mask = seq_ids[None, None, :]

attention_mask=torch.rand(3,5)
attention_mask = torch.cat([attention_mask, attention_mask.new_zeros((attention_mask.shape[0], 1))], dim=-1)
print(1)