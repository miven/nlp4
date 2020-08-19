
'''
研究一下pickle数据传输时候的bug!!!!!!!!!!!

'''

import json
# import gevent.monkey
import requests
from flask import app
'''
https://blog.csdn.net/weixin_44002829/article/details/99709232






'''
# gevent.monkey.patch_all()
# 跨域
from flask_cors import CORS


from flask import Flask
#创建app应用,__name__是python预定义变量，被设置为使用本模块.
app = Flask(__name__)
#如果你使用的IDE，在routes这里会报错，因为我们还没有创建呀，为了一会不要再回来写一遍，因此我先写上了

from flask import send_from_directory, request, send_file, jsonify
import struct
import pickle

import torch

# 这个接口使用方法: postman里面 body---form-data----key里面类型选file--value选文件即可.
@app.route('/1', methods=['POST', 'GET'])
def upload44():
            # name2 = request.form.get('pub')  # 获取post参数的方法
            # print(type(name2))
            # name2=struct.unpack('8s',name2)
            # print(name2,66666666666666666666666)
            #
            #
            #
            # print(99999999999999999999999999999999999,tmp)
            name2=torch.tensor([0])
            print(name2,'kaishi11111111111111')

            # print(name2,7777777777777777777)
            name2=pickle.dumps(name2)
            print(type(name2),888888888888888888888888888888888888)
            print(name2)
            # tmp = requests.get("http://127.0.0.1:34/1" ,params={'par':name2})

            html = requests.post('http://127.0.0.1:34/1', files={'f':name2}).text

            print(html)
            return '111111'
@app.route('/2', methods=['POST', 'GET'])
def upload44222():
            name2 = request.args['par']+"___a2"  # 获取参数的方法

            return name2

if __name__ == '__main__':
    app.run('127.0.0.1',
           33,
            )


    #  直接 curl 127.0.0.1:33/1?par=23213123 即可.