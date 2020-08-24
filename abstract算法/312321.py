from transformers import AutoTokenizer, AutoModelWithLMHead

tokenizer = AutoTokenizer.from_pretrained("google/pegasus-xsum")

model = AutoModelWithLMHead.from_pretrained("google/pegasus-xsum")

print(1)