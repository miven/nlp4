'''
https://blog.csdn.net/xixiaoyaoww/article/details/104548745/

'''
# 首先是简历字典.




import re, collections
def get_stats(vocab):
    pairs = collections.defaultdict(int)
    for word, freq in vocab.items():
     symbols = word.split()
     for i in range(len(symbols)-1):
        pairs[symbols[i],symbols[i+1]] += freq
    return pairs
def merge_vocab(pair, v_in):
    v_out = {}
    bigram = re.escape(' '.join(pair))
    p = re.compile(r'(?<!\S)' + bigram + r'(?!\S)')
    for word in v_in:
       w_out = p.sub(''.join(pair), word)
       v_out[w_out] = v_in[word]
    return v_out
vocab = {'l o w </w>' : 5, 'l o w e r </w>' : 2,
'n e w e s t </w>':6, 'w i d e s t </w>':3}
num_merges = 10
out=[]
for i in range(num_merges):
    pairs = get_stats(vocab)
    best = max(pairs, key=pairs.get)
    vocab = merge_vocab(best, vocab)
    out.append(''.join(best))
    print(best)
print("last23",out)

outreverse=out[::-1]

def encode(str2):
    #算法在out中从后往前找.尽量匹配后面的.因为后面的更可能整体切到,如果发生错误进行回溯,再找其他解.
    # 如果都没找到就返回unk-----------下面的写法不对.
    if str2=='':
        return 0
    for i in outreverse:
        if str2[:len(i)]==i:
            return encode(str2[len(i):])



# print output
# ('e', 's')
# ('es', 't')
# ('est', '</w>')
# ('l', 'o')
# ('lo', 'w')
# ('n', 'e')
# ('ne', 'w')
# ('new', 'est</w>')
# ('low', '</w>')
# ('w', 'i')
# ('wi', 'd')
# ('wid', 'est</w>')
# ('low', 'e')
# ('lowe', 'r')
# ('lower', '</w>')




def encode(str,vocab):
    pass







