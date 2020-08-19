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



start_scores, end_scores = model(input_ids)
span_scores = start_scores.softmax(dim=1).log()[:,:,None] + end_scores.softmax(dim=1).log()[:,None,:]
ignore_score = span_scores[:,0,0] #no answer scores






name='wptoux/albert-chinese-large-qa'
qa_pipeline = pipeline(
    "question-answering",
    model=name,
    tokenizer=name
)

b=qa_pipeline({
    'context': "Manuel Romero has been working hardly in the repository hugginface/transformers lately",
    'question': "Who has been working hard for hugginface/transformers lately?"

})

print(b)