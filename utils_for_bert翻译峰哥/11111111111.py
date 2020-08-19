from transformers.tokenization_bert import BertTokenizer



tmp=BertTokenizer.from_pretrained('bert-base-uncased')
tmp.do_basic_tokenize=False
tmp2=tmp._tokenize('i am unaffable You can link tokens to special vocabulary when instantiating'.lower())



#    </s>  <s>
# tmp=BertTokenizer.from_pretrained('bert-base-chinese')
# tmp.do_basic_tokenize=True
# tmp2=tmp._tokenize('FaceBook 近日提出了一个名为BART的预训练语言模型。该模型结合双向和自回归 Transformer 进行模型预训练，在一些自然语言处理任务上取得了SOTA性能表现')

print(tmp2)

tmp2=[tmp._convert_token_to_id(i)for i in tmp2]

print(tmp2)
tmp2=[tmp._convert_id_to_token(i)for i in tmp2]

print(tmp2)

tmp2=tmp.convert_tokens_to_string(tmp2)
print(tmp2)





