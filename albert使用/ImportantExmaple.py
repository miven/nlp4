from transformers import BartTokenizer, BartForQuestionAnswering
import torch # 试着在这个上面做finetune
# 可以手动去https://huggingface.co/valhalla/bart-large-finetuned-squadv1#   下载需要的文件.
tokenizer = BartTokenizer.from_pretrained('/mnt/qa_data')  # 只是一个纯英文的字典.
model = BartForQuestionAnswering.from_pretrained('/mnt/qa_data')

question, text = "Who am I ?", "he a nice dog in China, I am Zhangbo, and i love it very much, i deadly wanna to eat it"
encoding = tokenizer(question, text, return_tensors='pt')
input_ids = encoding['input_ids']
attention_mask = encoding['attention_mask']

start_scores, end_scores = model(input_ids, attention_mask=attention_mask, output_attentions=False)[:2]

all_tokens = tokenizer.convert_ids_to_tokens(input_ids[0])
answer = ' '.join(all_tokens[torch.argmax(start_scores) : torch.argmax(end_scores)+1])
answer = tokenizer.convert_tokens_to_ids(answer.split())
answer = tokenizer.decode(answer)
print(answer)
#answer => 'a nice puppet'