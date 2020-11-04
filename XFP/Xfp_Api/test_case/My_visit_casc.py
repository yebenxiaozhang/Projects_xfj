# -*- coding: utf-8 -*-
# @Time    : 2020/3/21 11:08
# @Author  : 潘师傅
# @File    : My_visit_casc.py

"""我的带看-相关"""
from XFP.PubilcAPI.flowPath import *
"""
无审核-正常流程：·····现状态··················· 流放公海状态
  1、创建带看          进行中                   已取消
  2、完成带看          已完成                   已完成
  3、取消带看          已取消                   已取消
 
 一级审核-正常流程：···················现状态···············流放公海的状态
  1、创建带看-待审核                   审核中 
  2、创建带看-审核成功                 进行中             已取消
  3、创建带看-审核失败                 已驳回             已取消
  4、审核成功-完成带看                 已完成             已完成
  5、审核成功-提前结束带看             已取消             已取消
 
 二级审核-正常流程············现状态······················流放公海的状态
  1、创建带看-待审核          申请中 
  2、创建带看-一级审核失败    已驳回                     已取消
  3、创建带看-一级审核成功    审核中 
  4、创建带看-二级审核失败    已驳回                     已取消
  5、创建带看-二级审核成功    进行中                     已取消
  6、审核成功-完成带看        已完成                     已完成
  7、审核成功-提前结束带看    已取消                     已取消
  
 操作事项：
  1、审核失败的带看---不允许操作
  2、提前结束的带看---不允许操作
  3、审核中的带看 ---不可以完成，可以取消，不可以释放公海
  4、同一个客户只能存在一个带看 一个带看代办
"""


