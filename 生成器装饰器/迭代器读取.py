def bylineread(fimename,batchsize=1):
    batchsize=batchsize
    with open(fimename) as f:

        cnt=0
        out=[]
        line = f.readline()
        while line:

            out.append(line)
            cnt+=1
            if cnt==batchsize:
               yield out
               out=[]
               cnt=0
            line = f.readline()
        yield out  # 用来强制返回最后不成batch的数据.

#read是一个生成器对象
read = bylineread('1',batchsize=2)
while 1:
    try:
        print(next(read))
    except:
        print('over')
        break
