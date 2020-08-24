'''
跑这个abstract 模型.

'''




from transformers import AutoTokenizer, AutoModelWithLMHead

tokenizer = AutoTokenizer.from_pretrained("sshleifer/distilbart-xsum-1-1")

model = AutoModelWithLMHead.from_pretrained("sshleifer/distilbart-xsum-1-1")






#https://huggingface.co/transformers/model_doc/bart.html?#transformers.BartForConditionalGeneration


ARTICLE_TO_SUMMARIZE = "The tower is 324 metres (1,063 ft) tall, about the same height as an 81-storey building, and the tallest structure in Paris. Its base is square, measuring 125 metres (410 ft) on each side. During its construction, the Eiffel Tower surpassed the Washington Monument to become the tallest man-made structure in the world, a title it held for 41 years until the Chrysler Building in New York City was finished in 1930. It was the first structure to reach a height of 300 metres. Due to the addition of a broadcasting aerial at the top of the tower in 1957, it is now taller than the Chrysler Building by 5.2 metres (17 ft). Excluding transmitters, the Eiffel Tower is the second tallest free-standing structure in France after the Millau Viaduct."
inputs = tokenizer([ARTICLE_TO_SUMMARIZE], max_length=1024, return_tensors='pt')
#https://huggingface.co/transformers/model_doc/distilbert.html  文档去那里面查.
# Generate Summary
summary_ids = model.generate(inputs['input_ids'], num_beams=5, max_length=50, early_stopping=True)
print('                   ')
print([tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=False) for g in summary_ids])



