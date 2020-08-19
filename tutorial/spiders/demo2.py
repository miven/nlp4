import shutil

import scrapy
from tutorial.items import *
class DmozSpider2(scrapy.Spider): # 继承Spider类
    import os
    if  os.path.exists('output'):
        shutil.rmtree('output')
    yuming='中国青年'
    lang='英语'

    '''
    超参数都在这里修改, 就下面这2个有用.name 随便起一个,在main函数里面调用这个名就行.
    html就是要爬取的网站.
    '''
    name = "dmoz2" # 爬虫的唯一标识，不能重复，启动爬虫的时候要用
    html='https://www.51voa.com/Bilingual_News_1.html'










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
    if 0:#调试用
     while 1:
        tmpurl=saveall[-1]
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)

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



    #成功爬取到下面.
    # 现在是预处理.就是要找到所有的一级网页!!!!!!!!!!! 然后赋值给saveall
    print(saveall,"打印主网页!!!!!!!!!!!!")
    # 提取所有的href
    tmpurl = saveall[-1]
    from .utilsme import driver


    base_url = tmpurl
    driver.get(base_url)  # 注意这里面结果直接写到deriver里面
    # print(driver.page_source)
    a = driver.page_source
    bs = BeautifulSoup(a, "html.parser")  # 缩进格式
    # print(bs('a'),888888888888)
    tmp=bs.find_all(class_='pagelist')
    out=[]
    for i in tmp:
        out+=[k['href'] for k in i.find_all('a')]


    base_url=html[:html.rindex(r'/')+1]
    # print(base_url,77777777777777)
    aaa=base_url
    baseUrl=base_url
    for i in range(len(out)):
        out[i]=aaa+out[i]
    # out=[aaa+i for i in out ]
    # print(out,6767676767)
    # 筛选  https://www.jianshu.com/p/5f207f7309ec
    saveall=out




    # print(saveall)














    start_urls =saveall  # 开始爬取的链接


    def parse(self, response): # 一级爬取代码
        #xpath教学:https://blog.csdn.net/qq_27283619/article/details/88704479
        #https://www.cnblogs.com/wt7018/p/11749778.html
        # @表示属性
        # 好像使用框架scrapy没法debug.只能疯狂print了
        print("111111111111111111")
        print(response,'**********************当前爬取的网页链接')
        div_list = response.xpath('//div[@class="List"]/ul/li/a/@href')
        # print(div_list[0])
        # print(div_list[-1])
        # print((div_list))
        print("进入了一级爬虫")
        print(div_list,99999999999999999999999999999999999999)
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
        # print(response.body,"???????????????")
        # print("********打印二次爬虫结果")#[@class="TRS_Editor"]
        item=en_youth()

        #下面要设计多重xpath判断.因为格式不同意.
        item['neirong']= response.xpath('//div[@class="Content"]/div/text()').extract()
        item['neirong']+= response.xpath('//div[@class="Content"]/div/p/text()').extract()
        print(item['neirong'],'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        item['neirong']+=response.xpath('//div[@class="Content"]/p/text()').extract()
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