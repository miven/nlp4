from selenium import webdriver

driver = webdriver.PhantomJS(executable_path=r'c:\phantomjs/phantomjs.exe')


html='http://en.youth.cn/TopStoroes/'
driver.get(html)
print (driver.page_source)