# -*- coding: utf-8 -*-
# @Time    : 2019/11/22 16:54
# @Author  : 潘师傅
# @File    : WebTools.py
import os
import sys
import time
import unittest

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

# from Common.readdata import ReadData as R

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(ROOT_DIR)


class WebTools(object):
    def __init__(self):
        self.browser_type = 'Chrome'

    # 跳转页面
    def Jumpwebpage(self, page, time_wait=3):
        # self.driver.get(self.Getwebpage(page))
        self.driver.maximize_window()

        if isinstance(time_wait, int):
            time.sleep(time_wait)

    # def Getwebpage(self, page):
    #     return R.ReadXmlData("%s.xml" % page, "page", 0, "url")

    # 浏览器前进操作
    def forward(self):
        self.driver.forward()

    # 浏览器后退操作
    def back(self):
        self.driver.back()

    # 隐式等待
    def wait(self, seconds):
        self.driver.implicitly_wait(seconds)

    # 保存图片
    def get_windows_img(self):
        """
        在这里我们把file_path这个参数写死，直接保存到我们项目根目录的一个文件夹.\Screenshots下
        """
        file_path = os.path.dirname(os.path.abspath('.')) + '/screenshots/'
        rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
        screen_name = file_path + rq + '.png'
        try:
            self.driver.get_screenshot_as_file(screen_name)
        except NameError as e:
            self.get_windows_img()

    def Current_handel(self):
        # 这时切换到新窗口
        all_handles = self.driver.window_handles
        for handle in all_handles:
            self.driver.switch_to.window(handle)

    def NewIframe(self, value):
        """切换新的表单"""
        New = self.driver.find_element_by_css_selector(value)
        self.driver.switch_to.frame(New)

    def QuitIframe(self):
        """推出表单"""
        self.driver.switch_to.default_content()

    # 打开浏览器的方法
    def Openbrowser(self):
        if self.browser_type == 'Firefox':
            self.driver = webdriver.Firefox()
        elif self.browser_type == 'Chrome':
            self.driver = webdriver.Chrome()
        elif self.browser_type == 'IE':
            self.driver = webdriver.Ie()
        elif self.browser_type == '':
            self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    def element(self, *loc):
        try:
            WebDriverWait(self.driver, 5, 0.3).until(
                EC.visibility_of_element_located(loc))
            return self.driver.find_element(*loc)
        except:
            print('%s无法定位到元素%s' % (self, loc))

    # 输入内容方法
    def Input(self, type, value, inputvalue):
        if type == "xpath":
            self.driver.find_element_by_xpath(value).send_keys(inputvalue)
        elif type == "class_name":
            self.driver.find_element_by_class_name(value).send_keys(inputvalue)
        elif type == "id":
            WebDriverWait(self.driver, 5, 0.3).until(
                lambda the_driver: the_driver.find_element(type, value).is_displayed())
            self.driver.find_element_by_id(value).send_keys(inputvalue)
        elif type == "name":
            self.driver.find_element_by_name(value).send_keys(inputvalue)
        elif type == "link_text":
            self.driver.find_element_by_link_text(value).send_keys(inputvalue)
        elif type == "partial_link_text":
            self.driver.find_element_by_partial_link_text(value).send_keys(inputvalue)
        elif type == "classs":
            self.driver.find_elements_by_class_name(value)[3].send_keys(inputvalue)

    # 鼠标事件方法一
    def Click(self, type, value, several=0, skip=0):
        # skip  跳转到元素的位置
        if type == "xpath":
            self.WebDriverWait(type=By.XPATH, value=value)
            self.driver.find_element_by_xpath(value).click()
            time.sleep(0.5)
        elif type == "class_name" or type == 'class':
            self.WebDriverWait(type=By.CLASS_NAME, value=value)
            self.driver.find_element_by_class_name(value).click()
        elif type == "id":
            self.WebDriverWait(type=By.ID, value=value)
            if skip == 1:
                target = self.driver.find_element(By.ID, value=value)
                self.driver.execute_script('arguments[0].scrollIntoView();', target)
            time.sleep(0.5)
            self.driver.find_element_by_id(value).click()
            time.sleep(0.5)
        elif type == "name":
            self.WebDriverWait(type=By.NAME, value=value)
            self.driver.find_element_by_name(value).click()
        elif type == "link_text":
            self.WebDriverWait(type=By.LINK_TEXT, value=value)
            self.driver.find_element_by_link_text(value).click()
        elif type == "link_texts":
            self.WebDriverWait(type=By.LINK_TEXT, value=value)
            self.driver.find_elements_by_link_text(value)[several].click()
        elif type == "partial_link_text":
            self.WebDriverWait(type=By.PARTIAL_LINK_TEXT, value=value)
            self.driver.find_element_by_partial_link_text(value).click()

    # 鼠标事件方法二
    def Clear(self, type, value):
        if type == "xpath":
            self.driver.find_element_by_xpath(value).clear()
        elif type == "id":
            self.driver.find_element_by_id(value).clear()
        elif type == "name":
            self.driver.find_element_by_name(value).clear()
        elif type == "link_text":
            self.driver.find_element_by_link_text(value).clear()
        elif type == "partial_link_text":
            self.driver.find_element_by_partial_link_text(value).clear()

    # 验证元素是否存在
    def Check_element(self, type, value):
        if type == "xpath":
            self.driver.find_element_by_xpath(value)
        elif type == "id":
            self.driver.find_element_by_id(value)
        elif type == "name":
            self.driver.find_element_by_name(value)
        elif type == "link_text":
            self.driver.find_element_by_link_text(value)
        elif type == "partial_link_text":
            self.driver.find_element_by_partial_link_text(value)

    # 获取子元素
    def Select_child_elements(self, type, value1, value2):
        if type == "xpath":
            Select(self.driver.find_element_by_xpath(value1)).select_by_visible_text(value2)
        elif type == "id":
            Select(self.driver.find_element_by_id(value1)).select_by_visible_text(value2)
        elif type == "name":
            Select(self.driver.find_element_by_name(value1)).select_by_visible_text(value2)
        elif type == "link_text":
            Select(self.driver.find_element_by_link_text(value1)).select_by_visible_text(value2)
        elif type == "partial_link_text":
            Select(self.driver.find_element_by_partial_link_text(value1)).select_by_visible_text(value2)

    # 获取输入框的值
    def Get_attribute(self, type, value1, value2):
        if type == "xpath":
            Value = self.driver.find_element_by_xpath(value1).get_attribute(value2)
            return Value
        elif type == "name":
            Value = self.driver.find_element_by_name(value1).get_attribute(value2)
            return Value
        elif type == "link_text":
            Value = self.driver.find_element_by_link_text(value1).get_attribute(value2)
            return Value
        elif type == "class_name":
            Value = self.driver.find_element_by_class_name(value1).get_attribute(value2)
            return Value
        elif type == "id":
            Value = self.driver.find_element_by_id(value1).get_attribute(value2)
            return Value

            # 获取下拉框的文本的值

    def GetText(self, type, value):
        if type == "xpath":
            text = self.driver.find_element_by_xpath(value).text
            return text
        elif type == "name":
            text = self.driver.find_element_by_name(value).text
            return text
        elif type == "link_text":
            text = self.driver.find_element_by_link_text(value).text
            return text
        elif type == "class_name":
            text = self.driver.find_element_by_class_name(value).text
            return text
        elif type == "id":
            text = self.driver.find_element_by_id(value).text
            return text

    # 显性等待时间
    def WebDriverWait(self, type, value):
        WebDriverWait(self.driver, 5, 0.3).until(
            lambda the_driver: the_driver.find_element(type, value).is_displayed())

        # element = self.driver.find_element(type, value)
        # WebDriverWait(self.driver, MaxTime, Mimtime).until(EC.presence_of_element_located(element))

    # # 鼠标移动点击机制
    def MoveAction(self, type, value):
        if type == "xpath":
            xm = self.driver.find_element_by_xpath(value)
            webdriver.ActionChains(self.driver).click(xm).perform()
        elif type == "id":
            xm = self.driver.find_element_by_id(value)
            webdriver.ActionChains(self.driver).click(xm).perform()
        elif type == "name":
            xm = self.driver.find_element_by_name(value)
            webdriver.ActionChains(self.driver).click(xm).perform()
        elif type == "link_text":
            xm = self.driver.find_element_by_link_text(value)
            webdriver.ActionChains(self.driver).click(xm).perform()

    # 校验按钮是否为选中状态
    def IsSelected(self, type, value):
        if type == "id":
            self.driver.find_element_by_id(value).is_selected()
        elif type == "xpath":
            self.driver.find_element_by_xpath(value).is_selected()
        elif type == "class_name":
            self.driver.find_element_by_class_name(value).is_selected()
        elif type == "name":
            self.driver.find_element_by_name(value).is_selected()
        elif type == "link_text":
            self.driver.find_element_by_link_text(value).is_selected()
