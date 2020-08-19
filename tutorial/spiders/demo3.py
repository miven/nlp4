import shutil
from urllib.request import quote
import scrapy
from tutorial.items import *
from urllib import parse
class DmozSpider3(scrapy.Spider): # 继承Spider类

    print("进入3了")
    import os
    if  os.path.exists('output'):
        shutil.rmtree('output')
    yuming='中国青年'
    lang='英语'

    '''
    超参数都在这里修改, 就下面这2个有用.name 随便起一个,在main函数里面调用这个名就行.
    html就是要爬取的网站.
    '''
    name = "dmoz3" # 爬虫的唯一标识，不能重复，启动爬虫的时候要用
    html='https://list.51test.net/w/?nclassid=69&key=&search_key=%CB%AB%D3%EF&search_key2=%D0%C2%CE%C5&page=1'










    from bs4 import BeautifulSoup
    #首页写这里

    baseUrl=html

    import requests
    # a=requests.get(html).content

    # bs = BeautifulSoup(a, "html.parser")  # 缩进格式
    # print(bs)
    # 下面冲bs中找到所有爬取的页.
    # print(bs.find_all("a"))  # 获取所有的a标签,也就是超链接
    from selenium import webdriver
    import sys



    # browser = webdriver.Firefox()  # Get local session of firefox
    # aaa=browser.get("http://news.sina.com.cn/c/2013-07-11/175827642839.shtml ")  # Load page
    # print(aaa)
    saveall=[html]
    if 0:#调试用, 一般不用这么跑.这个只是动态js代码需要这么使用而已. 一般网页没有这种方式.这个方式太慢爬虫.但是可以避免不必要的js bug
     while 1:
        tmpurl=saveall[-1]
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        from .utilsme import driver


        base_url = tmpurl
        driver.get(base_url)  # 注意这里面结果直接写到deriver里面
        # print(driver.page_source)
        a=driver.page_source

        bs = BeautifulSoup(a, "html.parser")  # 缩进格式
        # print(bs)
        # 下面冲bs中找到所有爬取的页.
        # print(bs.find_all("a"))
        import re
        # tmp=bs.find_all(text=re.compile("Next[ ]*"))
        # print(tmp)
        now=None

        for s in bs('a'):
            if s.text=="下一页":
                now=s.extract()
                # 需要对now进行中文转码
                # now=parse.quote(now.get('href'))
                print("loook",now)
                # 注意这种旧网站的编码方式.
                now = 'https://'+parse.quote(now.get('href'), safe=";/?:@&=+$, ", encoding="gbk")
                print(now,"now网页是!!!!!!!!!!")
        if now==None:
            break
        else:
            saveall.append(now)









    if 0:#调试用
     while 1:



        tmpurl=saveall[-1]

        import urllib
        from bs4 import BeautifulSoup

        url = tmpurl
        # print(url,8989898998)
        page = requests.get(url)
        page.encoding = 'gb18030'
        # soup = BeautifulSoup(page,"html.parser")

        bs = BeautifulSoup(page.text, "html.parser")  # 缩进格式
        # print(bs)
        # 下面冲bs中找到所有爬取的页.
        # print(bs.find_all("a"))
        import re
        # tmp=bs.find_all(text=re.compile("Next[ ]*"))
        # print(tmp)
        now=None
        # print(url,bs('a'),777777777777777777)
        for s in bs('a'):
            # print(s.text)
            if s.text=="下一页":
                now=s.extract()
                # print(now,12345)
                # 需要对now进行中文转码
                # now=parse.quote(now.get('href'))
                # print("loook",now)
                # 注意这种旧网站的编码方式.
                now = 'https:'+parse.quote(now.get('href'), safe=";/?:@&=+$, ", encoding="gbk")
                # print(now,"now网页是!!!!!!!!!!")
        if now==None:
            break
        else:
            # print(now,556565656565)
            saveall.append(now)











    #成功爬取到下面.
    # print("进入demo3!!!!!!!!!!")
    # 现在是预处理.就是要找到所有的一级网页!!!!!!!!!!! 然后赋值给saveall
    # print(saveall,"打印主网页!!!!!!!!!!!!")
    # # 提取所有的href
    # tmpurl = saveall[-1]
    # from selenium import webdriver
    # from selenium.webdriver.chrome.options import Options
    #
    # chrome_options = Options()
    # chrome_options.add_argument("--headless")
    # driver = webdriver.Chrome(options=chrome_options)
    #
    # base_url = tmpurl
    # driver.get(base_url)  # 注意这里面结果直接写到deriver里面
    # # print(driver.page_source)
    # a = driver.page_source
    # bs = BeautifulSoup(a, "html.parser")  # 缩进格式
    # # print(bs('a'),888888888888)
    # tmp=bs.find_all(class_='pagelist')
    # out=[]
    # for i in tmp:
    #     out+=[k['href'] for k in i.find_all('a')]
    #
    #
    # base_url=html[:html.rindex(r'/')+1]
    # print(base_url,77777777777777)
    # aaa=base_url
    # baseUrl=base_url
    # for i in range(len(out)):
    #     out[i]=aaa+out[i]
    # # out=[aaa+i for i in out ]
    # # print(out,6767676767)
    # # 筛选  https://www.jianshu.com/p/5f207f7309ec
    # saveall=out
    #
    #
    #
    #
    # print(saveall)
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    # start_urls =saveall  # 开始爬取的链接
    start_urls = saveall  # 开始爬取的链接

    def parse(self, response): # 一级爬取代码
        #xpath教学:https://blog.csdn.net/qq_27283619/article/details/88704479
        #https://www.cnblogs.com/wt7018/p/11749778.html
        # @表示属性
        # 好像使用框架scrapy没法debug.只能疯狂print了
        print("111111111111111111")
        print(response,'**********************当前爬取的网页链接')
        div_list = response.xpath('//div[@class="news-list-left-content"]/ul/li/a/@href')
        # print(div_list[0])
        # print(div_list[-1])
        # print((div_list))
        print("进入了一级爬虫")
        print(div_list,99999999999999999999999999999999999999)
        for i in div_list:
            # print(self.baseUrl+i.extract())# 获得了全部链接,进入二级爬虫.
            item = en_youth()
            item['link'] = 'https:'+i.extract()
            # print(item['link'],"lianjie !!!!!!!!!!!!!")
            #每一次一级爬虫得到的页面,都触发一次二级爬虫.
            yield scrapy.Request(item['link'], callback=self.parse_detail
                                 ,meta={'item':item})






        # 完成每页之后开始下一页
        '''
                for div in div_list:
            name = div.xpath('./div/div/h1/a/text()').extract_first()

            print('已找到:', name)

            url = div.xpath('.//div[@class="meta"]/h1/a/@href').extract_first()
            url = "https:" + url
            # 实例化item对象并存储
            item = en_youth()
            item['link'] = name
            # meta 传递第二次解析函数
            yield scrapy.Request(url=url, callback=self.parse_detail, meta={'item': item})
        
        
        if self.page < 3:
            self.page += 1
            new_url = self.base_url.format(self.page)
            yield scrapy.Request(url=new_url, callback=self.parse)

        '''



        '''
        filename = response.url.split("/")[-2] # 获取url，用”/”分段，获去倒数第二个字段
        print("filenmadsf",filename)
        with open('output/'+filename, 'wb') as f:
            f.write(response.body) # 把访问的得到的网页源码写入文件
        '''

    #https://blog.csdn.net/Light__1024/article/details/88763541 如何进行爬取二级界面

    def parse_detail(self, response):  # 二级爬取代码
        infomation=response.meta['item']['link']
        # print(infomation,"二级爬取的地址是")
        item = response.body
        # print(item)
        # print(response.body,"???????????????")
        # print("********打印二次爬虫结果")#[@class="TRS_Editor"]
        item=en_youth()

        #下面要设计多重xpath判断.因为格式不同意.
        item['neirong']= response.xpath('//div[@class="content-txt"]/div/text()').extract()
        item['neirong']+= response.xpath('//div[@class="content-txt"]/div/p/text()').extract()
        item['neirong']+= response.xpath('//div[@class="content-txt"]/p/text()').extract()


        print(item['neirong'], '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        # print(item['neirong'], 8888888888888888888)


        save2='\n'.join(item['neirong'])
        print(save2,9999999999999999999999999999999999999)
        item['neirong']=save2
        item['title']=infomation
        yield item
        # 下面学习pipeline, 进行文件读写.
        # setttings里面设置pipeline写入文件
        #https://www.cnblogs.com/python2687806834/p/9836935.html
        pass

#
# if __name__=="__main__":
#     DmozSpider()