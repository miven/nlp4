#coding:utf-8
import dill as pickle
tmp=pickle.load(open('./bpe_deen/bpe_vocab.pkl'),'rb')
# open(opt.data_pkl, 'rb')
print(tmp)

