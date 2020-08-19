'''
中文qa,在这个基础上做finetune即可.






https://github.com/wptoux/albert-chinese-large-webqa

'''

from transformers.data.processors.squad import SquadResult, SquadV1Processor, SquadV2Processor

from transformers import pipeline
from transformers import AutoModelForQuestionAnswering, BertTokenizer

model = AutoModelForQuestionAnswering.from_pretrained('wptoux/albert-chinese-large-qa')
tokenizer = BertTokenizer.from_pretrained('wptoux/albert-chinese-large-qa')
from transformers import pipeline
















from transformers import BartTokenizer, BartForQuestionAnswering
import torch # 试着在这个上面做finetune
# 可以手动去https://huggingface.co/valhalla/bart-large-finetuned-squadv1#   下载需要的文件.


question, text = "我是谁", "我是张博啊"
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