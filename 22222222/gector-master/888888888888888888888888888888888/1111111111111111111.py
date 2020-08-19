import argparse
import os
from random import seed

import torch
import allennlp
from allennlp.data.iterators import BucketIterator
from allennlp.data.vocabulary import DEFAULT_OOV_TOKEN, DEFAULT_PADDING_TOKEN
from allennlp.data.vocabulary import Vocabulary
from allennlp.modules.text_field_embedders import BasicTextFieldEmbedder

from gector.bert_token_embedder import PretrainedBertEmbedder
from gector.datareader import Seq2LabelsDatasetReader
from gector.seq2labels_model import Seq2Labels
from gector.trainer import Trainer
from gector.wordpiece_indexer import PretrainedBertIndexer
from utils.helpers import get_weights_name
# 学习allennlp 里面vocabulary库包.


train_data=['dsafljdslfjasdlfjas']

Vocabulary.from_instances(train_data,
                                          max_vocab_size={'tokens': 30000,
                                                          'labels': 5000,
                                                          'd_tags': 2},
                                          )
print(121212)