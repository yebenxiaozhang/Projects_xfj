# -*- coding: utf-8 -*-
# @Time    : 2020/3/9 14:52
# @Author  : 潘师傅
# @File    : User_casc.py

"""用户相关"""
from XFP.PubilcAPI.appApi import *


class UserTestCase(unittest.TestCase):
    """幸福派——用户相关"""

    def __init__(self, *args, **kwargs):
        super(UserTestCase, self).__init__(*args, **kwargs)
        self.XfpRequest = appApi()
        self.XmfpEXT = GlobalMap()

    @classmethod
    def setUpClass(cls):
        """登录幸福派 只执行一次
        登录经纪人 获取ID"""

    def test_Login_Pass(self):
        """登录"""
        self.XfpRequest.Login()
        self.XfpRequest.GetUserData()
        self.assertEqual(self.XmfpEXT.get('msg'), '成功')

    def test_UserIsNone(self):
        """用户名为空"""
        self.XfpRequest.Login(userName='')
        self.assertEqual(self.XmfpEXT.get('data'), '用户名或密码不正确')

    def test_PwdIsNone(self):
        """密码为空"""
        self.XfpRequest.Login(password='')
        self.assertEqual(self.XmfpEXT.get('data'), '用户名或密码不正确')

    def test_UserAndPwdNone(self):
        """用户名密码都为空"""
        self.XfpRequest.Login(userName='', password='')
        self.assertEqual(self.XmfpEXT.get('data'), '用户名或密码不正确')

    def test_UserError(self):
        """用户名不正确"""
        self.XfpRequest.Login(userName='11111111111')
        self.assertEqual(self.XmfpEXT.get('data'), '用户名或密码不正确')

    def test_PsdError(self):
        """密码错误"""
        self.XfpRequest.Login(password='11111111')
        self.assertEqual(self.XmfpEXT.get('data'), '用户名或密码不正确')

    def test_UserAndPwdError(self):
        """用户名密码都错误"""
        self.XfpRequest.Login(userName='11111111111', password='11111111')
        self.assertEqual(self.XmfpEXT.get('data'), '用户名或密码不正确')



