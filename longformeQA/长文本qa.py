from transformers import AutoTokenizer, AutoModelForQuestionAnswering

tokenizer = AutoTokenizer.from_pretrained("a-ware/longformer-QA")

model = AutoModelForQuestionAnswering.from_pretrained("a-ware/longformer-QA")









from transformers import BartTokenizer, BartForQuestionAnswering, AdamW
import torch # 试着在这个上面做finetune
# 可以手动去https://huggingface.co/valhalla/bart-large-finetuned-squadv1#   下载需要的文件.


question, text = "Who am I ?", "he a nice dog in China, I am Zhangbo, and i love it very much, i deadly wanna to eat it"
question, text = "Which name is also used to describe the Amazon rainforest in English?", """The Amazon rainforest (Portuguese: Floresta Amazônica or Amazônia; Spanish: Selva Amazónica, Amazonía or usually Amazonia; French: Forêt amazonienne; Dutch: Amazoneregenwoud), also known in English as Amazonia or the Amazon Jungle, is a moist broadleaf forest that covers most of the Amazon basin of South America. This basin encompasses 7,000,000 square kilometres (2,700,000 sq mi), of which 5,500,000 square kilometres (2,100,000 sq mi) are covered by the rainforest. This region includes territory belonging to nine nations. The majority of the forest is contained within Brazil, with 60% of the rainforest, followed by Peru with 13%, Colombia with 10%, and with minor amounts in Venezuela, Ecuador, Bolivia, Guyana, Suriname and French Guiana. States or departments in four nations contain "Amazonas" in their names. The Amazon represents over half of the planet's remaining rainforests, and comprises the largest and most biodiverse tract of tropical rainforest in the world, with an estimated 390 billion individual trees divided into 16,000 species."""
#---------Notes!!!!!!!!!
'''
上面这个问题的答案显然是Zhangbo,但是我就骗骗要把他finetune成a nice dog. 下面我们来进行finetune.
'''
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


    for _ in range(100):
        batch=[input_ids,attention_mask,torch.tensor([0]),torch.tensor([3])]
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
start_scores, end_scores = model(input_ids, attention_mask=attention_mask, output_attentions=False)[:2]




all_tokens = tokenizer.convert_ids_to_tokens(input_ids[0])
answer = ' '.join(all_tokens[torch.argmax(start_scores) : torch.argmax(end_scores)+1])
answer = tokenizer.convert_tokens_to_ids(answer.split())
answer = tokenizer.decode(answer)






print(answer)
#answer => 'a nice puppet'


