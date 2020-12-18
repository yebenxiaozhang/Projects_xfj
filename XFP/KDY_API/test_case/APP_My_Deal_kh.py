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

补：
    1、一级审核没有通过的情况下耳机列表不应该显示出来
"""


class TestCase(unittest.TestCase):
    """客第壹——我的成交"""

    def __init__(self, *args, **kwargs):
        super(TestCase, self).__init__(*args, **kwargs)
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
        cls.appApi = cls.do_request
        cls.appApi.Login()
        cls.appApi.GetUserData()
        cls.request = webApi()
        cls.webApi = cls.request
        cls.webApi.Audit_management()
        cls.flow = flowPath()
        cls.flowPath = cls.flow
        cls.appText = GlobalMap()

        cls.flowPath.client_list_non_null()
        cls.flowPath.add_visit()
        cls.flowPath.accomplish_visit()
        cls.appApi.visitProject_list()

        cls.webApi.auditList()
        while cls.appApi.appText.get('web_total') != 0:
            cls.webApi.audit(auditStatue=2, auditRemark=' 审核失败')
            cls.webApi.auditList()
        cls.webApi.auditList(auditLevel=2)
        while cls.appApi.appText.get('web_total') != 0:
            cls.webApi.audit(auditStatue=2, auditRemark=' 审核失败')
            cls.webApi.auditList(auditLevel=2)

    def test_my_deal_01(self):
        """1、录入成交          已确认                    已确认"""
        self.appApi.add_deal()
        self.appApi.deal_List()
        self.webApi.detail()
        self.flowPath.deal_status(status=0, keyWord=self.appText.get('dealPhone'))
        self.webApi.finance_deal_auditList(keyWord=self.appText.get('dealPhone'))
        self.webApi.finance_deal_audit()
        self.flowPath.deal_status(status=1, keyWord=self.appText.get('dealPhone'))

    def test_my_deal_02(self):
        """1、录入成交-待审核          审核中"""
        self.webApi.Audit_management(customerDeal=True, customerDealLevel=1)
        # self.appApi.deal_List(transStatus=1)
        # self.webApi.detail()
        self.appApi.add_deal(Status=1)
        self.flowPath.deal_status(status=0, keyWord=self.appText.get('dealPhone'))

        dome = time.strftime("%Y-%m-%d %H:%M:%S")
        """2、录入成交-审核失败        已驳回                         已驳回"""
        self.webApi.auditList(phoneNum=self.appText.get('cluePhone'))
        self.webApi.audit(auditStatue=2, auditRemark=dome + ' 成交审核不通过')
        self.flowPath.deal_status(status=2, keyWord=self.appText.get('dealPhone'))

    def test_my_deal_03(self):
        """3、录入成交-审核成功        已确认                         已确认"""
        self.webApi.Audit_management(customerDeal=True, customerDealLevel=1)
        # self.appApi.deal_List(transStatus=1)
        # self.webApi.detail()
        self.appApi.add_deal(Status=1)
        self.webApi.auditList(phoneNum=self.appText.get('cluePhone'))
        self.webApi.audit()
        self.flowPath.deal_status(status=0, keyWord=self.appText.get('dealPhone'))
        self.webApi.finance_deal_auditList(keyWord=self.appText.get('dealPhone'))
        self.webApi.finance_deal_audit()
        self.flowPath.deal_status(status=1, keyWord=self.appText.get('dealPhone'))

    def test_my_deal_04(self):
        """1、录入成交-待审核          申请中"""
        self.webApi.Audit_management(customerDeal=True, customerDealLevel=2)
        # self.appApi.deal_List(transStatus=1)
        # self.webApi.detail()
        self.appApi.add_deal(Status=1)
        dome = time.strftime("%Y-%m-%d %H:%M:%S")
        """2、录入成交-一级审核失败    已驳回                         已驳回"""

        self.webApi.auditList(phoneNum=self.appText.get('cluePhone'))
        self.webApi.audit(auditStatue=2, auditRemark=dome + ' 成交审核不通过')

        self.flowPath.deal_status(status=2, keyWord=self.appText.get('dealPhone'))

    def test_my_deal_05(self):
        """3、录入成交-一级审核成功    审核中"""
        self.webApi.Audit_management(customerDeal=True, customerDealLevel=2)
        # self.appApi.deal_List(transStatus=1)
        # self.webApi.detail()
        self.appApi.add_deal(Status=1)

        self.appApi.Login(userName='13062200302')
        self.webApi.auditList(phoneNum=self.appText.get('cluePhone'))
        self.webApi.audit(auditStatue=1)

        self.flowPath.deal_status(status=0, keyWord=self.appText.get('dealPhone'))

        """4、录入成交-二级审核成功    已确认                         已确认"""
        self.appApi.Login(userName='13062200303')
        self.webApi.auditList(phoneNum=self.appText.get('cluePhone'), auditLevel=2)
        self.webApi.audit(auditStatue=1)

        """财务审核"""
        self.appApi.Login(userName='13062200310')
        self.webApi.finance_deal_auditList(keyWord=self.appText.get('dealPhone'))
        self.webApi.finance_deal_audit()
        self.flowPath.deal_status(status=1, keyWord=self.appText.get('dealPhone'))
        self.appApi.transProgress()
        self.assertIn('总监', self.appText.get('directorAuditDesc'))
        self.assertIn('财务', self.appText.get('financialAuditDesc'))
        self.assertIn('经理', self.appText.get('managerAuditDesc'))

    def test_my_deal_06(self):
        """5、录入成交-二级审核失败    已驳回                         已驳回"""
        self.appApi.Login()
        self.webApi.Audit_management(customerDeal=True, customerDealLevel=2)
        # self.appApi.deal_List(transStatus=1)
        # self.webApi.detail()
        self.appApi.add_deal(Status=1)
        dome = time.strftime("%Y-%m-%d %H:%M:%S")
        self.webApi.auditList(phoneNum=self.appText.get('cluePhone'))
        self.webApi.audit(auditStatue=1)

        self.webApi.auditList(phoneNum=self.appText.get('cluePhone'), auditLevel=2)
        self.webApi.audit(auditStatue=2, auditRemark=dome + ' 成交审核不通过')

        self.flowPath.deal_status(status=2, keyWord=self.appText.get('dealPhone'))

    def test_my_deal_07(self):
        """1、审核中的成交              ---只能操作跟进，其他动作都不允许操作"""
        self.webApi.Audit_management(customerDeal=True, customerDealLevel=1)
        # self.appApi.deal_List(transStatus=1)
        # self.webApi.detail()
        self.appApi.add_deal(Status=1)
        dome1 = self.appApi.appText.get('dealPhone')

        # 流放公海  创建带看 暂缓跟进 客户转移 不可以删除
        self.appApi.client_exile_sea()
        self.assertEqual('已申请客户成交,正在审核中!', self.appApi.appText.get('data'))

        dome = time.strftime("%Y-%m-%d %H:%M:%S")
        self.appApi.ClientVisitAdd(projectAId=self.appApi.appText.get('houseId'),
                                   appointmentTime=dome,
                                   seeingConsultant=self.appApi.appText.get('consultantId'),
                                   appointConsultant=self.appApi.appText.get('consultantId'))
        self.assertEqual('已申请客户成交,正在审核中!', self.appApi.appText.get('data'))

        self.appApi.ClientTaskPause()
        self.assertEqual('已申请客户成交,正在审核中!', self.appApi.appText.get('data'))

        self.appApi.client_change()  # 线索转移
        self.assertEqual('已申请客户成交,正在审核中!', self.appApi.appText.get('data'))

        self.appApi.add_deal(Status=2)
        self.assertEqual('已申请客户成交,正在审核中!', self.appApi.appText.get('data'))

        """审核及财务审核"""
        self.webApi.auditList(phoneNum=self.appText.get('cluePhone'))
        self.webApi.audit()
        self.webApi.finance_deal_auditList(keyWord=dome1)
        self.webApi.finance_deal_audit()

    def test_my_deal_08(self):
        """2、修改成交后（如设置审核）  ---需重新审核"""
        self.webApi.Audit_management(customerDeal=True, customerDealLevel=1)
        # self.appApi.deal_List(transStatus=1)
        # self.webApi.detail()
        self.appApi.add_deal(Status=1)
        self.flowPath.deal_status(status=0, keyWord=self.appText.get('dealPhone'))
        dome = self.appApi.appText.get('clueId')
        self.assertNotEqual(0, int(self.webApi.webText.get('total')))
        self.assertEqual(dome, self.webApi.webText.get('clueId'))

        """审核及财务审核"""
        self.webApi.auditList(phoneNum=self.appText.get('cluePhone'))
        self.webApi.audit()
        self.webApi.finance_deal_auditList(keyWord=self.appText.get('dealPhone'))
        self.webApi.finance_deal_audit()

    def test_my_deal_10(self):
        """一级审核没有通过的情况下不显示出来"""
        self.webApi.Audit_management(customerDeal=True, customerDealLevel=2)
        self.flowPath.add_deal_new()
        self.webApi.auditList(phoneNum=self.appText.get('cluePhone'))
        self.webApi.audit(auditStatue=2, auditRemark='审核失败')

        self.webApi.auditList(phoneNum=self.appText.get('cluePhone'), auditLevel=2)
        if self.webText.get('web_total') != 0:
            raise RuntimeError('审核管理（成交）一级审核没有通过的情况， 总监审核出来了')

    def test_my_deal_11(self):
        """财务审核失败后 查看成交的状态？"""
        self.webApi.Audit_management(customerDeal=True, customerDealLevel=1)
        self.appApi.deal_List(transStatus=1)
        self.webApi.detail()
        self.appApi.add_deal(Status=1)
        self.webApi.auditList(phoneNum=self.appText.get('cluePhone'))
        self.webApi.audit()
        self.webApi.finance_deal_auditList(keyWord=self.appText.get('dealPhone'))
        self.webApi.finance_deal_audit(auditStatue=2, dealAmount='',
                                       remark=time.strftime("%Y-%m-%d %H:%M:%S") + '审核不通过')
        self.appApi.deal_List(keyWord=self.appText.get('dealPhone'))
        self.assertEqual('2', self.appText.get('transStatus'))

    def test_my_deal_12(self):
        """60天成交总套数业绩与带看成交统计进行对比"""
        self.appApi.agoTime()
        self.webApi.visit_deal_statistics()
        self.appApi.deal_statistics()

        """60天成交总套数对比"""
        if self.appText.get('dealCount') != self.webText.get('web_transactionCount'):
            raise RuntimeError('60天成交总套数与带看成交统计的不一致')

        """60天成交业绩"""
        if self.appText.get('totalAmount') != self.webText.get('web_transactionResults'):
            raise RuntimeError('60天成交业绩与带看成交统计的不一致')

        """还原日期"""
        self.appApi.get_current_month_start_and_end(date=time.strftime("%Y-%m-%d"))

    def test_my_deal_13(self):
        """查看成交进度审核人"""



