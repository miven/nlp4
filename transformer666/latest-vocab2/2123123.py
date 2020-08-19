
src_seq=[[1,2,6565,7, 6565,4,6565,7],[2,4,897,3]]
tgt_seq=[[1,2],[2,4]]
left=[6565,7]
right=[2]

for i1, (a, b) in enumerate(zip(src_seq, tgt_seq)):
    find_left_index = [i for i in range(len(a)) if a[i:i + len(left)] == left]
    find_right_index = [i for i in range(len(b)) if b[i:i + len(right)] == right]
    alldexleft = []
    alldexright = []
    for i in find_left_index:
        for j in range(len(left)):
            alldexleft.append(i + j)
    for i in find_right_index:
        for j in range(len(right)):
            alldexright.append(i + j)
    # alldexright = [range(i, i + len(left)) for i in find_right_index]
    print(i1,'3333333333333333')
    print(alldexleft, alldexright)