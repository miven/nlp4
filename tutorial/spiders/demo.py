import scrapy
from tutorial.items import *
class DmozSpider(scrapy.Spider): # 继承Spider类
    print("调用1了?")
    yuming='中国青年'
    lang='英语'
    name = "dmoz" # 爬虫的唯一标识，不能重复，启动爬虫的时候要用
    # 这个参数需要改.
    '''
    如果allowed_domains = ['https://blog.scrapinghub.com/']这么写的话 yield Request时不会调用callback方法；只能写为allowed_domains = ['blog.scrapinghub.com']

下图中的虽然调用了yield scrapy.Request(link.url, callback=self.parse)，但并不会再次代用parse方法

作者：Ten_Minutes
链接：https://www.jianshu.com/p/5d05549ca105
来源：简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
    '''
    # 注意这个地方只能写域名,不能写http和后面的/, 否则就错了,或者这里,干脆不写算了.烦的1b
    # allowed_domains = ["en.youth.cn"] # 限定域名，只爬取该域名下的网页,这个用来限制二级爬虫

    '''
直接在这这里找到我们所有需要的连接即可.
    '''
    # http: // en.youth.cn / TopStoroes /

    #只需要不停的调取next口即可.
    from bs4 import BeautifulSoup
    #首页写这里
    html='http://en.youth.cn/TopStoroes/'
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

    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
    # options.add_argument('window-size=1600x900')  # 指定浏览器分辨率
    options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
    options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
    options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
    options.add_argument('--headless')  # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
    from .utilsme import driver  # 引用自己的driver, 方便以后都不用重新配置参数了.
    if 0:#调试用
         while 1:

            tmpurl=saveall[-1]
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options


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
                if s.text=="Next":
                    now=s.extract()
            if now==None:
                break
            else:
                saveall.append(baseUrl+now.get('href'))
         print("浏览器插件获取js后的html",saveall)



    #成功爬取到下面.
    saveall=['http://en.youth.cn/TopStoroes/', 'http://en.youth.cn/TopStoroes/index_1.htm', 'http://en.youth.cn/TopStoroes/index_2.htm', 'http://en.youth.cn/TopStoroes/index_3.htm', 'http://en.youth.cn/TopStoroes/index_4.htm', 'http://en.youth.cn/TopStoroes/index_5.htm', 'http://en.youth.cn/TopStoroes/index_6.htm', 'http://en.youth.cn/TopStoroes/index_7.htm', 'http://en.youth.cn/TopStoroes/index_8.htm']
    saveall=['http://en.youth.cn/TopStoroes']
    # print(saveall)














    start_urls =saveall  # 开始爬取的链接


    def parse(self, response): # 一级爬取代码
        #xpath教学:https://blog.csdn.net/qq_27283619/article/details/88704479
        #https://www.cnblogs.com/wt7018/p/11749778.html
        # @表示属性
        # 好像使用框架scrapy没法debug.只能疯狂print了
        print(response,'**********************当前爬取的网页链接')
        div_list = response.xpath('//ul[@class="tj3_1"]/li/a/@href')
        # print(div_list[0])
        # print(div_list[-1])
        # print((div_list))
        print("进入了一级爬虫")
        for i in div_list:
            # print(self.baseUrl+i.extract())# 获得了全部链接,进入二级爬虫.
            item = en_youth()
            item['link'] = self.baseUrl+i.extract()
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
        # print(response.body)
        # print("********打印二次爬虫结果")#[@class="TRS_Editor"]
        item=en_youth()

        #下面要设计多重xpath判断.因为格式不同意.
        item['neirong']= response.xpath('//div[@class="TRS_Editor"]/div/text()').extract()
        # print(item['neirong'],8888888888888888888)
        item['neirong']+=response.xpath('//div[@class="TRS_Editor"]/p/text()').extract()
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


