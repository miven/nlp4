
class a():
    i1=3

a=[a(),a(),a()]
for i in a:
    i.i1=34
print(a[0].i1)