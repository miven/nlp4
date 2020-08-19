import torch

# English to German translation
en2de = torch.hub.load('pytorch/fairseq', 'transformer.wmt19.en-de', checkpoint_file='model1.pt:model2.pt:model3.pt:model4.pt',
                       tokenizer='moses', bpe='fastbpe')
tmp=en2de.translate("Machine learning is great!")  # 'Maschinelles Lernen ist großartig!'
print(tmp)
# German to English translation
de2en = torch.hub.load('pytorch/fairseq', 'transformer.wmt19.de-en', checkpoint_file='model1.pt:model2.pt:model3.pt:model4.pt',
                       tokenizer='moses', bpe='fastbpe')
de2en.translate("Maschinelles Lernen ist großartig!")  # 'Machine learning is great!'

# English to Russian translation
en2ru = torch.hub.load('pytorch/fairseq', 'transformer.wmt19.en-ru', checkpoint_file='model1.pt:model2.pt:model3.pt:model4.pt',
                       tokenizer='moses', bpe='fastbpe')
en2ru.translate("Machine learning is great!")  # 'Машинное обучение - это здорово!'

# Russian to English translation
ru2en = torch.hub.load('pytorch/fairseq', 'transformer.wmt19.ru-en', checkpoint_file='model1.pt:model2.pt:model3.pt:model4.pt',
                       tokenizer='moses', bpe='fastbpe')
ru2en.translate("Машинное обучение - это здорово!")  # 'Machine learning is great!'