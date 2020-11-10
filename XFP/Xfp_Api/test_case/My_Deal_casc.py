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
    """客第壹——我的成交"""

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
        cls.appApi = cls.do_request
        cls.appApi.Login()
        cls.appApi.GetUserData()
        cls.request = webApi()
        cls.webApi = cls.request
        cls.webApi.Audit_management()
        cls.flow = flowPath()
        cls.flowPath = cls.flow
        cls.appText = GlobalMap()
        """线索来源"""
        cls.flowPath.get_label(labelNo='XSLY', labelName='线索来源',
                               newlabelName='百度小程序')
        cls.appText.set_map('XSLY', cls.appText.get('labelId'))

        """线索来源_幸福派总部"""
        cls.flowPath.get_label(labelNo='XSLY', labelName='线索来源',
                               newlabelName='幸福派总部')
        cls.appText.set_map('XSLY_admin', cls.appText.get('labelId'))
        """线索标签"""
        cls.appApi.GetUserLabelList(userLabelType='线索标签')
        if cls.appText.get('total') == 0:
            cls.appApi.AddUserLabel()
            cls.appApi.GetUserLabelList(userLabelType='线索标签')
        cls.appText.set_map('XSBQ', cls.appText.get('labelData'))
        """终止跟进"""
        cls.flowPath.get_label(labelNo='SZGJYY', labelName='终止跟进原因',
                               newlabelName='客户已成交')
        cls.appText.set_map('ZZGJ', cls.appText.get('labelId'))
        """成交项"""
        cls.flowPath.get_label(labelNo='CJX', labelName='成交项目',
                               newlabelName='认购')
        cls.appText.set_map('CJX', cls.appText.get('labelId'))
        """出行方式"""
        cls.flowPath.get_label(labelNo='CXFS', labelName='出行方式',
                               newlabelName='自驾')
        cls.appText.set_map('CXFS', cls.appText.get('labelId'))
        """客户意向等级"""
        cls.appApi.GetLabelList(labelNo='KHYXDJ')                       # 查询购房意向loanSituation
        cls.appText.set_map('KHYXDJ', cls.appText.get('labelId'))
        cls.appApi.GetLabelList(labelNo='ZJZZ')                         # 查询资金资质
        cls.appText.set_map('ZJZZ', cls.appText.get('labelId'))
        cls.appApi.GetLabelList(labelNo='GFMD')                         # 查询购房目的
        cls.appText.set_map('GFMD', cls.appText.get('labelId'))
        cls.appApi.GetLabelList(labelNo='WYSX')                         # 查询物业属性
        cls.appText.set_map('WYSX', cls.appText.get('labelId'))
        cls.appApi.GetLabelList(labelNo='GFZZ')                         # 查询购房资质
        cls.appText.set_map('GFZZ', cls.appText.get('labelId'))
        cls.appApi.GetLabelList(labelNo='SFSTF')                        # 查询是否首套
        cls.appText.set_map('SFSTF', cls.appText.get('labelId'))
        cls.appApi.GetMatchingArea()                                    # 查询匹配区域
        cls.appApi.GetMatchingAreaHouse()                               # 匹配楼盘
        cls.appApi.GetLabelList(labelNo='QTKHXQ')                       # 查询客户需求
        cls.appText.set_map('QTKHXQ', cls.appText.get('labelId'))
        cls.appApi.ConsultantList()                                     # 咨询师列表
        cls.appApi.GetLabelList(labelNo='SQZHGJ', labelName='其他')
        cls.appText.set_map('ZHGJ', cls.appText.get('labelId'))         # 暂缓跟进
        cls.flowPath.get_label(labelNo='XXFL', labelName='信息分类',
                               newlabelName='信息分类一')
        cls.appText.set_map('XXFL', cls.appText.get('labelId'))         # 信息分类
        cls.flowPath.get_label(labelNo='DLGS', labelName='代理公司',
                               newlabelName='代理公司一')
        cls.appText.set_map('DLGS', cls.appText.get('labelId'))         # 代理公司
        cls.flowPath.get_label(labelNo='WDFL', labelName='问答分类',
                               newlabelName='问答分类一')
        cls.appText.set_map('WDFL', cls.appText.get('labelId'))         # 问答分类

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
        self.flowPath.deal_status(status=1)

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
        self.appApi.client_exile_sea()
        self.assertEqual('已申请客户成交,正在审核中!', self.appApi.appText.get('data'))

        self.appApi.GetMatchingAreaHouse()
        dome = time.strftime("%Y-%m-%d %H:%M:%S")
        self.appApi.ClientVisitAdd(projectAId=self.appApi.appText.get('houseId'),
                                   appointmentTime=dome,
                                   seeingConsultant=self.appApi.appText.get('consultantId'),
                                   appointConsultant=self.appApi.appText.get('consultantId'))
        self.assertEqual('已申请客户成交,正在审核中!', self.appApi.appText.get('data'))

        self.appApi.GetLabelList(labelNo='SQZHGJ', labelName='其他')
        self.appApi.ClientTaskPause()
        self.assertEqual('已申请客户成交,正在审核中!', self.appApi.appText.get('data'))

        self.appApi.client_change()        # 线索转移
        self.assertEqual('已申请客户成交,正在审核中!', self.appApi.appText.get('data'))

        self.appApi.deal_List()
        self.appApi.add_deal(Status=2, isDeleted=1)
        self.assertEqual('已申请客户成交,正在审核中!', self.appApi.appText.get('data'))

    def test_my_deal_08(self):
        """2、修改成交后（如设置审核）  ---需重新审核"""
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






