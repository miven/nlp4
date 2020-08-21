from bert_serving.client import BertClient
bc = BertClient()
print(bc.encode(['中国人是天才', '美国']))
print("获得了")# 启用多线程,如果没有服务响应的时候会自动等待,还是符合需求的!!!!!!!!!

# 怀疑底层用的bert 里面的cls编码来表示整个句子的向量表示.所以多长的句子都是768维度.