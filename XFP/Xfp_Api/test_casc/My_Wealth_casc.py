# -*- coding: utf-8 -*-
# @Time    : 2020/3/21 11:08
# @Author  : 潘师傅
# @File    : My_Wealth_casc.py

"""客户相关"""
from XFP.PubilcAPI.webApi import *


class MyWealthTestCase(unittest.TestCase):
    """幸福派——客户列表"""

    def __init__(self, *args, **kwargs):
        super(MyWealthTestCase, self).__init__(*args, **kwargs)
        self.xfp_web = webApi()
        self.webApi = self.xfp_web

        self.xfp_app = appApi()
        self.appApi = self.xfp_app

        self.appText = GlobalMap()
        self.webText = GlobalMap()

    @classmethod
    def setUpClass(cls):
        """登录幸福派 只执行一次
        登录幸福派 获取ID"""
        cls.do_request = appApi()
        cls.app_api = cls.do_request
        cls.app_api.Login()
        cls.app_api.GetUserData()
    #     cls.request = webApi()
    #     cls.webApi = cls.request
    #     cls.webApi.Audit_management()

    def test_01(self):
        """11"""
        self.appApi.my_Wealth()


