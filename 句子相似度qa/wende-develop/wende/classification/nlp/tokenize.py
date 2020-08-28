# -*- coding:utf-8 -*-
"""
    tokenize.py
    ~~~~~~~~~~~

    NLP: 分词
"""

from __future__ import unicode_literals
import fileinput
import logging
import jieba
from wende.config import STOPWORDS_FILE

__all__ = ['tokenize']

jieba.setLogLevel('INFO')
stopwords = [line.strip()
             for line in fileinput.input(STOPWORDS_FILE)]
fileinput.close()

def tokenize(question):
    """ 分词，使用结巴分词
    :param question: 待分词问题句子
    :return: 已去停用词分词结果
    """
    rv = _remove_stopwords(jieba.lcut(question))
    logging.debug("NLP:tokenize: {}".format(" ".join(rv)))
    return rv


def _remove_stopwords(words):
    """  去停用词，默认停用词表仅包含中英文常用标点符号
    :param words: 分词结果
    :return: 去停用词后的词列表
    """
    for word in words:
        if word in stopwords:
            words.remove(word)
    return words
