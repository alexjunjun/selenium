# coding = utf-8
import os
import time
from selenium.webdriver.support.select import Select
from lib.init_env import init_env
from lib.log_config import get_logger

'''
页面操作常用方法集合
'''

_mylogger = get_logger(os.path.basename(__file__))


class BasePage(object):

    """
    定义一些基类，让所有页面都继承这个类，封装定位元素的常用方法，以及元素的常用操作
    """

    def __init__(self, driver):
        self.driver = driver
        # self.driver = init_env().open_browser('chrome')

    # 打开网页
    def get(self, selector=None, text=None):
        self.driver.get(text)
        _mylogger.info('打开网页{}'.format(text))

    def back(self):
        self.driver.back()
        _mylogger.info('后退')

    def forward(self):
        self.driver.forward()
        _mylogger.info('前进')

    def scroll_page(self, selector=None, text=None):
        # 向下滚动
        self.driver.execute_script("window.scrollTo(0,1000)")
        time.sleep(2)
        # 向上滚动
        self.driver.execute_script("window.scrollTo(0,0)")
        time.sleep(1)

    def close(self):
        self.driver.close()
        _mylogger.info('关闭当前窗口')

    def quit(self):
        self.driver.quit()
        _mylogger.info('退出')

    def wait(self, seconds):
        self.driver.implicitly_wait(seconds)
        _mylogger.info('等待{}秒'.format(seconds))

    def get_window_img(self):
        imgPath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        screen_name = imgPath + '/screenshot/' + time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())) + '.png'
        try:
            self.driver.get_screenshot_as_file(screen_name)
            _mylogger.info('已截图，保存在{}'.format(screen_name))
        except NameError as e:
            _mylogger.error('截图失败，异常信息：{}'.format(e))

    def find(self, selector):
        '''
        通过传入的selector自动识别定位方式，并定位到元素再返回element
        定位方式包括：by_id,by_tag_name,by_class_name,by_name,by_link_text,by_partial_link_text,by_css_selector,by_xpath
        selector规范：selector_by=>selector_value
        :param selector:
        :return: element
        '''
        if '=>' not in selector:
            return self.driver.find_element_by_id(selector)
        selector_by = selector.split('=>')[0]
        selector_value = selector.split('=>')[1]
        element = None
        if selector_by == 'i' or selector_by == 'id':
            try:
                _mylogger.info('开始通过{}查找元素{}'.format(selector_by, selector_value))
                element = self.driver.find_element_by_id(selector_value)
            except:
                element = None
        elif selector_by == 'n' or selector_by == 'name':
            try:
                _mylogger.info('开始通过{}查找元素{}'.format(selector_by, selector_value))
                element = self.driver.find_element_by_name(selector_value)
            except:
                element = None
        elif selector_by == 'c' or selector_by == 'class_name':
            try:
                _mylogger.info('开始通过{}查找元素{}'.format(selector_by, selector_value))
                element = self.driver.find_element_by_class_name(selector_value)
            except:
                element = None
        elif selector_by == 't' or selector_by == 'tag_name':
            try:
                _mylogger.info('开始通过{}查找元素{}'.format(selector_by, selector_value))
                element = self.driver.find_element_by_tag_name(selector_value)
            except:
                element = None
        elif selector_by == 'l' or selector_by == 'link_text':
            try:
                _mylogger.info('开始通过{}查找元素{}'.format(selector_by, selector_value))
                element = self.driver.find_element_by_link_text(selector_value)
            except:
                element = None
        elif selector_by == 'p' or selector_by == 'partial_link_text':
            try:
                _mylogger.info('开始通过{}查找元素{}'.format(selector_by, selector_value))
                element = self.driver.find_element_by_partial_link_text(selector_value)
            except:
                element = None
        elif selector_by == 'x' or selector_by == 'xpath':
            try:
                _mylogger.info('开始通过{}查找元素{}'.format(selector_by, selector_value))
                element = self.driver.find_element_by_xpath(selector_value)
            except:
                element = None
        elif selector_by == 's' or selector_by == 'selector_selector':
            try:
                _mylogger.info('开始通过{}查找元素{}'.format(selector_by, selector_value))
                element = self.driver.find_element_by_css_selector(selector_value)
            except:
                element = None
        return element

    def find_element(self, selector):
        '''
        本方法会先在default_content中查找，若页面存在iframe，没有定位到元素会遍历页面中所有的frame去查找元素
        :param selector:
        :return: element
        '''

        # 切到默认
        self.driver.switch_to_default_content()

        element = self.find(selector)
        if element is not None:
            return element

        # 判断页面中是否存在iframe，如果有就遍历
        iframes = self.driver.find_elements_by_tag_name('iframe')
        if iframes is None:
            _mylogger.error('未找到控件，发生异常')
            raise Exception('未找到控件，发生异常')
        for iframe in iframes:
            self.driver.switch_to.frame(iframe)
            _mylogger.info('default_content中未找到元素，切入{}继续查找'.format(iframe))
            element = self.find(selector)
            if element is not None:
                return element
        if element is None:
            _mylogger.error('查找元素失败')
            self.get_window_img()
            raise Exception('未找到控件，发生异常')

    def get(self, selector=None, text=None):
        self.driver.get(text)
        _mylogger.info('打开页面:{}'.format(text))
        self.sleep(1)

    def input(self, selector=None, text=None):
        if selector is None:
            _mylogger.error('请正确填写元素信息')

        else:
            el = self.find_element(selector)
            try:
                el.clear()
                el.send_keys(text)
                _mylogger.info('已输入{}'.format(text))
            except Exception as e:
                _mylogger.error('发生异常{}'.format(e))
                self.get_window_img()

    def click(self, selector=None, text=None):
        if selector is None:
            _mylogger.error('请正确填写元素信息')

        else:
            el = self.find_element(selector)
            try:
                el.click()
                _mylogger.info('已点击按钮')
            except Exception as e:
                _mylogger.error('发生异常{}'.format(e))
                self.get_window_img()

    def clear(self, selector=None, text=None):
        if selector is None:
            _mylogger.error('请正确填写元素信息')
        else:
            el = self.find_element(selector)
            try:
                el.clear()
                _mylogger.info('已清空输入框')
            except Exception as e:
                _mylogger.error('发生异常{}'.format(e))
                self.get_window_img()

    def seletor(self, selector=None, text=None):
        if selector is None:
            _mylogger.error('请正确填写元素信息')
        else:
            el = self.find_element(selector)
            try:
                el.click()
                selector = Select(el)
                selector.select_by_value(text)
                _mylogger.info('从下拉框中选择{}'.format(text))
            except Exception as e:
                _mylogger.error('发生异常{}'.format(e))
                self.get_window_img()

    # 或者网页标题
    def get_page_title(self, selector=None, text=None):
        _mylogger.info("Current page title is %s" % self.driver.title)
        return self.driver.title

    @staticmethod
    def sleep(seconds):
        time.sleep(seconds)
        _mylogger.info("Sleep for %d seconds" % seconds)


if __name__ == '__main__':
    driver = init_env().open_browser('Chrome')
    homepage = BasePage(driver)
    homepage.get('http://www.baidu.com')
    homepage.sleep(1)
    homepage.input('id=>kw', 'python')
    homepage.sleep(1)
    homepage.click('xpath=>//*[@id="su"]')
    homepage.sleep(1)
    homepage.quit_browser()
