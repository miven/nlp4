'''
ltp里面的句法依存分析


https://www.jianshu.com/p/867478f0e674         接口说明.
'''

'''
text:   我现在在天津,我想知道天津的大学都有什么学校.
'''
# -*- coding: utf-8 -*-
import os
# text='姚明的老婆的丈夫的老婆'
# text='中国的首都的名字叫什么'
text='我现在在天津,我想知道这里的大学都有什么学校.'
# text='拉布拉多是什么'

'''
这个东西,就没法理解是什么,该如何跳转, 所以这时候需要bert进行语义匹配.来辅助跳转.
把所有跳转的东西,跟这个text做距离计算.看拉布拉多的哪个edge更符合这个句子的需要!
'''







## 加载模型文件
LTP_DATA_DIR = '/ltp_data_v3.4.0'  # ltp模型目录的路径
pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')  # 词性标注模型路径，模型名称为`pos.model`
cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')  # 分词模型路径，模型名称为`cws.model`
par_model_path = os.path.join(LTP_DATA_DIR, 'parser.model')  # 依存句法分析模型路径，模型名称为`parser.model`



## 词性标注
from pyltp import Postagger



from pyltp import Segmentor









par_model_path = os.path.join(LTP_DATA_DIR, 'parser.model')  # 依存句法分析模型路径，模型名称为`parser.model`
from pyltp import Segmentor
segmentor = Segmentor()  # 初始化实例
segmentor.load_with_lexicon(cws_model_path,'dict1.txt')  # 加载模型
from pyltp import Parser
parser = Parser() # 初始化实例
parser.load(par_model_path)  # 加载模型
words = list(segmentor.segment(text)) # 分词

## 词性标注
from pyltp import Postagger
postagger = Postagger() # 初始化实例
postagger.load(pos_model_path)  # 加载模型
print(words,'分词结果')
postags = postagger.postag(words)  # 词性标注
tags=list(postags)
print(tags,"词性标注")


## 依存句法分析
from pyltp import Parser
parser = Parser() # 初始化实例
parser.load(par_model_path)  # 加载模型


arcs = parser.parse(words, postags)  # 句法分析

rely_id = [arc.head for arc in arcs]    # 提取依存父节点id
relation = [arc.relation for arc in arcs]   # 提取依存关系
heads = ['Root' if id == 0 else str((words[id-1],id-1)) for id in rely_id]  # 匹配依存父节点词语
print('带索引的关联关系')
for i in range(len(words)):
    print (relation[i] + '(' + str(words[i])+' '+str(i)+  ', ' + heads[i] + ')')

parser.release()  # 释放模型


'''
结果说明:
SBV(欧几里得, 是)
HED(是, Root)
ATT(西元前, 世纪)
ATT(三, 世纪)
ATT(世纪, 数学家)
RAD(的, 世纪)
ATT(希腊, 数学家)
VOB(数学家, 是)
WP(。, 是)

以上是结果表:




说明在这里:
https://blog.csdn.net/sinat_33741547/article/details/79258045



写下来:
sbv:主谓结构          SBV(欧几里得, 是)         subject-------verb
vob:动宾关系        verb -------  object
iob:见宾关系.   间接宾语.         句子中有两个宾语时，其中指物或指事的就是直接宾语。指人（或动物）的就是间接宾语。        所以简介宾语用来指人的宾语.


fob:前置宾语 宾语放到verb前面         front ---obj
hed:核心关系
att: 定语关系.
rad:又附加关系.
wp:标点符号

dbl:2个动词.



'''

'''
下面我们找到入口: kg的入口, 就是ner识别即可
'''


ner_model_path = os.path.join(LTP_DATA_DIR, 'ner.model')  # 命名实体识别模型路径，模型名称为`ner.model`

from pyltp import NamedEntityRecognizer
recognizer = NamedEntityRecognizer() # 初始化实例
recognizer.load(ner_model_path)  # 加载模型


nertags = recognizer.recognize(words, postags)  # 命名实体识别
print(words,'分词结果')
print (' '.join(nertags),'ner结果')
recognizer.release()  # 释放模型

'''
结果:  S-Nh O O O O O O

：人名（Nh），地名（NS），机构名（Ni）
'''






'''
张博:
再配上ner就行了

张博:
ATT(姚明, 老婆)
RAD(的, 姚明)
ATT(老婆, 丈夫)
RAD(的, 老婆)
ATT(丈夫, 老婆)
RAD(的, 丈夫)
HED(老婆, Root)
S-Nh O O O O O O

张博:
第一个S-Nh 表示noune-human 人名

张博:
o表示非实体

张博:
所以从第一个词姚明开始去图谱里面搜索就行了


一步一步的跳转, att和vob目前使用.





张博:
搭起来也容易

张博:
用1.4亿开源的中文kg资料即可

'''





'''
张博:
['涅槃[佛教用语]', '描述', '涅槃，一切变现不为烦恼，皆合涅槃清净妙德。']
['涅槃[佛教用语]', '中文名', '涅槃']
['涅槃[佛教用语]', '外文名', 'nirvana']
['涅槃[佛教用语]', '文字', '梵文、藏文、中文、日文、英文等']
['涅槃[佛教用语]', '宗教', '佛教']
['涅槃[佛教用语]', '世界', '西方极乐世界']
['涅槃[佛教用语]', '修行方式', '戒定慧三无漏学']
['涅槃[佛教用语]', '语言', '多国语言']
['涅槃[佛教用语]', '地方语言', '闽南语、台湾话、日语']
['涅槃[佛教用语]', '身份', '四生的慈母、慈父']
['涅槃[佛教用语]', '标签', '佛教']

张博:
我又想到一个

张博:
比如这个是涅槃的所有属性

张博:
如果客户要的东西在这里面表述方式不一样,我们就根据词向量,找一个最相似的返回.

张博:
这个词向量可以用bert来给

'''



'''
以上的方案是在知识图谱已经存入数据库Neo4j里面之后的操作.
后续可以讨论知识图谱如何用3元以上的方法,  比如5元组,来更精细刻画,和知识图谱里面的知识如何扩充的问题.
'''





'''
root----------找动词,
逆向找ner到root的一条线路,进行跳转.

bfs
'''







