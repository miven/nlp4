import json
import gevent.monkey
import requests
from flask import app

gevent.monkey.patch_all()
# 跨域
from flask_cors import CORS


from flask import Flask
#创建app应用,__name__是python预定义变量，被设置为使用本模块.
app = Flask(__name__)
#如果你使用的IDE，在routes这里会报错，因为我们还没有创建呀，为了一会不要再回来写一遍，因此我先写上了

from flask import send_from_directory, request, send_file, jsonify


# 这个接口使用方法: postman里面 body---form-data----key里面类型选file--value选文件即可.
@app.route('/1', methods=['POST', 'GET'])
def upload44():
            name2 = request.args['par']+"___b"  # 获取参
            # 数的方法
            tmp = requests.get("http://127.0.0.1:33/2" ,params={'par':name2})
            return tmp.content


if __name__ == '__main__':
    app.run('127.0.0.1',
           34,
            )


    #  直接 curl 127.0.0.1:33/1?par=23213123 即可.