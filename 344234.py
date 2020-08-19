from selenium import webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')  # 这句一定要加

driver = webdriver.Chrome(executable_path='/chromedriver', chrome_options=chrome_options)
aaa=driver.get("https://www.baidu.com/")
print(aaa)
