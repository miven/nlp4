with open('1') as f:
    tmp=f.readlines()
    print(tmp)
    tmp=[i for i in tmp if '$TRANSFORM'in i]
    print(111111111)