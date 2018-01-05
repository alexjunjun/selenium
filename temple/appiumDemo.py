# coding =UTF-8

from appium import webdriver

desired_caps ={}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '5.1'
desired_caps['deviceName'] = 'SGAMHA6D99999999'
desired_caps['appPackage'] = 'com.android.calculator2'
desired_caps['appActivity'] = '.Calculator'

driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
# driver.find_element_by_id('cancel').click()
# driver.find_element_by_id('digit1').click()
# driver.find_element_by_id('digit5').click()
# driver.find_element_by_id('digit9').click()
# driver.press_keycode(112)
# driver.press_keycode(13)
# # driver.find_element_by_id('del').click()
# driver.close_app()
# # print(driver.getContext())
# driver.launch_app()
#
# driver.find_element_by_id('digit9').click()
# driver.find_element_by_id('digit5').click()
# driver.find_element_by_id('plus').click()
# driver.find_element_by_id('digit6').click()
# driver.find_element_by_id('equal').click()
print(driver.contexts)
print(driver.page_source)

driver.quit()

