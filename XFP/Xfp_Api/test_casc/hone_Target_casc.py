# -*- coding: utf-8 -*-
# @Time    : 2020/3/21 10:48
# @Author  : 潘师傅
# @File    : Hone_casc.py

"""用户相关"""
from XFP.PubilcAPI.appApi import *
"""
1、新增线索，上户数量是否新增，线索转客户是否新增
2、直接新增客户，上户数量是否新增
3、公海领取线索，上户数量是否新增
4、公海领取客户，上户数量是否新增
5、客户创建带看，带看次数是否新增
6、客户重复创建带看，带看是否继续新增
7、录入成交（认筹）以外，其他类型，认购是否新增
8、录入成交（网签）以外，其他类型，签约是否新增
9、录入成交的客户，流放公海，首页的信息是否会变
"""


class HomeTestCase(unittest.TestCase):
    """小秘——客户列表"""

    def __init__(self, *args, **kwargs):
        super(HomeTestCase, self).__init__(*args, **kwargs)
        self.XfpRequest = appApi()
        self.XmfpEXT = GlobalMap()

    @classmethod
    def setUpClass(cls):
        """登录幸福派 只执行一次
        登录经纪人 获取ID"""
        cls.do_request = appApi()
        cls.XmRequest = cls.do_request
        cls.XmRequest.Login()
        cls.XmRequest.GetUserData()

    def test_GetUserData(self):
        """获取咨询师信息"""
        self.XfpRequest.GetUserData()
        self.assertEqual('潘师傅', self.XmfpEXT.get('consultantName'))
        self.assertNotEqual('', self.XmfpEXT.get('consultantLabels'))

    def test_GetUserAgenda(self):
        """获取咨询师待办"""
        self.XfpRequest.GetUserAgenda(endTime='2020-09-07')

    def test_GetUserEmploymentObjective(self):
        """获取咨询师工作目标"""
        self.XfpRequest.GetUserEmploymentObjective()

    def test_intersectError(self):
        """今日上户咨询师A流放公海登录咨询师B查看今日上户是否存在"""

