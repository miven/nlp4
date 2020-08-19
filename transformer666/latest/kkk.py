#coding:utf-8
import dill as pickle
tmp=pickle.load(open('./bpe_deen/bpe_vocab.pkl','rb'))
# open(opt.data_pkl, 'rb')
abc=tmp['vocab'].vocab.itos
abc2={}
for i in range(len(abc)):
    abc2[i]=abc[i]
efg=tmp['vocab'].vocab.stoi
tmp5=[1,2,34,45,6,7]
out=[efg[i] for i in tmp5]

print(tmp)

