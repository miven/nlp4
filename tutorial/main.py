'''
zhuyanshu

'''


# 注意这个爬虫项目一定是这个目录结构.
# pycharm 的运行步奏是,先进入服务器中当前这个项目的根目录,对于这个项目也就是fairseq-gec这个文件夹.
# 这个文件夹是对应的爬虫根目录,进入这个之后才能找到对应的cfg.才能正常运行.所以不能随便改目录结构.
import shutil ,os

# 每一次爬虫先闪了旧的文件夹output,省的每次都手动删,麻烦.
if os.path.exists('output'):
    shutil.rmtree('output')
'''
https://blog.csdn.net/weixin_41990913/article/details/90936149?utm_medium=distribute.pc_relevant_t0.none-task-blog-BlogCommendFromMachineLearnPai2-1.nonecase&depth_1-utm_source=distribute.pc_relevant_t0.none-task-blog-BlogCommendFromMachineLearnPai2-1.nonecase
'''
# 好像是需要先进入这个目录才能运行.
# os.system('cd /tmp/pycharm_project_557/爬虫999/tutorial')
import os,sys
# os.system("scrapy crawl dmoz")  # 爬取https://blog.scrapinghub.com/
# os.system("scrapy crawl dmoz2")  # 爬取https://www.51voa.com/Bilingual_News_1.html
# os.system("scrapy crawl dmoz3")  # 爬取 https://www.51test.net/yyzy/syxw/
# os.system("scrapy crawl dmoz4")  # 爬取 http://www.kekenet.com/read/news/
# os.system("scrapy crawl dmoz5")  # 爬取 http://www.171english.cn/news/
# os.system("scrapy crawl dmoz6")  # 爬取 http://www.for68.com/eyu/yuedu/
# os.system("scrapy crawl dmoz7")  # 爬取 http://ru.tingroom.com/yuedu/zedzyd/
os.system("scrapy crawl dmoz8")  # 爬取 https://ru.hujiang.com/new/yuedu/





