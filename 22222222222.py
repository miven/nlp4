#from pyvirtualdisplay import Display

from selenium import webdriver

#display = Display(visible=0, size=(800, 600))

#display.start()

chrome_opt = webdriver.ChromeOptions()

chrome_opt.add_argument('--headless')

chrome_opt.add_argument('--disable-gpu')
chrome_opt.add_argument('--no-sandbox')  # 这句一定要加
#chrome_opt.add_argument('--ignore-certificate-errors')

try:

    a=(webdriver.Chrome('/chromedriver'))

except Exception as e:

    print(e)

    #display.stop()

else:

    a.get("http://www.baidu.com")

    print(a.title)

    a.quit()

    #display.stop()
