import os
tex='445'



def getTrueAdd(tex) :
    return os.path.abspath(tex)


def getTmpLayerAddress(tex) :
    out = []
    # 下面一行是真正地址.

    for i in os.listdir(tex) :
        tmp=tex+'/'+i

        if os.path.isfile(tmp) :
            out.append(tmp)
        else :
            out += getTmpLayerAddress(tmp)
    return out





f1 = open('21212.py', encoding='utf-8')
f1 = f1.readlines()
with open('tmpfile999', 'w') as f :
    for i in f1 :
        f.write(i)







