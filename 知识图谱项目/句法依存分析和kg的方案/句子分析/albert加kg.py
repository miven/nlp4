'''
1111111111111
#


使用前pip 一下transformers 保证版本最新.
'''

# https://www.ctolib.com/amp/brightmart-albert_zh.html


##
# 先引入句向量.
from transformers import *
import torch
from torch.nn.functional import softmax

from transformers import *

pretrained = 'voidful/albert_chinese_xxlarge'
tokenizer = BertTokenizer.from_pretrained(pretrained)  # 主要这里面的tokenizer是bert的.
model = AlbertModel.from_pretrained(pretrained)




##
inputtext = "今天情很好"  # 编码后第一个位置是cls,所以msk的索引是3
# 看看这个函数怎么用
input_ids = torch.tensor(tokenizer.encode(inputtext, add_special_tokens=True)).unsqueeze(0)


outputs = model(input_ids, )
print(outputs)




##















inputtext = "今天[MASK]情很好"  # 编码后第一个位置是cls,所以msk的索引是3
# 计算mask所在的索引位置,




maskpos = tokenizer.encode(inputtext, add_special_tokens=True).index(103)

input_ids = torch.tensor(tokenizer.encode(inputtext, add_special_tokens=True)).unsqueeze(0)  # Batch size 1
outputs = model(input_ids, masked_lm_labels=input_ids)
loss, prediction_scores = outputs[:2]
logit_prob = softmax(prediction_scores[0, maskpos]).data.tolist()
predicted_index = torch.argmax(prediction_scores[0, maskpos]).item()
predicted_token = tokenizer.convert_ids_to_tokens([predicted_index])[0]
print(predicted_token, logit_prob[predicted_index])

'''
下面进行使用hugging face 进行模型训练.
'''
model.num_parameters()
# model.train()


from transformers import LineByLineTextDataset

dataset = LineByLineTextDataset(
    tokenizer=tokenizer,
    file_path="./lunyu.txt",
    block_size=256,
)
from transformers import DataCollatorForLanguageModeling

data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer, mlm=True, mlm_probability=0.15
)

from transformers import Trainer, TrainingArguments

training_args = TrainingArguments(
    output_dir="./lunyuAlbert",
    overwrite_output_dir=True,
    num_train_epochs=20,
    per_gpu_train_batch_size=16,
    save_steps=2000,
    save_total_limit=2,
)

trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=dataset,
    prediction_loss_only=True,
)

# %%time
trainer.train()

'''
模型名	MODEL_NAME
albert_tiny_google_zh	voidful/albert_chinese_tiny
albert_small_google_zh	voidful/albert_chinese_small
albert_base_zh (from google)	voidful/albert_chinese_base
albert_large_zh (from google)	voidful/albert_chinese_large
albert_xlarge_zh (from google)	voidful/albert_chinese_xlarge
albert_xxlarge_zh (from google)	voidful/albert_chinese_xxlarge
'''

print(1)

'''
调用简单:去https://huggingface.co/voidful/albert_chinese_xxlarge
上面搜索模型,然后
'''

from transformers import AlbertTokenizer, AlbertForSequenceClassification
import torch

tokenizer = AlbertTokenizer.from_pretrained('albert-base-v2')
model = AlbertForSequenceClassification.from_pretrained('albert-base-v2')
input_ids = torch.tensor(tokenizer.encode("Hello, my dog is cute")).unsqueeze(0)  # Batch size 1
labels = torch.tensor([1]).unsqueeze(0)  # Batch size 1
outputs = model(input_ids, labels=labels)
loss, logits = outputs[:2]

from ltp import LTP

ltp = LTP()
text='我现在在天津,我想知道这里的大学都有什么学校.'
seg, hidden = ltp.seg([text])
sdp = ltp.sdp(hidden, graph=False)

print(seg,"seg")
pos = ltp.pos(hidden)
ner = ltp.ner(hidden)
print("ner",ner)
srl = ltp.srl(hidden)
dep = ltp.dep(hidden)
sdp = ltp.sdp(hidden)



seg=seg[0]
for i in sdp[0]:

    print(i, seg[i[0]-1], seg[i[1]-1]) # 注意下标会多一个, 箭1后为真正下标.



