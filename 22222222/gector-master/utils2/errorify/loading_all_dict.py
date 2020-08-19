"""Synthetic data generator."""
import math
import pickle
import random
from numpy.random import choice as npchoice
# 读取预处理文件.都是一些pickle , 都是一些已经pickle好的东西.也需要研究下里面的数据.
VERBS = pickle.load(open('verbs.p', 'rb')) # 这里面的数据是所有的动词.一共有5w个单词. key是单词, value是一个列表表示他的变形次.
COMMON_INSERTS = set(pickle.load(open('common_inserts.p', 'rb'))) # 一些虚词
COMMON_REPLACES = pickle.load(open('common_replaces.p', 'rb')) # 一些同义词
COMMON_DELETES = pickle.load(open('common_deletes.p','rb')) # 虚词
print(111111111)