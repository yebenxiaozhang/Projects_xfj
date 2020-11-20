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

        cls.flowPath.get_label(labelNo='XXFL', labelName='信息分类',
                               newlabelName='信息分类一')
        cls.appText.set_map('XXFL', cls.appText.get('labelId'))         # 信息分类
        cls.flowPath.get_label(labelNo='DLGS', labelName='代理公司',
                               newlabelName='代理公司一')
        cls.appText.set_map('DLGS', cls.appText.get('labelId'))         # 代理公司
        cls.flowPath.get_label(labelNo='WDFL', labelName='问答分类',
                               newlabelName='问答分类一')
        cls.appText.set_map('WDFL', cls.appText.get('labelId'))         # 问答分类
        cls.webApi.consultant_allocition(isAppoint=1)

    def test_follow_apply_01(self):
        """1、线索无效终止        已同意"""
        self.flowPath.clue_non_null()
        self.appApi.follow_apply(keyWord=self.appText.get('cluePhone'))
        dome1 = self.appText.get('total')
        self.flowPath.clue_exile_sea()
        self.appApi.follow_apply(keyWord=self.appText.get('cluePhone'))
        if dome1 != self.appText.get('total'):
            raise RuntimeError("无审核的情况下 线索终止会多添加一个跟进申请")

    def test_follow_apply_02(self):
        """2、线索无效终止-待审核           申请中"""
        self.flowPath.clue_non_null()
        self.webApi.Audit_management(clueStop=True, clueStopLevel=1)
        self.flowPath.clue_exile_sea()

        try:
            self.flowPath.apply_status(status='申请中', keyWord=self.appText.get('cluePhone'))
        except:
            self.flowPath.apply_status(status='审核中', keyWord=self.appText.get('cluePhone'))

        """3、线索无效终止-审核失败         已驳回"""
        dome = time.strftime("%Y-%m-%d %H:%M:%S")
        self.webApi.audit_List(keyWord=self.appText.get('cluePhone'))  # 审核列表
        self.webApi.auditApply(isAudit=False, auditRemark=dome + ' 线索流放审核不通过')
        self.flowPath.apply_status(status='已驳回')
        self.assertEqual(dome + ' 线索流放审核不通过', self.appApi.appText.get('auditRemark'))

    def test_follow_apply_03(self):
        """6、线索无效终止-审核成功         已同意"""
        self.flowPath.clue_non_null()
        self.webApi.Audit_management(clueStop=True, clueStopLevel=1)
        self.flowPath.clue_exile_sea()
        self.webApi.audit_List(keyWord=self.appText.get('cluePhone'))  # 审核列表
        self.webApi.auditApply()
        self.flowPath.apply_status(status='已同意')

    def test_follow_apply_04(self):
        """6、线索无效终止-待审核                  申请中"""
        self.flowPath.clue_non_null()
        self.webApi.Audit_management(clueStop=True, clueStopLevel=2)
        self.flowPath.clue_exile_sea()
        try:
            self.flowPath.apply_status(status='申请中', keyWord=self.appText.get('cluePhone'))
        except:
            self.flowPath.apply_status(status='审核中', keyWord=self.appText.get('cluePhone'))
        """7、线索无效终止-一级审核失败            已驳回"""
        self.webApi.audit_List(keyWord=self.appText.get('cluePhone'))        # 审核列表
        dome = time.strftime("%Y-%m-%d %H:%M:%S")
        self.webApi.auditApply(isAudit=False, auditRemark=dome + ' 线索流放审核不通过')
        self.flowPath.apply_status(status='已驳回', vlue=1, keyWord=self.appText.get('cluePhone'))
        self.assertEqual(dome + ' 线索流放审核不通过', self.appApi.appText.get('auditRemark'))

    def test_follow_apply_05(self):
        """8、线索无效终止-一级审核成功            审核中"""
        self.flowPath.clue_non_null()
        self.webApi.Audit_management(clueStop=True, clueStopLevel=2)
        self.flowPath.clue_exile_sea()
        try:
            self.flowPath.apply_status(status='申请中', keyWord=self.appText.get('cluePhone'))
        except:
            self.flowPath.apply_status(status='审核中', keyWord=self.appText.get('cluePhone'))
        dome = time.strftime("%Y-%m-%d %H:%M:%S")
        self.webApi.audit_List(keyWord=self.appText.get('cluePhone'))        # 审核列表
        self.webApi.auditApply()
        try:
            self.flowPath.apply_status(status='申请中', keyWord=self.appText.get('cluePhone'))
        except:
            self.flowPath.apply_status(status='审核中', keyWord=self.appText.get('cluePhone'))

        """9、线索无效终止-二级审核失败            已驳回"""
        self.webApi.audit_List(keyWord=self.appText.get('cluePhone'),auditLevel=2)        # 审核列表
        self.webApi.auditApply(vlue=2, isAudit=False, auditRemark=dome + ' 线索流放审核不通过')
        self.flowPath.apply_status(status='已驳回', keyWord=self.appText.get('cluePhone'))
        self.assertEqual(dome + ' 线索流放审核不通过', self.appApi.appText.get('auditRemark'))

    def test_follow_apply_06(self):
        """10、线索无效终止-二级审核成功           已同意"""
        self.flowPath.clue_non_null()
        self.webApi.Audit_management(clueStop=True, clueStopLevel=2)
        self.flowPath.clue_exile_sea()
        self.webApi.audit_List(keyWord=self.appText.get('cluePhone'))        # 审核列表
        self.webApi.auditApply()
        self.webApi.audit_List(keyWord=self.appText.get('cluePhone'), auditLevel=2)        # 审核列表
        self.webApi.auditApply(vlue=2)
        self.flowPath.apply_status(status='已同意')

    def test_follow_apply_07(self):
        """1、线索终止审核中 ---不允许转客户"""
        self.flowPath.clue_non_null()
        self.webApi.Audit_management(clueStop=True, clueStopLevel=1)
        self.flowPath.clue_exile_sea()
        self.appApi.ClientEntering(callName=self.appApi.RandomText(textArr=surname),
                                   loanSituation='这个是贷款情况')
        self.assertEqual('已申请线索终止,正在审核中!', self.appApi.appText.get('data'))


