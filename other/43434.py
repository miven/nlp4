from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
chrome_options.set_headless()
brower = webdriver.Chrome(chrome_options=chrome_options)
a=brower.get('https://www.baidu.com')
print(a)
brower.close()