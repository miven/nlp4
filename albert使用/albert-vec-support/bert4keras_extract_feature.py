#!/usr/bin/python
# -*- coding:utf-8 -*-

from bert4keras.models import build_transformer_model
from bert4keras.tokenizers import Tokenizer
import numpy as np
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'  # 屏蔽GPU

# config_path: albert模型结构描述文件路径
config_path = 'model/albert_tiny_zh_google/albert_config_tiny_g.json'
# checkpoint_path: TensorFlow checkpoint文件路径
checkpoint_path = 'model/albert_tiny_zh_google/albert_model.ckpt'
# dict_path: albert词汇表路径
dict_path = 'model/albert_tiny_zh_google/vocab.txt'

# 载入预训练ALBERT模型
model = build_transformer_model(config_path, checkpoint_path, model='albert',
                                with_pool=True)

tokenizer = Tokenizer(dict_path, do_lower_case=True)
token_ids, segment_ids = tokenizer.encode(u'你好 世界')
print("Token ID: " + str(token_ids))
print("Segment ID:" + str(segment_ids))


print('\n ===== predicting =====\n')
vec1 = model.predict([np.array([token_ids]), np.array([segment_ids])])
print(vec1.shape)
