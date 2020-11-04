# -*- coding: utf-8 -*-
# @Time    : 2020/3/21 11:08
# @Author  : 潘师傅
# @File    : Follow_apply_casc.py

"""跟进申请-相关"""
from XFP.PubilcAPI.flowPath import *

"""
无审核-正常流程：·······现状态··············· 操作流放公海
  1、客户申请暂缓        已同意                 已同意
  2、线索无效终止        已同意
  3、客户无效终止        已同意
  
 一级审核-正常流程：···············现状态··················操作流放公海成功
  1、客户申请暂缓跟进-待审核       申请中 
  2、客户申请暂缓跟进-审核失败     已驳回                 已取消
  3、客户申请暂缓跟进-审核成功     已同意                 已同意
  4、线索无效终止-待审核           申请中                
  5、线索无效终止-审核失败         已驳回
  6、线索无效终止-审核成功         已同意
  7、客户无效终止-待审核           申请中
  8、客户无效终止-审核成功         已同意
  9、客户无效终止-审核失败         已驳回
  
 二级审核-正常流程························现状态·········流放公海的状态
  1、客户申请暂缓跟进-待审核              申请中 
  2、客户申请暂缓跟进-一级审核失败        已驳回            已取消
  3、客户申请暂缓跟进-一级审核成功        审核中 
  4、客户申请暂缓跟进-二级审核失败        已驳回            已取消
  5、客户申请暂缓跟进-二级审核成功        已同意            已同意
  6、线索无效终止-待审核                  申请中
  7、线索无效终止-一级审核失败            已驳回
  8、线索无效终止-一级审核成功            审核中
  9、线索无效终止-二级审核失败            已驳回
  10、线索无效终止-二级审核成功           已同意
  11、客户无效终止-待审核                 申请中
  12、客户无效终止-一级审核失败           已驳回
  13、客户无效终止-一级审核成功           审核中
  14、客户无效终止-二级审核失败           已驳回
  15、客户无效终止-二级审核成功           已同意
 
 注意事项：
  1、线索终止审核中 ---不允许转客户
  2、客户终止跟进审核中 ---不允许创建带看，不允许录成交，不允许暂缓，不允许流放公海（无论是否开启审核，都不允许操作）
  3、客户暂缓审核中---不允许创建带看，不允许录成交，不允许流放公海（无论是否开启审核，都不允许操作）
  4、客户带看审核中---不允许再次录带看，不可以完成本次带看，不能提前结束带看，不允许流放公海（无论是否开启审核，都不允许操作）     
  
"""


