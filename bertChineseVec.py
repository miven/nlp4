# 测试代码可用性: 提取特征

from bert4keras.backend import keras
from bert4keras.models import build_transformer_model
from bert4keras.tokenizers import Tokenizer
from bert4keras.snippets import to_array
import numpy as np

config_path = '/mnt/chinese_L-12_H-768_A-12/bert_config.json'
checkpoint_path = '/mnt/chinese_L-12_H-768_A-12/bert_model.ckpt'
dict_path = '/mnt/chinese_L-12_H-768_A-12/vocab.txt'

tokenizer = Tokenizer(dict_path, do_lower_case=True)  # 建立分词器
model = build_transformer_model(config_path, checkpoint_path)  # 建立模型，加载权重
tex='语言模型'
# 编码测试
token_ids, segment_ids = tokenizer.encode(tex)
token_ids, segment_ids = to_array([token_ids], [segment_ids])

print('\n ===== predicting =====\n')
tmp=model.predict([token_ids, segment_ids])
print(tmp)