truedata = []
falsedata = []
with open('gra_evaldata',encoding='utf-8') as f:
    tmp = f.readlines()
    for i in tmp:
        a, b, c = i.split('|')
        truedata.append(c)
        falsedata.append(b+'\n')



with open('truedata', 'w',encoding='utf-8') as f:
    f.writelines(truedata)


with open('falseShuju', 'w',encoding='utf-8') as f2:
    for i in falsedata:
        f2.write(i)
