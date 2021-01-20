# -*- coding: utf-8 -*-
# @Time    : 2020/3/21 11:08
# @Author  : 潘师傅
# @File    : Follow_apply_casc.py

"""跟进申请-相关"""
from PubilcAPI.flowPath import *

"""
无审核-正常流程：·······现状态··············· 操作流放公海
  1、线索无效终止        已同意                 已同意
    A-1 线索释放公海--无审核--跟进减少

 一级审核-正常流程：···············现状态··················操作流放公海成功
  2、线索无效终止-待审核           申请中      
    A-2 线索释放公海--审核中--跟进不变    
  3、线索无效终止-审核失败         已驳回
    A-3 线索释放公海--审核失败--跟进不变
  4、线索无效终止-审核成功         已同意
    A-4 线索释放公海--审核成功--跟进减少

 二级审核-正常流程························现状态·········流放公海的状态
  5、线索无效终止-待审核                  申请中
  6、线索无效终止-一级审核失败            已驳回
  7、线索无效终止-一级审核成功            审核中
  8、线索无效终止-二级审核失败            已驳回
  9、线索无效终止-二级审核成功           已同意


 注意事项：
  10、线索终止审核中 ---不允许转客户
  11、无审核跟进内容为：线索终止跟进
  12、有审核跟进内容为：申请线索终止跟进

"""


