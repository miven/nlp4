'''
中文qa,在这个基础上做finetune即可.






https://github.com/wptoux/albert-chinese-large-webqa

'''

from transformers.data.processors.squad import SquadResult, SquadV1Processor, SquadV2Processor

from transformers import pipeline, AdamW
from transformers import AutoModelForQuestionAnswering, BertTokenizer

model = AutoModelForQuestionAnswering.from_pretrained('wptoux/albert-chinese-large-qa') #64mb
tokenizer = BertTokenizer.from_pretrained('wptoux/albert-chinese-large-qa')
from transformers import pipeline
















from transformers import BartTokenizer, BartForQuestionAnswering
import torch # 试着在这个上面做finetune
# 可以手动去https://huggingface.co/valhalla/bart-large-finetuned-squadv1#   下载需要的文件.


question, text = "我是谁", "我是朱光旭啊啊啊啊啊啊啊啊啊啊啊啊"
encoding = tokenizer(question, text, return_tensors='pt')
input_ids = encoding['input_ids']
attention_mask = encoding['attention_mask']



if 0:
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
    optimizer = AdamW(optimizer_grouped_parameters, lr=args.learning_rate, eps=args.adam_epsilon)
    #开启finetune模式 ,,,,,,,C:\Users\Administrator\.PyCharm2019.3\system\remote_sources\-456540730\-337502517\transformers\data\processors\squad.py 从这个里面进行抄代码即可.
    model.zero_grad()
    model.train()


    for _ in range(10):
        batch=[input_ids,attention_mask,torch.tensor([7]),torch.tensor([9])]  # ---------表示训练数据. 注意所以所以是整个q,t 放一起算的
        inputs = {
            "input_ids": batch[0],
            "attention_mask": batch[1],

            "start_positions": batch[2],
            "end_positions": batch[3],
        }
        print('start_train')
        outputs = model(**inputs)
        loss = outputs[0]
        print(loss)
        loss.backward()
        optimizer.step()

        model.zero_grad()


    print("train_over!!!!!!!!!!")

#---------下面开始测试
model.eval()
print("8888888888888888888888")



question, text = "时间", "上午八时,我杀了一个人"
encoding = tokenizer(question, text, return_tensors='pt')
input_ids = encoding['input_ids']
attention_mask = encoding['attention_mask']


start_scores, end_scores = model(input_ids, attention_mask=attention_mask, output_attentions=False)[:2]




all_tokens = tokenizer.convert_ids_to_tokens(input_ids[0])
end=torch.argmax(end_scores)+1
start=torch.argmax(start_scores)
if end<start:
    answer = ' '.join(all_tokens[start:])
else:

    answer = ' '.join(all_tokens[start:end])
answer = tokenizer.convert_tokens_to_ids(answer.split())
answer = tokenizer.decode(answer)

print(answer)
