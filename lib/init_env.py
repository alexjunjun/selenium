# coding = utf-8
'''
用于初始化浏览器，并新建浏览器driver
'''
import os

from selenium import webdriver

from lib.log_config import get_logger

_mylogger = get_logger(os.path.basename(__file__))
class init_env():
    def __init__(self):
        pass
    def open_browser(self, browser = 'chrome'):
        if str.lower(browser) == 'chrome':
            driver = webdriver.Chrome()
            _mylogger.info(u'chrome浏览器已经申明')
        elif str.lower(browser) == 'firefox':
            driver = webdriver.Firefox()
            _mylogger.info(u'firefox浏览器已经申明')
        elif str.lower(browser) == 'ie':
            driver = webdriver.Ie()
            _mylogger.info(u'ie浏览器已经申明')
        else :
            _mylogger.warning(u'不知道的浏览器')
            exit()
        driver.maximize_window()
        return driver