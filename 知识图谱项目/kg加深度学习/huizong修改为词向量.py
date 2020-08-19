
from transformers import AutoTokenizer, AutoModelWithLMHead

tokenizer = AutoTokenizer.from_pretrained("bert-base-chinese")

model = AutoModelWithLMHead.from_pretrained("bert-base-chinese")