class TestCase(unittest.TestCase):
    """客第壹——线索终止跟进"""

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

    def test_follow_apply_01(self):
        """1、线索无效终止        已同意"""
        """    A-1 线索释放公海--无审核--跟进减少"""
        self.clue_front()
        self.appApi.follow_apply(keyWord=self.appText.get('cluePhone'))
        dome1 = self.appText.get('total')
        self.follow_front()
        self.appApi.ExileSea()
        """11、无审核跟进内容为：线索终止跟进"""
        self.appApi.ClueFollowList()
        self.assertEqual(self.appText.get('followContent'),
                         '线索终止跟进</br>原因:客户已成交</br>备注:python-线索释放公海')
        self.follow_later(vlue=-1)
        self.appApi.follow_apply(keyWord=self.appText.get('cluePhone'))
        if dome1 + 1 != self.appText.get('total'):
            raise RuntimeError("无审核的情况下 线索终止没有多加一条跟进申请")

    def test_follow_apply_02(self):
        """2、线索无效终止-待审核           申请中"""
        self.webApi.Audit_management(clueStop=True, clueStopLevel=1)
        """    A-2 线索释放公海--审核中--跟进不变    """
        self.clue_front()
        self.follow_front()
        self.appApi.ExileSea()
        self.appApi.ClueFollowList()
        self.assertEqual(self.appText.get('followContent'),
                         '申请线索终止跟进</br>原因:客户已成交</br>备注:python-线索释放公海')
        self.flowPath.apply_status(status='申请中', keyWord=self.appText.get('cluePhone'))

        self.follow_later()
        """3、线索无效终止-审核失败         已驳回"""
        """    A-3 线索释放公海--审核失败--跟进不变"""
        dome = time.strftime("%Y-%m-%d %H:%M:%S")
        self.webApi.auditList(phoneNum=self.appText.get('cluePhone'))
        self.webApi.audit(auditStatue=2, auditRemark=dome + ' 审核失败')
        self.flowPath.apply_status(status='已驳回', keyWord=self.appText.get('cluePhone'))
        self.assertEqual(dome + ' 审核失败', self.appApi.appText.get('auditRemark'))
        self.follow_later()

    def test_follow_apply_03(self):
        """4、线索无效终止-审核成功         已同意"""
        self.webApi.Audit_management(clueStop=True, clueStopLevel=1)
        """    A-4 线索释放公海--审核成功--跟进减少"""
        self.clue_front()
        self.follow_front()
        self.appApi.ExileSea()
        self.webApi.auditList(phoneNum=self.appText.get('cluePhone'))
        self.webApi.audit()
        self.flowPath.apply_status(status='已同意')
        self.follow_later(vlue=-1)

    def test_follow_apply_04(self):
        """5、线索无效终止-待审核                  申请中"""
        self.flowPath.clue_non_null()
        self.webApi.Audit_management(clueStop=True, clueStopLevel=2)
        self.flowPath.clue_exile_sea()
        self.flowPath.apply_status(status='申请中', keyWord=self.appText.get('cluePhone'))
        """6、线索无效终止-一级审核失败            已驳回"""

        dome = time.strftime("%Y-%m-%d %H:%M:%S")
        self.webApi.auditList(phoneNum=self.appText.get('cluePhone'))
        self.webApi.audit(auditStatue=2, auditRemark=dome + ' 审核失败')
        self.flowPath.apply_status(status='已驳回', keyWord=self.appText.get('cluePhone'))
        self.assertEqual(dome + ' 审核失败', self.appApi.appText.get('auditRemark'))

    def test_follow_apply_05(self):
        """7、线索无效终止-一级审核成功            审核中"""
        self.flowPath.clue_non_null()
        self.webApi.Audit_management(clueStop=True, clueStopLevel=2)
        self.flowPath.clue_exile_sea()
        self.flowPath.apply_status(status='申请中', keyWord=self.appText.get('cluePhone'))
        dome = time.strftime("%Y-%m-%d %H:%M:%S")
        self.webApi.auditList(phoneNum=self.appText.get('cluePhone'))
        self.webApi.audit()
        self.flowPath.apply_status(status='申请中', keyWord=self.appText.get('cluePhone'))

        """8、线索无效终止-二级审核失败            已驳回"""
        self.webApi.auditList(phoneNum=self.appText.get('cluePhone'), auditLevel=2)
        self.webApi.audit(auditStatue=2, auditRemark=dome + ' 审核失败')
        self.flowPath.apply_status(status='已驳回', keyWord=self.appText.get('cluePhone'))
        self.assertEqual(dome + ' 审核失败', self.appApi.appText.get('auditRemark'))

    def test_follow_apply_06(self):
        """9、线索无效终止-二级审核成功           已同意"""
        self.flowPath.clue_non_null()
        self.webApi.Audit_management(clueStop=True, clueStopLevel=2)
        self.flowPath.clue_exile_sea()
        self.webApi.auditList(phoneNum=self.appText.get('cluePhone'))
        self.webApi.audit()
        self.webApi.auditList(phoneNum=self.appText.get('cluePhone'), auditLevel=2)
        self.webApi.audit()
        self.flowPath.apply_status(status='已同意')

    def test_follow_apply_07(self):
        """10、线索终止审核中 ---不允许转客户"""
        self.flowPath.clue_non_null()
        self.webApi.Audit_management(clueStop=True, clueStopLevel=1)
        self.flowPath.clue_exile_sea()
        self.appApi.ClientEntering(callName=self.appApi.RandomText(textArr=surname),
                                   loanSituation='这个是贷款情况')
        self.assertEqual('已申请线索终止,正在审核中!', self.appApi.appText.get('data'))
        self.webApi.auditList(phoneNum=self.appText.get('cluePhone'))
        self.webApi.audit(auditStatue=2, auditRemark=time.strftime("%Y-%m-%d %H:%M:%S") + ' 审核失败')

    def follow_front(self):
        """跟进前"""
        self.appApi.GetUserAgenda()
        globals()['dome'] = self.appText.get('total')

    def follow_later(self, vlue=0):
        """跟进后"""
        self.appApi.GetUserAgenda()
        if vlue == 0:
            self.assertEqual(globals()['dome'], self.appText.get('total'))
        else:
            self.assertNotEqual(globals()['dome'], self.appText.get('total'))
            if vlue == -1:
                self.assertEqual(globals()['dome'] - 1, self.appText.get('total'))
            else:
                self.assertEqual(globals()['dome'] + 1, self.appText.get('total'))

    def clue_front(self):
        """线索前"""
        self.flowPath.clue_non_null()
        self.appApi.my_clue_list()
        self.appApi.ClueFollowList()
        self.appApi.ClueFollowSave(taskEndTime=time.strftime("%Y-%m-%d %H:%M:%S"))

