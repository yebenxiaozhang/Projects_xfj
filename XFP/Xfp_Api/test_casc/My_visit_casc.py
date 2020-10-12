# -*- coding: utf-8 -*-
# @Time    : 2020/3/21 11:08
# @Author  : 潘师傅
# @File    : My_visit_casc.py

"""我的带看-相关"""
from XFP.PubilcAPI.flowPath import *
"""
无审核-正常流程：····························· 流放公海状态
    1、创建带看          进行中                   已取消
    2、完成带看          已完成                   已完成
    3、提前结束带看      已取消                   已取消

一级审核-正常流程：·····································流放公海的状态
    1、创建带看-待审核                   审核中             已取消
    2、创建带看-审核成功                 进行中             已取消
    3、创建带看-审核失败                 已驳回             已取消
    4、审核成功-完成带看                 已完成             已完成
    5、审核成功-提前结束带看             已取消             已取消

二级审核-正常流程······································流放公海的状态
    1、创建带看-待审核          申请中                     已取消
    2、创建带看-一级审核失败    已驳回                     已取消
    3、创建带看-一级审核成功    审核中                     已取消
    4、创建带看-二级审核失败    已驳回                     已取消
    5、创建带看-二级审核成功    进行中                     已取消
    6、审核成功-完成带看        已完成                     已完成
    7、审核成功-提前结束带看    已取消                     已取消
    
操作事项：
    1、审核失败的带看---不允许操作
    2、提前结束的带看---不允许操作
    3、审核中的带看  ---不允许操作
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
        """3、提前结束带看      已取消                   已取消"""
        self.flowPath.add_visit()
        self.flowPath.advance_over_visit()
        self.flowPath.visit_status(status='已取消')
        self.flowPath.client_exile_sea()
        self.flowPath.visit_status(status='已取消')

    def test_my_visit_04(self):
        """1、创建带看-待审核                   审核中             已取消"""
        self.webApi.Audit_management(customerVisit=True, customerVisitLevel=1)  # 修改配置审核
        self.flowPath.add_visit()
        self.flowPath.visit_status(status='申请中')
        self.flowPath.client_exile_sea()
        self.flowPath.visit_status(status='已取消')

    def test_my_visit_05(self):
        """2、创建带看-审核成功                 进行中             已取消"""
        self.webApi.Audit_management(customerVisit=True, customerVisitLevel=1)  # 修改配置审核
        self.flowPath.add_visit()
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
        self.webApi.auditApply(customerId=self.appText.get('customerId'), isAudit=False)  # 审核失败
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
        self.flowPath.visit_status(status='申请中')
        self.flowPath.client_exile_sea()
        self.flowPath.visit_status(status='已取消')

    def test_my_visit_10(self):
        """2、创建带看-一级审核失败    已驳回                     已驳回"""
        self.webApi.Audit_management(customerVisit=True, customerVisitLevel=2)  # 修改配置审核
        self.flowPath.add_visit()
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
        self.flowPath.client_exile_sea()
        self.flowPath.visit_status(status='已取消')

    def test_my_visit_12(self):
        """4、创建带看-二级审核失败    已驳回                     已驳回"""
        self.webApi.Audit_management(customerVisit=True, customerVisitLevel=2)  # 修改配置审核
        self.flowPath.add_visit()
        self.webApi.audit_List()  # 审核列表
        self.webApi.auditApply(customerId=self.appText.get('customerId'))  # 审核
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
        self.flowPath.client_exile_sea()
        self.flowPath.visit_status(status='已取消')

    def test_my_visit_14(self):
        """6、审核成功-完成带看        已完成                     已完成"""
        self.webApi.Audit_management(customerVisit=True, customerVisitLevel=2)  # 修改配置审核
        self.flowPath.add_visit()
        self.webApi.audit_List()  # 审核列表
        self.webApi.auditApply(customerId=self.appText.get('customerId'))  # 审核
        self.webApi.audit_List(auditLevel=2)  # 审核列表
        self.webApi.auditApply(customerId=self.appText.get('customerId'), vlue=2)  # 审核
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



