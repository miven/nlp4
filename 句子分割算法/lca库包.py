from LAC import LAC

# 装载分词模型
lac = LAC(mode='seg')

# 单个样本输入，输入为Unicode编码的字符串


# 批量样本输入, 输入为多个句子组成的list，平均速率会更快
texts = [u"LAC是个优秀的分词工具", u"百度是一家高科技公司",'泰坦尼克号是一个好电影']
seg_result = lac.run(texts)


print(seg_result)
'''
https://github.com/baidu/lac         百度开源的lac库包.
'''




# 装载LAC模型
lac = LAC(mode='lac')

# 单个样本输入，输入为Unicode编码的字符串


# 批量样本输入, 输入为多个句子组成的list，平均速率更快

lac_result = lac.run(texts)


print(lac_result)






