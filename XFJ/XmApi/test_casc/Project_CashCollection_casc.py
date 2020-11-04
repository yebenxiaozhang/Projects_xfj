# -*- coding: utf-8 -*-
# @Time    : 2019/11/29 9:43
# @Author  : 潘师傅
# @File    : Project_CashCollection_casc.py
"""现金收款/付款"""
"""
1、只收款：大于 | 小于
2、只收款：等于
3、只付款：大于 | 小于
4、只付款：等于
5、收款付款：收款大于总佣金、付款大于联盟商总佣金 | 收款大于联盟商总佣金、付款小于联盟商总佣金
6、收款付款：收款大于总佣金、付款等于联盟商总佣金
7、收款付款：收款小于总佣金、付款大于联盟商总佣金 | 收款小于总佣金、付款小于联盟商总佣金
8、收款付款：收款小于总佣金、付款等于联盟商总佣金
9、收款付款：收款等于总佣金、付款大于联盟商总佣金 | 收款等于总佣金、付款小于联盟商总佣金
10、收款付款：收款等于总佣金、付款等于联盟商总佣金
11、两次以上录入？是否可以超过总的联盟商总价？
"""

from XFJ.PubilcAPI.FlowPath import *


class CashCollection(unittest.TestCase):
    """小秘----项目---现金收款/付款"""
    def __init__(self, *args, **kwargs):
        super(CashCollection, self).__init__(*args, **kwargs)
        self.do_request = XmApi()
        self.XmRequest = self.do_request
        self.XmTEXT = GlobalMap()
        self.AgentRequest = AgentApi()
        self.ToAgentRequest = self.AgentRequest
        self.AgentTEXT = GlobalMap()
        self.Xfk_request = XfkApi()
        self.XfkRequest = self.Xfk_request
        self.XfkTEXT = GlobalMap()
        self.FlowPath = FlowPath()
        self.FlowPath = self.FlowPath
        self.city = LogIn()
        self.City = self.city
        self.Web = WebTools()
        self.WebTooles = self.Web

    @classmethod
    def setUpClass(cls):
        """登录小秘 只执行一次
        登录经纪人 获取ID"""
        cls.do_request = XmApi()
        cls.XmRequest = cls.do_request
        cls.XmRequest.ApiLogin()
        cls.request = AgentApi()
        cls.AgentRequest = cls.request
        cls.AgentRequest.LoginAgent()
        cls.AgentRequest.ForRegistrationID()
        cls.do_request = XfkApi()
        cls.to_request = cls.do_request
        cls.to_request.LoginXfk()

    def test_CashCollection(self):
        """随机账户---现金收款 大于 | 小于 ==>随机"""
        AGENTUSER = [AgentUser1, AgentUser5]
        dome = self.XmRequest.RandomText(AGENTUSER)
        dome1 =self.XmRequest.RandomText([1, -1])
        try:
            self.FlowPath.TheNewDeal(user=dome)
            self.FlowPath.DealTicket()
            self.XmRequest.ResultsTheChangeStayList(projectId=self.AgentTEXT.get('projectId'), excludeType=2,
                                                    keyWord=self.XfkTEXT.get('RoomNoStr'))
            self.XmRequest.CashCollectionEntering(isCashRefund=1, cashPic=img + ',' + img, value=dome1)
            # self.assertEqual(0, self.XmTEXT.get('resultCode'))  # 大于
            # self.XmRequest.CashCollectionEntering(isCashRefund=1, cashPic=img + ',' + img, value=-1)
            self.assertEqual(1, self.XmTEXT.get('resultCode'))  # 小于
            """录入成功后 查看列表"""
            self.FlowPath.TheReceivableReview()
        except BaseException as e:
            print("错误，错误原因：%s" % e)
            raise RuntimeError(self.XmTEXT.get('xmurl'))

    def test_CashCollection_1(self):
        """现金收款 只收款：等于"""
        AGENTUSER = [AgentUser1, AgentUser5]
        dome = self.XmRequest.RandomText(AGENTUSER)
        try:
            self.FlowPath.TheNewDeal(user=dome)
            self.FlowPath.DealTicket()
            self.XmRequest.ResultsTheChangeStayList(projectId=self.AgentTEXT.get('projectId'), excludeType=2,
                                                    keyWord=self.XfkTEXT.get('RoomNoStr'))
            self.XmRequest.CashCollectionEntering(isCashRefund=1, cashPic=img + ',' + img, value=0)
            self.assertEqual(1, self.XmTEXT.get('resultCode'))  # 小于
            """录入成功后 查看列表"""
            self.FlowPath.TheReceivableReview()
        except BaseException as e:
            print("错误，错误原因：%s" % e)
            raise RuntimeError(self.XmTEXT.get('xmurl'))

    def test_CashCollection_2(self):
        """只付款：大于 | 小于"""
        # AGENTUSER = [AgentUser1, AgentUser5]
        # dome = self.XmRequest.RandomText(AGENTUSER)
        try:
            # self.FlowPath.TheNewDeal(user=dome)
            # self.FlowPath.DealTicket()
            self.XmRequest.ResultsTheChangeStayList(projectId=self.AgentTEXT.get('projectId'), excludeType=2,
                                                    keyWord=self.XfkTEXT.get('RoomNoStr'))
            # self.XmRequest.CashCollectionEntering(isCashRefund=0, cashPic=img + ',' + img, value1=1)
            # self.assertEqual(0, self.XmTEXT.get('resultCode'))  # 大于
            self.XmRequest.CashCollectionEntering(isCashRefund=0, cashPic=img + ',' + img, value1=-1)
            self.assertEqual(1, self.XmTEXT.get('resultCode'))  # 小于
            """录入成功后 查看列表"""
            self.FlowPath.TheReceivableReview()
        except BaseException as e:
            print("错误，错误原因：%s" % e)
            raise RuntimeError(self.XmTEXT.get('xmurl'))

    def test_CashCollection_3(self):
        """只付款：等于"""
        AGENTUSER = [AgentUser1, AgentUser5]
        dome = self.XmRequest.RandomText(AGENTUSER)
        try:
            self.FlowPath.TheNewDeal(user=dome)
            self.FlowPath.DealTicket()
            self.XmRequest.ResultsTheChangeStayList(projectId=self.AgentTEXT.get('projectId'), excludeType=2,
                                                    keyWord=self.XfkTEXT.get('RoomNoStr'))
            # self.XmRequest.CashCollectionEntering(isCashRefund=0, cashPic=img + ',' + img, value1=1)
            # self.assertEqual(0, self.XmTEXT.get('resultCode'))  # 大于
            self.XmRequest.CashCollectionEntering(isCashRefund=0, cashPic=img + ',' + img, value1=0)
            self.assertEqual(1, self.XmTEXT.get('resultCode'))  # 等于
            """录入成功后 查看列表"""
            self.FlowPath.TheReceivableReview()
        except BaseException as e:
            print("错误，错误原因：%s" % e)
            raise RuntimeError(self.XmTEXT.get('xmurl'))

    def test_CashCollection_4(self):
        """收款付款，收款金额等于佣金，付款金额等于佣金"""
        AGENTUSER = [AgentUser1, AgentUser5]
        dome = self.XmRequest.RandomText(AGENTUSER)
        try:
            self.FlowPath.TheNewDeal(user=dome)
            self.FlowPath.DealTicket()
            self.XmRequest.ResultsTheChangeStayList(projectId=self.AgentTEXT.get('projectId'), excludeType=2,
                                                    keyWord=self.XfkTEXT.get('RoomNoStr'))
            # self.XmRequest.CashCollectionEntering(isCashRefund=0, cashPic=img + ',' + img, value1=1)
            # self.assertEqual(0, self.XmTEXT.get('resultCode'))  # 大于
            self.XmRequest.CashCollectionEntering(isCashRefund=1, meanwhile=1, cashPic=img + ',' + img, value1=0, value=0)
            self.assertEqual(1, self.XmTEXT.get('resultCode'))  # 等于
            """录入成功后 查看列表"""
            self.FlowPath.TheReceivableReview()
        except BaseException as e:
            print("错误，错误原因：%s" % e)
            raise RuntimeError(self.XmTEXT.get('xmurl'))

