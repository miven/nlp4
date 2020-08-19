import torch
from transformers import CTRLTokenizer, CTRLModel
tokenizer = CTRLTokenizer.from_pretrained('ctrl')
model = CTRLModel.from_pretrained('ctrl')
input_ids =torch.tensor(tokenizer.encode("Links Hello, my dog is cute",add_special_tokens=True)).unsqueeze(0) # Batch size 1 #因为只有一个句子所以需要unsqueeze去掉一层.
outputs = model(input_ids)# 输出的第一个是结果,第二个是cache没啥用.










