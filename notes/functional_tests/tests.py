from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.common.exceptions import WebDriverException
import os

MAX_WAIT = 10

class NewVisitorTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()
        real_server = "39.101.64.202"
        if real_server:
            self.live_server_url='http://' + real_server

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element(By.ID,'id_list_table')
                rows = table.find_elements(By.TAG_NAME,'tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_list_and_retrieve_it_later(self):
        # 网页的首页
        self.browser.get(self.live_server_url)

        # 网页里包含“To-Do”这个词
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME,'h1').text
        self.assertIn('To-Do',  header_text)

        # 应用有一个输入待办事项的文本输入框
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
            )

        # 输入“Buy flowers”
        inputbox.send_keys('Buy flowers')

        #按回车键页面更新
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy flowers')
        
        # 应用又显示一个文本输入框，可以输入其他代办事项
        # 输入'Give a gift to Lisi'
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Give a gift to Lisi')
        inputbox.send_keys(Keys.ENTER)

        #页面更新，显示了两个待办事项
        self.wait_for_row_in_list_table('1: Buy flowers')
        self.wait_for_row_in_list_table('2: Give a gift to Lisi')

    def test_multiple_users_can_start_lists_at_different_urls(self):
        #新建一个待办事项清单
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element(By.ID,'id_new_item')
        inputbox.send_keys('Buy flowers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy flowers')

        #清单有个唯一的URL
        zhangsan_list_url = self.browser.current_url
        self.assertRegex(zhangsan_list_url, '/lists/.+')

        #新用户王五访问网站 使用新浏览器会话 确保张三的信息不会从cookies中泄露出去
        self.browser.quit()
        self.browser = webdriver.Chrome()

        #王五访问首页 页面中看不到张三的清单
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertNotIn('Buy flowers', page_text)
        self.assertNotIn('Give a gift to Lisi', page_text)

        #王五输入一个新待办事项，新建一个清单
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        #王五获得唯一的URL
        wangwu_list_url = self.browser.current_url
        self.assertRegex(wangwu_list_url, '/lists/.+')
        self.assertNotEqual(wangwu_list_url, zhangsan_list_url)

        #这个页面还没有张三的清单
        page_text = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertNotIn('Buy flowers', page_text)
        self.assertIn('Buy milk', page_text)
        
        #网站生成了一个唯一的URL
        
    def test_layout_and_styling(self):
        #张三访问首页
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)
        
        #输入框完美地居中显示
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )
        
        #新建一个菜单，看到输入框仍然完美的居中显示
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: testing')
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
         )
    
