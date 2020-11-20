# -*- coding: utf-8 -*-
# @Time    : 2020/3/21 11:08
# @Author  : 潘师傅
# @File    : Follow_apply_casc.py

"""跟进申请-相关"""
from XFP.PubilcAPI.flowPath import *

"""
无审核-正常流程：·······现状态··············· 操作流放公海
  1、客户申请暂缓        已同意                 已同意
  
 一级审核-正常流程：···············现状态··················操作流放公海成功
  4、线索无效终止-待审核           申请中                
  5、线索无效终止-审核失败         已驳回
  6、线索无效终止-审核成功         已同意
  
 二级审核-正常流程························现状态·········流放公海的状态
  6、线索无效终止-待审核                  申请中
  7、线索无效终止-一级审核失败            已驳回
  8、线索无效终止-一级审核成功            审核中
  9、线索无效终止-二级审核失败            已驳回
  10、线索无效终止-二级审核成功           已同意

 
 注意事项：
  1、线索终止审核中 ---不允许转客户
  
"""


class TestCase(unittest.TestCase):
    """客第壹——跟进申请"""

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
        """残留审核 失败！！！"""
        cls.webApi.audit_List()
        while cls.webApi.webText.get('total') != 0:
            cls.webApi.auditApply(isAudit=False, auditRemark='客户流放公海')
            cls.webApi.audit_List()
        cls.webApi.audit_List(auditLevel=2)
        while cls.webApi.webText.get('total') != 0:
            cls.webApi.auditApply(isAudit=False, auditRemark='客户流放公海')
            cls.webApi.audit_List()

    def test_follow_apply_02(self):
        """2、线索无效终止        已同意"""
        self.flowPath.clue_non_null()
        self.flowPath.clue_exile_sea()
        dome = self.appApi.appText.get('clueId')
        self.appApi.follow_apply()
        self.assertNotEqual(dome, self.appApi.appText.get('clueId'))

    def test_follow_apply_07(self):
        """4、线索无效终止-待审核           申请中"""
        self.flowPath.clue_non_null()
        self.webApi.Audit_management(clueStop=True, clueStopLevel=1)
        self.flowPath.clue_exile_sea()

        try:
            self.flowPath.apply_status(status='申请中')
        except:
            self.flowPath.apply_status(status='审核中')

        """5、线索无效终止-审核失败         已驳回"""
        dome = time.strftime("%Y-%m-%d %H:%M:%S")
        self.webApi.audit_List(keyWord=self.appText.get('cluePhone'))  # 审核列表
        self.webApi.auditApply(isAudit=False, auditRemark=dome + ' 线索流放审核不通过')
        self.flowPath.apply_status(status='已驳回')
        self.assertEqual(dome + ' 线索流放审核不通过', self.appApi.appText.get('auditRemark'))

    def test_follow_apply_09(self):
        """6、线索无效终止-审核成功         已同意"""
        self.flowPath.clue_non_null()
        self.webApi.Audit_management(clueStop=True, clueStopLevel=1)
        self.flowPath.clue_exile_sea()
        self.webApi.audit_List(keyWord=self.appText.get('cluePhone'))  # 审核列表
        self.webApi.auditApply()
        self.flowPath.apply_status(status='已同意')

    def test_follow_apply_18(self):
        """6、线索无效终止-待审核                  申请中"""
        self.flowPath.clue_non_null()
        self.webApi.Audit_management(clueStop=True, clueStopLevel=2)
        self.flowPath.clue_exile_sea()
        try:
            self.flowPath.apply_status(status='申请中')
        except:
            self.flowPath.apply_status(status='审核中')
        """7、线索无效终止-一级审核失败            已驳回"""
        self.webApi.audit_List(keyWord=self.appText.get('cluePhone'))        # 审核列表
        dome = time.strftime("%Y-%m-%d %H:%M:%S")
        self.webApi.auditApply(isAudit=False, auditRemark=dome + ' 线索流放审核不通过')
        self.flowPath.apply_status(status='已驳回', vlue=1)
        self.assertEqual(dome + ' 线索流放审核不通过', self.appApi.appText.get('auditRemark'))

    def test_follow_apply_20(self):
        """8、线索无效终止-一级审核成功            审核中"""
        self.flowPath.clue_non_null()
        self.webApi.Audit_management(clueStop=True, clueStopLevel=2)
        self.flowPath.clue_exile_sea()
        try:
            self.flowPath.apply_status(status='申请中')
        except:
            self.flowPath.apply_status(status='审核中')
        dome = time.strftime("%Y-%m-%d %H:%M:%S")
        self.webApi.audit_List(keyWord=self.appText.get('cluePhone'))        # 审核列表
        self.webApi.auditApply()
        try:
            self.flowPath.apply_status(status='申请中')
        except:
            self.flowPath.apply_status(status='审核中')

        """9、线索无效终止-二级审核失败            已驳回"""
        self.webApi.audit_List(keyWord=self.appText.get('cluePhone'),auditLevel=2)        # 审核列表
        self.webApi.auditApply(vlue=2, isAudit=False, auditRemark=dome + ' 线索流放审核不通过')
        self.flowPath.apply_status(status='已驳回')
        self.assertEqual(dome + ' 线索流放审核不通过', self.appApi.appText.get('auditRemark'))

    def test_follow_apply_21(self):
        """10、线索无效终止-二级审核成功           已同意"""
        self.flowPath.clue_non_null()
        self.webApi.Audit_management(clueStop=True, clueStopLevel=2)
        self.flowPath.clue_exile_sea()
        self.webApi.audit_List(keyWord=self.appText.get('cluePhone'))        # 审核列表
        self.webApi.auditApply()
        self.webApi.audit_List(keyWord=self.appText.get('cluePhone'),auditLevel=2)        # 审核列表
        self.webApi.auditApply(vlue=2)
        self.flowPath.apply_status(status='已同意')

    def test_follow_apply_25(self):
        """1、线索终止审核中 ---不允许转客户"""
        self.flowPath.clue_non_null()
        self.webApi.Audit_management(clueStop=True, clueStopLevel=1)
        self.flowPath.clue_exile_sea()
        self.appApi.ClientEntering(callName=self.appApi.RandomText(textArr=surname),
                                   loanSituation='这个是贷款情况')
        self.assertEqual('已申请线索终止,正在审核中!', self.appApi.appText.get('data'))


