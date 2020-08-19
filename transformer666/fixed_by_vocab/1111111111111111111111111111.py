# 测试一下读取数据集. train也就3万个句子,很小. 但是nlp任务做基本算法性能测试够了.

with  open('yunixng_bash/data/multi30k/test.en')as f:
    tmp=f.readline()
    print(tmp)