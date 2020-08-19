from django.shortcuts import render, HttpResponse
from django.views import View
# Create
# your views here.
import os
import sys

sys.path.append('..')
sys.path.append('../')
sys.path.append('..')
'''
这个接口处理package情况
'''
from word2vec2 import views
import word2vec2
import jieba
import logging
jieba.setLogLevel(logging.INFO)

class Word2VecService(View) :

    def get(self, request) :
        '''
        打包上传

        :param request:
        :return:
        '''

        return HttpResponse("GET Service From Word2VecService")

    def post(self, request) :
        '''
        打包上传

        :param request:
        :return:
        '''

        '''
        发现用库包解压会乱码,所以调用linx 命令
        先写本地把.
        '''
        pack = request.POST.get('url')  # POST必须大写

        '''
        建立文件夹.让他跟同级文件夹永远不重名.
        还是用时间错,重码率最低,因为这个整数足够大
        '''
        import time
        import os
        FileName = int(time.time()) * 1000
        FileName = str(FileName)
        liebiao = os.listdir()

        # FileName='tmpDatabyzncs'
        while 1 :
            if FileName not in liebiao :
                break
            FileName = FileName + "1"
        FileName="TMPFiledirectory99999"#还是用固定名字好维护吧.

        if pack.split('.')[-1] == 'zip' or pack.split('.')[-1] == 'rar' :


            import os
            import subprocess


            '''
            处理一下目录文件名的问题:
            用时间错,循环判断当前文件夹里面文件夹的名字,如果崇明时间错+1.循环下去.直到找到不重名的.
            '''


            import zipfile
            if os.path.exists(FileName):
                try:
                    os.remove(FileName)
                except:
                    os.system("rm -rf   " + FileName) #还是linux 命令给力!!!!!!!!!!!!
                finally:
                    pass
            if pack.split('.')[-1] == 'zip' :

                # os.system("mkdir test")经过这个测试发现是在当前目录.也就是代码运行时候的目录,不是这个.py的目录
                # 是调用python xxx.py时候的目录.
                # os.system("unzip -d   "+FileName+" -u "+pack) #解压到当前tmp目录  #这个参数必须用-u


                # zipfile.ZipFile(pack).extractall(FileName)

                os.system("unzip -O gbk "+pack+"  -d  "+FileName)












            else :


                os.system("mkdir " + FileName + "  & unrar x -y  " + pack + " ./" + FileName)  # 解压到当前tmp目录



                #下面这一行代码是因为有些软件对于linux 不兼容,那么就用zip来解压rar包即可!!!!!!!!1
                if os.listdir(FileName)==[]:

                    os.system("unzip -O gbk " + pack + "  -d  " + FileName)

                # #这个参数必须用-u


            # 注意目录会按照程序运行时候的目录来算,所以要起一个怪名.
            # import commands

            '''
            下面进行解析
            '''
            tmp = subprocess.getoutput('ls ' + FileName)




            t = os.listdir(FileName)




            '''
            尽量使用os这个,这个模块跨屏他.
            '''
            out = []
            import json
            for i in t :
                # out.append(views.Word2VecService.post1(tex='tmpFileByZhangBo/'+i))

                tmp5=views.Word2VecService().post1(tex=FileName + '/' + i)


                if len(tmp5)==2 and tmp5!={} and tmp5!='{}':#这里面等于2表示返回的是一个tuple,第一个是一个list的结果.
                    #之所以不写>1是因为返回可能是一个字符串类型的字典.json.dumps结果是一个字符串.

                    out+=json.loads(tmp5[0])
                # raise
                else:
                  out.append(tmp5)
                # 调用其他的类的函数,必须要先构造一个对象.



            '''
            直接数组包jason会bug,再load回去
            '''

            out2 = []
            import json
            for i in out :
                if i !=None:
                  out2.append(json.loads(i))

                # tmp = json.loads(i)


            out2 = json.dumps(out2, sort_keys=True, indent=4, ensure_ascii=False)  # dump参数要一直.
            out = out2

            # out=[out]
            # out=out[0]
            '''
            wget https://www.rarlab.com/rar/rarlinux-x64-5.5.0.tar.gz
            装不上去,网速不行.所以就不支持rar了
            已经可以装上了,支持了!






            unrar x *.rar /tmp
            '''

            import json
            os.system("rm -rf   " + FileName)
            # out=json.dump(out)



            # out=[1]

            return HttpResponse(out)


        else :
            return HttpResponse("Fail,Check your File Style")

        return HttpResponse("POST service from Word2VecService")