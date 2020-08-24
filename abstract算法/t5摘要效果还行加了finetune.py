
from transformers import AutoTokenizer, AutoModelWithLMHead


from transformers import AutoTokenizer, AutoModelWithLMHead

tokenizer = AutoTokenizer.from_pretrained("t5-small")

model = AutoModelWithLMHead.from_pretrained("t5-small")

#https://huggingface.co/transformers/model_doc/bart.html?#transformers.BartForConditionalGeneration


ARTICLE_TO_SUMMARIZE = "The tower is 324 metres (1,063 ft) tall, about the same height as an 81-storey building, and the tallest structure in Paris. Its base is square, measuring 125 metres (410 ft) on each side. During its construction, the Eiffel Tower surpassed the Washington Monument to become the tallest man-made structure in the world, a title it held for 41 years until the Chrysler Building in New York City was finished in 1930. It was the first structure to reach a height of 300 metres. Due to the addition of a broadcasting aerial at the top of the tower in 1957, it is now taller than the Chrysler Building by 5.2 metres (17 ft). Excluding transmitters, the Eiffel Tower is the second tallest free-standing structure in France after the Millau Viaduct."
inputs = tokenizer([ARTICLE_TO_SUMMARIZE], max_length=1024, return_tensors='pt')


# 注意前面要加上prefix 才对! 这点跟ctrl一样,都是要加一个prefix 作为激活,故称为Conditional.
input_ids  = tokenizer.encode("summarize: "+ARTICLE_TO_SUMMARIZE, return_tensors="pt")  # Batch size 1
#https://huggingface.co/transformers/model_doc/distilbert.html  文档去那里面查.
# Generate Summary

#-----------------------------参考的训练代码:
#https://huggingface.co/transformers/_modules/transformers/modeling_t5.html#T5ForConditionalGeneration

outputs = model.generate(input_ids, num_beams=5, max_length=50, early_stopping=True)

print(outputs)
print([tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=False) for g in outputs])


print("---------------------------")



'''
下面开始finetune
'''



# 参考train代码 :huggingface项目中重要例子/transformers/examples/seq2seq/finetune.py

#
# model = T5ForConditionalGeneration(config=config).to(torch_device).eval()
#         outputs = model(
#             input_ids=input_ids,
#             decoder_input_ids=decoder_input_ids,
#             decoder_attention_mask=decoder_attention_mask,
#             labels=lm_labels,
#         )
#         loss, prediction_scores, _, _ = outputs
#
# pad_token_id = self.tokenizer.pad_token_id
# source_ids, source_mask, y = batch["input_ids"], batch["attention_mask"], batch["decoder_input_ids"]
# y_ids = y[:, :-1].contiguous()
# lm_labels = y[:, 1:].clone()
# lm_labels[y[:, 1:] == pad_token_id] = -100
# outputs = self(source_ids, attention_mask=source_mask, decoder_input_ids=y_ids, labels=lm_labels, )
# loss = outputs[0]
# return (loss,)










#-------https://huggingface.co/transformers/model_doc/t5.html#t5forconditionalgeneration










'''

>>> tokenizer = T5Tokenizer.from_pretrained('t5-small')
        >>> model = T5ForConditionalGeneration.from_pretrained('t5-small')
        >>> input_ids = tokenizer.encode("Hello, my dog is cute", return_tensors="pt")  # Batch size 1
        >>> outputs = model(input_ids=input_ids, decoder_input_ids=input_ids, labels=input_ids)
        >>> loss, prediction_scores = outputs[:2]









'''


print("下面打印finetune之前**的结果!!!!!!!!!!!!!!!")
input_ids = tokenizer.encode("summarize: "+"Hello, my dog is cute and what is the problem of it ? i don't know", return_tensors="pt")
outputs = model.generate(input_ids, num_beams=5, max_length=50, early_stopping=True)

print(outputs)
print([tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=False) for g in outputs])



print("下面是finetune代码!!!!!!!!!!!!!!!!!!!!!!!!!!")


#做finetune
if 1:
    from transformers import pipeline, AdamW
    class A():
        pass


    args = A()
    args.learning_rate = 3e-5
    args.adam_epsilon = 1e-8
    args.weight_decay = 0
    no_decay = ["bias", "LayerNorm.weight"]
    optimizer_grouped_parameters = [
        {
            "params": [p for n, p in model.named_parameters() if not any(nd in n for nd in no_decay)],
            "weight_decay": args.weight_decay,
        },
        {"params": [p for n, p in model.named_parameters() if any(nd in n for nd in no_decay)], "weight_decay": 0.0},
    ]
    optimizer = AdamW(optimizer_grouped_parameters, lr=args.learning_rate, eps=args.adam_epsilon)
    # 开启finetune模式 ,,,,,,,C:\Users\Administrator\.PyCharm2019.3\system\remote_sources\-456540730\-337502517\transformers\data\processors\squad.py 从这个里面进行抄代码即可.
    model.zero_grad()
    model.train()
    num=100
    for _ in range(num):
        input_ids = tokenizer.encode("summarize: "+"Hello, my dog is cute and what is the problem of it ? i don't know", return_tensors="pt")  # Batch size 1
        input_ids2 = tokenizer.encode("Hello, my dog is cute.", return_tensors="pt")  # Batch size 1
        outputs = model(input_ids=input_ids, decoder_input_ids=input_ids2, labels=input_ids2)
        loss, prediction_scores = outputs[:2]
        print(loss)
        loss.backward()
        optimizer.step()

        model.zero_grad()



    print("train_over!!!!!!!!!!")



# 测试----------------
model.eval()


print("下面打印finetune之后的结果!!!!!!!!!!!!!!!")
input_ids = tokenizer.encode("summarize: "+"Hello, my dog is cute and what is the problem of it ? i don't know", return_tensors="pt")
outputs = model.generate(input_ids, num_beams=5, max_length=50, early_stopping=True)

print(outputs)
print([tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=False) for g in outputs])













