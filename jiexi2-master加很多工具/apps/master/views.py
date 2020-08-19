from django.shortcuts import render, HttpResponse
from django.views import View

# Create your views here.

'''

用replace in path 删除全部p4rint

替换为空

nohup python manage.py runserver 0:8089 &


2019-08-19,18点58
https://www.jianshu.com/p/2897b7f4da76
让jieba不打印日志

只有不打日志,才能无shell跑.




#################1111111
'''
import time
import json

class DocTokenizerService(View):
    '''
    做轮询,需要用类方法,来做sigliton,
    pycharm 的编码问题,这个项目所有文件用utf-8书写,遇到gbk的点右下角,改成utf-8然后点convert.
    '''
    import configparser

    config = configparser.ConfigParser()
    config.read('properties.conf')
    lists_header = config.sections()


    tmp = config['ports']['ports']


    tmp = tmp.split(' ')
    ports = [i for i in tmp] #ports是一个类变量.
    count=0
    def __init__(self):
            pass

    def get(self, request):

        return HttpResponse("GET method from DocTokenizerService")
    @classmethod
    def post( self,request):
        import time
        start=time.time()

        '''
        解决并发!!!!!!!!!!!!!2019-11-14,16点29
        
        
        因为多人访问时候会被别的进程清楚save9999文件夹.所以需要做时间错和rand
        让只有进程自己有权利删除.
        '''

        import time
        a = (int(time.time()))
        import random
        b = (random.randint(1, 10000))
        print(a * b)
        weiyibiaoshi=a
        weiyibiaoshi=str(weiyibiaoshi)





        '''
        发送请求到子服务器上

        :param request:
        :return:
        '''



        ports=DocTokenizerService.ports #类变量要用类来调用
        dex=DocTokenizerService.count%len(ports)


        DocTokenizerService.count+=1
        #下面发送请求到子服务上.

        import requests

        '''
        因为这个master是发送请求的.所以需要设置发送次数.不然链接多次会
        Max retries exceeded with url
        解决就是设置下面一行的参数.
        '''
        requests.adapters.DEFAULT_RETRIES = 2

        '''
        处理url先要进行trim操作
        '''
        try :

            '''
            处理url先要进行trim操作
            '''
            tmp2 = request.POST.get('url')
            tmp2=tmp2.strip()
            data = request.POST.copy()
            data['url'] = tmp2
            request.POST = data



            from urllib.request import quote, unquote
            tmp2 = unquote(tmp2)


        except :
            import sys
            import json
            info_dict = {}
            info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
            info_dict['error message'] = info
            info_dict['create_at'] = str(time.ctime())
            return HttpResponse(json.dumps(info_dict))











        import logging as log

        '''
        改成critical,不要写入过多信息.上线就用这个配置.提高性能.
        '''


        log.basicConfig(level=log.CRITICAL,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        handlers={

                            log.FileHandler(filename='rizhi.log', mode='a', encoding='utf-8')

                        })


        log.info("当前数据传入的url是",str(tmp2))

        #往屏幕输出
        # log.setLevel(log.INFO)
        # format = log.Formatter(self.format, datefmt=self.datefmt)
        # # 日志输出到文件
        # file_handler = log.FileHandler(self.filename)
        # file_handler.setLevel(log.INFO)
        # file_handler.setFormatter(format)
        # # 使用StreamHandler输出到屏幕
        # console = log.StreamHandler()
        # console.setLevel(log.INFO)
        # console.setFormatter(format)
        # # 添加两个Handler
        # log.addHandler(file_handler)
        # log.addHandler(console)



        if  tmp2.split('.')[-1] in ['zip','rar']:






            url = "http://localhost:"+DocTokenizerService.ports[dex]+'/'+'package'



            r = requests.get(tmp2)

            print(r,"r的内容是!!!!!!!!!!!!!!")
            print(type(r),"r的类型是")


            import os
            #如果之前步奏建立了文件夹,但是后面删除没有运行的话,就会有陈余的目录产生.
            if os.path.exists('saveFile9999999'+weiyibiaoshi) :
                os.system("rm -rf   " + 'saveFile9999999'+weiyibiaoshi)
            if not os.path.exists('saveFile9999999'+weiyibiaoshi) :
                os.mkdir('saveFile9999999'+weiyibiaoshi)
            houzui = tmp2.split('.')[-1]

            mingzi = tmp2.split('/')[-1]
            mingzi = mingzi.split('.')[-2]

            with open('./saveFile9999999'+weiyibiaoshi+'/' + mingzi + '.' + houzui, "wb") as f :  # 这里面补上后缀名

                f.write(r.content)

            os.system('cp '+ './saveFile9999999'+weiyibiaoshi+'/' + mingzi + '.' + houzui+' /tmp/999.rar')
            print(33333333333333333333333333333333)
            print(type(r.content),"99999999999")
            print(r,"9999999999121212")

            '''
            利用copy就可以修改url了. 先copy再修改再赋值回去,即可.
            '''
            data = request.POST.copy()
            data['url'] = './saveFile9999999'+weiyibiaoshi+'/' + mingzi + '.' + houzui
            request.POST = data

            '''
            django 修改request.get或request.post提示：This QueryDict instance is immutable
            '''







            res = requests.post(url=url, data=request.POST)  # 这里使用post方法，参数和get方法一样











            '''
            加字段
            '''
            #注意字典是一个对象


            try:
                tmp = res.json()
            except:
                tmp=res.json("Fail")
            for i in tmp:
                i['foreverStatus'] = 1

            import json



            tmp = json.dumps(tmp)
            res = tmp





        else:
            url = "http://localhost:"+DocTokenizerService.ports[dex]+'/'+'single'


            '''
            如果是html那么不用保存了,直接解析
            '''

            if tmp2.split('.')[-1]=='html':

                res = requests.post(url=url, data=request.POST)  # 这里使用post方法，参数和get方法一样



                '''
                加一个字段
                '''

                tmp = res.json()

                tmp['foreverStatus'] = 1
                import json
                tmp = json.dumps(tmp)
                res = tmp
                log.info("接口" + DocTokenizerService.ports[dex] + "返回的是")
                '''
                不删除了,因为每一次覆盖,占用不了太大硬盘,buxign 
                '''
                import os
                if os.path.exists('saveFile9999999'+weiyibiaoshi) :
                    os.system("rm -rf   " + 'saveFile9999999'+weiyibiaoshi)

                return HttpResponse(tmp)  # 注意这个地方的bug地方,res打印类型是response但是直接返回不行,需要再套一层菜心 ..





            #tmp2


            r = requests.get(tmp2)

            import os
            if os.path.exists('saveFile9999999'+weiyibiaoshi) :
                os.system("rm -rf   " + 'saveFile9999999'+weiyibiaoshi)
            if not os.path.exists('saveFile9999999'+weiyibiaoshi) :
                os.mkdir('saveFile9999999'+weiyibiaoshi)
            houzui=tmp2.split('.')[-1]


            mingzi=tmp2.split('/')[-1]
            mingzi=mingzi.split('.')[-2]




            with open('./saveFile9999999'+weiyibiaoshi+'/'+mingzi+'.'+houzui, "wb") as f :  #这里面补上后缀名

                f.write(r.content)

            '''
            利用copy就可以修改url了. 先copy再修改再赋值回去,即可.
            '''
            data = request.POST.copy()
            data['url']='./saveFile9999999'+weiyibiaoshi+'/'+mingzi+'.'+houzui
            data['weiyibiaoshi']=weiyibiaoshi
            request.POST=data

            '''
            django 修改request.get或request.post提示：This QueryDict instance is immutable
            '''









































            #
            #
            # log.info("发送之前")#数据在requst.POST里面
            res = requests.post(url=url,data=request.POST,)  # 这里使用post方法，参数和get方法一样




            '''
            加一个字段
            '''





            tmp=res.json()

            tmp['foreverStatus']=1
            import json
            tmp=json.dumps(tmp)
            res=tmp
            # log.info("接口"+DocTokenizerService.ports[dex]+"返回的是")
            '''
            不删除了,因为每一次覆盖,占用不了太大硬盘,buxign 
            '''
            if  os.path.exists('saveFile9999999'+weiyibiaoshi):
                os.system("rm -rf   "+'saveFile9999999'+weiyibiaoshi )
        if  os.path.exists('saveFile9999999'+weiyibiaoshi):
            os.system("rm -rf   "+'saveFile9999999'+weiyibiaoshi )



        import time

        # log.critical("接口" + DocTokenizerService.ports[dex] + "返回的数据")
        print(tmp,"返回结果!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        return HttpResponse(tmp)#注意这个地方的bug地方,res打印类型是response但是直接返回不行,需要再套一层菜心 ..
