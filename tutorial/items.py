import scrapy
class en_youth(scrapy.Item): #创建一个类，继承scrapy.item类，就是继承人家写好的容器
    title = scrapy.Field() # 需要取哪些内容，就创建哪些容器
    link = scrapy.Field()
    desc = scrapy.Field()
    neirong = scrapy.Field()

