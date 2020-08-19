from ltp import LTP

ltp = LTP()
text='我现在在天津,我想知道这里的大学都有什么学校.'
seg, hidden = ltp.seg([text])
sdp = ltp.sdp(hidden, graph=False)

print(seg,"seg")
pos = ltp.pos(hidden)
ner = ltp.ner(hidden)
print("ner",ner)
srl = ltp.srl(hidden)
dep = ltp.dep(hidden)
sdp = ltp.sdp(hidden)



seg=seg[0]
for i in sdp[0]:

    print(i, seg[i[0]-1], seg[i[1]-1]) # 注意下标会多一个, 箭1后为真正下标.



