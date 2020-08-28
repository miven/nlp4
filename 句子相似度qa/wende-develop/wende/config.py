# -*- coding: utf-8 -*-
""" 系统配置 """

from __future__ import unicode_literals
import logging
import logging.config
from os import path

WEB_APP_DEBUG = False
NLP_LOG_LEVEL = 'DEBUG'

# 系统数据集合路径
DATA_DIR = path.normpath(path.join(path.dirname(path.abspath(__file__)), '../data/'))
# 模型路径
MODELS_DIR = path.join(DATA_DIR, 'models/')
# 疑问词表文档路径
INTERROGATIVE_WORD_FILE = path.join(DATA_DIR, 'interrogative_words.txt')
# 停用词表文档路径
STOPWORDS_FILE = path.join(DATA_DIR, 'stopwords.txt')
# 分类模型训练数据集路径
DATASET = path.join(DATA_DIR, 'dataset.txt')
# 用户问题缓存路径
USER_ASK = path.join(DATA_DIR, 'user_ask.txt')

# LTP 模型路径
LTP_DATADIR = path.join(MODELS_DIR, 'ltp_data/')
# Wor2Vec 模型路径
WORD2VEC_MODEL_DIR = path.join(MODELS_DIR, 'word2vec/wiki_cn_word2vec.model')
WORD2VEC_MODEL_SIZE = 200
# Wende 模型路径
APP_MODEL_DIR = path.join(MODELS_DIR, 'wende/')

# Hit LTPCloud API TOKEN See：http://www.ltp-cloud.com/document/
LTP_API_TOKEN = ''


# Here change your app secret key for csrf
SECRET_KEY = 'devkey12345'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'default': {
            'format': '%(asctime)s %(levelname)s %(module)s: %(message)s'
        },
        'simple': {
            'format': '[%(levelname)8s (%(module)s)] -- %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': NLP_LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': NLP_LOG_LEVEL,
        },
    }
}
logging.config.dictConfig(LOGGING)
logger = logging.getLogger()
logging.getLogger('gensim').setLevel('ERROR')
