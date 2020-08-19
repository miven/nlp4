import json
import gevent.monkey
import requests
from flask import app
'''
https://blog.csdn.net/weixin_44002829/article/details/99709232






'''
gevent.monkey.patch_all()
# 跨域
from flask_cors import CORS


from flask import Flask
#创建app应用,__name__是python预定义变量，被设置为使用本模块.
app = Flask(__name__)
#如果你使用的IDE，在routes这里会报错，因为我们还没有创建呀，为了一会不要再回来写一遍，因此我先写上了

from flask import send_from_directory, request, send_file, jsonify


# 这个接口使用方法: postman里面 body---form-data----key里面类型选file--value选文件即可.


import numpy as np
from sklearn.datasets import load_diabetes

# import phe as paillier


# keypair = paillier.generate_paillier_keypair(n_length=1024)
# pubkey, privkey = keypair

#
#
# import pickle
# pub=pickle.dumps(pubkey)
# print(33333333,pub)
# import sys
# print(sys.getdefaultencoding())
# pub=str(pub)
# print(44444444,pub)

# b1=b'\x80\x03cphe.paillier\nPaillierPublicKey\nq\x00)\x81q\x01}q\x02'
# s1='sag'
# print(type(b1),type(s1))#<class 'bytes'> <class 'str'>
#
# s2=s1.encode('utf8')#str按utf8的方式编码成bytes
# print(type(s2))#<class 'bytes'>
# tmp=b1.decode('unicode').encode('utf-8')
# print(tmp)

# import struct
# aaa=struct.pack('8s',b1)
import pickle
import torch
# print(aaa,56756756756765756756)
@app.route('/1', methods=['POST', 'GET'])
def upload44():
            # name2 = request.args['par']+"___a1"  # 获取参数的方法
            tmp = request.files['f'].read()

            print(tmp)
            print(type(tmp))
            print(pickle.loads(tmp))
            return tmp
@app.route('/2', methods=['POST', 'GET'])
def upload44222():
            name2 = request.args['par']+"___a2"  # 获取参数的方法

            return name2

if __name__ == '__main__':
    app.run('127.0.0.1',
           34,
            )


    #  直接 curl 127.0.0.1:33/1?par=23213123 即可.