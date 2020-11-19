# -*- coding: utf-8 -*-
# @Time    : 2019/11/5 17:09
# @Author  : 潘师傅
# @File    : Project_ResultsTheChange_casc.py
from XFJ.PubilcAPI.FlowPath import *
"""主要有---
--------调价
--------挞定----：挞定后不能再次挞定
--------修改业主信息-------手机号码尚未做限制  不需要审核
--------换房"""


class ResultsTheChangeTestCace(unittest.TestCase):
    """小秘----项目---业绩变更"""
    def __init__(self, *args, **kwargs):
        super(ResultsTheChangeTestCace, self).__init__(*args, **kwargs)
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

    @classmethod
    def tearDownClass(cls):
        """所用用例执行之后的操作"""
        pass

    def test_1_ResultsTheChangeChangeHouseIdentical(self):
        """相同房号"""
        self.FlowPath.ResultsTheChange(TypeValue='换房', repetition=1)
        self.assertEqual(0, self.XmTEXT.get('resultCode'))

    def test_RandomUserTartSet(self):
        """随机账户 ---挞定"""
        AGENTUSER = [AgentUser1, AgentUser3, AgentUser5, AgentUser7, AgentUser9]
        dome = self.XmRequest.RandomText(AGENTUSER)
        try:
            self.FlowPath.ResultsTheChange(user=dome, TypeValue='挞定')
            self.assertEqual(1, self.XmTEXT.get('resultCode'))
        except BaseException as e:
            print("错误，错误原因：%s" % e)
            print(dome)
            raise RuntimeError(self.XmTEXT.get('xmurl'))

    def test_RandomUserAlterTheownerinformation(self):
        """随机账户 ---更名"""
        AGENTUSER = [AgentUser1, AgentUser3, AgentUser5, AgentUser7, AgentUser9]
        dome = self.XmRequest.RandomText(AGENTUSER)
        try:
            self.FlowPath.ResultsTheChange(user=dome, TypeValue='更名',
                                           signTime=time.strftime("%Y-%m-%d"))
            self.assertEqual(1, self.XmTEXT.get('resultCode'))
        except BaseException as e:
            print("错误，错误原因：%s" % e)
            print(dome)
            raise RuntimeError(self.XmTEXT.get('xmurl'))

    def test_RandomUserPriceAdjustment(self):
        # self.FlowPath.ResultsTheChange()
        """随机账户 ---调价及调佣"""
        AGENTUSER = [AgentUser1, AgentUser3, AgentUser5, AgentUser7, AgentUser9]
        dome = self.XmRequest.RandomText(AGENTUSER)
        try:
            self.FlowPath.ResultsTheChange(user=dome)
            self.assertEqual(1, self.XmTEXT.get('resultCode'))
            print(dome)
        except BaseException as e:
            print("错误，错误原因：%s" % e)
            print(dome)
            raise RuntimeError(self.XmTEXT.get('xmurl'))

    def test_RandomUserResultsTheChangeRoomChange(self):
        """随机账户--换房"""
        AGENTUSER = [AgentUser1, AgentUser3, AgentUser5, AgentUser7, AgentUser9]
        dome = self.XmRequest.RandomText(AGENTUSER)
        try:
            self.FlowPath.ResultsTheChange(user=dome, TypeValue='换房')
            if self.XmTEXT.get('xmcontent') == '应付佣金超过了应收代理费':
                pass
            else:
                self.assertEqual(1, self.XmTEXT.get('resultCode'))
        except BaseException as e:
            print("错误，错误原因：%s" % e)
            raise RuntimeError(self.XmTEXT.get('xmurl'))

    def test_RandomUserBetterBillingCompany(self):
        """随机账户--更换开票公司"""
        AGENTUSER = [AgentUser1, AgentUser3, AgentUser5, AgentUser7, AgentUser9]
        dome = self.XmRequest.RandomText(AGENTUSER)
        try:
            self.FlowPath.ResultsTheChange(user=dome, TypeValue='更换开票公司',remark=time.strftime("%Y-%m-%d"))
            self.assertEqual(1, self.XmTEXT.get('resultCode'))
        except BaseException as e:
            print("错误，错误原因：%s" % e)
            print(dome)
            raise RuntimeError(self.XmTEXT.get('xmurl'))

    def test_002(self):
        """备注为空-申请修改备注是否报错"""

    def test_003(self):
        """变更成功后，从换房的详情查看，与调价中查看"""
    # def test_(self):
    #     test = 1
    #     while test != 200:
    #         # AGENTUSER = [AgentUser1, AgentUser3, AgentUser5, AgentUser7, AgentUser9]
    #         # dome = self.XmRequest.RandomText(AGENTUSER)
    #
    #         self.FlowPath.DealTicket()
    #         test = test + 1
    #     # self.FlowPath.DealTicket()


