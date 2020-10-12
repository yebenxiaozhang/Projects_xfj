# -*- coding: utf-8 -*-
# @Time    : 2020/3/21 11:08
# @Author  : 潘师傅
# @File    : My_Deal_casc.py

"""我的成交-相关"""
from XFP.PubilcAPI.flowPath import *

"""
无审核-正常流程：····························· 流放公海状态
    1、录入成交          已确认                    已确认
一级审核-正常流程：·····································流放公海的状态
    1、录入成交-待审核          审核中                         审核中
    2、录入成交-审核失败        已驳回                         已驳回
    3、录入成交-审核成功        已确认                         已确认

二级审核-正常流程······································流放公海的状态
    1、录入成交-待审核          申请中                         申请中
    2、录入成交-一级审核失败    已驳回                         已驳回
    3、录入成交-一级审核成功    审核中                         审核中
    4、录入成交-二级审核成功    已确认                         已确认
    5、录入成交-二级审核失败    已驳回                         已驳回

操作事项：
    1、审核中的成交                ---不允许操作
    2、修改成交后（如设置审核）    ---需重新审核
    3、已确认的成交                ---不允许删除？或需要审核？
    
"""


class MyDealTestCase(unittest.TestCase):
    """幸福派——我的带看"""

    def __init__(self, *args, **kwargs):
        super(MyDealTestCase, self).__init__(*args, **kwargs)
        self.xfp_web = webApi()
        self.webApi = self.xfp_web

        self.xfp_app = appApi()
        self.appApi = self.xfp_app

        self.flow = flowPath()
        self.flowPath = self.flow

    @classmethod
    def setUpClass(cls):
        """登录幸福派 只执行一次
        登录幸福派 获取ID"""
        cls.do_request = appApi()
        cls.app_api = cls.do_request
        cls.app_api.Login()
        cls.app_api.GetUserData()
        cls.request = webApi()
        cls.webApi = cls.request
        cls.webApi.Audit_management()
