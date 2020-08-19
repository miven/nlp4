from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)

base_url = "http://www.baidu.com/"
driver.get(base_url) #注意这里面结果直接写到deriver里面
print(driver.page_source)