from pyhanlp import *
print(HanLP.segment("今天开心了吗？"))



'''
安装方法: 
pip pyhanlp 
yum java
'''








from pyhanlp import *
sentence = "下雨天地面积水"

# 返回一个list，每个list是一个分词后的Term对象，可以获取word属性和nature属性，分别对应的是词和词性
terms = HanLP.segment(sentence )
for term in terms:
	print(term.word,term.nature)

#--------------------核心!!!!!!!!!!!






# text='姚明的妻子的丈夫的妻子'
# text='我现在在天津,这里有什么大学?'
text='天津最好的治疗骨科的大夫是谁'
# text='天津的医院'
# text='姚明可以吃吗'
# text='黄瓜的烹饪方法'
# text='决明子的烹饪方法'          #  决明子---------烹饪方法
# text='姚明的妻子'
text='泰坦尼克号的导演'
from pyhanlp import *
tmp=HanLP.parseDependency(text)


print(tmp)

'''
感觉也不咋滴, 还不如ltp呢.
'''



