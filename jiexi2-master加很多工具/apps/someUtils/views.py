from django.shortcuts import render, HttpResponse
from django.views import View

# Create your views here.
import sys
sys.path.append('.')

from .textfilter import  filter as ft

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

    def post( self,request):
        '''
        封装一个dirty word过滤的功能.
https://github.com/observerss/textfilter
        :param request:
        :return:





        下面是实现代码.




         #传入一个html然后返回去掉dirtyword的




        pack = request.POST.get('url')  # POST必须大写
        import urllib

        import requests
        res = requests.get(pack)
        res.encoding = 'utf-8'

        tmp=res.text
        tmp=str(tmp)




        gfw = ft.DFAFilter()

        r=gfw.filter(tmp,'*')
        gfw1=gfw.filter('文件','*')
        aa=gfw.filter("文件", "*")







        return HttpResponse(aa)#注意这个地方的bug地方,res打印类型是response但是直接返回不行,需要再套一层菜心 ..
        '''

        '''
        https://github.com/zhangbo2008/funNLP  还是这个里面的代码.
        
        
        
        识别语言:
        
        pip install langid

>>> import langid
>>> langid.classify("This is a test")
('en', -54.41310358047485)

查询号码,算法还是二分.
from phone import Phone
p  = Phone()
p.find(18100065143)
#return {'phone': '18100065143', 'province': '上海', 'city': '上海', 'zip_code': '200000', 'area_code': '021', 'phone_type': '电信'}




另外一个抽取库包,cocoNLP,底层用的hanlp

>>> from cocoNLP.extractor import extractor

>>> ex = extractor()

>>> text = '急寻特朗普，男孩，于2018年11月27号11时在陕西省安康市汉滨区走失。丢失发型短发，...如有线索，请迅速与警方联系：18100065143，132-6156-2938，baizhantang@sina.com.cn 和yangyangfuture at gmail dot com'

# 抽取邮箱
>>> emails = ex.extract_email(text)


['baizhantang@sina.com.cn', 'yangyangfuture@gmail.com.cn']
# 抽取手机号
>>> cellphones = ex.extract_cellphone(text,nation='CHN')


['18100065143', '13261562938']
# 抽取身份证号
>>> ids = ex.extract_ids(text)


['410105196904010537']
# 抽取手机归属地、运营商
>>> cell_locs = [ex.extract_cellphone_location(cell,'CHN') for cell in cellphones]


cellphone_location [{'phone': '18100065143', 'province': '上海', 'city': '上海', 'zip_code': '200000', 'area_code': '021', 'phone_type': '电信'}]
# 抽取地址信息
>>> locations = ex.extract_locations(text)

['陕西省安康市汉滨区', '安康市汉滨区', '汉滨区']
# 抽取时间点
>>> times = ex.extract_time(text)

time {"type": "timestamp", "timestamp": "2018-11-27 11:00:00"}
# 抽取人名
>>> name = ex.extract_name(text)

特朗普







ngender 根据名字判断性别：observerss/ngender 基于朴素贝叶斯计算的概率

pip install ngender

>>> import ngender
>>> ngender.guess('赵本山')
('male', 0.9836229687547046)
>>> ngender.guess('宋丹丹')
('female', 0.9759486128949907)



简体繁体转化,在
import nstools.zhtools.chconv.py
import nstools.zhtools.langconv.py
里面.

原始地址https://github.com/skydark/nstools


英文分词:
https://github.com/keredson/wordninja




        '''












        return HttpResponse(323)


