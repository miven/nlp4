from transformers import AutoTokenizer, AutoModelWithLMHead

tokenizer = AutoTokenizer.from_pretrained("hfl/chinese-bert-wwm-ext")

model = AutoModelWithLMHead.from_pretrained("hfl/chinese-bert-wwm-ext")