b1=b'\x80\x03cphe.paillier\nPaillierPublicKey\nq\x00)\x81q\x01}q\x02'
s1='sag'
print(type(b1),type(s1))#<class 'bytes'> <class 'str'>

s2=s1.encode('utf8')#str按utf8的方式编码成bytes
print(type(s2))#<class 'bytes'>
# tmp=b1.decode('unicode').encode('utf-8')
# print(tmp)

import struct
tmp=struct.pack('8s',b1)


print(tmp)