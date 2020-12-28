# -*- coding: utf-8 -*-
# @Time    : 2020/9/1 16:25
# @Author  : 潘师傅
# @File    : Houses_casc.py

from PubilcAPI.flowPath import *
"""楼盘相关"""


class HousesTestCase(unittest.TestCase):
    """幸福派APP——楼盘相关"""

    def __init__(self, *args, **kwargs):
        super(HousesTestCase, self).__init__(*args, **kwargs)
        self.xfp_web = webApi()
        self.web_api = self.xfp_web

        self.xfp_app = appApi()
        self.app_api = self.xfp_app

        self.flow = flowPath()
        self.flowPath = self.flow

        self.appText = GlobalMap()
        self.webText = GlobalMap()

    @classmethod
    def setUpClass(cls):
        """登录幸福派 只执行一次"""
        cls.do_request = appApi()
        cls.appApi = cls.do_request
        cls.appApi.Login()
        cls.appApi.GetUserData()

    def test_AllBuildingUpdate(self):
        """全部楼盘"""
        try:
            self.app_api.AllBuildingUpdate()
            globals()['total'] = self.appText.get('total')
            self.app_api.AllBuildingUpdate(keyWord='ABCDEFG')
            self.assertNotEqual(globals()['total'], self.appText.get('total'))
        except BaseException as e:
                print("错误，错误原因：%s" % e)
                raise RuntimeError(self.appText.get('ApiXfpUrl'))

    def test_BusinessInformation(self):
        """商务信息"""
        try:
            self.app_api.BusinessInformation()
            globals()['total'] = self.appText.get('total')
            self.app_api.BusinessInformation(keyWord='ABCDEFG')
            self.assertNotEqual(globals()['total'], self.appText.get('total'))
        except BaseException as e:
            print("错误，错误原因：%s" % e)
            raise RuntimeWarning(self.appText.get('ApiXfpUrl'))

    def test_Information(self):
        """资料信息"""
        try:
            self.app_api.Information()
            globals()['total'] = self.appText.get('total')
            self.app_api.Information(keyWord='ABCDEFG')
            self.assertNotEqual(globals()['total'], self.appText.get('total'))
        except BaseException as e:
            print("错误，错误原因：%s" % e)
            raise RuntimeWarning(self.appText.get('ApiXfpUrl'))

    def test_HouseQA(self):
        """楼盘QA"""
        try:
            self.app_api.HouseQA()
            globals()['total'] = self.appText.get('total')
            self.app_api.HouseQA(keyWord='ABCDEFG')
            self.assertNotEqual(globals()['total'], self.appText.get('total'))
        except BaseException as e:
            print("错误，错误原因：%s" % e)
            raise RuntimeWarning(self.appText.get('ApiXfpUrl'))


