# -*- coding: utf-8 -*-
# @Time    : 2019/12/9 16:39
# @Author  : 潘师傅
# @File    : Project_DealPrecollected.py

from XFJ.PubilcAPI.FlowPath import *


class DealPrecollected(unittest.TestCase):
    """小秘----项目---预收预付"""
    def __init__(self, *args, **kwargs):
        super(DealPrecollected, self).__init__(*args, **kwargs)
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

    def test_Receivable(self):
        """录入预收"""
        AGENTUSER = [AgentUser1, AgentUser5]
        dome = self.XmRequest.RandomText(AGENTUSER)
        try:
            self.FlowPath.TheNewDeal(user=dome)
            self.FlowPath.DealTicket()
            self.XmRequest.ResultsTheChangeStayList(projectId=self.AgentTEXT.get('projectId'), excludeType=3,
                                                    keyWord=self.XfkTEXT.get('RoomNoStr'))
            self.XmRequest.PrecollectedApply(isAdvanceCollect=1)
            self.FlowPath.TheReceivableReview(tpyeName='预收预付')    # 审核及检查
        except BaseException as e:
                print("错误，错误原因：%s" % e)
                raise RuntimeError(self.XmTEXT.get('xmurl'))

    def test_Payment(self):
        """录入预付"""
        AGENTUSER = [AgentUser1, AgentUser5]
        dome = self.XmRequest.RandomText(AGENTUSER)
        try:
            self.FlowPath.TheNewDeal(user=dome)
            self.FlowPath.DealTicket()
            self.XmRequest.ResultsTheChangeStayList(projectId=self.AgentTEXT.get('projectId'), excludeType=3,
                                                    keyWord=self.XfkTEXT.get('RoomNoStr'))
            self.XmRequest.PrecollectedApply()
            self.FlowPath.TheReceivableReview(tpyeName='预收预付')    # 审核及检查
        except BaseException as e:
                print("错误，错误原因：%s" % e)
                raise RuntimeError(self.XmTEXT.get('xmurl'))

    def test_ReceivableAndPayment(self):
        """录入预付和预付"""
        AGENTUSER = [AgentUser1, AgentUser5]
        dome = self.XmRequest.RandomText(AGENTUSER)
        try:
            self.FlowPath.TheNewDeal(user=dome)
            self.FlowPath.DealTicket()
            self.XmRequest.ResultsTheChangeStayList(projectId=self.AgentTEXT.get('projectId'), excludeType=3,
                                                    keyWord=self.XfkTEXT.get('RoomNoStr'))
            self.XmRequest.PrecollectedApply(isAdvanceCollect=1, meanwhile=1)
            self.FlowPath.TheReceivableReview(tpyeName='预收预付')    # 审核及检查
        except BaseException as e:
                print("错误，错误原因：%s" % e)
                raise RuntimeError(self.XmTEXT.get('xmurl'))

    # def testGreaterThanAndEqualTo(self):
    #     """预付大于幸福家总佣金
    #         预付等于幸福家总佣金"""
    #     AGENTUSER = [AgentUser1, AgentUser3, AgentUser5, AgentUser7, AgentUser9]
    #     dome = self.XmRequest.RandomText(AGENTUSER)
    #     try:
    #         self.FlowPath.TheNewDeal(user=dome)
    #         self.FlowPath.DealTicket()
    #         self.XmRequest.ResultsTheChangeStayList(projectId=self.AgentTEXT.get('projectId'), excludeType=3)
    #         self.XmRequest.PrecollectedApply(compare=1)
    #         self.assertEqual('预付金额超过幸福家总佣金', self.XmTEXT.get('xmcontent'))
    #         self.XmRequest.PrecollectedApply()
    #         self.assertEqual(1, self.XmTEXT.get('resultCode'))
    #         self.XmRequest.PrecollectedList()
    #         self.assertEqual('审批中', self.XmTEXT.get('advanceStatusStr'))
    #     except BaseException as e:
    #             print("错误，错误原因：%s" % e)
    #             raise RuntimeError(self.XmTEXT.get('xmurl'))
    #
    # def test_PrepayLessThan(self):
    #     """预付小于幸福家总佣金"""
    #     AGENTUSER = [AgentUser1, AgentUser3, AgentUser5, AgentUser7, AgentUser9]
    #     dome = self.XmRequest.RandomText(AGENTUSER)
    #     try:
    #         self.FlowPath.TheNewDeal(user=dome)
    #         self.FlowPath.DealTicket()
    #         self.XmRequest.ResultsTheChangeStayList(projectId=self.AgentTEXT.get('projectId'), excludeType=3)
    #         self.XmRequest.PrecollectedApply(compare=-1)
    #         self.assertEqual(1, self.XmTEXT.get('resultCode'))
    #         self.XmRequest.PrecollectedList()
    #         self.assertEqual('审批中', self.XmTEXT.get('advanceStatusStr'))
    #     except BaseException as e:
    #             print("错误，错误原因：%s" % e)
    #             raise RuntimeError(self.XmTEXT.get('xmurl'))
    #
    # def testAdvanceIsGreaterThanAdvance(self):
    #     """预收大于预付"""
    #     AGENTUSER = [AgentUser1, AgentUser3, AgentUser5, AgentUser7, AgentUser9]
    #     dome = self.XmRequest.RandomText(AGENTUSER)
    #     try:
    #         self.FlowPath.TheNewDeal(user=dome)
    #         self.FlowPath.DealTicket()
    #         self.XmRequest.ResultsTheChangeStayList(projectId=self.AgentTEXT.get('projectId'), excludeType=3)
    #         self.XmRequest.PrecollectedApply(compare=-1, compare1=0, isAdvanceCollect=1)
    #         self.assertEqual(1, self.XmTEXT.get('resultCode'))
    #         self.XmRequest.PrecollectedList()
    #         self.assertEqual('财务确认中', self.XmTEXT.get('advanceStatusStr'))
    #     except BaseException as e:
    #             print("错误，错误原因：%s" % e)
    #             raise RuntimeError(self.XmTEXT.get('xmurl'))
    #
    # def testAdvanceIsEqualToAdvance(self):
    #     """预收等于预付"""
    #     AGENTUSER = [AgentUser1, AgentUser3, AgentUser5, AgentUser7, AgentUser9]
    #     dome = self.XmRequest.RandomText(AGENTUSER)
    #     try:
    #         self.FlowPath.TheNewDeal(user=dome)
    #         self.FlowPath.DealTicket()
    #         self.XmRequest.ResultsTheChangeStayList(projectId=self.AgentTEXT.get('projectId'), excludeType=3)
    #         self.XmRequest.PrecollectedApply(compare=0, compare1=0, isAdvanceCollect=1)
    #         self.assertEqual(1, self.XmTEXT.get('resultCode'))
    #         self.XmRequest.PrecollectedList()
    #         self.assertEqual('财务确认中', self.XmTEXT.get('advanceStatusStr'))
    #     except BaseException as e:
    #             print("错误，错误原因：%s" % e)
    #             raise RuntimeError(self.XmTEXT.get('xmurl'))
    #
    # def testAdvanceIsLessThanAdvance(self):
    #     """预收小于预付"""
    #     AGENTUSER = [AgentUser1, AgentUser3, AgentUser5, AgentUser7, AgentUser9]
    #     dome = self.XmRequest.RandomText(AGENTUSER)
    #     try:
    #         self.FlowPath.TheNewDeal(user=dome)
    #         self.FlowPath.DealTicket()
    #         self.XmRequest.ResultsTheChangeStayList(projectId=self.AgentTEXT.get('projectId'), excludeType=3)
    #         self.XmRequest.PrecollectedApply(compare=0, compare1=-1, isAdvanceCollect=1)
    #         self.assertEqual(1, self.XmTEXT.get('resultCode'))
    #         self.XmRequest.PrecollectedList()
    #         self.assertEqual('财务确认中', self.XmTEXT.get('advanceStatusStr'))
    #     except BaseException as e:
    #             print("错误，错误原因：%s" % e)
    #             raise RuntimeError(self.XmTEXT.get('xmurl'))


