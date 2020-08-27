from transformers import AutoTokenizer, AutoModelWithLMHead, AdamW

tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-zh")

model = AutoModelWithLMHead.from_pretrained("Helsinki-NLP/opus-mt-en-zh")


'''
说明书:https://huggingface.co/transformers/model_doc/marian.html#multilingual-models
'''


from transformers import MarianTokenizer, MarianMTModel
from typing import List
# src = 'fr'  # source language
# trg = 'en'  # target language
sample_text = "Where is the the bus stop ?"
# mname = f'Helsinki-NLP/opus-mt-{src}-{trg}'
# model = MarianMTModel.from_pretrained(mname)
# tok = MarianTokenizer.from_pretrained(mname)
batch = tokenizer.prepare_translation_batch(src_texts=[sample_text])  # don't need tgt_text for inference
gen = model.generate(**batch)  # for forward pass: model(**batch)
tmp= tokenizer.batch_decode(gen, skip_special_tokens=True)  # returns "Where is the the bus stop ?"
print(tmp)


# 下面开始写finetune代码




if 1:
    class A():
        pass
    args=A()
    args.learning_rate=3e-5
    args.adam_epsilon=1e-8
    args.weight_decay=0
    no_decay = ["bias", "LayerNorm.weight"]
    optimizer_grouped_parameters = [
        {
            "params": [p for n, p in model.named_parameters() if not any(nd in n for nd in no_decay)],
            "weight_decay": args.weight_decay,
        },
        {"params": [p for n, p in model.named_parameters() if any(nd in n for nd in no_decay)], "weight_decay": 0.0},
    ]

    sample_text = "Where is the the bus stop ?"
    # mname = f'Helsinki-NLP/opus-mt-{src}-{trg}'
    # model = MarianMTModel.from_pretrained(mname)
    # tok = MarianTokenizer.from_pretrained(mname)
    batch = tokenizer.prepare_translation_batch(src_texts=[sample_text])
    optimizer = AdamW(optimizer_grouped_parameters, lr=args.learning_rate, eps=args.adam_epsilon)
    #开启finetune模式 ,,,,,,,C:\Users\Administrator\.PyCharm2019.3\system\remote_sources\-456540730\-337502517\transformers\data\processors\squad.py 从这个里面进行抄代码即可.
    model.zero_grad()
    model.train()


    for _ in range(10):
        # batch=[input_ids,attention_mask,torch.tensor([7]),torch.tensor([9])]  # ---------表示训练数据. 注意所以所以是整个q,t 放一起算的
        # inputs = {
        #     "input_ids": batch[0],
        #     "attention_mask": batch[1],
        #
        #     "start_positions": batch[2],
        #     "end_positions": batch[3],
        # }
        import torch
        print('start_train')
        outputs = model(**batch,labels=torch.tensor([1,2,3,4,5]))
        loss = outputs[0]
        print(loss)
        loss.backward()
        optimizer.step()

        model.zero_grad()


    print("train_over!!!!!!!!!!")

#---------下面开始测试
model.eval()
gen = model.generate(**batch)  # for forward pass: model(**batch)
tmp= tokenizer.batch_decode(gen, skip_special_tokens=True)  # returns "Where is the the bus stop ?"
print(tmp)


print(tmp)













