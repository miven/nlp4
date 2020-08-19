import codecs
# 从文件读取数据
data = codecs.open("bpe_deen/codes.txt", encoding="UTF-8")
# 一行一行读取数据
data1 = data.readline()
print(data1)
# 度去完数据要把数据对象进行关闭，从内存里面释放出来
data.close()