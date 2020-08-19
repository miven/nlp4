import unittest, time
from selenium import webdriver


class TestClass(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome('/chromedriver')
        # webdriver.Chrome('chromedriver.exe文件位置')
        self.base_url = "http://www.testclass.net"

    def tearDown(self):
        time.sleep(2)
        self.driver.quit()

    def test_case(self):
        self.driver.get(self.base_url)
        search_input = self.driver.find_element_by_id("wd")
        search_input.send_keys("selenium")
        search_input.submit()

    def test_case2(self):
        self.driver.get(self.base_url)
        search_input = self.driver.find_element_by_id("wd")
        search_input.send_keys("jenkins")
        search_input.submit()


if __name__ == '__main__':
    unittest.main()