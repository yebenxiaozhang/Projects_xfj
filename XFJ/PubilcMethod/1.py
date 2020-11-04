# -*- coding: utf-8 -*-
# @Time    : 2019/11/15 14:36
# @Author  : 潘师傅
# @File    : FlowPath.py
"""幸福家主要流程"""
from XFJ.GlobalMap import GlobalMap
from XFJ.PubilcAPI.XmApi import *
from XFJ.PubilcAPI.AgentAPI import *
from XFJ.PubilcAPI.XfkApi import *
from XFJ.PubilcMethod.HandleRequest import *
from XFJ.PubilcMethod.LogIn import *
from XFJ.PubilcMethod.WebTools import *
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait

import json


class FlowPath:
    """小秘----成交确认"""
    def __init__(self, *args, **kwargs):
        super(FlowPath, self).__init__(*args, **kwargs)
        self.do_request = XmApi()
        self.XmRequest = self.do_request
        self.XmTEXT = GlobalMap()
        self.Agent_request = AgentApi()
        self.AgentRequest = self.Agent_request
        self.AgentTEXT = GlobalMap()
        self.Xfk_request = XfkApi()
        self.XfkRequest = self.Xfk_request
        self.XfkTEXT = GlobalMap()
        self.NRTEXT = HandleRequest()
        self.TEXT = self.NRTEXT
        self.NRTEXT = GlobalMap()
        self.city = LogIn()
        self.City = self.city
        self.Web = WebTools()
        self.WebTooles = self.Web

    @classmethod
    def setUpClass(cls):
        """登录小秘、幸福客 只执行一次"""
        cls.do_request = XmApi()
        cls.to_request = cls.do_request
        cls.to_request.ApiLogin()
        cls.do_request = XfkApi()
        cls.to_request = cls.do_request
        cls.to_request.LoginXfk()



    def CityEstablishMessage(self):
        """新成交--城市发票申请"""
        self.WebTooles.Openbrowser()
        self.city.LogIn(method='City', d=self.WebTooles.driver)


if __name__ == '__main__':
    a = FlowPath()
