from django.shortcuts import render, HttpResponse
from django.views import View
# Create your views here.
import numpy as np
import django
import json
from . import check
import pdfplumber
from pydocx import PyDocX
import sys
import datetime
sys.path.append('.')
import gensim
import jieba

from collections import defaultdict
from gensim.models import Word2Vec
import gensim.models.word2vec as w2v
import numpy as np
import os
# import pandas as pd
from pyhanlp import *
# 第一个demo
import numpy as np
from pydocx import PyDocX
import docx
import re
'''
这个文件处理single情况
'''
'''
超参数写这里面
'''
import configparser
import jieba
import logging
jieba.setLogLevel(logging.INFO)
config = configparser.ConfigParser()
config.read('properties.conf',encoding='utf-8')
lists_header = config.sections()  # 配置组名, ['luzhuo.me', 'mysql'] # 不含'DEFAULT'



import urllib

import urllib









class Word2VecService(View):
    '''
    用静态变量来加速.
    把需要读取的文件写到静态变量里面.这样
    每一次建立一个类来跑代码的时候,这些数据都不用重新读取磁盘了.!

    '''



    STOPWORDS=[line.strip() for line in open('chineseStopWord', encoding='UTF-8').readlines()]



    # def get(self, request):

    '''
    C:\policy\policy_files\txt\23页第6.txt

    '''
    def delkongbai(self,tmp):

        tmp = re.sub(r'[:[} \f\r\t\v。]', "", tmp) #去掉没用的空白
        return tmp

    def chaxunshijian(self,tmp) :
        tmp1 = re.search(r'自.*年.*月.*日起.*有效期至.*年.*月.*日', tmp)

        if tmp1 :


            res = re.findall(r'[1-2][0-9]{3} *年 *[0-1]?[0-9] *月[0-3]?[0-9] *日', tmp)
            # res = re.findall('日', tmp)


            if len(res) >= 2 :
                return res
        return None

    def __init__(self):#这里面定义的变量self.都是对象变量,没法用classmethod的方法来访问,所以只能
        #创建对象来访问这个函数.

        # init里面定义一些函数通用的变量,起名为self.XXX 他们作为下面所有函数公共的变量.全局变量.








        import pymysql
        # 连接database
        conn = pymysql.connect(
            host=config['mysql']['ip'],
            port=3306,
            user=config['mysql']['user'],
            password=config['mysql']['password'],
            database=config['mysql']['db'],
            charset="utf8"
        )
        self.conn=conn



        from pymongo import MongoClient
        myclient = MongoClient("mongodb://"+config['mongodb']['ip'],

                               username='root',
                               password='root',

                               maxPoolSize=30000, minPoolSize=8, connectTimeoutMS=30000)
        self.myclient=myclient
        # self.repl_for_zhengcebianhao='[\u4e00-\u9fa5]{1,3}? *发? *?〔[0-9]{4}〕[0-9]*? *号'
        # self.repl_for_zhengcebianhao = '[\u4e00-\u9fa5]{1,3} *发 *(\〔|\[)[0-9]{4}(\]|〕)[0-9]*? *号'
        self.repl_for_zhengcebianhao = '[\u4e00-\u9fa5]{1,4} *发? *(\〔|\[)[0-9]{4}(\]|〕)[0-9]*? *号'
        # self.repl_for_zhengcebianhao = '[\u4e00-\u9fa5]{1,3} *发? *(\〔|\[)[0-9]{4}(\]|〕)[0-9]*? *号'

        self.scoreForTheme=8.0




        '''
        
        串行用时
/data/zb/1.docx :用2.66s返回



        '''
    # @classmethod
    def post1(self, tex,savingTex=None,savingTitle=None,weiyibiaoshi=None):
        #weiyibiaoshi是doc保存docx时候使用.
        repl_for_zhengcebianhao = self.repl_for_zhengcebianhao

        from urllib.request import quote, unquote
        tex = unquote(tex)#解决中文编码问题

        if tex.split('.')[-1] == 'html':

            from bs4 import BeautifulSoup
            import urllib
            '''
            2019-09-23,13点19
处理linux 解析doc的问题:
https://stackoverflow.com/questions/52277264/convert-doc-to-docx-using-soffice-not-working
 
 
具体就是:
1.yum install libreoffice
2.soffice --headless --convert-to docx   2.doc
 

            '''
            def get_content(url):#如果url是网上链接
                try:


                    resp = urllib.request.urlopen(url)

                    html = resp.read()
                    html = (html.replace('<br>', '\n')).replace('<br/>', '\n')

                    #urllib.request.urlopen(url).read()
                    bs = BeautifulSoup(html, "html.parser")

                    return bs.get_text(),bs
                except:#如果url是本地地址.
                    try:
                        htmlfile = open(url, 'r', encoding='utf-8')
                        html = htmlfile.read()
                        html = (html.replace('<br>', '\n')).replace('<br/>', '\n')
                        bs = BeautifulSoup(html, "html.parser")

                        return bs.getText(),bs
                    except:#第三种是假的html,还是需要先下载.
                        import requests


                        r = requests.get(url)

                        with open('laji.html', "wb") as f :  # 这里面补上后缀名
                            f.write(r.content)
                        url='laji.txt'

                        htmlfile = open('laji.html', 'r', encoding='utf-8')
                        html = htmlfile.read()
                        html = (html.replace('<br>', '\n')).replace('<br/>', '\n')
                        bs = BeautifulSoup(html, "html.parser")


                        return bs.getText(),bs


                return bs.get_text(),bs
            tmpnow=get_content(tex)[0]

            tmpnow2=get_content(tex)[1]




            '''
            因为解析之后只有一行的str,效果很差,所以用句号回车替换句号
            '''

            if "。" in tmpnow:
                tmpnow=tmpnow.split('。')
                for i in range(len(tmpnow)):
                    if  tmpnow[i]!='':
                        tmpnow[i]=tmpnow[i]+'。\n'
                if '' in tmpnow:
                   tmpnow.remove('')
            else:
                pass
            tmpnow=tmpnow[:10000]





            '''
            解释一下参数,tmpnow是tex, tmpnow2是html码,tex是地址.
            '''
            return self.util(tex,tmpnow,Forhtml=tmpnow2,savingTex=savingTex)


        if tex.split('.')[-1] == 'txt':

            someList=open(tex,encoding='utf-8').readlines()


            out = self.util(tex, someList)

            return out

        # 下面处理doc问题.
        print(tex,243242)
        if tex.split('.')[-1] == 'docx' or tex.split('.')[-1] == 'doc':

            import requests
            print('duandian 234')
            try:
                if tex.split('.')[-1] == 'doc':
                    import subprocess
                    cmdfasdf='soffice --headless --convert-to docx   '+tex
                    print(cmdfasdf)
                    print(os.getcwd())

                    aaaa=subprocess.getoutput('soffice --headless --convert-to docx  --outdir  '+'./saveFile9999999'+weiyibiaoshi+'/ ' +tex)
                    # print(aaaa)
                    print('转化为docx了')
                    tex=tex  +'x'
                import chardet
                print(11111111111)



                print('duandifan23423423')
                print(tex)
                html = PyDocX.to_html(tex)
                print(html)
                print('duandian')

                name2=tex.split('/')[-1].split('.')[-2]+'.html'
                with open(name2, 'w') as f :
                    f.write(html)

                import docx2txt
                textForLiaoyong = docx2txt.process(tex)
                #用了html转tex,但是效果很差.所以用docx转txt换回.


                tmp= self.post1(name2,savingTex=textForLiaoyong,savingTitle=tex)









                if os.path.exists(name2):
                    os.remove(name2)


                return tmp



            except:
                pass







        if tex.split('.')[-1] == 'pdf':





            path = tex
            pdf = pdfplumber.open(path)
            out = []
            for page in pdf.pages:
                # 获取当前页面的全部文本信息，包括表格中的文字


                # help(page)


                # help(page)

                out.append(page.extract_text())
            inputtex = out


            out = self.util(tex, inputtex)
            return out





        '''
        给出图片支持:
        '''
        if tex.split('.')[-1] == 'png' or tex.split('.')[-1] == 'jpg':
            import pytesseract
            from PIL import Image
            image = Image.open(tex)
            someList = [pytesseract.image_to_string(image, lang='chi_sim')]

            out = self.util(tex, someList)
            return out



        #如果都不是就返回空信息.
        if os.path.isdir(tex):
            '''
            下面用递归来获取所有文件的地址
            '''
            out=[]

            def getTrueAdd(tex) :
                return os.path.abspath(tex)



            def getTmpLayerAddress(tex) :
                out = []
                # 下面一行是真正地址.

                for i in os.listdir(tex) :
                    tmp = tex + '/' + i

                    if os.path.isfile(tmp) :
                        out.append(tmp)
                    else :
                        out += getTmpLayerAddress(tmp)
                return out
            out=getTmpLayerAddress(tex)



            out2 = []

            for i in out :
                # out.append(views.Word2VecService.post1(tex='tmpFileByZhangBo/'+i))

                tmp5=self.post1(tex=i)




                # raise
                out2.append(tmp5)
            # out2 = []
            # import json
            # for i in out :
            #     if i != None :
            #         out2.append(json.loads(i))

                # tmp = json.loads(i)

            out2 = json.dumps(out2, sort_keys=True, indent=4, ensure_ascii=False)  # dump参数要一直.
            out = out2
            return out,"isAlist" #只有这种情况返回一个数组.所以用参数数量来区分.
        else:#如果还有打不开的就用txt强开.
            f1=open(tex, encoding='utf-8')

            f1=f1.readlines()
            with open('tmpfile999.txt','w') as f:
                for i in f1:
                     f.write( i)
            return self.post1('tmpfile999.txt')









        tmp=json.dumps({})


        return json.dumps({})


    def post(self,request):



     return HttpResponse(self.post1(tex=request.POST.get('url'),weiyibiaoshi=request.POST.get('weiyibiaoshi')))







    def get(self, request):

            return HttpResponse("Please Use POST method!!!!!!!")



    '''
    词性表:https://blog.csdn.net/zaishijizhidian/article/details/82828212
    '''
    def checkdizhi(self,input):
        if not input:
            return False
        input = self.delkongbai(input)
        HanLP.Config.ShowTermNature = True
        tmp99 = HanLP.segment(input)
        flag = 0

        for i in tmp99:

            if str(i.nature) in ['nt', 'nis','nto','nit','ni'] :

                return True
                break

        return False
    def checkshijian(self,input):
        input=self.delkongbai(input)

        return re.fullmatch(r'[1-2][0-9]{3}-[0-1]?[0-9]-[0-3]?[0-9]',input)!=None or \
                    re.fullmatch(r'[1-2][0-9]{3}年[0-1]?[0-9]月[0-3]?[0-9]日',input) !=None

    def util(self,tex,someList,Forhtml=None,savingTex=None):

        #python 数组过滤用[i for i in a if i!=2]  这么写!!!!!



        '''


        :param tex:
        :param someList:
        :param Forhtml:
        :param savingTex:
        :return:
        '''



        #对someList重新进行修改拼接:
        tmp68=[]
        for i in someList:
            if '\n' in i:
                tmp68+=i.split('\n')
            else:
                tmp68.append(i)
        someList=tmp68






        #ForhtmlOld 是源html
        ForhtmlOld=Forhtml

        #Forhtml现在是去掉head的html
        from bs4 import BeautifulSoup

        '''
        处理br标签
        '''







        if Forhtml:
           dongxi = Forhtml.select('head')
           [s.extract() for s in Forhtml("head")]#这行去除head标签.

           if len(Forhtml.select('p'))>10000:
                Forhtml=''.join(Forhtml.select('head'),Forhtml.select('p')[:10000])


        # del Forhtml('head')






        #这个预留字段只为了处理html
        repl_for_zhengcebianhao=self.repl_for_zhengcebianhao


        '''
        函数说明,tex是文件地址.someList是一个数组,里面的东西是一堆字符串,代表每一行的str.也就是说
        someList<str>

        如果早知道这些代码可以复用上面会少些很多.

        :param tex:
        :param someList:
        :return:
        '''
        path = tex
        '''
        需要对someList做预处理,去掉/n
        
        '''
        tmp20=[]
        import re
        for i in someList:
                if not re.fullmatch(' *\n',i):
                    tmp20.append(i)
        someList=tmp20

        someList=someList[:10000]
        inputtex = someList






        if savingTex:#表示当前util函数被doc调用.
            inputtex=savingTex.split('\n')

        sys.path.append('.')

        '''
        test

        :return:
        '''

        '''
        下面返回标题.  ZHENGCEMINGCHENG
        '''

        if '/' not in tex:
            if '.' in tex:
                ZHENGCEMINGCHENG = tex.split('.')[0]
            else:
                ZHENGCEMINGCHENG = tex
        else:
            ZHENGCEMINGCHENG = tex.split('/')[-1]
            if '.' in ZHENGCEMINGCHENG:
                ZHENGCEMINGCHENG = ZHENGCEMINGCHENG.split('.')[0]
            else:
                ZHENGCEMINGCHENG = ZHENGCEMINGCHENG

        HanLP.Config.ShowTermNature = False

        CRFnewSegment = HanLP.newSegment("crf")

        import jieba.posseg as pseg
        # tmp = (dirname + '/' + i for i in os.listdir(dirname))
        # tmp = list(tmp)
        tmp = []
        tmp.append(tex)
        texts = []


        '''
        对于关键词,只留名词和动词,去掉数量词
        '''


        if 1:

            stopwords = Word2VecService.STOPWORDS
            stopwords.append('\n')  # 去掉回车字符
            stopwords.append('\u00A0')  # 去掉回车字符
            stopwords.append('\u0020')  # 去掉回车字符
            stopwords.append('\u3000')  # 去掉回车字符
            stopwords.append('万')  # 去掉回车字符
            stopwords.append('元')  # 去掉回车字符

            #

            # seg_list=jieba._lcut("大事发生大放")
            out = []


            for line in inputtex:
                # seg_list = jieba._lcut(line)
                HanLP.Config.ShowTermNature = False
                seg_list = HanLP.segment(line)
                #如果seg_list太大.进行截取操作



                seg_list=list(seg_list)
                seg_list=seg_list[:20000]

                tmp2 = []


                for ii in seg_list:


                    tmp2.append(ii.word)
                seg_list = tmp2


                seg_list = list(seg_list)

                for i in seg_list:
                    if i in stopwords:
                        continue
                    out.append(i)
            outputForhangyexinxi=out
            texts.append(out)

        # 去掉只出现一次的
        # freq=defaultdict(int)

        # for text in texts:
        #     for i in text:
        #         freq[i]+=1
        #





        '''
        算了还是用自带的
        '''

        import jieba.analyse.tfidf as tf
        out2 = jieba.analyse.tfidf(''.join(texts[-1]))


        # TextRankKeyword = JClass("com.hankcs.hanlp.summary.TextRankKeyword")
        # out3=HanLP.extractKeyword(''.join(texts[-1]),5)
        # out3=HanLP.extractKeyword(''.join([i for  i in open(tex,encoding='utf-8').readlines()]),5)

        '''
        根据词性去掉
        '''
        # out2=HanLP.segment(''.join((out2)))
        out3 = []
        for i in out2:

            if str((HanLP.segment(i))[0].nature) in ['a', 'ad','m']:
                continue
            else:
                out3.append(i)



        '''
        根据标题赛选
        '''
        if '/' in tex:
            biaoti = tex.split('/')[-1]
        else:
            biaoti = tex
        out4 = []
        out44 = []
        for i in out3:
            if i in biaoti:
                out4.append(i)
            else:
                out44.append(i)
        out5 = out4 + out44

        KEYWORD = out5


        quchu = []
        for i in range(len(KEYWORD)) :
            for j in KEYWORD[:i] + KEYWORD[i + 1 :] :
                if KEYWORD[i] in j :
                    quchu.append(i)
        KEYWORD3 = []
        for i in range(len(KEYWORD)) :
            if i not in quchu :
                KEYWORD3.append(KEYWORD[i])
        KEYWORD = KEYWORD3

        '''
        第二个函数是获取文档的分类结果
        '''

        # 根据keyword的结果来进行分类
        KEYWORD = KEYWORD[:10]

        from pymongo import MongoClient
        fn = tex
        from pymongo import MongoClient
        from pymongo import InsertOne
        import time

        start = time.time()

        myclient = self.myclient
        # myclient = Connection("mongodb://localhost:27017/")
        mydb = myclient["d1"]
        my_collection = mydb['c6']

        # 得到的东西是一个数组,之后是一个字典.
        time5 = time.time()
        vec1 = my_collection.find_one({'hanzi': '政策'})['bianma']
        vec11 = my_collection.find_one({'hanzi': '政策'})['bianma']
        vec2 = my_collection.find_one({'hanzi': '法律'})['bianma']
        vec22 = my_collection.find_one({'hanzi': '法规'})['bianma']
        vec3 = my_collection.find_one({'hanzi': '公告'})['bianma']
        vec33 = my_collection.find_one({'hanzi': '通知'})['bianma']

        import numpy as np
        import re




        def process(vec1):
            vec1 = str(vec1)

            vec1 = vec1.replace(r'\n', '')

            vec1 = vec1.replace('[', '')

            vec1 = vec1.replace(']', '')

            vec1 = vec1.replace('\'', '')

            vec1 = re.sub('\s+', ' ', vec1)

            vec1 = vec1[1:]




            vec1 = np.fromstring(vec1, dtype=float, sep=',')


            return vec1

        score1 = []
        score2 = []
        score3 = []
        vec1 = process(vec1)
        vec11 = process(vec11)
        vec2 = process(vec2)
        vec22 = process(vec22)
        vec3 = process(vec3)
        vec33 = process(vec33)
        for i in KEYWORD:
            try:
                tmp = my_collection.find_one({'hanzi': i})['bianma']

            except:
                continue
            tmp = process(tmp)







            score1.append(np.dot(tmp, vec1) / (np.linalg.norm(tmp) * np.linalg.norm(vec1)))
            score1.append(np.dot(tmp, vec11) / (np.linalg.norm(tmp) * np.linalg.norm(vec11)))
            score2.append(np.dot(tmp, vec2) / (np.linalg.norm(tmp) * np.linalg.norm(vec2)))
            score2.append(np.dot(tmp, vec22) / (np.linalg.norm(tmp) * np.linalg.norm(vec22)))
            score3.append(np.dot(tmp, vec3) / (np.linalg.norm(tmp) * np.linalg.norm(vec3)))
            score3.append(np.dot(tmp, vec33) / (np.linalg.norm(tmp) * np.linalg.norm(vec33)))
        score1 = sum(score1)
        score2 = sum(score2)
        score3 = sum(score3)
        outname = {0: '政策', 1: '法律', 2: '公告'}
        outname2 = {0: ['政策', '策略', '规定'], 1: ['法律', '法规'], 2: ['公告', '公示', '告知', '通知', '名单']}
        tmp = (score1, score2, score3)

        tmp = np.array(tmp)

        out = outname[tmp.argmax()]


        end = time.time()

        CLASSIFY = out

        # 用标题做修正
        def fix():
            nonlocal CLASSIFY
            for i in outname2:
                tmp = outname2[i]
                for j in tmp:
                    if j in ZHENGCEMINGCHENG:



                        CLASSIFY = outname[i]
                        break

        fix()




        '''
        返回政策文号 ZHENGCEWENHAO
        '''

        # with open(tex) as f :
        #     dex=0
        #     for i in f:

        '''
            返回政策文号 ZHENGCEWENHAO
        '''
        import re
        out = ''

        tmp3 = inputtex
        if 1:

            for i in tmp3:
                # 正则匹配 xxx发

                tmp = re.search(repl_for_zhengcebianhao, i)
                if tmp != None:
                    out = tmp.group()
                    break

        ZHENGCEWENHAO = out

        '''
        返回fanhui返回
        政策级别:
        国家,省,是, 去

        政策级别JIBIE
        '''

        import re
        out = ''
        guojia = 0
        sheng = 0
        shi = 0
        qu = 0
        if '国' in tex:
            out = '国家级'
        elif '省' in tex:
            out = '省级'
        elif '市' in tex:
            out = '市级'
        elif '区' in tex:
            out = '区县级'
        elif '县' in tex:
            out = '区县级'
        else:
            if 1:

                for i in tmp3:
                    sheng += i.count('省')
                    guojia += i.count('国')
                    shi += i.count('市')
                    qu += i.count('区')
                    qu += i.count('县')
            dic = {0: '国家级', 1: '省级', 2: '市级', 3: '区县级'}
            out = dic[np.array([guojia, sheng, shi, qu]).argmax()]


        JIBIE = out

        '''
        发布单位:想不出来,正则表达式.
        
        2019-08-22,16点17 zhao zuihouyihang
        '''

        fuzhudizhi, fuzhushijian = None, None
        out = ''
        if 1:

            for i in tmp3:

                a = re.match(r'由.*负责解释', i)
                if a != None:
                    out = a.group()
                    break
        if out=='':#处理分词前就是结果的情况
            tmp99 = tmp3[-1]

            tmp99=self.delkongbai(tmp99)

            tmp99=tmp99.split('\n')

            while  '' in tmp99:
                tmp99.remove('')
            index=len(tmp99)
            tmpdizhi = []
            tmpshijian = ''


            while  index-2>=0:

                try:

                    if self.checkshijian(tmp99[-1].strip()) and self.checkdizhi(tmp99[index-2].strip()):
                        tmpdizhi.append(tmp99[index-2].strip())
                except:
                    pass
                index-=1

            '''
            因为机构单位很多,所以要对-2行之前的进行严格赛选!
            '''



            def saixuan(a):
                    #haishi yong cixing

                    input=a
                    HanLP.Config.ShowTermNature = True
                    tmp99 = HanLP.segment(input)
                    tmpcixing=[]

                    for i in tmp99 :
                        tmpcixing.append(i.nature)


                    tmp72=[]
                    for i in tmpcixing:
                        tmp72.append(str(i))
                    if tmp72==['n','nto']:
                        return True
                    for i in tmpcixing:
                        #注意因为hanlp底层用的java,所以调用之后需要用str转化过来才可以用!!!!!!!!!!!!!
                        if str(i) not in ['nt', 'nis', 'nto', 'nit', 'ni','ns'] :
                            return False


                    return True


















            if len(tmpdizhi)>1:
                tmp98=[tmpdizhi[0]]

                for i in tmpdizhi[1:]:

                    if saixuan(i):

                        tmp98.append(str(i))
                tmpdizhi=tmp98

                #正则修改
                import re
                tmpdizhi=','.join(tmpdizhi)
                out=re.sub(r'[\[\]\' ]','',tmpdizhi)





                if tmpshijian:
                    fuzhushijian=tmpshijian
            else:
                if tmpdizhi:
                    tmpdizhi=tmpdizhi[0]
                    fuzhudizhi=str(tmpdizhi)
                    out=fuzhudizhi
                if tmpshijian:
                    fuzhushijian=tmpshijian



        if out=='':

            tmp99=tmp3[-1]

            tmp98=tmp99


            if len(tmp99)>=2:
                tmp99 = re.findall('[\u4e00-\u9fa5].*\n', tmp99)

                panduan=False
                if len(tmp99)>=2:
                     panduan=re.search(r'[1-2][0-9]{3}-[0-1]?[0-9]-[0-3]?[0-9]', tmp99[-1])or re.search(r'[1-2][0-9]{3}年[0-1]?[0-9]月[0-3]?[0-9]日', tmp99[-1])

            if len(tmp99)>=2 and  panduan:

                tmp98=tmp99[-2]
                tmp99=tmp99[-2]


                HanLP.Config.ShowTermNature = True
                tmp99 = HanLP.segment(tmp99)
                flag=0

                for i in tmp99:

                    if str(i.nature) in ['nt','nis']:
                        flag=1
                        break
                if flag==0:
                    out=str(tmp98.strip('\n'))

            #nt   nis
        dongxi=None




        if out=='' and Forhtml:#处理附件问题.
            tmp4=Forhtml

            from bs4 import BeautifulSoup

            dongxi=tmp4.select('p')
            fuzhudizhi,fuzhushijian=None,None

            '''
            需要先删除空白行
            '''
            dongxi2=[]
            for i in range(len(dongxi)) :
                if dongxi[i].getText().strip()!='':

                    dongxi2.append(dongxi[i])

            dongxi=dongxi2





            for i in range(len(dongxi)) :

                if (dongxi[i].getText().strip()=='附件' or dongxi[i].getText().strip()=='附件：') and '此件公开' not in dongxi[i-1].getText().strip() and self.checkdizhi(dongxi[i-2].getText().strip()) and self.checkshijian(dongxi[i-1].getText().strip()):
                    fuzhudizhi=dongxi[i-2].getText().strip()
                    fuzhushijian=dongxi[i-1].getText().strip()
                    break
                if (dongxi[i].getText().strip() == '附件' or dongxi[i].getText().strip()=='附件：')  and '此件公开'  in dongxi[i - 1].getText().strip() and self.checkdizhi(dongxi[i-3].getText().strip())and self.checkshijian(dongxi[i-2].getText().strip()):

                    fuzhudizhi=dongxi[i-3].getText().strip()
                    fuzhushijian=dongxi[i-2].getText().strip()
                    break

            if fuzhudizhi:
                  out=fuzhudizhi



        if out=='' and dongxi: #如果还是空就按照时间匹配.


            for i in range(len(dongxi)) :

                tmp=re.fullmatch(r'[1-2][0-9]{3}-[0-1]?[0-9]-[0-3]?[0-9]',dongxi[i].getText().strip()) or \
                    re.fullmatch(r'[1-2][0-9]{3}年[0-1]?[0-9]月[0-3]?[0-9]日',dongxi[i].getText().strip())

                if tmp:
                    fuzhushijian=dongxi[i].getText().strip()
                    out=dongxi[i-1].getText().strip()

                    break

        '''
        下面处理没有html码的情况用someList来做
        '''


        if out=='' :#处理附件问题.

            for i in range(len(someList)) :
                #注意层级判断需要加括号.不然会短路
                if (someList[i].strip()=='附件' or someList[i].strip()=='附件：') and '此件公开' not in someList[i-1].strip() and self.checkdizhi(someList[i-2].strip()) and self.checkshijian(someList[i-1].strip()):
                    fuzhudizhi=someList[i-2].strip()
                    fuzhushijian=someList[i-1].strip()
                    break
                if (someList[i].strip()=='附件' or someList[i].strip()=='附件：')  and '此件公开'  in someList[i-1].strip() and self.checkdizhi(someList[i-3].strip())and self.checkshijian(someList[i-2].strip()):

                    fuzhudizhi=someList[i-3].strip()
                    fuzhushijian=someList[i-2].strip()
                    break

            if fuzhudizhi:
                  out=fuzhudizhi





        if out=='' : #如果还是空就按照时间匹配.

            for i in range(len(someList)) :

                tmp=re.fullmatch(r'[1-2][0-9]{3}-[0-1]?[0-9]-[0-3]?[0-9]',someList[i].strip()) or \
                    re.fullmatch(r'[1-2][0-9]{3}年[0-1]?[0-9]月[0-3]?[0-9]日',someList[i].strip())

                if tmp:
                    fuzhushijian=someList[i].strip()
                    out=someList[i-1].strip()

                    break





























































        if self.checkdizhi(out):




            pass
        else:
            fuzhushijian=''
            out=''


                 # dongxi[i].getText()



            # import urllib
            #
            # bs = BeautifulSoup(tmp4, "html.parser")

            # soup = BeautifulSoup(tmp4, "lxml")

        #



        fabudanwei = out
        fabudanwei = fabudanwei.replace('）', '')
        fabudanwei = fabudanwei.replace('（', '')









        '''
        政策内容NEIRONG
        '''
        out = ''
        if 1:

            for i in tmp3:
                out += i


        NEIRONG = out


        '''
        发布时间:第二行,或者第一行.
        SHIJIAN
        '''
        dex = 0
        out = ''
        start_date = ''

        if 1:


            for ii in range(len(tmp3)) :
                i=tmp3[ii]
                if ii == 0:
                    a99 =  re.search(r'[1-2][0-9]{3}-[0-1]?[0-9]-[0-3]?[0-9]', i)
                    if a99:
                        SHIJIAN=a99.group()

                        start_date=SHIJIAN
                        break
                    a99 =  re.search(r'[1-2][0-9]{3}年[0-1]?[0-9]月[0-3]?[0-9]日', i)
                    if a99:
                        SHIJIAN=a99.group()

                        start_date=SHIJIAN
                        break
                if ii==1:
                    a99 = re.search(r'[1-2][0-9]{3}-[0-1]?[0-9]-[0-3]?[0-9]', i)
                    if a99 :
                        SHIJIAN = a99.group()
                        start_date = SHIJIAN

                        break
                    a99 =  re.search(r'[1-2][0-9]{3}年[0-1]?[0-9]月[0-3]?[0-9]日', i)
                    if a99:
                        SHIJIAN=a99.group()

                        start_date=SHIJIAN
                        break
                if ii==len(tmp3)-1:

                    a99 = re.search(r'[1-2][0-9]{3}-[0-1]?[0-9]-[0-3]?[0-9]', i)

                    if a99 :
                        SHIJIAN = a99.group()
                        start_date = SHIJIAN

                        break
                    a99 =  re.search(r'[1-2][0-9]{3}年[0-1]?[0-9]月[0-3]?[0-9]日', i)

                    if a99:
                        SHIJIAN=a99.group()

                        start_date=SHIJIAN
                        break


        # 因为时间不输入会数据库bug,所以写一个虚拟的时间.
        if start_date=='':
            if fuzhushijian:
                     start_date=fuzhushijian
        SHIJIAN = start_date
        SHIJIAN=SHIJIAN.replace('年','-')
        SHIJIAN=SHIJIAN.replace('月','-')
        SHIJIAN=SHIJIAN.replace('日','')

        '''
        进行发布时间修正
        '''
        beixuan = None
        if Forhtml:
            tmp96=Forhtml.select('p')

            beixuan=None

            for i in tmp96:


                if '发布时间：' in i.getText():
                    tmp95=i.getText()

                    a99 = re.search(r'[1-2][0-9]{3}-[0-1]?[0-9]-[0-3]?[0-9]', tmp95)
                    if a99 :
                        beixuan = a99.group()

                        break
                    a99 = re.search(r'[1-2][0-9]{3}年[0-1]?[0-9]月[0-3]?[0-9]日', tmp95)
                    if a99 :
                        beixuan = a99.group()


                        break


        if beixuan:
            SHIJIAN=str(beixuan)


        SHIJIAN=str(SHIJIAN)





        '''
        有效时间youxiaoshijian
        '''
        shijianduan=None
        for i in tmp3:

            tmp8=self.chaxunshijian(i)

            if tmp8:

                shijianduan=tmp8
                break
        if not shijianduan and Forhtml:

                #用自印发之日起施行，有效期来匹配.
                tmp60=Forhtml.select('p')



                for i in tmp60:
                    if '自印发之日起施行，有效期' in i.getText():
                        tmp70=str(i.getText())
                        tmp70=re.search(r'自印发之日起施行，有效期.*?年',tmp70).group()



                        tmp70=tmp70.strip('自印发之日起施行，有效期')
                        tmp70=tmp70.strip('年')

                        try:
                            tmp70=int(tmp70)
                            now = datetime.datetime.strptime(SHIJIAN,'%Y-%m-%d')
                            delta = datetime.timedelta(days=tmp70*365)

                            tmp70 = (now + delta).strftime('%Y-%m-%d')



                        except:
                            tmp70=''
                        shijianduan=SHIJIAN,tmp70











        youxiaoshijian = SHIJIAN

        '''
        政策主题:theme
        '''
        theme = ['财政支持', '税收优惠', '金融支持', '产业升级', '绿色发展', '创新促进', '创业扶持', '就业稳扩', '人才发展', '市场拓展', '要素保障', '平台建设',
                 '环境优化',
                 '费金减免']
        '''


        '''
        myclient = self.myclient
        # myclient = Connection("mongodb://localhost:27017/")
        mydb = myclient["d1"]
        my_collection = mydb['c6']

        # 得到的东西是一个数组,之后是一个字典.
        time5 = time.time()
        vecall = []  # yigogne 28
        vecall.append(my_collection.find_one({'hanzi': '财政'})['bianma'])

        vecall.append(my_collection.find_one({'hanzi': '财政'})['bianma'])
        vecall.append(my_collection.find_one({'hanzi': '税收'})['bianma'])
        vecall.append(my_collection.find_one({'hanzi': '优惠'})['bianma'])
        vecall.append(my_collection.find_one({'hanzi': '金融'})['bianma'])
        vecall.append(my_collection.find_one({'hanzi': '金融'})['bianma'])
        vecall.append(my_collection.find_one({'hanzi': '产业'})['bianma'])
        vecall.append(my_collection.find_one({'hanzi': '升级'})['bianma'])
        vecall.append(my_collection.find_one({'hanzi': '绿色'})['bianma'])
        '''
        绿色发展 创新促进 创业扶持 就业稳扩 人才发展 市场拓展 要素保障 平台建设 环境优化 费金减免
        '''
        vecall.append(my_collection.find_one({'hanzi': '绿色'})['bianma'])
        vecall.append(my_collection.find_one({'hanzi': '创新'})['bianma'])
        vecall.append(my_collection.find_one({'hanzi': '促进'})['bianma'])
        vecall.append(my_collection.find_one({'hanzi': '创业'})['bianma'])
        vecall.append(my_collection.find_one({'hanzi': '扶持'})['bianma'])
        vecall.append(my_collection.find_one({'hanzi': '就业'})['bianma'])
        vecall.append(my_collection.find_one({'hanzi': '就业'})['bianma'])
        vecall.append(my_collection.find_one({'hanzi': '人才'})['bianma'])
        vecall.append(my_collection.find_one({'hanzi': '人才'})['bianma'])
        vecall.append(my_collection.find_one({'hanzi': '市场'})['bianma'])
        vecall.append(my_collection.find_one({'hanzi': '市场'})['bianma'])
        vecall.append(my_collection.find_one({'hanzi': '要素'})['bianma'])
        vecall.append(my_collection.find_one({'hanzi': '要素'})['bianma'])
        vecall.append(my_collection.find_one({'hanzi': '平台'})['bianma'])
        vecall.append(my_collection.find_one({'hanzi': '平台'})['bianma'])
        vecall.append(my_collection.find_one({'hanzi': '环境'})['bianma'])
        vecall.append(my_collection.find_one({'hanzi': '环境'})['bianma'])
        vecall.append(my_collection.find_one({'hanzi': '费金'})['bianma'])
        vecall.append(my_collection.find_one({'hanzi': '减免'})['bianma'])
        import numpy as np
        import re



        def process(vec1):
            vec1 = str(vec1)

            vec1 = vec1.replace(r'\n', '')

            vec1 = vec1.replace('[', '')

            vec1 = vec1.replace(']', '')

            vec1 = vec1.replace('\'', '')

            vec1 = re.sub('\s+', ' ', vec1)

            vec1 = vec1[1:]




            vec1 = np.fromstring(vec1, dtype=float, sep=',')


            return vec1

        score = []
        for j in range(len(vecall) // 2):
            score.append([])
        for i in KEYWORD:
            try:
                tmp = my_collection.find_one({'hanzi': i})['bianma']

            except:
                continue
            tmp = process(tmp)






            for j in range(len(vecall)):
                tmp = np.array(tmp, dtype=float)
                #下面一行代码非常秀,通过定义dtype自动强转了 string类型的字符串到数组.
                vecall[j] = np.array(vecall[j], dtype=float)

                score[j // 2].append(np.dot(tmp, vecall[j]) / (np.linalg.norm(tmp) * np.linalg.norm(vecall[j])))
        out = []
        for i in range(len(score)):
            score[i] = sum(score[i])

        '''


        注意这个地方的6是人工指定的,跟word2vec向量数据,样本集.等douyouguan,可能需要重新调整.
        '''
        score5=score
        score = [i for i in range(len(score)) if score[i] > self.scoreForTheme]

        theme = np.array(theme)
        out = theme[score]

        '''
        下面对hangye进行判断.
        '''



        if len(out)==0:
            score5=np.array(score5)
            score5=np.argmax(score5)
            score5=int(score5)
            out=theme[score5]

            out=[out]
            pass





        zhuti = out

        endtime = ''
        KEYWORD2 = KEYWORD
        zhuti2 = zhuti
        zhuti2 = list(zhuti2)
        KEYWORD2 = list(KEYWORD2)
        zhuti = list(zhuti)
        zhuti = str(zhuti)
        KEYWORD = str(KEYWORD)

        '''
        2019-09-10,20点31
        
        新需求:返回行业信息.
        '''
        hangyexinxi=''
        hangye=[]
        tmp88=my_collection.find_one({'hanzi': '费金'})['bianma']
        '''
        医疗健康	  生态文化旅游	制造业	教育	金融	汽车产业	 房产服务 	数字产业 	生物产业	新一代信息技术	新能源	新材料	航空航天

        '''
        shuchuhangyeshuzu=['医疗健康',
                           "生态文化旅游",
                           '制造业',
                           '教育',
                           '金融',
                           '汽车产业',
                           '房产服务',
                           '数字产业',
                           '生物产业',
                           '新一代信息技术',
                           '新能源',
                           '新材料',
                           '航空航天'
                           ]
        hangye.append(np.array(my_collection.find_one({'hanzi': '医疗'})['bianma'], dtype=float))
        hangye.append(np.array(my_collection.find_one({'hanzi': '旅游'})['bianma'], dtype=float))
        hangye.append(np.array(my_collection.find_one({'hanzi': '制造业'})['bianma'], dtype=float))
        hangye.append(np.array(my_collection.find_one({'hanzi': '教育'})['bianma'], dtype=float))
        hangye.append(np.array(my_collection.find_one({'hanzi': '金融'})['bianma'], dtype=float))
        hangye.append(np.array(my_collection.find_one({'hanzi': '汽车'})['bianma'], dtype=float))
        hangye.append(np.array(my_collection.find_one({'hanzi': '房产'})['bianma'], dtype=float))
        hangye.append(np.array(my_collection.find_one({'hanzi': '数字科技'})['bianma'], dtype=float))
        hangye.append(np.array(my_collection.find_one({'hanzi': '生物医药'})['bianma'], dtype=float))
        hangye.append(np.array(my_collection.find_one({'hanzi': '信息技术'})['bianma'], dtype=float))
        hangye.append(np.array(my_collection.find_one({'hanzi': '新能源'})['bianma'], dtype=float))
        hangye.append(np.array(my_collection.find_one({'hanzi': '新材料'})['bianma'], dtype=float))
        hangye.append(np.array(my_collection.find_one({'hanzi': '航空'})['bianma'], dtype=float))

        score=[0]*len(hangye)










        # hangyeci=outputForhangyexinxi
        #
        # hangyeci=list(set(hangyeci))
        # out55=[]
        # for i in hangyeci:
        #
        #
        #     HanLP.Config.ShowTermNature = True
        #     seg_list = HanLP.segment(i)
        #     seg=str(seg_list[0])
        #     if seg  in ['nn' ,'nnd']:
        #         out55.append(seg)
        # hangyeci=out55
        # print(hangyeci,"kankanhdafdsfasdf")


        score=[]
        for i in (hangye):
            score.append([])


        for i in KEYWORD2:
            try:
                tmp = np.array(my_collection.find_one({'hanzi': i})['bianma'], dtype=float)

            except:
                continue

            for j in range(len(hangye)):

                #下面一行代码非常秀,通过定义dtype自动强转了 string类型的字符串到数组.


                score[j].append((np.dot(tmp, hangye[j]) / (np.linalg.norm(tmp) * np.linalg.norm(hangye[j]))))
        score1=[sum(i)/len(i) for i in score]
        #因为航天总是偏高.所以乘以一个系数
        print("00011111111111111", score1)
        score1[-1]=score1[-1]*0.8
        score1[3]=score1[3]*0.8
        print(score1)
        score1=np.array(score1)
        hangye=np.array(hangye)
        shuchuhangyeshuzu=np.array(shuchuhangyeshuzu)
        shuchuhangyeshuzu1=list(shuchuhangyeshuzu)
        print(1111111111,score1)
        score2=shuchuhangyeshuzu[score1>0.4]

        #至多反3个,太多hold不住.
        print(score2,"22222222222213213123123")
        if len(score2)>=3:

            score2=shuchuhangyeshuzu[score1.argsort()[-3:]]
            print(score2,111111111111111111)
        print(KEYWORD2,"关键词")
        print(score2,"得分")

        tmp89=[i for i in shuchuhangyeshuzu1 if i in KEYWORD2]
        print(23232323232,tmp89)
        score2=list(score2)
        for i in tmp89:
            if i not in score2:
                score2.append(i)
        score2=np.array(score2)
        print('11111')
        print('11111')
        print('11111')
        print('11111')
        print('11111')
        print('11111')
        print('11111')
        print('11111')
        print('11111')
        print(score2,11111111111111111)



        canyexinxi=list(score2)



















































        print(canyexinxi,3243242423)
        if tex.split('.')[-1] == 'html':

            '''
            这部分是保存html源码用的.
            '''
















            try:

                htmlfile = open(tex, 'r', encoding='utf-8')
                html = htmlfile.read()
            except:
                try:
                    import urllib
                    from bs4 import BeautifulSoup
                    resp = urllib.request.urlopen(tex)

                    html = resp.read()
                except:

                    import requests
                    url=tex


                    r = requests.get(url)

                    with open('laji.html', "wb") as f :  # 这里面补上后缀名

                        f.write(r.content)
                    url = 'laji.txt'

                    htmlfile = open('laji.html', 'r', encoding='utf-8')
                    html = htmlfile.read()

















            # import requests
            # res = requests.get(tex)
            # res.encoding = 'utf-8'
            # html = res.text
            # html=BeautifulSoup(html, 'html.parser')
            html=str(html)


            # html=resp
            '''
            html:给子操
            NEIRONG:txt
            '''


            # sql = 'insert into policy_article (title,context,category,keywords.txt,releaser,theme,' \
            #       'release_time) values (%s,%s,%s,%s,%s,%s,%s);'
            #
            #
            #
            # # 执行SQL语句

            #                        #    ])
            #
            #
            # # lastid = int(cursor.lastrowid)
            # conn.commit()
            # # 关
            # # i闭光标对象
            # cursor.close()
            # # 关闭数据库连接
            # conn.close()
            textForLiaoyong=NEIRONG
            import requests


            # try:
            #     requests.post("http://116.196.87.166:8080/tokenizer/", data=json.dumps({'context' : textForLiaoyong,
            #                                                                         'doc_id' : lastid}))
            # except:
            #     ppp=1








            # return HttpResponse("GET Service From Word2VecService")
            #
            KEYWORD = list(KEYWORD)
            zhuti = list(zhuti)

            if savingTex!=None:
                NEIRONG=savingTex
            if shijianduan :
                youxiaoshijian = shijianduan[0]
                endtime = shijianduan[1]
            #输入数据本身就是html返回这个判断
            print("htmld",canyexinxi)
            data = { "keywords" : KEYWORD2, "type" : CLASSIFY, "refNumber" : ZHENGCEWENHAO,
                    "title" : ZHENGCEMINGCHENG, "level" : JIBIE, "createDepartment" : fabudanwei, "content" : html,
                    "txt":NEIRONG,
                    "issueTime" : SHIJIAN, "startTime" : youxiaoshijian, "endTime" : endtime, "themes" : zhuti2,"applyIndustry":canyexinxi}




            return json.dumps(data)






        # sql = 'insert into policy_article (title,context,category,keywords.txt,releaser,theme,' \
        #       'release_time) values (%s,%s,%s,%s,%s,%s,%s);'
        #
        #
        #
        # # 执行SQL语句

        #                            # ])
        #
        #
        # # lastid = int(cursor.lastrowid)
        # conn.commit()
        # # 关
        # # i闭光标对象
        # cursor.close()
        # # 关闭数据库连接
        # conn.close()


        # return HttpResponse("GET Service From Word2VecService")

        KEYWORD = list(KEYWORD)
        zhuti = list(zhuti)
        if shijianduan:
            youxiaoshijian=shijianduan[0]
            endtime=shijianduan[1]
        if ForhtmlOld:#返回doc用这个判断.
             print(21321312,canyexinxi)
             data = { "keywords": KEYWORD2, "type": CLASSIFY, "refNumber": ZHENGCEWENHAO,
                "title": ZHENGCEMINGCHENG, "level": JIBIE, "createDepartment": fabudanwei, "content": ForhtmlOld,
                "issueTime": SHIJIAN, "startTime": youxiaoshijian, "endTime": endtime, "themes": zhuti2,"applyIndustry":canyexinxi}
        else:#返回pdf用这个判断
            print("pdf", canyexinxi)
            data = {"keywords" : KEYWORD2, "type" : CLASSIFY, "refNumber" : ZHENGCEWENHAO,
                    "title" : ZHENGCEMINGCHENG, "level" : JIBIE, "createDepartment" : fabudanwei,
                    "content" : NEIRONG,"txt":NEIRONG,
                    "issueTime" : SHIJIAN, "startTime" : youxiaoshijian, "endTime" : endtime, "themes" : zhuti2,"applyIndustry":canyexinxi}
        return json.dumps(data)






# Word2VecService().get(request=None)
