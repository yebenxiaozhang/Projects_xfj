# 先引入
from selenium import webdriver
import time
from selenium.webdriver.support.wait import WebDriverWait

# 访问谷歌浏览器
URL = "http://city.ykb100.com/"
driver = webdriver.Chrome()
driver.maximize_window()
driver.get(URL)
# cookie用字典存储
driver.find_element_by_css_selector('#j_username').send_keys("17605087327")
driver.find_element_by_css_selector('#j_password').send_keys("123456")
time.sleep(2)
WebDriverWait(driver, 5, 0.3).until(
    lambda the_driver: the_driver.find_element_by_class_name('btn-primary').is_displayed())
driver.find_elements_by_class_name('btn-primary')[0].click()
driver.find_element_by_css_selector('#showCityName').click()
driver.find_element_by_link_text('珠海').click()
WebDriverWait(driver, 5, 0.3).until(
    lambda the_driver: the_driver.find_element_by_link_text('结算中心').is_displayed())
driver.find_element_by_link_text('结算中心').click()
a = 0
dome = driver.find_elements_by_class_name('hidden-tablet')[a].text
while dome == " 回款管理":
    a = a + 1
    dome = driver.find_elements_by_class_name('hidden-tablet')[a].text
target = driver.find_elements_by_class_name('hidden-tablet')[a]
driver.execute_script('arguments[0].scrollIntoView();', target)
driver.find_elements_by_class_name('hidden-tablet')[a].click()

a = 0
dome = driver.find_elements_by_class_name('btn-success')[a].text
while dome == '回款':
    a = a + 1
    dome = driver.find_elements_by_class_name('btn-success')[a].text
target = driver.find_elements_by_class_name('hidden-tablet')[a]
driver.execute_script('arguments[0].scrollIntoView();', target)
driver.find_elements_by_class_name('hidden-tablet')[a].click()



