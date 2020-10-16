# -*- coding: utf-8 -*-
# @Time    : 2020/3/21 11:08
# @Author  : 潘师傅
# @File    : My_Deal_casc.py

"""我的成交-相关"""
from XFP.PubilcAPI.flowPath import *

"""
无审核-正常流程：·····现状态················· 流放公海状态
  1、录入成交          已确认                    已确认
 一级审核-正常流程：··········现状态····················流放公海的状态
  1、录入成交-待审核          审核中 
  2、录入成交-审核失败        已驳回                         已驳回
  3、录入成交-审核成功        已确认                         已确认
 
 二级审核-正常流程············现状态··················流放公海的状态
  1、录入成交-待审核          申请中 
  2、录入成交-一级审核失败    已驳回                         已驳回
  3、录入成交-一级审核成功    审核中 
  4、录入成交-二级审核成功    已确认                         已确认
  5、录入成交-二级审核失败    已驳回                         已驳回
 
 操作事项：
  1、审核中的成交              ---只能操作跟进，其他动作都不允许操作
  2、修改成交后（如设置审核）  ---需重新审核
  3、已确认的成交              ---不允许删除
    
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

    def tearDown(self):
        """残留审核 失败！！！"""
        self.webApi.audit_List()
        while self.webApi.webText.get('total') != 0:
            self.webApi.auditApply(customerId=self.appApi.appText.get('customerId'),
                                   isAudit=False, auditRemark='客户流放公海')
            self.webApi.audit_List()
        self.webApi.audit_List(auditLevel=2)
        while self.webApi.webText.get('total') != 0:
            self.webApi.auditApply(customerId=self.appApi.appText.get('customerId'), vlue=2,
                                   isAudit=False, auditRemark='客户流放公海')
            self.webApi.audit_List()

    def test_my_deal_01(self):
        """1、录入成交          已确认                    已确认"""
        self.flowPath.add_deal()
        self.flowPath.deal_status(status='1')

    def test_my_deal_02(self):
        """1、录入成交-待审核          审核中"""
        self.webApi.Audit_management(customerDeal=True, customerDealLevel=1)
        self.flowPath.add_deal()
        dome = time.strftime("%Y-%m-%d %H:%M:%S")
        self.assertEqual(0, self.appApi.appText.get('transStatus'))
        """2、录入成交-审核失败        已驳回                         已驳回"""
        self.webApi.audit_List()  # 审核列表
        self.webApi.auditApply(customerId=self.appApi.appText.get('customerId'), isAudit=False,
                               auditRemark=dome + '成交审核不通过')
        self.flowPath.deal_status(status=2)
        self.assertEqual(dome + '成交审核不通过', self.appApi.appText.get('auditRemark'))

    def test_my_deal_03(self):
        """3、录入成交-审核成功        已确认                         已确认"""
        self.webApi.Audit_management(customerDeal=True, customerDealLevel=1)
        self.flowPath.add_deal()
        self.assertEqual(0, self.appApi.appText.get('transStatus'))
        """2、录入成交-审核失败        已驳回                         已驳回"""
        self.webApi.audit_List()  # 审核列表
        self.webApi.auditApply(customerId=self.appApi.appText.get('customerId'))
        self.flowPath.deal_status(status=1)

    def test_my_deal_04(self):
        """1、录入成交-待审核          申请中"""
        self.webApi.Audit_management(customerDeal=True, customerDealLevel=2)
        self.flowPath.add_deal()
        dome = time.strftime("%Y-%m-%d %H:%M:%S")
        self.assertEqual(0, self.appApi.appText.get('transStatus'))
        """2、录入成交-一级审核失败    已驳回                         已驳回"""
        self.webApi.audit_List()  # 审核列表
        self.webApi.auditApply(customerId=self.appApi.appText.get('customerId'), isAudit=False,
                               auditRemark=dome + '成交审核不通过')
        self.flowPath.deal_status(status=2)
        self.assertEqual(dome + '成交审核不通过', self.appApi.appText.get('auditRemark'))

    def test_my_deal_05(self):
        """3、录入成交-一级审核成功    审核中"""
        self.webApi.Audit_management(customerDeal=True, customerDealLevel=2)
        self.flowPath.add_deal()
        self.assertEqual(0, self.appApi.appText.get('transStatus'))
        self.webApi.audit_List()  # 审核列表
        self.webApi.auditApply(customerId=self.appApi.appText.get('customerId'))
        self.flowPath.deal_status(status=0)
        """4、录入成交-二级审核成功    已确认                         已确认"""
        self.webApi.audit_List(auditLevel=2)  # 审核列表
        self.webApi.auditApply(customerId=self.appApi.appText.get('customerId'), vlue=2)
        self.flowPath.deal_status(status=1)

    def test_my_deal_06(self):
        """5、录入成交-二级审核失败    已驳回                         已驳回"""
        self.webApi.Audit_management(customerDeal=True, customerDealLevel=2)
        self.flowPath.add_deal()
        dome = time.strftime("%Y-%m-%d %H:%M:%S")
        self.assertEqual(0, self.appApi.appText.get('transStatus'))
        self.webApi.audit_List()  # 审核列表
        self.webApi.auditApply(customerId=self.appApi.appText.get('customerId'))
        self.webApi.audit_List(auditLevel=2)  # 审核列表
        self.webApi.auditApply(customerId=self.appApi.appText.get('customerId'), isAudit=False, vlue=2,
                               auditRemark=dome + '成交审核不通过')
        self.flowPath.deal_status(status=2)
        self.assertEqual(dome + '成交审核不通过', self.appApi.appText.get('auditRemark'))

    def test_my_deal_07(self):
        """1、审核中的成交              ---只能操作跟进，其他动作都不允许操作"""
        self.webApi.Audit_management(customerDeal=True, customerDealLevel=1)
        self.flowPath.add_deal()
        self.assertEqual(0, self.appApi.appText.get('transStatus'))
        # 流放公海  创建带看 暂缓跟进 客户转移 不可以删除
        self.flowPath.client_exile_sea()
        self.assertEqual('已申请客户成交,正在审核中!', self.appApi.appText.get('data'))

        self.appApi.GetMatchingAreaHouse()
        dome = time.strftime("%Y-%m-%d %H:%M:%S")
        self.appApi.ClientVisitAdd(projectAId=self.appApi.appText.get('houseId'),
                                   appointmentTime=dome)
        self.assertEqual('已申请客户成交,正在审核中!', self.appApi.appText.get('data'))

        self.appApi.GetLabelList(labelNo='SQZHGJ', labelName='其他')
        self.appApi.ClientTaskPause()
        self.assertEqual('已申请客户成交,正在审核中!', self.appApi.appText.get('data'))

        self.appApi.ConsultantList()
        self.appApi.client_change()        # 线索转移
        self.assertEqual('已申请客户成交,正在审核中!', self.appApi.appText.get('data'))

        self.appApi.deal_List()
        self.appApi.add_deal(Status=2, isDeleted=1)
        self.assertEqual('已申请客户成交,正在审核中!', self.appApi.appText.get('data'))

    def test_my_deal_08(self):
        """2、修改成交后（如设置审核）  ---需重新审核"""
        # self.webApi.Audit_management()
        # self.test_my_deal_01()
        self.webApi.Audit_management(customerDeal=True, customerDealLevel=1)
        self.appApi.deal_List(transStatus=1)
        self.appApi.add_deal(Status=2, transOwnerName=self.appApi.RandomText(textArr=surname),
                             transReservedTellphone='1' + str(int(time.time())))
        self.flowPath.deal_status(status=0)
        dome = self.appApi.appText.get('clueId')
        self.webApi.audit_List()
        self.assertNotEqual(0, self.webApi.webText.get('total'))
        self.assertEqual(dome, self.webApi.webText.get('clueId'))

    def test_my_deal_09(self):
        """3、已确认的成交              ---不允许删除"""
        self.webApi.Audit_management()
        self.test_my_deal_01()
        self.appApi.deal_List()
        self.appApi.add_deal(Status=2, isDeleted=1)
        self.assertEqual('该成交已完成,无法删除!', self.appApi.appText.get('data'))


















