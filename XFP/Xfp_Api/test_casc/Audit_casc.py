# -*- coding: utf-8 -*-
# @Time    : 2020/9/8 17:47
# @Author  : 潘师傅
# @File    : audit_casc.py

"""审核相关"""

from XFP.PubilcAPI.webApi import *
from XFP.PubilcAPI.appApi import *
import unittest


class AuditTestCasc(unittest.TestCase):
    # 线索流放公海 | 客户流放公海  | 申请带看 | 成交审核 | 暂缓跟进

    def __init__(self, *args, **kwargs):
        super(AuditTestCasc, self).__init__(*args, **kwargs)
        self.appApi = appApi()
        self.appText = GlobalMap()
        self.webApi = webApi()
        self.webText = GlobalMap()

    @classmethod
    def setUpClass(cls):
        cls.do_request = appApi()
        cls.XfpRequest = cls.do_request
        cls.XfpRequest.Login()
        cls.XfpRequest.GetUserData()
        cls.request = webApi()
        cls.webApi = cls.request
        cls.webApi.Audit_management()

    def setUp(self):
        """每次开始获取一个线索"""
        self.appApi.SeaList()
        if self.appText.get('total') != 0:
            self.XfpRequest.clue_Assigned()     # 直接领取一个线索
            self.XfpRequest.my_clue_list()      # 线索列表
            self.assertNotEqual(0, self.appText.get('total'))
        else:
            self.appApi.my_clue_list()          # 线索列表
            if self.appText.get('total') == 0:      # 为空则新增
                self.appApi.GetLabelList(labelNo='XSLY', labelName='百度小程序')
                if self.appText.get('labelId') is None:
                    self.webApi.add_label(labelName='百度小程序', labelId=self.appText.get('LabelId'),
                                          pid=self.appText.get('LabelId'))
                    self.appApi.GetLabelList(labelNo='XSLY', labelName='百度小程序')
                self.appApi.GetUserLabelList(userLabelType='线索标签')
                if self.appText.get('total') == 0:
                    self.appApi.AddUserLabel()
                    self.appApi.GetUserLabelList(userLabelType='线索标签')
                self.appApi.ClueSave(clueNickName=self.appApi.RandomText(textArr=surname),
                                     sourceId=self.appText.get('labelId'),
                                     keyWords=self.appText.get('labelData'))

    def test_clue_exile_sea_audit(self):
        """线索流放公海审核 0-3及审核 审核通过"""
        try:
            # a = 0   # 不审核  直接跳过  在别的测试用例 有
            a = 1
            while a != 3:
                if a != 0:
                    clueStop = True
                else:
                    clueStop = False
                dome = self.appText.get('cluePhone')
                self.webApi.Audit_management(clueStop=clueStop, clueStopLevel=a)
                self.appApi.GetLabelList(labelNo='SZGJYY', labelName='客户已成交')
                self.appApi.ExileSea(labelId=self.appText.get('labelId'))
                if a != 0:
                    self.webApi.audit_List()    # 审核列表
                    self.assertNotEqual(0, self.webText.get('total'))
                    self.appApi.audit_List()
                    self.assertNotEqual(0, self.appText.get('total'))
                    self.assertEqual(self.appText.get('auditStatueStr'), '申请中')
                    self.assertEqual(self.appText.get('auditStatue'), 0)
                    self.webApi.auditApply()
                    self.appApi.audit_List()
                    if a == 1:
                        self.assertEqual(self.appText.get('auditStatueStr'), '已同意')
                        self.assertEqual(self.appText.get('auditStatue'), 1)
                    if a == 2:
                        self.assertEqual(self.appText.get('auditStatueStr'), '审核中')
                        self.assertEqual(self.appText.get('auditStatue'), 1)
                        self.webApi.audit_List(auditLevel=2)
                        self.assertNotEqual(0, self.webText.get('total'))
                        self.webApi.auditApply()
                        self.appApi.audit_List()
                        self.assertEqual(self.appText.get('auditStatueStr'), '已同意')
                        self.assertEqual(self.appText.get('auditStatue'), 1)
                self.appApi.my_clue_list()
                if self.appText.get('total') != 0:
                    self.assertNotEqual(self.appText.get('cluePhone'), dome)
                a = a + 1
                if a != 3:
                    self.setUp()
        except BaseException as e:
                print("错误，错误原因：%s" % e)
                raise RuntimeError(self.appText.get('ApiXfpUrl'))
        # 0--->1--->2

    def test_clue_exile_audit_out(self):
        """线索流放公海
        一级审核失败
        一级审核成功  二级审核失败
        """
        try:
            a = 1
            while a != 3:
                if a != 0:
                    clueStop = True
                else:
                    clueStop = False
                dome = self.appText.get('cluePhone')
                dome1 = time.strftime("%Y-%m-%d %H:%M:%S")
                self.webApi.Audit_management(clueStop=clueStop, clueStopLevel=a)
                self.appApi.GetLabelList(labelNo='SZGJYY', labelName='客户已成交')
                self.appApi.ExileSea(labelId=self.appText.get('labelId'))
                if a != 0:
                    self.webApi.audit_List()    # 审核列表
                    self.assertNotEqual(0, self.webText.get('total'))
                    self.appApi.audit_List()
                    self.assertNotEqual(0, self.appText.get('total'))
                    self.assertEqual(self.appText.get('auditStatueStr'), '申请中')
                    self.assertEqual(self.appText.get('auditStatue'), 0)
                    if a == 2:
                        self.assertNotEqual(0, self.webText.get('total'))
                        self.webApi.auditApply()
                        self.appApi.audit_List()
                        self.assertEqual(self.appText.get('auditStatueStr'), '审核中')
                        self.assertEqual(self.appText.get('auditStatue'), 1)
                        # self.webApi.audit_List(auditLevel=2)
                    self.webApi.audit_List(auditLevel=a)    # 审核列表
                    self.assertNotEqual(0, self.webText.get('total'))
                    self.webApi.auditApply(vlue=a, isAudit=False, auditRemark=dome1 + ' 线索流放审核不通过')
                    self.appApi.audit_List()
                    self.assertEqual(self.appText.get('auditStatueStr'), '已驳回')
                    self.assertEqual(self.appText.get('auditRemark'), dome1 + ' 线索流放审核不通过')
                    self.assertEqual(self.appText.get('auditStatue'), 2)

                self.appApi.my_clue_list()
                if self.appText.get('total') != 0:
                    self.assertEqual(self.appText.get('cluePhone'), dome)
                a = a + 1
                if a != 3:
                    self.setUp()
        except BaseException as e:
                print("错误，错误原因：%s" % e)
                raise RuntimeError(self.appText.get('ApiXfpUrl'))

    def test_client_exile_sea_audit(self):
        """客户流放公海审核  0-3级审核通过"""
        a = 1
        while a != 3:
            if a != 0:
                customerStop = True
            else:
                customerStop = False
            self.appApi.ClientList()
            if self.appText.get('total') == 0:  # 没有客户
                self.appApi.my_clue_list()
                self.appApi.ClientEntering(callName=self.appApi.RandomText(textArr=surname),
                                           loanSituation='这个是贷款情况')
                self.appApi.ClientList()
                self.assertEqual(1, self.appText.get('total'))
            dome = self.appText.get('total')
            self.webApi.Audit_management(customerStop=customerStop, customerStopLevel=a)      # 修改配置审核
            self.appApi.GetLabelList(labelNo='SZGJYY', labelName='客户已成交')
            self.appApi.client_exile_sea(labelId=self.appText.get('labelId'))
            if a != 0:
                self.webApi.audit_List()  # 审核列表
                self.assertNotEqual(0, self.webText.get('total'))
                self.appApi.audit_List()
                self.assertNotEqual(0, self.appText.get('total'))
                self.assertEqual(self.appText.get('auditStatueStr'), '申请中')
                self.assertEqual(self.appText.get('auditStatue'), 0)
                self.webApi.auditApply(customerId=self.appText.get('customerId'))
                self.appApi.audit_List()
                if a == 1:
                    self.assertEqual(self.appText.get('auditStatueStr'), '已同意')
                    self.assertEqual(self.appText.get('auditStatue'), 1)
                if a == 2:
                    self.assertEqual(self.appText.get('auditStatueStr'), '审核中')
                    self.assertEqual(self.appText.get('auditStatue'), 1)
                    self.webApi.audit_List(auditLevel=2)
                    self.assertNotEqual(0, self.webText.get('total'))
                    self.webApi.auditApply(customerId=self.appText.get('customerId'))
                    self.appApi.audit_List()
                    self.assertEqual(self.appText.get('auditStatueStr'), '已同意')
                    self.assertEqual(self.appText.get('auditStatue'), 1)
            self.appApi.ClientList()
            if self.appText.get('total') != 0:
                self.assertNotEqual(self.appText.get('total'), dome)
            a = a + 1

    def test_client_exile_sea_audit_out(self):
        """客户流放公海审核  1-2级审核不通过"""
        a = 2
        while a != 3:
            if a != 0:
                customerStop = True
            else:
                customerStop = False
            self.appApi.ClientList()
            dome1 = time.strftime("%Y-%m-%d %H:%M:%S")
            if self.appText.get('total') == 0:  # 没有客户
                self.appApi.ClientEntering(callName=self.appApi.RandomText(textArr=surname),
                                           loanSituation='这个是贷款情况')
                self.appApi.ClientList()
                self.assertEqual(1, self.appText.get('total'))
            dome = self.appText.get('total')
            self.webApi.Audit_management(customerStop=customerStop, customerStopLevel=a)      # 修改配置审核
            self.appApi.GetLabelList(labelNo='SZGJYY', labelName='客户已成交')
            self.appApi.client_exile_sea(labelId=self.appText.get('labelId'))
            if a != 0:
                self.webApi.audit_List()  # 审核列表
                self.assertNotEqual(0, self.webText.get('total'))
                self.appApi.audit_List()
                self.assertNotEqual(0, self.appText.get('total'))
                self.assertEqual(self.appText.get('auditStatueStr'), '申请中')
                self.assertEqual(self.appText.get('auditStatue'), 0)
                if a == 2:
                    self.assertNotEqual(0, self.webText.get('total'))
                    self.webApi.auditApply(customerId=self.appText.get('customerId'))
                    self.appApi.audit_List()
                    self.assertEqual(self.appText.get('auditStatueStr'), '审核中')
                    self.assertEqual(self.appText.get('auditStatue'), 1)
                    self.webApi.audit_List(auditLevel=2)
                self.webApi.audit_List(auditLevel=a)  # 审核列表
                self.assertNotEqual(0, self.webText.get('total'))
                self.webApi.auditApply(isAudit=False, customerId=self.appText.get('customerId'), vlue=a,
                                       auditRemark=dome1 + ' 客户流放公海 审核不通过')
                self.appApi.audit_List()
                self.assertEqual(self.appText.get('auditRemark'), dome1 + ' 客户流放公海 审核不通过')
                self.assertEqual(self.appText.get('auditStatueStr'), '已驳回')
                self.assertEqual(self.appText.get('auditStatue'), 2)
            self.appApi.ClientList()
            if self.appText.get('total') != 0:
                self.assertEqual(self.appText.get('total'), dome)
            a = a + 1

    def test_Visit_audit(self):
        """申请带看-----0-3级审核"""
        a = 1
        while a != 3:
            if a != 0:
                customerStop = True
            else:
                customerStop = False
            self.appApi.ClientList()
            if self.appText.get('total') == 0:  # 没有客户
                self.appApi.ClientEntering(callName=self.appApi.RandomText(textArr=surname),
                                           loanSituation='这个是贷款情况')
                self.appApi.ClientList()
                self.assertEqual(1, self.appText.get('total'))
            self.webApi.Audit_management(customerVisit=customerStop, customerVisitLevel=a)  # 修改配置审核
            self.appApi.GetMatchingAreaHouse()
            dome = time.strftime("%Y-%m-%d %H:%M:%S")
            self.appApi.ClientVisitAdd(projectAId=self.appText.get('houseId'),
                                       appointmentTime=dome)
            while self.appText.get('data') == '该客户已申请客户带看跟进,正在审核中!':
                self.appApi.GetLabelList(labelNo='SZGJYY', labelName='客户已成交')
                self.appApi.client_exile_sea(labelId=self.appText.get('labelId'))
                self.appApi.ClientList()
                if self.appText.get('total') == 0:  # 客户列表为空
                    self.appApi.SeaList()  # 公海列表
                    if self.appText.get('total') == 0:  # 公海列表为空
                        raise RuntimeError('直接新增客户还没写')
                    else:
                        self.appApi.clue_Assigned()  # 领取线索
                        self.appApi.my_clue_list()
                        self.appApi.ClientEntering(callName=self.appApi.RandomText(textArr=surname),
                                                   loanSituation='这个是贷款情况')  # 线索转客户
                    self.appApi.ClientList()  # 客户列表
                    self.assertEqual(1, self.appText.get('total'))
                self.webApi.Audit_management(customerVisit=customerStop, customerVisitLevel=a)  # 修改配置审核
                self.appApi.GetMatchingAreaHouse()
                self.appApi.ClientVisitAdd(projectAId=self.appText.get('houseId'),
                                           appointmentTime=dome)
            self.appApi.Task_Visit_List(appointmentTime=dome)
            self.assertEqual(self.appText.get('visiteStatus'), '3')
            self.assertEqual(self.appText.get('visiteStatusStr'), '申请中')

            self.webApi.audit_List()  # 审核列表
            self.webApi.auditApply(customerId=self.appText.get('customerId'))  # 审核成功
            if a == 2:
                self.appApi.Task_Visit_List(appointmentTime=dome)
                self.assertEqual(self.appText.get('visiteStatus'), '3')
                self.assertEqual(self.appText.get('visiteStatusStr'), '申请中')
                self.webApi.audit_List(auditLevel=2)
                self.webApi.auditApply(customerId=self.appText.get('customerId'))  # 审核成功
            self.appApi.Task_Visit_List(appointmentTime=dome)
            self.assertEqual(self.appText.get('visiteStatus'), '0')
            self.assertEqual(self.appText.get('visiteStatusStr'), '进行中')
            self.appApi.ClientTask(taskTypeStr='带看行程')
            if self.appText.get('total') < 1:
                raise RuntimeError(self.appText.get('ApiXfpUrl'))
            self.appApi.visit_info()
            self.appApi.VisitFlow1()
            self.appApi.ClientTask()
            self.appApi.Task_Visit_List(appointmentTime=dome)
            self.assertEqual(self.appText.get('visiteStatus'), '1')
            self.assertEqual(self.appText.get('visiteStatusStr'), '已完成')
            a = a + 1

    def test_Visit_audit_out(self):
        """申请带看-----1-3级审核失败"""
        a = 1
        while a != 3:
            if a != 0:
                customerStop = True
            else:
                customerStop = False
            self.appApi.ClientList()
            if self.appText.get('total') == 0:  # 没有客户
                self.appApi.ClientEntering(callName=self.appApi.RandomText(textArr=surname),
                                           loanSituation='这个是贷款情况')
                self.appApi.ClientList()
                self.assertEqual(1, self.appText.get('total'))
            self.webApi.Audit_management(customerVisit=customerStop, customerVisitLevel=a)  # 修改配置审核
            self.appApi.GetMatchingAreaHouse()
            dome = time.strftime("%Y-%m-%d %H:%M:%S")
            self.appApi.ClientVisitAdd(projectAId=self.appText.get('houseId'),
                                       appointmentTime=dome)
            while self.appText.get('data') == '该客户已申请客户带看跟进,正在审核中!':
                self.appApi.GetLabelList(labelNo='SZGJYY', labelName='客户已成交')
                self.appApi.client_exile_sea(labelId=self.appText.get('labelId'))
                self.appApi.ClientList()
                if self.appText.get('total') == 0:  # 客户列表为空
                    self.appApi.SeaList()  # 公海列表
                    if self.appText.get('total') == 0:  # 公海列表为空
                        raise RuntimeError('直接新增客户还没写')
                    else:
                        self.appApi.clue_Assigned()  # 领取线索
                        self.appApi.my_clue_list()
                        self.appApi.ClientEntering(callName=self.appApi.RandomText(textArr=surname),
                                                   loanSituation='这个是贷款情况')  # 线索转客户
                    self.appApi.ClientList()  # 客户列表
                    self.assertEqual(1, self.appText.get('total'))
                self.webApi.Audit_management(customerVisit=customerStop, customerVisitLevel=a)  # 修改配置审核
                self.appApi.GetMatchingAreaHouse()
                self.appApi.ClientVisitAdd(projectAId=self.appText.get('houseId'),
                                           appointmentTime=dome)
            self.appApi.Task_Visit_List(appointmentTime=dome)
            self.assertEqual(self.appText.get('visiteStatus'), '3')
            self.assertEqual(self.appText.get('visiteStatusStr'), '申请中')
            # if a == 1:
            #     self.webApi.audit_List()  # 审核列表
            #     self.webApi.auditApply(customerId=self.appText.get('customerId'), isAudit=False)  # 审核失败
            if a == 2:
                self.webApi.audit_List()  # 审核列表
                self.webApi.auditApply(customerId=self.appText.get('customerId'))  # 审核成功
                self.appApi.Task_Visit_List(appointmentTime=dome)
                self.assertEqual(self.appText.get('visiteStatus'), '3')
                self.assertEqual(self.appText.get('visiteStatusStr'), '申请中')

            self.webApi.audit_List()  # 审核列表
            self.webApi.auditApply(customerId=self.appText.get('customerId'), isAudit=False,
                                   auditRemark=dome + ' 带看审核不通过')  # 审核失败
            self.appApi.Task_Visit_List(appointmentTime=dome)
            self.assertEqual(self.appText.get('auditRemark'), dome + ' 带看审核不通过')
            self.assertEqual(self.appText.get('visiteStatus'), '2')
            self.assertEqual(self.appText.get('visiteStatusStr'), '已驳回')
            a = a + 1

    def test_deal_audit(self):
        """录入成交审核"""
        try:
            # a = 0   # 不审核  直接跳过  在别的测试用例 有
            a = 1
            while a != 3:
                if a != 0:
                    clueStop = True
                else:
                    clueStop = False
                self.appApi.TransactionList()
                dome = self.appText.get('total')
                self.webApi.Audit_management(customerDeal=clueStop, customerDealLevel=a)
                self.appApi.ClientList()
                if self.appText.get('total') == '0':  # 没有客户
                    self.appApi.my_clue_list()
                    self.appApi.ClientEntering(callName=self.appApi.RandomText(textArr=surname),
                                               loanSituation='这个是贷款情况')
                    self.appApi.ClientList()
                    self.assertEqual(1, self.appText.get('total'))
                self.appApi.GetMatchingAreaHouse()  # 匹配楼盘
                self.assertNotEqual(0, self.appText.get('total'))
                self.appApi.GetLabelList(labelNo='CJX', labelName='认购')
                self.appApi.TransactionSave()  # 录入成交
                while self.appText.get('data') == '该客户成交正在审核中!':
                    self.appApi.GetLabelList(labelNo='SZGJYY', labelName='客户已成交')
                    self.appApi.client_exile_sea(labelId=self.appText.get('labelId'))
                    self.appApi.my_clue_list()
                    self.appApi.ClientEntering(callName=self.appApi.RandomText(textArr=surname),
                                               loanSituation='这个是贷款情况')
                    self.appApi.ClientList()
                    self.appApi.GetLabelList(labelNo='CJX', labelName='认购')
                    self.appApi.TransactionSave()  # 录入成交
                if a != 0:
                    self.webApi.audit_List()    # 审核列表
                    self.assertNotEqual(0, self.webText.get('total'))
                    self.appApi.TransactionList()
                    self.assertNotEqual(0, self.appText.get('total'))
                    self.assertEqual(self.appText.get('transStatus'), 0)
                    self.webApi.auditApply(customerId=self.appText.get('customerId'))
                    self.appApi.TransactionList()
                    if a == 1:
                        self.assertEqual(self.appText.get('transStatus'), 1)
                    if a == 2:
                        self.assertEqual(self.appText.get('transStatus'), 0)
                        self.webApi.audit_List(auditLevel=2)
                        self.assertNotEqual(0, self.webText.get('total'))
                        self.webApi.auditApply(customerId=self.appText.get('customerId'))
                        self.appApi.TransactionList()
                        self.assertEqual(self.appText.get('transStatus'), 1)
                self.appApi.TransactionList()
                if self.appText.get('total') != 0:
                    self.assertNotEqual(self.appText.get('total'), dome)
                a = a + 1
        except BaseException as e:
                print("错误，错误原因：%s" % e)
                raise RuntimeError(self.appText.get('ApiXfpUrl'))

    def test_deal_audit_out(self):
        """录入成交审核 1-2级审核失败"""
        try:
            # a = 0   # 不审核  直接跳过  在别的测试用例 有
            a = 2
            while a != 3:
                if a != 0:
                    clueStop = True
                else:
                    clueStop = False
                self.appApi.TransactionList()
                dome = self.appText.get('total')
                self.webApi.Audit_management(customerDeal=clueStop, customerDealLevel=a)
                self.appApi.ClientList()
                if self.appText.get('total') == 0:  # 没有客户
                    self.appApi.my_clue_list()
                    self.appApi.ClientEntering(callName=self.appApi.RandomText(textArr=surname),
                                               loanSituation='这个是贷款情况')
                    self.appApi.ClientList()
                    self.assertEqual(1, self.appText.get('total'))
                self.appApi.GetMatchingAreaHouse()  # 匹配楼盘
                self.assertNotEqual(0, self.appText.get('total'))
                self.appApi.GetLabelList(labelNo='CJX', labelName='认购')
                self.appApi.TransactionSave()  # 录入成交
                while self.appText.get('data') == '该客户成交正在审核中!':
                    self.appApi.GetLabelList(labelNo='SZGJYY', labelName='客户已成交')
                    self.appApi.client_exile_sea(labelId=self.appText.get('labelId'))
                    self.appApi.my_clue_list()
                    self.appApi.ClientEntering(callName=self.appApi.RandomText(textArr=surname),
                                               loanSituation='这个是贷款情况')
                    self.appApi.ClientList()
                    self.appApi.GetLabelList(labelNo='CJX', labelName='认购')
                    self.appApi.TransactionSave()  # 录入成交
                if a != 0:
                    self.webApi.audit_List()    # 审核列表
                    self.assertNotEqual(0, self.webText.get('total'))
                    self.appApi.TransactionList()
                    self.assertNotEqual(0, self.appText.get('total'))
                    self.assertEqual(self.appText.get('transStatus'), 0)
                    if a == 2:
                        self.webApi.auditApply(customerId=self.appText.get('customerId'))
                        self.appApi.TransactionList()
                        self.assertEqual(self.appText.get('transStatus'), 0)
                        self.webApi.audit_List(auditLevel=2)  # 审核列表
                    self.webApi.auditApply(customerId=self.appText.get('customerId'),isAudit=False)
                    self.appApi.TransactionList()
                    self.assertEqual(self.appText.get('transStatus'), 2)
                    if self.appText.get('total') != 0:
                        self.assertNotEqual(self.appText.get('total'), dome)
                a = a + 1
        except BaseException as e:
                print("错误，错误原因：%s" % e)
                raise RuntimeError(self.appText.get('ApiXfpUrl'))

    def test_pause_follow_audit(self):
        """暂停跟进  0-3级审核通过"""
        a = 2
        while a != 3:
            if a != 0:
                customerStop = True
            else:
                customerStop = False
            self.appApi.ClientList()
            if self.appText.get('total') == 0:  # 没有客户
                self.appApi.my_clue_list()
                self.appApi.ClientEntering(callName=self.appApi.RandomText(textArr=surname),
                                           loanSituation='这个是贷款情况')
                self.appApi.ClientList()
                self.assertEqual(1, self.appText.get('total'))
            self.webApi.Audit_management(suspend=customerStop, suspendLevel=a)      # 修改配置审核
            self.appApi.GetLabelList(labelNo='SQZHGJ', labelName='其他')
            self.appApi.ClientTaskPause()
            while self.appText.get('data') == '该客户已被暂缓!':
                self.appApi.GetLabelList(labelNo='SZGJYY', labelName='客户已成交')
                self.appApi.client_exile_sea(labelId=self.appText.get('labelId'))
                self.appApi.ClientList()
                if self.appText.get('total') == 0:  # 没有客户
                    self.appApi.my_clue_list()
                    self.appApi.ClientEntering(callName=self.appApi.RandomText(textArr=surname),
                                               loanSituation='这个是贷款情况')
                    self.appApi.ClientList()
                    self.assertEqual(1, self.appText.get('total'))
                self.webApi.Audit_management(suspend=customerStop, suspendLevel=a)  # 修改配置审核
                self.appApi.GetLabelList(labelNo='SQZHGJ', labelName='其他')
                self.appApi.ClientTaskPause()
            if a != 0:
                self.webApi.audit_List()  # 审核列表
                self.assertNotEqual(0, self.webText.get('total'))
                self.appApi.audit_List()
                self.assertNotEqual(0, self.appText.get('total'))
                self.assertEqual(self.appText.get('auditStatueStr'), '申请中')
                self.assertEqual(self.appText.get('auditStatue'), 0)
                self.webApi.auditApply(customerId=self.appText.get('customerId'),
                                       endTime=time.strftime("%Y-%m-%d ") + '22:00:00')
                self.appApi.audit_List()
                if a == 1:
                    self.assertEqual(self.appText.get('auditStatueStr'), '已同意')
                    self.assertEqual(self.appText.get('auditStatue'), 1)
                if a == 2:
                    self.assertEqual(self.appText.get('auditStatueStr'), '审核中')
                    self.assertEqual(self.appText.get('auditStatue'), 1)
                    self.webApi.audit_List(auditLevel=2)
                    self.assertNotEqual(0, self.webText.get('total'))
                    self.webApi.auditApply(customerId=self.appText.get('customerId'),
                                           endTime=time.strftime("%Y-%m-%d ") + '22:00:00')
                    self.appApi.audit_List()
                    self.assertEqual(self.appText.get('auditStatueStr'), '已同意')
                    self.assertEqual(self.appText.get('auditStatue'), 1)
            a = a + 1

    def test_pause_follow_audit_out(self):
        """暂停跟进  1-2级审核不通过"""
        a = 2
        while a != 3:
            if a != 0:
                customerStop = True
            else:
                customerStop = False
            self.appApi.ClientList()
            dome1 = time.strftime("%Y-%m-%d %H:%M:%S")
            if self.appText.get('total') == 0:  # 没有客户
                self.appApi.my_clue_list()
                self.appApi.ClientEntering(callName=self.appApi.RandomText(textArr=surname),
                                           loanSituation='这个是贷款情况')
                self.appApi.ClientList()
                self.assertEqual(1, self.appText.get('total'))
            self.webApi.Audit_management(suspend=customerStop, suspendLevel=a)      # 修改配置审核
            self.appApi.GetLabelList(labelNo='SQZHGJ', labelName='其他')
            self.appApi.ClientTaskPause()
            while self.appText.get('data') == '该客户已被暂缓!':
                self.appApi.GetLabelList(labelNo='SZGJYY', labelName='客户已成交')
                self.appApi.client_exile_sea(labelId=self.appText.get('labelId'))
                self.appApi.ClientList()
                if self.appText.get('total') == 0:  # 没有客户
                    self.appApi.my_clue_list()
                    self.appApi.ClientEntering(callName=self.appApi.RandomText(textArr=surname),
                                               loanSituation='这个是贷款情况')
                    self.appApi.ClientList()
                    self.assertEqual(1, self.appText.get('total'))
                self.webApi.Audit_management(suspend=customerStop, suspendLevel=a)  # 修改配置审核
                self.appApi.GetLabelList(labelNo='SQZHGJ', labelName='其他')
                self.appApi.ClientTaskPause()
            if a != 0:
                self.webApi.audit_List()  # 审核列表
                self.assertNotEqual(0, self.webText.get('total'))
                self.appApi.audit_List()
                self.assertNotEqual(0, self.appText.get('total'))
                self.assertEqual(self.appText.get('auditStatueStr'), '申请中')
                self.assertEqual(self.appText.get('auditStatue'), 0)
                if a == 2:
                    self.webApi.auditApply(customerId=self.appText.get('customerId'),
                                           endTime=time.strftime("%Y-%m-%d ") + '22:00:00')
                    self.appApi.audit_List()
                    self.assertEqual(self.appText.get('auditStatueStr'), '审核中')
                    self.assertEqual(self.appText.get('auditStatue'), 1)
                    self.webApi.audit_List(auditLevel=2)
                    self.assertNotEqual(0, self.webText.get('total'))
                self.webApi.auditApply(customerId=self.appText.get('customerId'), isAudit=False,
                                       auditRemark=dome1 + ' 暂申请不通过', vlue=a,
                                       endTime=time.strftime("%Y-%m-%d ") + '22:00:00')
                self.appApi.audit_List()
                self.assertEqual(self.appText.get('auditRemark'), dome1 + ' 暂申请不通过')
                self.assertEqual(self.appText.get('auditStatueStr'), '已驳回')
                self.assertEqual(self.appText.get('auditStatue'), 2)
            a = a + 1
