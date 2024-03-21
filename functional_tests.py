from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # 弹出网页有一个定位输入的网页
        # 他去看了这个网页的首页
        self.browser.get('http://localhost:8000')

        # 他注意到网页里包含“To-Do”这个词
        self.assertIn('To-Do', self.browser.title), "browser title was:" + self.browser.title
        self.fail('Finish the test!')

        # 应用有一个输入代办事项的文本输入框
        # 他在文本输入框里输入了“Buy flowers"

        # 他访问了URL，发现他的待办事项列表还在
        # 他满意的离开了

if __name__ == '__main__':
    unittest.main()
    
browser.quit()
