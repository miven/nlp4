#!/usr/bin/env python
# -*- coding:utf-8 -*-
from collections import defaultdict
import re


import sys,os
'''
添加keywords这个文件.
'''

sys.path.append(os.path.dirname(os.path.abspath( __file__ ) ))












'''
读这个py代码.前2个不难,最后一个dfa算法很6.速度很快
'''
__all__ = ['NaiveFilter', 'BSFilter', 'DFAFilter']
__author__ = 'observer'
__date__ = '2012.01.05'
















'''
一共有3个类,先看第一个类
'''


class NaiveFilter():

    '''Filter Messages from keywords.txt

    very simple filter implementation

    >>> f = NaiveFilter()
    >>> f.add("sexy")
    >>> f.filter("hello sexy baby")
    hello **** baby
    '''

    def __init__(self):
        self.keywords = set([])

    def parse(self, path):
        '''
        加载dirty word词表.

        :param path:
        :return:
        '''
        for keyword in open(path,encoding='utf-8'):  #open 里面要配上encoding 参数
            self.keywords.add(keyword.strip().lower())

    def filter(self, message, repl="*"):
        '''
        替换即可.

        :param message:
        :param repl:
        :return:
        '''
        message = str(message).lower()
        for kw in self.keywords:  #这个遍历了整个词表.所以很慢
            message = message.replace(kw, repl)
        return message



'''
再看第二个类
'''



class BSFilter:

    '''Filter Messages from keywords.txt

    Use Back Sorted Mapping to reduce replacement times
    做算法加速

    怎么实现的?

    >>> f = BSFilter()
    >>> f.add("sexy")
    >>> f.filter("hello sexy baby")
    hello **** baby
    '''

    def __init__(self):
        self.keywords = []
        self.kwsets = set([])
        self.bsdict = defaultdict(set)
        self.pat_en = re.compile(r'^[0-9a-zA-Z]+$')  # english phrase or not

    '''
   Back Sorted Mapping
    '''
    def add(self, keyword):
        if not isinstance(keyword, str):
            keyword = keyword.decode('utf-8')
        keyword = keyword.lower()
        if keyword not in self.kwsets:
            self.keywords.append(keyword)
            self.kwsets.add(keyword)
            index = len(self.keywords) - 1
            for word in keyword.split():
                if self.pat_en.search(word):
                    self.bsdict[word].add(index) #所以bsdict的结构是 key 汉字----value  索引组成的set
                else:
                    for char in word:
                        self.bsdict[char].add(index)

    def parse(self, path):
        with open(path, "r",encoding='utf-8') as f:
            for keyword in f:
                self.add(keyword.strip())

    def filter(self, message, repl="*"):
        if not isinstance(message, str):
            message = message.decode('utf-8')
        message = message.lower()
        for word in message.split():#这个算法每一个汉子只找了和他匹配的那些keyword做替换.所以快很多.
            if self.pat_en.search(word):#if  word is English word
                for index in self.bsdict[word]:
                    message = message.replace(self.keywords[index], repl)
            else:
                for char in word:#if word is a chinese essay
                    for index in self.bsdict[char]:
                        message = message.replace(self.keywords[index], repl)
        return message

















class DFAFilter():

    '''Filter Messages from keywords.txt

    Use DFA to keep algorithm perform constantly

    超级快       DFA全称为:Deterministic Finite Automaton,

    >>> f = DFAFilter()
    >>> f.add("sexy")
    >>> f.filter("hello sexy baby")
    hello **** baby
    '''

    def __init__(self):



        self.keyword_chains = {}
        self.delimit = '\x00'



        #调用哪个类,就需要把超参数都写到init这个函数中.才运行.类外面的东西不运行的.
        from collections import defaultdict
        import re

        import sys, os
        '''
        添加keywords这个文件.
        '''

        sys.path.append(os.path.dirname(os.path.abspath(__file__)))













        self.parse(os.path.dirname(os.path.abspath(__file__))+"/keywords.txt")


    def add(self, keyword):

        if not isinstance(keyword, str):
            keyword = keyword.decode('utf-8')
        keyword = keyword.lower()
        chars = keyword.strip()
        if not chars:
            return
        level = self.keyword_chains
        for i in range(len(chars)):
            if chars[i] in level:
                level = level[chars[i]] #首先用for循环进到最深层的字对应的value字典里面.
            else:
                if not isinstance(level, dict):
                    break
                for j in range(i, len(chars)):
                    level[chars[j]] = {} #第一次就把回写进去, last_char=回,lastlevel=当前字典
                    #然后level进去当前这个字典的value,继续写,写族....都写完了,就



                    last_level, last_char = level, chars[j]
                    level = level[chars[j]]
                last_level[last_char] = {self.delimit: 0}
                break
        if i == len(chars) - 1:
            level[self.delimit] = 0

    def parse(self, path):
        with open(path,encoding='utf-8') as f:
            for keyword in f:
                self.add(keyword.strip())

    def filter(self, message, repl="*"):


        if not isinstance(message, str):
            message = message.decode('utf-8')
        message = message.lower()
        ret = []
        start = 0
        while start < len(message):
            level = self.keyword_chains
            step_ins = 0

            #二重循环遍历,这个算法跟dat挺像.nlp里面高效率算法挺多.操作可以各种秀.
            for char in message[start:]:
                if char in level:
                    step_ins += 1
                    if self.delimit not in level[char]:
                        level = level[char]
                    else:
                        ret.append(repl * step_ins)
                        start += step_ins - 1
                        break
                else:#这是说明下面是一个新词了,所以可以break,然后把词放进ret中.
                    ret.append(message[start])
                    break
            else:
                ret.append(message[start])
            start += 1

        return ''.join(ret)


def test_first_character():
    gfw = DFAFilter()
    gfw.add("1989年")
    assert gfw.filter("1989", "*") == "1989"


if __name__ == "__main__":
    # gfw = NaiveFilter()   #0.01s

    # gfw = BSFilter()           #0.00148s
    gfw = DFAFilter()          #这个更秀直接0s
           #0.0004956722259521484

    '''
    https://blog.csdn.net/cdj0311/article/details/79789480
    '''
    import time
    t = time.time()










    # test_first_character()