class MyVisitTestCase(unittest.TestCase):
    """幸福派——我的带看"""

    def __init__(self, *args, **kwargs):
        super(MyVisitTestCase, self).__init__(*args, **kwargs)
        self.xfp_web = webApi()
        self.webApi = self.xfp_web

        self.xfp_app = appApi()
        self.appApi = self.xfp_app

        self.flow = flowPath()
        self.flowPath = self.flow

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
        cls.request = webApi()
        cls.webApi = cls.request
        cls.webApi.Audit_management()

    # def setUp(self):
    #     pass

    def setUp(self):
        """残留审核 失败！！！"""
        self.webApi.audit_List()
        while self.webApi.webText.get('total') != 0:
            self.webApi.auditApply(isAudit=False,
                                   auditRemark='客户流放公海', customerId=self.webText.get('customerId'))
            self.webApi.audit_List()
        self.webApi.audit_List(auditLevel=2)
        while self.webApi.webText.get('total') != 0:
            self.webApi.auditApply(isAudit=False,
                                   auditRemark='客户流放公海', customerId=self.webText.get('customerId'))
            self.webApi.audit_List()

    def test_my_visit_01(self):
        """1、创建带看          进行中                   已取消"""
        self.flowPath.add_visit()
        self.flowPath.visit_status(status='进行中')
        self.flowPath.client_exile_sea()
        self.flowPath.visit_status(status='已取消')

    def test_my_visit_02(self):
        """2、完成带看          已完成                   已完成"""
        self.flowPath.add_visit()
        self.flowPath.accomplish_visit()
        self.flowPath.visit_status(status='已完成')
        self.flowPath.client_exile_sea()
        self.flowPath.visit_status(status='已完成')

    def test_my_visit_03(self):
        """3、取消带看      已取消                   已取消"""
        self.flowPath.add_visit()
        self.flowPath.advance_over_visit()
        self.flowPath.visit_status(status='已取消')
        self.flowPath.client_exile_sea()
        self.flowPath.visit_status(status='已取消')

    def test_my_visit_04(self):
        """1、创建带看-待审核                   审核中"""
        self.webApi.Audit_management(customerVisit=True, customerVisitLevel=1)  # 修改配置审核
        self.flowPath.add_visit()
        self.flowPath.visit_status(status='审核中')
        """2、创建带看-审核成功                 进行中             已取消"""
        self.webApi.audit_List()  # 审核列表
        self.webApi.auditApply(customerId=self.appText.get('customerId'))  # 审核成功
        self.flowPath.visit_status(status='进行中')
        self.flowPath.client_exile_sea()
        self.flowPath.visit_status(status='已取消')

    def test_my_visit_06(self):
        """3、创建带看-审核失败                 已驳回             已驳回"""
        self.webApi.Audit_management(customerVisit=True, customerVisitLevel=1)  # 修改配置审核
        self.flowPath.add_visit()
        self.webApi.audit_List()  # 审核列表
        self.webApi.auditApply(customerId=self.appText.get('customerId'),
                               isAudit=False, auditRemark=int(time.time()))  # 审核失败
        self.flowPath.visit_status(status='已驳回')
        self.flowPath.client_exile_sea()
        self.flowPath.visit_status(status='已取消')

    def test_my_visit_07(self):
        """4、审核成功-完成带看                 已完成             已完成"""
        self.webApi.Audit_management(customerVisit=True, customerVisitLevel=1)  # 修改配置审核
        self.flowPath.add_visit()
        self.webApi.audit_List()  # 审核列表
        self.webApi.auditApply(customerId=self.appText.get('customerId'))  # 审核成功
        self.flowPath.accomplish_visit()
        self.flowPath.visit_status(status='已完成')
        self.flowPath.client_exile_sea()
        self.flowPath.visit_status(status='已完成')

    def test_my_visit_08(self):
        """5、审核成功-提前结束带看             已取消             已取消"""
        self.webApi.Audit_management(customerVisit=True, customerVisitLevel=1)  # 修改配置审核
        self.flowPath.add_visit()
        self.webApi.audit_List()  # 审核列表
        self.webApi.auditApply(customerId=self.appText.get('customerId'))  # 审核成功
        self.flowPath.advance_over_visit()
        self.flowPath.visit_status(status='已取消')
        self.flowPath.client_exile_sea()
        self.flowPath.visit_status(status='已取消')

    def test_my_visit_09(self):
        """1、创建带看-待审核          申请中                     已取消"""
        self.webApi.Audit_management(customerVisit=True, customerVisitLevel=2)  # 修改配置审核
        self.flowPath.add_visit()
        self.flowPath.visit_status(status='审核中')
        """2、创建带看-一级审核失败    已驳回                     已驳回"""
        self.webApi.audit_List()  # 审核列表
        self.webApi.auditApply(customerId=self.appText.get('customerId'), isAudit=False)  # 审核失败
        self.flowPath.visit_status(status='已驳回')
        self.flowPath.client_exile_sea()
        self.flowPath.visit_status(status='已取消')

    def test_my_visit_11(self):
        """3、创建带看-一级审核成功    审核中                     已取消"""
        self.webApi.Audit_management(customerVisit=True, customerVisitLevel=2)  # 修改配置审核
        self.flowPath.add_visit()
        self.webApi.audit_List()  # 审核列表
        self.webApi.auditApply(customerId=self.appText.get('customerId'))  # 审核
        self.flowPath.visit_status(status='审核中')
        """4、创建带看-二级审核失败    已驳回                     已取消"""
        self.webApi.audit_List(auditLevel=2)  # 审核列表
        self.webApi.auditApply(customerId=self.appText.get('customerId'), vlue=2, isAudit=False)  # 审核
        self.flowPath.visit_status(status='已驳回')
        self.flowPath.client_exile_sea()
        self.flowPath.visit_status(status='已取消')

    def test_my_visit_13(self):
        """5、创建带看-二级审核成功    进行中                     已取消"""
        self.webApi.Audit_management(customerVisit=True, customerVisitLevel=2)  # 修改配置审核
        self.flowPath.add_visit()
        self.webApi.audit_List()  # 审核列表
        self.webApi.auditApply(customerId=self.appText.get('customerId'))  # 审核
        self.webApi.audit_List(auditLevel=2)  # 审核列表
        self.webApi.auditApply(customerId=self.appText.get('customerId'), vlue=2)  # 审核
        self.flowPath.visit_status(status='进行中')
        self.flowPath.accomplish_visit()
        self.flowPath.visit_status(status='已完成')
        self.flowPath.client_exile_sea()
        self.flowPath.visit_status(status='已完成')

    def test_my_visit_15(self):
        """7、审核成功-提前结束带看    已取消                     已取消"""
        self.webApi.Audit_management(customerVisit=True, customerVisitLevel=2)  # 修改配置审核
        self.flowPath.add_visit()
        self.webApi.audit_List()  # 审核列表
        self.webApi.auditApply(customerId=self.appText.get('customerId'))  # 审核
        self.webApi.audit_List(auditLevel=2)  # 审核列表
        self.webApi.auditApply(customerId=self.appText.get('customerId'), vlue=2)  # 审核
        self.flowPath.advance_over_visit()
        self.flowPath.visit_status(status='已取消')
        self.flowPath.client_exile_sea()
        self.flowPath.visit_status(status='已取消')

    def test_my_visit_16(self):
        """1、审核失败的带看---不允许操作"""
        self.webApi.Audit_management(customerVisit=True, customerVisitLevel=1)  # 修改配置审核
        self.flowPath.add_visit()
        self.appApi.ClientTask(taskType='3')
        if self.appApi.appText.get('total') < 1:
            raise RuntimeError(self.appApi.appText.get('ApiXfpUrl'))
        self.appApi.visit_info()
        self.webApi.audit_List()  # 审核列表
        self.webApi.auditApply(customerId=self.appText.get('customerId'), isAudit=False)  # 审核失败
        self.appApi.GetLabelList(labelNo='CXFS', labelName='自驾')
        self.appApi.VisitFlow1(agencyId=self.appApi.appText.get('labelId'),
                               receptionName=self.appApi.RandomText(textArr=surname),
                               receptionPhone='1' + str(int(time.time())), attachmentIds='1')
        self.assertEqual('带看计划已取消', self.appApi.appText.get('data'))

    # def test_my_visit_17(self):
    #     """2、提前结束的带看---不允许操作"""
    #     self.webApi.Audit_management()  # 修改配置审核
    #     self.flowPath.add_visit()
    #     self.appApi.ClientTask(taskType='3')
    #     self.appApi.visit_info()
    #     self.appApi.OverVisit()  # 提前结束代办
    #     self.appApi.GetLabelList(labelNo='CXFS', labelName='自驾')
    #     self.appApi.VisitFlow1(agencyId=self.appApi.appText.get('labelId'),
    #                            receptionName=self.appApi.RandomText(textArr=surname),
    #                            receptionPhone='1' + str(int(time.time())), attachmentIds='1')
    #     self.assertEqual('带看计划已取消', self.appApi.appText.get('data'))

    def test_my_visit_18(self):
        """3、审核中的带看 ---不可以完成，不可以提前结束，不可以释放公海"""
        self.webApi.Audit_management(customerVisit=True, customerVisitLevel=1)  # 修改配置审核
        self.flowPath.add_visit()
        self.appApi.ClientTask(taskType='3')
        if self.appApi.appText.get('total') < 1:
            raise RuntimeError(self.appApi.appText.get('ApiXfpUrl'))
        self.appApi.visit_info()
        self.appApi.GetLabelList(labelNo='CXFS', labelName='自驾')
        self.appApi.VisitFlow1(agencyId=self.appApi.appText.get('labelId'),
                               receptionName=self.appApi.RandomText(textArr=surname),
                               receptionPhone='1' + str(int(time.time())), attachmentIds='1')
        self.assertEqual('带看计划审核中', self.appApi.appText.get('data'))

        self.appApi.GetMatchingAreaHouse()  # 匹配楼盘
        assert 0 != self.appApi.appText.get('total'), '匹配楼盘为空？'
        self.appApi.GetLabelList(labelNo='CJX', labelName='认购')
        self.appApi.add_deal()  # 录入成交
        self.assertNotEqual(200, self.appApi.appText.get('code'))
        # self.assertEqual('带看计划审核中', self.appApi.appText.get('data'))

        self.flowPath.client_exile_sea()
        self.assertNotEqual(200, self.appApi.appText.get('code'))
        # self.assertEqual('带看计划审核中', self.appApi.appText.get('data'))

        self.appApi.GetLabelList(labelNo='SQZHGJ', labelName='其他')
        self.appApi.ClientTaskPause()
        self.assertNotEqual(200, self.appApi.appText.get('code'))
        # self.assertEqual('带看计划审核中', self.appApi.appText.get('data'))

        # self.appApi.visit_info()
        # self.appApi.OverVisit()  # 提前结束代办
        # self.assertEqual(200, self.appApi.appText.get('code'))

    def test_my_visit_19(self):
        """同一个客户只能存在一个带看 一个带看代办"""
        self.webApi.Audit_management()
        self.flowPath.add_visit()
        self.appApi.ClientVisitAdd(projectAId=self.appApi.appText.get('houseId'),
                                   seeingConsultant=self.appApi.appText.get('consultantId'),
                                   appointConsultant=self.appApi.appText.get('consultantId'))
        self.assertEqual(301, self.appText.get('code'))
        self.assertEqual('该客户存在未完成带看', self.appApi.appText.get('data'))


