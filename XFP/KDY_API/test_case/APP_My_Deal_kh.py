# -*- coding: utf-8 -*-
# @Time    : 2020/3/21 11:08
# @Author  : 潘师傅
# @File    : My_Deal_casc.py

"""我的成交-相关"""
from PubilcAPI.flowPath import *

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

        """审核-成交相关-财务"""
        cls.webApi.finance_deal_auditList()
        while cls.appText.get('web_total') != 0:
            cls.webApi.finance_deal_audit(auditStatue=2, remark=time.strftime("%Y-%m-%d %H:%M:%S") + '审核不通过')
            cls.webApi.finance_deal_auditList()

        """审核-成交相关-经理"""
        cls.webApi.auditList()
        while cls.appText.get('web_total') != 0:
            cls.webApi.audit(auditStatue=2, auditRemark=' 审核失败')
            cls.webApi.auditList()
        cls.webApi.auditList(auditLevel=2)
        while cls.appText.get('web_total') != 0:
            cls.webApi.audit(auditStatue=2, auditRemark=' 审核失败')
            cls.webApi.auditList(auditLevel=2)

        """去除一些客户及线索"""
        cls.appApi.my_clue_list()
        while cls.appText.get('total') >= 5:
            cls.flowPath.clue_exile_sea()
            cls.appApi.my_clue_list()

        cls.appApi.ClientList()
        while cls.appText.get('total') >= 5:
            cls.appApi.client_exile_sea()
            cls.appApi.ClientList()

        cls.flowPath.client_list_non_null()
        cls.appApi.visitProject_list()
        if cls.appText.get('web_total') == 0:
            cls.flowPath.add_visit()
            cls.flowPath.accomplish_visit()
            cls.appApi.visitProject_list()

    def test_my_deal_01(self):
        """1、录入成交          已确认                    已确认"""
        """1- 客户录入成交不影响首页待办"""
        self.appApi.GetUserAgenda()
        dome = self.appText.get('total')
        self.appApi.ClientList()
        self.appApi.add_deal()
        self.appApi.GetUserAgenda()
        self.assertEqual(dome, self.appText.get('total'))
        self.appApi.deal_List(keyWord=self.appText.get('dealPhone'))
        """成交列表查询是否有成交单号"""
        if self.appText.get('transOrderNo') is None:
            print('新建成交没有成交单号')
        self.webApi.detail()
        self.flowPath.deal_status(status=1, keyWord=self.appText.get('dealPhone'))
        """成交项目为网签 才需要财务进行审核"""
        self.webApi.finance_deal_auditList(keyWord=self.appText.get('dealPhone'))
        if self.appText.get('web_total') != 0:
            raise RuntimeError('成交项目为网签 才需要财务进行审核')

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
        self.flowPath.deal_status(status=1, keyWord=self.appText.get('dealPhone'))
        # self.webApi.finance_deal_auditList(keyWord=self.appText.get('dealPhone'))
        # self.webApi.finance_deal_audit()
        # self.flowPath.deal_status(status=1, keyWord=self.appText.get('dealPhone'))

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
        # self.appApi.ClueInfo()
        self.appApi.add_deal(Status=1)

        self.appApi.Login(userName='13062200302')
        self.webApi.auditList(phoneNum=self.appText.get('cluePhone'))
        self.webApi.audit(auditStatue=1)

        """4、录入成交-二级审核成功    已确认                         已确认"""
        self.appApi.Login(userName='13062200303')
        self.webApi.auditList(phoneNum=self.appText.get('cluePhone'), auditLevel=2)
        self.webApi.audit(auditStatue=1)

        """查看审核人是否一一对应"""
        self.appApi.transProgress()
        self.assertIn('总监', self.appText.get('directorAuditDesc'))
        # self.assertIn('财务', self.appText.get('financialAuditDesc'))
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

        """审核及"""
        self.webApi.auditList(phoneNum=self.appText.get('cluePhone'))
        self.webApi.audit()

    def test_my_deal_08(self):
        """2、修改成交后（如设置审核）  ---需重新审核"""
        self.webApi.Audit_management(customerDeal=True, customerDealLevel=1)
        # self.appApi.deal_List(transStatus=1)
        # self.webApi.detail()
        """成交项为网签"""
        self.flowPath.get_label(labelNo='CJX', labelName='成交项目',
                                newlabelName='网签')
        self.appText.set_map('CJX', self.appText.get('labelId'))
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
        self.appApi.deal_List(transStatus=1, transProgressStatus=2)
        self.appApi.ClueInfo()
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
            print('我的成交60天成交总套数与带看成交统计的不一致')

        """60天成交业绩"""
        if self.appText.get('totalAmount') != self.webText.get('web_transactionResults'):
            print('我的成交60天成交业绩与带看成交统计的不一致')

        """还原日期"""
        self.appApi.get_current_month_start_and_end(date=time.strftime("%Y-%m-%d"))

    def test_my_deal_13(self):
        """公海不显示已经成交的客户"""
        self.webApi.Audit_management()
        self.appApi.ClientList()
        self.appApi.deal_List(keyWord=self.appText.get('orderNo'))
        if self.appText.get('total') == 0:
            self.appApi.visitProject_list()
            if self.appText.get('web_total') == 0:
                self.flowPath.add_visit()
                self.flowPath.accomplish_visit()
                self.appApi.visitProject_list()
            self.appApi.add_deal()
            self.webApi.finance_deal_auditList(keyWord=self.appText.get('dealPhone'))
            self.webApi.finance_deal_audit()
        self.appApi.client_info()
        self.appApi.client_exile_sea()
        self.appApi.SeaList(keyWord=self.appText.get('cluePhone'), isTrans=2)  # 公海列表
        if self.appText.get('total') != 0:
            raise RuntimeError('公海不显示已经成交的客户')

        # 验证返回字段 是否为 ture
        self.appApi.SeaList(keyWord=self.appText.get('cluePhone'))  # 公海列表
        if self.appText.get('isTrans') is 'ture':
            raise RuntimeError('公海列表已成交的客户返回值isTrans=True')



