from transformers import BertTokenizer

tokenizer = BertTokenizer.from_pretrained('deepset/minilm-uncased-squad2')
truncated_query = tokenizer.encode(
        'Who has been working hard for hugginface/transformers lately?', add_special_tokens=False, truncation=True, max_length=64
    )
print(truncated_query)