class FollowApplyTestCase(unittest.TestCase):
    """客第壹——跟进申请"""

    def __init__(self, *args, **kwargs):
        super(FollowApplyTestCase, self).__init__(*args, **kwargs)
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

    def setUp(self):
        """残留审核 失败！！！"""
        self.webApi.audit_List()
        while self.webApi.webText.get('total') != 0:
            self.webApi.auditApply(isAudit=False, auditRemark='客户流放公海')
            self.webApi.audit_List()
        self.webApi.audit_List(auditLevel=2)
        while self.webApi.webText.get('total') != 0:
            self.webApi.auditApply(isAudit=False, auditRemark='客户流放公海')
            self.webApi.audit_List()

    def test_follow_apply_01(self):
        """1、客户申请暂缓        已同意                 已同意"""
        self.flowPath.client_list_non_null()
        self.flowPath.suspend_follow()
        self.appApi.ClientTask(taskType=2)  # 待办
        self.assertEqual(time.strftime("%Y-%m-%d"), self.appApi.appText.get('endTime')[:10])
        dome = self.appApi.appText.get('clueId')
        self.appApi.follow_apply()
        self.assertNotEqual(dome, self.appApi.appText.get('clueId'))
        self.flowPath.client_exile_sea()
        self.assertEqual(200, self.appApi.appText.get('code'))

    def test_follow_apply_02(self):
        """2、线索无效终止        已同意"""
        self.flowPath.clue_non_null()
        self.flowPath.clue_exile_sea()
        dome = self.appApi.appText.get('clueId')
        self.appApi.follow_apply()
        self.assertNotEqual(dome, self.appApi.appText.get('clueId'))

    def test_follow_apply_03(self):
        """3、客户无效终止        已同意"""
        self.flowPath.client_list_non_null()
        self.flowPath.client_exile_sea()
        dome = self.appApi.appText.get('clueId')
        self.appApi.follow_apply()
        self.assertNotEqual(dome, self.appApi.appText.get('clueId'))

    def test_follow_apply_04(self):
        """1、客户申请暂缓跟进-待审核       申请中"""
        self.flowPath.client_list_non_null()
        self.webApi.Audit_management(suspend=True, suspendLevel=1)  # 修改配置审核
        self.flowPath.suspend_follow()
        self.flowPath.apply_status(status='申请中')

        """2、客户申请暂缓跟进-审核失败     已驳回                 已取消"""
        dome = time.strftime("%Y-%m-%d %H:%M:%S")
        self.webApi.audit_List()  # 审核列表
        self.webApi.auditApply(customerId=self.appApi.appText.get('customerId'),
                               isAudit=False, auditRemark=dome + ' python-跟进申请不通过',
                               endTime=time.strftime("%Y-%m-%d ") + '22:00:00')
        self.flowPath.apply_status(status='已驳回')
        self.assertEqual(dome + ' python-跟进申请不通过', self.appApi.appText.get('auditRemark'))
        self.flowPath.client_exile_sea()
        self.flowPath.apply_status(status='已驳回')

    def test_follow_apply_06(self):
        """3、客户申请暂缓跟进-审核成功     已同意                 已同意"""
        self.flowPath.client_list_non_null()
        self.webApi.Audit_management(suspend=True, suspendLevel=1)  # 修改配置审核
        self.flowPath.suspend_follow()
        self.webApi.audit_List()  # 审核列表
        self.webApi.auditApply(customerId=self.appApi.appText.get('customerId'),
                               endTime=time.strftime("%Y-%m-%d ") + '22:00:00')
        self.flowPath.apply_status(status='已同意')
        self.flowPath.client_exile_sea()
        self.flowPath.apply_status(status='已同意')

    def test_follow_apply_07(self):
        """4、线索无效终止-待审核           申请中"""
        self.flowPath.clue_non_null()
        self.webApi.Audit_management(clueStop=True, clueStopLevel=1)
        self.flowPath.clue_exile_sea()
        self.flowPath.apply_status(status='申请中')

        """5、线索无效终止-审核失败         已驳回"""
        dome = time.strftime("%Y-%m-%d %H:%M:%S")
        self.webApi.audit_List()  # 审核列表
        self.webApi.auditApply(isAudit=False, auditRemark=dome + ' 线索流放审核不通过')
        self.flowPath.apply_status(status='已驳回')
        self.assertEqual(dome + ' 线索流放审核不通过', self.appApi.appText.get('auditRemark'))

    def test_follow_apply_09(self):
        """6、线索无效终止-审核成功         已同意"""
        self.flowPath.clue_non_null()
        self.webApi.Audit_management(clueStop=True, clueStopLevel=1)
        self.flowPath.clue_exile_sea()
        self.webApi.audit_List()  # 审核列表
        self.webApi.auditApply()
        self.flowPath.apply_status(status='已同意')

    def test_follow_apply_10(self):
        """7、客户无效终止-待审核           申请中"""
        self.flowPath.client_list_non_null()
        self.webApi.Audit_management(customerStop=True, customerStopLevel=1)  # 修改配置审核
        self.flowPath.client_exile_sea()
        self.flowPath.apply_status(status='申请中')

        """8、客户无效终止-审核成功         已同意"""
        self.webApi.audit_List()  # 审核列表
        self.webApi.auditApply(customerId=self.appApi.appText.get('customerId'))
        self.flowPath.apply_status(status='已同意')

    def test_follow_apply_12(self):
        """9、客户无效终止-审核失败         已驳回"""
        dome = time.strftime("%Y-%m-%d %H:%M:%S")
        self.flowPath.client_list_non_null()
        self.webApi.Audit_management(customerStop=True, customerStopLevel=1)  # 修改配置审核
        self.flowPath.client_exile_sea()
        self.webApi.audit_List()  # 审核列表
        self.webApi.auditApply(isAudit=False, auditRemark=dome + '客户无效终止审核失败')
        self.flowPath.apply_status(status='已驳回')
        self.assertEqual(dome + '客户无效终止审核失败', self.appApi.appText.get('auditRemark'))

    def test_follow_apply_13(self):
        """ 1、客户申请暂缓跟进-待审核              申请中            已取消"""
        self.webApi.Audit_management(suspend=True, suspendLevel=2)  # 修改配置审核
        self.flowPath.client_list_non_null()
        self.flowPath.suspend_follow()
        self.flowPath.apply_status(status='申请中')

        """2、客户申请暂缓跟进-一级审核失败        已驳回            已驳回"""
        dome = time.strftime("%Y-%m-%d %H:%M:%S")
        self.webApi.audit_List()  # 审核列表
        self.webApi.auditApply(customerId=self.appApi.appText.get('customerId'),
                               isAudit=False, auditRemark=dome + 'python-跟进申请不通过',
                               endTime=time.strftime("%Y-%m-%d ") + '22:00:00')
        self.flowPath.apply_status(status='已驳回')
        self.assertEqual(dome + 'python-跟进申请不通过', self.appApi.appText.get('auditRemark'))
        self.flowPath.client_exile_sea()
        self.flowPath.apply_status(status='已驳回')

    def test_follow_apply_15(self):
        """3、客户申请暂缓跟进-一级审核成功        审核中            已取消"""
        self.webApi.Audit_management(suspend=True, suspendLevel=2)  # 修改配置审核
        self.flowPath.client_list_non_null()
        self.flowPath.suspend_follow()
        self.webApi.audit_List()  # 审核列表
        self.webApi.auditApply(customerId=self.appApi.appText.get('customerId'),
                               endTime=time.strftime("%Y-%m-%d ") + '22:00:00')
        self.flowPath.apply_status(status='审核中')

        """4、客户申请暂缓跟进-二级审核失败        已驳回            已取消"""
        dome = time.strftime("%Y-%m-%d %H:%M:%S")
        self.webApi.audit_List()  # 审核列表
        self.webApi.auditApply(customerId=self.appApi.appText.get('customerId'),
                               endTime=time.strftime("%Y-%m-%d ") + '22:00:00')
        self.webApi.audit_List(auditLevel=2)
        self.webApi.auditApply(customerId=self.appApi.appText.get('customerId'), isAudit=False,
                               auditRemark=dome + ' 暂申请不通过', vlue=2,
                               endTime=time.strftime("%Y-%m-%d ") + '22:00:00')
        self.flowPath.apply_status(status='已驳回')
        self.assertEqual(dome + ' 暂申请不通过', self.appApi.appText.get('auditRemark'))
        self.flowPath.client_exile_sea()
        self.flowPath.apply_status(status='已驳回')

    def test_follow_apply_17(self):
        """5、客户申请暂缓跟进-二级审核成功        已同意            已同意"""
        self.webApi.Audit_management(suspend=True, suspendLevel=2)  # 修改配置审核
        self.flowPath.client_list_non_null()
        self.flowPath.suspend_follow()
        self.webApi.audit_List()  # 审核列表
        self.webApi.auditApply(customerId=self.appApi.appText.get('customerId'),
                               endTime=time.strftime("%Y-%m-%d ") + '22:00:00')
        self.webApi.audit_List(auditLevel=2)
        self.webApi.auditApply(customerId=self.appApi.appText.get('customerId'), vlue=2,
                               endTime=time.strftime("%Y-%m-%d ") + '22:00:00')
        self.flowPath.apply_status(status='已同意')
        self.flowPath.client_exile_sea()
        self.flowPath.apply_status(status='已同意')

    def test_follow_apply_18(self):
        """6、线索无效终止-待审核                  申请中"""
        self.flowPath.clue_non_null()
        self.webApi.Audit_management(clueStop=True, clueStopLevel=2)
        self.flowPath.clue_exile_sea()
        self.flowPath.apply_status(status='申请中')

        """7、线索无效终止-一级审核失败            已驳回"""
        self.webApi.audit_List()        # 审核列表
        dome = time.strftime("%Y-%m-%d %H:%M:%S")
        self.webApi.auditApply(isAudit=False, auditRemark=dome + ' 线索流放审核不通过')
        self.flowPath.apply_status(status='已驳回')
        self.assertEqual(dome + ' 线索流放审核不通过', self.appApi.appText.get('auditRemark'))

    def test_follow_apply_20(self):
        """8、线索无效终止-一级审核成功            审核中"""
        self.flowPath.clue_non_null()
        self.webApi.Audit_management(clueStop=True, clueStopLevel=2)
        self.flowPath.clue_exile_sea()
        self.flowPath.apply_status(status='申请中')
        dome = time.strftime("%Y-%m-%d %H:%M:%S")
        self.webApi.audit_List()        # 审核列表
        self.webApi.auditApply()
        self.flowPath.apply_status(status='审核中')

        """9、线索无效终止-二级审核失败            已驳回"""
        self.webApi.audit_List(auditLevel=2)        # 审核列表
        self.webApi.auditApply(vlue=2, isAudit=False, auditRemark=dome + ' 线索流放审核不通过')
        self.flowPath.apply_status(status='已驳回')
        self.assertEqual(dome + ' 线索流放审核不通过', self.appApi.appText.get('auditRemark'))

    def test_follow_apply_21(self):
        """10、线索无效终止-二级审核成功           已同意"""
        self.flowPath.clue_non_null()
        self.webApi.Audit_management(clueStop=True, clueStopLevel=2)
        self.flowPath.clue_exile_sea()
        self.webApi.audit_List()        # 审核列表
        self.webApi.auditApply()
        self.webApi.audit_List(auditLevel=2)        # 审核列表
        self.webApi.auditApply(vlue=2)
        self.flowPath.apply_status(status='已同意')

    def test_follow_apply_22(self):
        """  11、客户无效终止-待审核                 申请中"""
        self.flowPath.client_list_non_null()
        self.webApi.Audit_management(customerStop=True, customerStopLevel=2)  # 修改配置审核
        self.flowPath.client_exile_sea()
        self.flowPath.apply_status(status='申请中')
        dome = time.strftime("%Y-%m-%d %H:%M:%S")

        """12、客户无效终止-一级审核失败           已驳回"""
        self.webApi.audit_List()        # 审核列表
        self.webApi.auditApply(isAudit=False, auditRemark=dome + '客户无效终止审核失败')
        self.flowPath.apply_status(status='已驳回')
        self.assertEqual(dome + '客户无效终止审核失败', self.appApi.appText.get('auditRemark'))

    def test_follow_apply_23(self):
        """13、客户无效终止-一级审核成功           审核中"""
        self.flowPath.client_list_non_null()
        self.webApi.Audit_management(customerStop=True, customerStopLevel=2)  # 修改配置审核
        self.flowPath.client_exile_sea()
        self.flowPath.apply_status(status='申请中')
        dome = time.strftime("%Y-%m-%d %H:%M:%S")
        self.webApi.audit_List()        # 审核列表
        self.webApi.auditApply()
        self.flowPath.apply_status(status='审核中')

        """14、客户无效终止-二级审核失败           已驳回"""
        self.webApi.audit_List(auditLevel=2)        # 审核列表
        self.webApi.auditApply(vlue=2, isAudit=False, auditRemark=dome + '客户无效终止审核失败')
        self.flowPath.apply_status(status='已驳回')
        self.assertEqual(dome + '客户无效终止审核失败', self.appApi.appText.get('auditRemark'))

    def test_follow_apply_24(self):
        """15、客户无效终止-二级审核成功           已同意"""
        self.flowPath.client_list_non_null()
        self.webApi.Audit_management(customerStop=True, customerStopLevel=2)  # 修改配置审核
        self.flowPath.client_exile_sea()
        self.flowPath.apply_status(status='申请中')
        self.webApi.audit_List()        # 审核列表
        self.webApi.auditApply()
        self.flowPath.apply_status(status='审核中')

        """14、客户无效终止-二级审核失败           已驳回"""
        self.webApi.audit_List(auditLevel=2)        # 审核列表
        self.webApi.auditApply(customerId=self.appApi.appText.get('customerId'),
                               vlue=2)
        self.flowPath.apply_status(status='已同意')

    def test_follow_apply_25(self):
        """1、线索终止审核中 ---不允许转客户"""
        self.flowPath.clue_non_null()
        self.webApi.Audit_management(clueStop=True, clueStopLevel=1)
        self.flowPath.clue_exile_sea()
        self.appApi.ClueInfo()
        self.appApi.ClientEntering(callName=self.appApi.RandomText(textArr=surname),
                                   loanSituation='这个是贷款情况')
        self.assertEqual('已申请线索终止,正在审核中!', self.appApi.appText.get('data'))

    def test_follow_apply_26(self):
        """2、客户终止跟进审核中 ---不允许创建带看，不允许录成交，
        不允许暂缓，（无论是否开启审核，都不允许操作）"""
        self.flowPath.client_list_non_null()
        self.webApi.Audit_management(customerStop=True, customerStopLevel=1)  # 修改配置审核
        self.flowPath.client_exile_sea()

        self.appApi.GetMatchingAreaHouse()
        dome = time.strftime("%Y-%m-%d %H:%M:%S")
        self.appApi.ClientVisitAdd(projectAId=self.appApi.appText.get('houseId'),
                                   appointmentTime=dome,
                                   seeingConsultant=self.appApi.appText.get('consultantId'),
                                   appointConsultant=self.appApi.appText.get('consultantId'))
        self.assertEqual('已申请客户终止,正在审核中!', self.appApi.appText.get('data'))

        self.appApi.GetMatchingAreaHouse()  # 匹配楼盘
        assert 0 != self.appApi.appText.get('total'), '匹配楼盘为空？'
        self.appApi.GetLabelList(labelNo='CJX', labelName='认购')
        self.appApi.add_deal()  # 录入成交
        self.assertEqual('已申请客户终止,正在审核中!', self.appApi.appText.get('data'))

        self.appApi.GetLabelList(labelNo='SQZHGJ', labelName='其他')
        self.appApi.ClientTaskPause()
        self.assertEqual('已申请客户终止,正在审核中!', self.appApi.appText.get('data'))

    def test_follow_apply_27(self):
        """3、客户暂缓审核中---不允许创建带看，不允许录成交，不允许流放公海（无论是否开启审核，都不允许操作）"""
        self.webApi.Audit_management(suspend=True, suspendLevel=1)  # 修改配置审核
        self.flowPath.client_list_non_null()
        self.flowPath.suspend_follow()

        self.appApi.GetMatchingAreaHouse()
        dome = time.strftime("%Y-%m-%d %H:%M:%S")
        self.appApi.ClientVisitAdd(projectAId=self.appApi.appText.get('houseId'),
                                   appointmentTime=dome,
                                   seeingConsultant=self.appApi.appText.get('consultantId'),
                                   appointConsultant=self.appApi.appText.get('consultantId'))
        self.assertEqual('已申请暂缓跟进,正在审核中!', self.appApi.appText.get('data'))

        self.appApi.GetMatchingAreaHouse()  # 匹配楼盘
        assert 0 != self.appApi.appText.get('total'), '匹配楼盘为空？'
        self.appApi.GetLabelList(labelNo='CJX', labelName='认购')
        self.appApi.add_deal()  # 录入成交
        self.assertEqual('已申请暂缓跟进,正在审核中!', self.appApi.appText.get('data'))

        self.flowPath.client_exile_sea()
        self.assertEqual('已申请暂缓跟进,正在审核中!', self.appApi.appText.get('data'))

    def test_follow_apply_28(self):
        """暂停后再次申请暂停"""
        self.flowPath.client_list_non_null()
        self.webApi.Audit_management(suspend=True, suspendLevel=1)  # 修改配置审核
        self.flowPath.suspend_follow()
        self.webApi.audit_List()  # 审核列表
        self.webApi.auditApply(customerId=self.appApi.appText.get('customerId'),
                               endTime=time.strftime("%Y-%m-%d ") + '22:00:00')
        self.appApi.ClientFollowList()
        self.appApi.ClueFollowSave(followType='客户', taskEndTime=time.strftime("%Y-%m-%d") + ' 22:00:00')
        self.appApi.GetLabelList(labelNo='SQZHGJ', labelName='其他')
        self.appApi.ClientTaskPause()
        self.assertEqual(200, self.appApi.appText.get('code'))


