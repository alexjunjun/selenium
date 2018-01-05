# coding = UTF-8
import os

import time

from lib.base_page import BasePage
from lib.log_config import get_logger
from lib.read_config import readConfig

_mylogger = get_logger(os.path.basename(__file__))
class SpecialMethods(BasePage):
    def __init__(self, driver):
        # self.driver = driver
        super().__init__(driver)

    def chose_fundManager(self, selector=None, text=None):
        value = readConfig('constant','const','FUNDMANAGER')
        try :
            _mylogger.info(u'选择基金经理')
            element = self.find_element(selector)
            element.click()
            time.sleep(0.5)
            element.find_element_by_xpath(value).click()
            # 向上滚动
            self.driver.execute_script("window.scrollTo(0,0)")
        except Exception as e :
            _mylogger.error('发生异常：{}'.format(e))

    def chose_customerName(self, selector=None, text=None):
        value = readConfig('constant','const','CUSTOMERNAME')
        try :
            _mylogger.info(u'选择客户名称')
            element = self.find_element(selector)
            element.click()
            time.sleep(0.5)
            element.find_element_by_xpath(value).click()

        except Exception as e :
            _mylogger.error('发生异常：{}'.format(e))

    def chose_product(self, selector=None, text=None):
        value = readConfig('constant','const','PRODUCT')
        try :
            _mylogger.info(u'选择产品')
            element = self.find_element(selector)
            element.click()
            time.sleep(0.5)
            element.find_element_by_xpath(value).click()

        except Exception as e :
            _mylogger.error('发生异常：{}'.format(e))
