
# 下面开始正式代码

import json
import os

from flask_wtf import FlaskForm
from wtforms import SubmitField

from app import create_app, Users
# debug走一遍流程还是必须的.

# 从app/config.py读取配置文件.
from app.auth.auths import Auth


# 创建表格、插入数据

from run import app


from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask import send_from_directory, request, send_file, jsonify


from  demo.parse_book import parse_book
from otherAlgorithm.demo.bin.sentence_align import pageToSentences
@app.route('/api/fun3', methods=['GET'])
def fun1223():
    return "model"


# 这个接口使用方法: postman里面 body---form-data----key里面类型选file--value选文件即可.
@app.route('/api/upload3', methods=['POST', 'GET'])
def upload44322():


    # 下面这一段是通用的.
        result = Auth.identify(Auth, request)
        print(898989898989,result)


        if not result["status"]:
            return jsonify({"status":401})
        if result["status"]:
            username2id=result['data']
            # 因为是类函数所以第一个参数传入这个类他自己.
            user = Users.get( Users,result['data'])
            print(66666,user.username)
            wenjianjia=user.username




            f = request.files
            #http://www.voidcn.com/article/p-hfxcccsv-btt.html
            print(7777777777777,f)
            print(7777777777777,f.values())
            k=f.getlist('file')
            changdu=len(k)
            print(k)
            num=0
            for i in k:
                print(i)
                print(type(i))
        # 先获取文件的名字.
                print(1111111111111,i.filename)
                name2=i.filename.split('.')[-2]+'.json'
                basepath = os.path.dirname(__file__)  # 当前文件所在路径
                upload_path = os.path.join(basepath, '/uploads')  #注意：没有的文件夹一定要先创建，不然会提示没有该路径
                if not os.path.exists(r"uploads/"+wenjianjia):
                    os.mkdir(r"uploads/"+wenjianjia)
                pa34=r"uploads/"+wenjianjia+r"/"+name2
                # i.save(pa34)   # 带字符串的一定要前面写上r.这样少了很多转义字符,方便多了!!!!!!!!!!!!!11
                num+=parse_book(i,pa34) # 这里面有保存代码
                print(name2)












    # 下面这一段是通用的.
        result = Auth.identify(Auth, request)
        print(898989898989,result)


        if not result["status"]:
            return jsonify({"status":401})
        if result["status"]:
            username2id=result['data']
            # 因为是类函数所以第一个参数传入这个类他自己.
            user = Users.get( Users,result['data'])
            print(66666,user.username)
            wenjianjia=user.username+"_juzifenxi"  # 这里规定带有这个后缀的是句子,不带的是篇章




            f = request.files
            #http://www.voidcn.com/article/p-hfxcccsv-btt.html
            print(7777777777777,f)
            print(7777777777777,f.values())
            k=f.getlist('file')
            changdu=len(k)
            print(k)
            num=0
            for i in k:
                print(i)
                print(type(i))
        # 先获取文件的名字.
                print(1111111111111,i.filename)
                name2=i.filename.split('.')[-2]+'.json'
                basepath = os.path.dirname(__file__)  # 当前文件所在路径
                upload_path = os.path.join(basepath, '/uploads')  #注意：没有的文件夹一定要先创建，不然会提示没有该路径
                if not os.path.exists(r"uploads/"+wenjianjia):
                    os.mkdir(r"uploads/"+wenjianjia)
                pa34=r"uploads/"+wenjianjia+r"/"+name2
                # i.save(pa34)   # 带字符串的一定要前面写上r.这样少了很多转义字符,方便多了!!!!!!!!!!!!!11
                pageToSentences(i,pa34) # 这里面有保存代码
                print("句子解析的结果!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print("保存在",pa34)
                print(name2)

            return "成功完成"+str(changdu)+"个文件的句子对齐任务"
        return  "bug"













# 下面做一个jiexi函数.输入文件,输出解析的json,返回给浏览器下载.
# 参数是file, 然后value 是要下载的文件名称.就能下载了.
@app.route('/api/jiexi3', methods=['POST', 'GET'])
def upload2223():
    # 下面这一段是通用的.
    result = Auth.identify(Auth, request)
    print(898989898989,result)


    if not result["status"]:
        return jsonify({"status":401})
    if result["status"]:
        username2id=result['data']
        # 因为是类函数所以第一个参数传入这个类他自己.
        user = Users.get( Users,result['data'])
        print(66666,user.username)
        wenjianjia=user.username+"_juzifenxi"  # 这里规定带有这个后缀的是句子,不带的是篇章





        name2=request.args['file']  # 获取参数的方法
        print(111111111111111111111111,name2)
       # 为什么目录跳了一级???
       #  return send_file(r"..\uploads\fuck222.png")
       #  return send_file(r"..\uploads\1_abs.txt")
       # attachment_filename	the filename for the attachment if it differs from the file’s filename.



        tmp=send_from_directory(r"../uploads/"+wenjianjia, filename=name2+".json" ,as_attachment=True)
        print(tmp)
        print(type(tmp))
        print(tmp.headers)
        # 下面这段是修改header的方法.!!!!!!!!!!!!!!!!!!!!!!
        #<class 'werkzeug.datastructures.Headers'>  看源码
        print(type(tmp.headers))
        print("45645645",tmp.headers)
        tmp.headers.add('Content-Type', 'application/octet-stream')

        return tmp









# 可以了,上传下载都可以了
        return send_from_directory(r"../uploads/"+wenjianjia, filename=name2+".json" ,as_attachment=True)







# 这个接口是前端传json,然后我保存到后端.



# 这个用来测试save接口







@app.route('/api/save3', methods=['POST', 'GET'])
def upload454232():
    # 下面这一段是通用的.
    result = Auth.identify(Auth, request)
    print(898989898989,result)


    if not result["status"]:
        return jsonify({"status":401})
    if result["status"]:
        username2id=result['data']
        # 因为是类函数所以第一个参数传入这个类他自己.
        user = Users.get( Users,result['data'])
        print(66666,user.username)
        wenjianjia=user.username+"_juzifenxi"  # 这里规定带有这个后缀的是句子,不带的是篇章






        data = request.get_json()
        print(data)
        print(data['filename'])
        print(data['data'])
        print(data['page'])


        import json
        # print(json.load(r"uploads/"+wenjianjia+r'/'+data['filename']+".json",ensure_ascii=False))
        print(99999999999999999999999999999)
        with open(r"uploads/"+wenjianjia+r'/'+data['filename']+".json", 'r', encoding='utf-8') as f:

            # print(f)
            tmp= json.load(f)
            # print(8888888888,tmp)
            # json.dump(data['data'], f, ensure_ascii=False)
            print(999999999333333333333333)
        tmp[data['page']-1]=data['data']
        # print(tmp[data['page']])

        with open(r"uploads/" + wenjianjia + r'/' + data['filename'] + ".json", 'w', encoding='utf-8') as f:
            json.dump(tmp, f, ensure_ascii=False)




        return r'json保存到服务器了'


# 用户离开界面的时候触发这个.保存用户的环境.  前端先调用save,把用户的数据都存到服务器.
# 然后再给调用baocun接口.保存用户的环境.
# 这个接口返回上次用户离开时后的状态.  返回需要恢复的json数据.

# user.param1  就用来保存用户的篇章对齐的下次需要回复的那些文章.

from app import db
@app.route('/api/baocun3', methods=['POST', 'GET'])
def upload454666232():
    # 下面这一段是通用的.
    result = Auth.identify(Auth, request)
    print(898989898989,result)


    if not result["status"]:
        return jsonify({"status":401})
    if result["status"]:
        username2id=result['data']
        # 因为是类函数所以第一个参数传入这个类他自己.
        user = Users.get( Users,result['data'])
        print(66666,user.username)
        wenjianjia = user.username + "_juzifenxi"  # 这里规定带有这个后缀的是句子,不带的是篇章


        #
        # wenjianjia = user.username
        #
        #
        # data = request.get_json()
        # print(data)
        # print(data['filename'])
        # print(data['data'])
        # import json
        # with open(r"uploads/"+wenjianjia+r'//'+data['filename']+".json", 'w', encoding='utf-8') as f:
        #     json.dump(data['data'], f, ensure_ascii=False)


        return r'环境保存到服务器额数据库了'






# 从文件把读取的json数据也返回去.

from app import db
@app.route('/api/huifu3', methods=['POST', 'GET'])
def upload454666388822():
    # 下面这一段是通用的.
    result = Auth.identify(Auth, request)
    print(898989898989,result)


    if not result["status"]:
        return jsonify({"status":401})
    if result["status"]:
        username2id=result['data']
        # 因为是类函数所以第一个参数传入这个类他自己.
        user = Users.get( Users,result['data'])
        print(66666,user.username)
        wenjianjia = user.username + "_juzifenxi"  # 这里规定带有这个后缀的是句子,不带的是篇章




        username2id = result['data']
        # 因为是类函数所以第一个参数传入这个类他自己.
        user = Users.get(Users, result['data']) # result['data'] 表示的是用户id号.
        print(66666, user.username)
        print(66666, user.param1) # 把所有需要保存的文件名放入param1里面
        print(type(user.param1))
        import json
        a=json.loads((user.param1))  # 通过loads读取json字符串
        print(888888,a)
        fanhui={}
        print("zonggiongshi j",a)
        for i in a:

            iii=r"uploads/"+user.username+r'/'+i+".json"
            print(iii)
            with open(iii,encoding='utf-8') as i2:

                import json
                tmp=json.load(i2)
                fanhui[i]=tmp
                print(i)
        print(len(fanhui))
        print(fanhui.keys())
        print(fanhui['古文观止2'])




        #
        # wenjianjia = user.username
        #
        #
        # data = request.get_json()
        # print(data)
        # print(data['filename'])
        # print(data['data'])
        # import json
        # with open(r"uploads/"+wenjianjia+r'//'+data['filename']+".json", 'w', encoding='utf-8') as f:
        #     json.dump(data['data'], f, ensure_ascii=False)


        return jsonify(fanhui)







@app.route('/api/chakan3', methods=['POST', 'GET'])
def upload2222322():
    # 下面这一段是通用的.
    result = Auth.identify(Auth, request)
    print(898989898989,result)


    if not result["status"]:
        return jsonify({"status":401})
    if result["status"]:
        username2id=result['data']
        # 因为是类函数所以第一个参数传入这个类他自己.
        user = Users.get( Users,result['data'])
        print(66666,user.username)
        wenjianjia = user.username + "_juzifenxi"  # 这里规定带有这个后缀的是句子,不带的是篇章





        name2=request.args['file']  # 获取参数的方法
        page2=request.args['page']  # 获取参数的方法
        page2=int(page2)
        print(111111111111111111111111,name2)
       # 为什么目录跳了一级???
       #  return send_file(r"..\uploads\fuck222.png")
       #  return send_file(r"..\uploads\1_abs.txt")
       # attachment_filename	the filename for the attachment if it differs from the file’s filename.
# 可以了,上传下载都可以了
        with open(r"uploads/"+wenjianjia+r'/'+name2+".json",encoding='utf-8') as f:
           tmp=json.load(f)
        # print("111111111111111111111111",tmp)
        # print(22222222222222,page2)
        # print(tmp[page2-1])
        tmp3=tmp[page2-1]
        # print(tmp)
        # print(type(tmp),343434343)
        # tmp2={'data':tmp}
        # # tmp2=jsonify(tmp2)
        # print(9999999999)
        # print(tmp2['data'][0])
        tmp3['totalpage']=len(tmp)
        return   jsonify(tmp3)





@app.route('/api/liebiao3', methods=['POST', 'GET'])
def upload22222322222():
    # 下面这一段是通用的.
    result = Auth.identify(Auth, request)
    print(898989898989,result)


    if not result["status"]:
        return jsonify({"status":401})
    if result["status"]:
        username2id=result['data']
        # 因为是类函数所以第一个参数传入这个类他自己.
        user = Users.get( Users,result['data'])
        print(66666,user.username)
        wenjianjia = user.username + "_juzifenxi"  # 这里规定带有这个后缀的是句子,不带的是篇章




        if not os.path.exists(r"uploads/" + wenjianjia):
            return jsonify([])




        tmp=os.listdir(r"uploads/"+wenjianjia)
        tmp2=[]
        for i in tmp:
            tmp2.append(i.split('.')[-2])
        print(tmp2)



        # name2=request.args['file']  # 获取参数的方法
        # print(111111111111111111111111,name2)
       # 为什么目录跳了一级???
       #  return send_file(r"..\uploads\fuck222.png")
       #  return send_file(r"..\uploads\1_abs.txt")
       # attachment_filename	the filename for the attachment if it differs from the file’s filename.
# # 可以了,上传下载都可以了
#         with open(r"uploads/"+wenjianjia+r'/'+name2+".json",encoding='utf-8') as f:
# #            tmp=json.load(f)
        # print(tmp)
        # print(type(tmp),343434343)
        # tmp2={'data':tmp}
        # # tmp2=jsonify(tmp2)
        # print(9999999999)
        # print(tmp2['data'][0])

        return   jsonify(tmp2)




@app.route('/api/delete3', methods=['POST', 'GET'])
def upload2222223223():
    # 下面这一段是通用的.
    result = Auth.identify(Auth, request)
    print(898989898989,result)


    if not result["status"]:
        return jsonify({"status":401})
    if result["status"]:
        username2id=result['data']

        beidelete = request.args['delete']  # 获取参数的方法
        # 因为是类函数所以第一个参数传入这个类他自己.
        user = Users.get( Users,result['data'])
        print(66666,user.username)
        wenjianjia=user.username+ "_juzifenxi"



        if not os.path.exists(r"uploads/" + wenjianjia):
            return jsonify([])

        os.remove(r"uploads/" + wenjianjia+'/'+str(beidelete))



        tmp=os.listdir(r"uploads/"+wenjianjia)
        tmp2=[]
        for i in tmp:
            tmp2.append(i.split('.')[-2])
        print(tmp2)



        # name2=request.args['file']  # 获取参数的方法
        # print(111111111111111111111111,name2)
       # 为什么目录跳了一级???
       #  return send_file(r"..\uploads\fuck222.png")
       #  return send_file(r"..\uploads\1_abs.txt")
       # attachment_filename	the filename for the attachment if it differs from the file’s filename.
# # 可以了,上传下载都可以了
#         with open(r"uploads/"+wenjianjia+r'/'+name2+".json",encoding='utf-8') as f:
# #            tmp=json.load(f)
        # print(tmp)
        # print(type(tmp),343434343)
        # tmp2={'data':tmp}
        # # tmp2=jsonify(tmp2)
        # print(9999999999)
        # print(tmp2['data'][0])

        return   jsonify(tmp2)