import torch

# bart = torch.hub.load('pytorch/fairseq', 'bart.large')
# bart.eval()  # disable dropout (or leave in train mode to finetune)
# tokens = bart.encode('Hello world!')
# print(tokens)
# tmp=bart.decode(tokens)
# print(tmp)

bart = torch.hub.load('pytorch/fairseq', 'bart.large.mnli')
bart.eval()  # disable dropout for evaluation

# Encode a pair of sentences and make a prediction
tokens = bart.encode('BART is a seq2seq model.', 'BART is not sequence to sequence.')
bart.predict('mnli', tokens).argmax()  # 0: contradiction  # 表示语义相互矛盾

# Encode another pair of sentences
tokens = bart.encode('BART is denoising autoencoder.', 'nlp is version of autoencoder.')
tmp=bart.predict('mnli', tokens).argmax()  # 2: entailment   # 表示语义相互接近, 如果返回1表示语义无关.
print(tmp)
111111111

'''
这些代码直接能跑,会自动下载权重.
'''














