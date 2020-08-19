'''
1111111111111



使用前pip 一下transformers 保证版本最新.
'''




##


# https://www.ctolib.com/amp/brightmart-albert_zh.html

from transformers import *
import torch
from torch.nn.functional import softmax

pretrained = 'voidful/albert_chinese_xxlarge'
tokenizer = BertTokenizer.from_pretrained(pretrained)      # 主要这里面的tokenizer是bert的.
model = AlbertForMaskedLM.from_pretrained(pretrained)



t1='[MASK]'


##
inputtext = "今天我吃了一[MASK]"
while 1:
      # 编码后第一个位置是cls,所以msk的索引是3
    #计算mask所在的索引位置,
    maskpos = tokenizer.encode(inputtext, add_special_tokens=True).index(103)

    input_ids = torch.tensor(tokenizer.encode(inputtext, add_special_tokens=True)).unsqueeze(0)  # Batch size 1
    outputs = model(input_ids, masked_lm_labels=input_ids)
    loss, prediction_scores = outputs[:2]
    logit_prob = softmax(prediction_scores[0, maskpos]).data.tolist()
    predicted_index = torch.argmax(prediction_scores[0, maskpos]).item()
    predicted_token = tokenizer.convert_ids_to_tokens([predicted_index])[0]
    # print(predicted_token,logit_prob[predicted_index])
    inputtext=inputtext.replace('[MASK]',predicted_token)
    print(inputtext)
    inputtext+='[MASK]'






















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
# trainer.train()







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