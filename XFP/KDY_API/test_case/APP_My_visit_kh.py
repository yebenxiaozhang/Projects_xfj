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


class TestCase(unittest.TestCase):
    """幸福派——我的带看"""

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
        cls.webApi.auditList()
        while cls.appApi.appText.get('web_total') != 0:
            cls.webApi.audit(auditStatue=2, auditRemark=' 审核失败')
            cls.webApi.auditList()
        cls.webApi.auditList(auditLevel=2)
        while cls.appApi.appText.get('web_total') != 0:
            cls.webApi.audit(auditStatue=2, auditRemark=' 审核失败')
            cls.webApi.auditList(auditLevel=2)

    def test_my_visit_01(self):
        """1、创建带看          进行中                   已取消"""
        self.flowPath.add_visit()
        self.flowPath.visit_status(status='无需审核')
        self.appApi.client_exile_sea()
        self.flowPath.visit_status(status='已取消')

    def test_my_visit_02(self):
        """2、完成带看          已完成                   已完成"""
        self.flowPath.add_visit()
        self.flowPath.accomplish_visit()
        self.flowPath.visit_status(status='已完成')
        self.appApi.client_exile_sea()
        self.flowPath.visit_status(status='已完成')

    def test_my_visit_03(self):
        """3、取消带看      已取消                   已取消"""
        self.flowPath.add_visit()
        self.flowPath.advance_over_visit()
        self.flowPath.visit_status(status='已取消')
        self.appApi.client_exile_sea()
        self.flowPath.visit_status(status='已取消')

    def test_my_visit_04(self):
        """1、创建带看-待审核                   审核中"""
        self.webApi.Audit_management(customerVisit=True, customerVisitLevel=1)  # 修改配置审核
        self.flowPath.add_visit()
        self.flowPath.visit_status(status='队长审核中')
        """2、创建带看-审核成功                 进行中             已取消"""
        self.webApi.auditList(phoneNum=self.appText.get('cluePhone'))
        self.webApi.audit()
        self.flowPath.visit_status(status='已同意')
        self.appApi.client_exile_sea()
        self.flowPath.visit_status(status='已取消')

    def test_my_visit_06(self):
        """3、创建带看-审核失败                 已驳回             已驳回"""
        self.webApi.Audit_management(customerVisit=True, customerVisitLevel=1)  # 修改配置审核
        self.flowPath.add_visit()
        self.webApi.auditList(phoneNum=self.appText.get('cluePhone'))
        self.webApi.audit(auditStatue=2, auditRemark=time.strftime("%Y-%m-%d %H:%M:%S") + ' 审核失败')

        self.flowPath.visit_status(status='已驳回')
        self.appApi.client_exile_sea()
        self.flowPath.visit_status(status='已取消')

    def test_my_visit_07(self):
        """4、审核成功-完成带看                 已完成             已完成"""
        self.webApi.Audit_management(customerVisit=True, customerVisitLevel=1)  # 修改配置审核
        self.flowPath.add_visit()
        self.webApi.auditList(phoneNum=self.appText.get('cluePhone'))
        self.webApi.audit()

        self.flowPath.accomplish_visit()
        self.flowPath.visit_status(status='已完成')
        self.appApi.client_exile_sea()
        self.flowPath.visit_status(status='已完成')

    def test_my_visit_08(self):
        """5、审核成功-提前结束带看             已取消             已取消"""
        self.webApi.Audit_management(customerVisit=True, customerVisitLevel=1)  # 修改配置审核
        self.flowPath.add_visit()
        self.webApi.auditList(phoneNum=self.appText.get('cluePhone'))
        self.webApi.audit()

        self.flowPath.advance_over_visit()
        self.flowPath.visit_status(status='已取消')
        self.appApi.client_exile_sea()
        self.flowPath.visit_status(status='已取消')

    def test_my_visit_09(self):
        """1、创建带看-待审核          申请中                     已取消"""
        self.webApi.Audit_management(customerVisit=True, customerVisitLevel=2)  # 修改配置审核
        self.flowPath.add_visit()
        self.flowPath.visit_status(status='队长审核中')
        """2、创建带看-一级审核失败    已驳回                     已驳回"""
        self.webApi.auditList(phoneNum=self.appText.get('cluePhone'))
        self.webApi.audit(auditStatue=2, auditRemark=time.strftime("%Y-%m-%d %H:%M:%S") + ' 审核失败')

        self.flowPath.visit_status(status='已驳回')
        self.appApi.client_exile_sea()
        self.flowPath.visit_status(status='已取消')

    def test_my_visit_11(self):
        """3、创建带看-一级审核成功    审核中                     已取消"""
        self.webApi.Audit_management(customerVisit=True, customerVisitLevel=2)  # 修改配置审核
        self.flowPath.add_visit()
        self.webApi.auditList(phoneNum=self.appText.get('cluePhone'))
        self.webApi.audit()

        self.flowPath.visit_status(status='总监审核中')
        """4、创建带看-二级审核失败    已驳回                     已取消"""
        self.webApi.auditList(phoneNum=self.appText.get('cluePhone'), auditLevel=2)
        self.webApi.audit(auditStatue=2, auditRemark=time.strftime("%Y-%m-%d %H:%M:%S") + ' 审核失败')

        self.flowPath.visit_status(status='已驳回')
        self.appApi.client_exile_sea()
        self.flowPath.visit_status(status='已取消')

    def test_my_visit_13(self):
        """5、创建带看-二级审核成功    进行中                     已取消"""
        self.webApi.Audit_management(customerVisit=True, customerVisitLevel=2)  # 修改配置审核
        self.flowPath.add_visit()
        self.webApi.auditList(phoneNum=self.appText.get('cluePhone'))
        self.webApi.audit()

        self.webApi.auditList(phoneNum=self.appText.get('cluePhone'), auditLevel=2)
        self.webApi.audit()

        self.flowPath.visit_status(status='已同意')
        self.flowPath.accomplish_visit()
        self.flowPath.visit_status(status='已完成')
        self.appApi.client_exile_sea()
        self.flowPath.visit_status(status='已完成')

    def test_my_visit_15(self):
        """7、审核成功-提前结束带看    已取消                     已取消"""
        self.webApi.Audit_management(customerVisit=True, customerVisitLevel=2)  # 修改配置审核
        self.flowPath.add_visit()
        self.webApi.auditList(phoneNum=self.appText.get('cluePhone'))
        self.webApi.audit()

        self.webApi.auditList(phoneNum=self.appText.get('cluePhone'), auditLevel=2)
        self.webApi.audit()

        self.flowPath.advance_over_visit()
        self.flowPath.visit_status(status='已取消')
        self.appApi.client_exile_sea()
        self.flowPath.visit_status(status='已取消')

    def test_my_visit_16(self):
        """1、审核失败的带看---不允许操作"""
        self.webApi.Audit_management(customerVisit=True, customerVisitLevel=1)  # 修改配置审核
        self.flowPath.add_visit()
        self.appApi.ClientTask(taskType='3')
        if self.appApi.appText.get('total') < 1:
            raise RuntimeError(self.appApi.appText.get('ApiXfpUrl'))
        self.appApi.visit_info()
        self.webApi.auditList(phoneNum=self.appText.get('cluePhone'))
        self.webApi.audit(auditStatue=2, auditRemark=time.strftime("%Y-%m-%d %H:%M:%S") + ' 审核失败')

        self.appApi.VisitFlow1(agencyId=self.appApi.appText.get('DLGS'),
                               receptionName=self.appApi.RandomText(textArr=surname),
                               receptionPhone='1' + str(int(time.time())), attachmentIds='1')
        self.assertEqual('带看计划已取消', self.appApi.appText.get('data'))

    def test_my_visit_18(self):
        """3、审核中的带看 ---不可以完成，不可以提前结束，不可以释放公海"""
        self.webApi.Audit_management()  # 修改配置审核
        self.flowPath.add_visit()
        self.flowPath.accomplish_visit()
        self.webApi.Audit_management(customerVisit=True, customerVisitLevel=1)  # 修改配置审核
        self.appApi.ClientVisitAdd(projectAId=self.appApi.appText.get('houseId'),
                                   appointmentTime=time.strftime("%Y-%m-%d %H:%M:%S"),
                                   seeingConsultant=self.appApi.appText.get('consultantId'),
                                   appointConsultant=self.appApi.appText.get('consultantId'))
        self.appApi.ClientTask(taskType='3')
        if self.appApi.appText.get('total') < 1:
            raise RuntimeError(self.appApi.appText.get('ApiXfpUrl'))
        self.appApi.visit_info()
        self.appApi.VisitFlow1(agencyId=self.appApi.appText.get('DLGS'),
                               receptionName=self.appApi.RandomText(textArr=surname),
                               receptionPhone='1' + str(int(time.time())), attachmentIds='1')
        self.assertEqual('带看计划审核中', self.appApi.appText.get('data'))

        self.appApi.visitProject_list()
        self.appApi.add_deal()  # 录入成交
        self.assertNotEqual(200, self.appApi.appText.get('code'))
        self.appApi.client_exile_sea()
        self.assertNotEqual(200, self.appApi.appText.get('code'))

        self.appApi.ClientTaskPause()
        self.assertNotEqual(200, self.appApi.appText.get('code'))

    def test_my_visit_19(self):
        """同一个客户只能存在一个带看 一个带看代办"""
        self.webApi.Audit_management()
        self.flowPath.add_visit()
        self.appApi.ClientVisitAdd(projectAId=self.appApi.appText.get('houseId'),
                                   seeingConsultant=self.appApi.appText.get('consultantId'),
                                   appointConsultant=self.appApi.appText.get('consultantId'))
        self.assertEqual(301, self.appText.get('code'))
        self.assertEqual('该客户存在未完成带看', self.appApi.appText.get('data'))
        self.flowPath.accomplish_visit()



