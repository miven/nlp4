
import os, re, json
import json
import nmslib
import torch
import random
import pandas as pd
from tqdm import tqdm
import numpy as np
#import tensorflow_hub as hub
from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer
from joblib import dump, load
from string import punctuation
from operator import itemgetter
from functools import wraps
from pytorch_pretrained_bert import BertModel, BertTokenizer, BertConfig
from sklearn.metrics.pairwise import cosine_similarity
from rusenttokenize import ru_sent_tokenize


def singleton(cls):
    instance = None
    @wraps(cls)
    def inner(*args, **kwargs):
        nonlocal instance
        if instance is None:
            instance = cls(*args, **kwargs)
        return instance
    return inner


class BertEmbedder(object):
    """
    Embedding Wrapper on Bert Multilingual Cased
    """

    def __init__(self, path=''):
        # use self.model_file with a path instead of 'bert-base-uncased' if you have a custom pretrained model
        self.model_file = 'bert-base-uncased'  # os.path.join(path, "bert-base-multilingual-cased.tar.gz")
        self.vocab_file = 'bert-base-uncased-vocab.txt'  # os.path.join(path, "data_bert-base-multilingual-cased-vocab.txt")         # 'bert-base-uncased'
        self.model = self.bert_model()
        self.tokenizer = self.bert_tokenizer()
        self.embedding_matrix = self.get_bert_embed_matrix()

    @singleton
    def bert_model(self):
        model = BertModel.from_pretrained(self.model_file).eval()
        return model

    @singleton
    def bert_tokenizer(self):
        tokenizer = BertTokenizer.from_pretrained(self.vocab_file, do_lower_case=False)
        return tokenizer

    @singleton
    def get_bert_embed_matrix(self):
        bert_embeddings = list(self.model.children())[0]
        bert_word_embeddings = list(bert_embeddings.children())[0]
        matrix = bert_word_embeddings.weight.data.numpy()
        return matrix

    def sentence_embedding(self, text):
        token_list = self.tokenizer.tokenize("[CLS] " + text + " [SEP]")
        segments_ids, indexed_tokens = [1] * len(token_list), self.tokenizer.convert_tokens_to_ids(token_list)
        segments_tensors, tokens_tensor = torch.tensor([segments_ids]), torch.tensor([indexed_tokens])
        with torch.no_grad():
            encoded_layers, _ = self.model(tokens_tensor, segments_tensors)
        sent_embedding = torch.mean(encoded_layers[11], 1)
        return sent_embedding

    def sentences_embedding(self, text_list):
        embeddings = []
        for text in tqdm(text_list):
            token_list = self.tokenizer.tokenize("[CLS] " + text + " [SEP]")
            segments_ids, indexed_tokens = [1] * len(token_list), self.tokenizer.convert_tokens_to_ids(token_list)
            segments_tensors, tokens_tensor = torch.tensor([segments_ids]), torch.tensor([indexed_tokens])
            with torch.no_grad():
                encoded_layers, _ = self.model(tokens_tensor, segments_tensors)
            sent_embedding = torch.mean(encoded_layers[11], 1)
            embeddings.append(sent_embedding)
        return embeddings

    def token_embedding(self, token_list):
        token_embedding = []
        for token in token_list:
            ontoken = self.tokenizer.tokenize(token)
            segments_ids, indexed_tokens = [1] * len(ontoken), self.tokenizer.convert_tokens_to_ids(ontoken)
            segments_tensors, tokens_tensor = torch.tensor([segments_ids]), torch.tensor([indexed_tokens])
            with torch.no_grad():
                encoded_layers, _ = self.model(tokens_tensor, segments_tensors)
            ontoken_embeddings = []
            for subtoken_i in range(len(ontoken)):
                hidden_layers = []
                for layer_i in range(len(encoded_layers)):
                    vector = encoded_layers[layer_i][0][subtoken_i]
                    hidden_layers.append(vector)
                ontoken_embeddings.append(hidden_layers)
            cat_last_4_layers = [torch.cat((layer[-4:]), 0) for layer in ontoken_embeddings]
            token_embedding.append(cat_last_4_layers)
        token_embedding = torch.stack(token_embedding[0], 0) if len(token_embedding) > 1 else token_embedding[0][0]
        return token_embedding



tmp=BertEmbedder()
tmp=tmp.sentence_embedding


tmp2=tmp('我们')
tmp3=tmp('他们')





print(1)




















