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
        cls.webApi.audit_List()
        while cls.webApi.webText.get('total') != 0:
            cls.webApi.auditApply(isAudit=False, auditRemark='客户流放公海')
            cls.webApi.audit_List()
        cls.webApi.audit_List(auditLevel=2)
        while cls.webApi.webText.get('total') != 0:
            cls.webApi.auditApply(isAudit=False, auditRemark='客户流放公海')
            cls.webApi.audit_List()

    def test_follow_apply(self):
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
        self.appApi.add_deal()  # 录入成交
        self.assertEqual('已申请暂缓跟进,正在审核中!', self.appApi.appText.get('data'))

        self.appApi.client_exile_sea()
        self.assertEqual('已申请暂缓跟进,正在审核中!', self.appApi.appText.get('data'))

    def test_follow_apply_01(self):
        """1、客户申请暂缓        已同意                 已同意"""
        self.flowPath.client_list_non_null()
        self.appApi.follow_apply(keyWord=self.appText.get('cluePhone'))
        dome = self.appText.get('total')
        self.flowPath.suspend_follow()
        self.appApi.ClientTask(taskType=2)  # 待办
        self.assertEqual(time.strftime("%Y-%m-%d"), self.appApi.appText.get('endTime')[:10])
        self.appApi.follow_apply(keyWord=self.appText.get('cluePhone'))
        if self.appText.get('total') != dome:
            raise RuntimeError("无审核的情况下 客户申请暂缓多了一个跟进")

    def test_follow_apply_03(self):
        """3、客户无效终止        已同意"""
        self.flowPath.client_list_non_null()
        self.appApi.follow_apply(keyWord=self.appText.get('cluePhone'))
        dome = self.appText.get('total')
        self.appApi.client_exile_sea()
        self.appApi.follow_apply(keyWord=self.appText.get('cluePhone'))
        if dome != self.appText.get('total'):
            raise RuntimeError("无审核的情况下 客户终止会多添加一个跟进申请")

    def test_follow_apply_04(self):
        """1、客户申请暂缓跟进-待审核       申请中"""
        self.flowPath.client_list_non_null()
        self.webApi.Audit_management(suspend=True, suspendLevel=1)  # 修改配置审核
        self.flowPath.suspend_follow()
        try:
            self.flowPath.apply_status(status='申请中', keyWord=self.appText.get('cluePhone'))
        except:
            self.flowPath.apply_status(status='审核中', keyWord=self.appText.get('cluePhone'))

        """2、客户申请暂缓跟进-审核失败     已驳回                 已取消"""
        dome = time.strftime("%Y-%m-%d %H:%M:%S")
        self.webApi.audit_List(keyWord=self.appText.get('cluePhone'))  # 审核列表
        self.webApi.auditApply(customerId=self.appApi.appText.get('customerId'),
                               isAudit=False, auditRemark=dome + ' python-跟进申请不通过',
                               endTime=time.strftime("%Y-%m-%d ") + '22:00:00')
        self.flowPath.apply_status(status='已驳回', keyWord=self.appText.get('cluePhone'))
        self.assertEqual(dome + ' python-跟进申请不通过', self.appApi.appText.get('auditRemark'))
        self.appApi.client_exile_sea()
        self.flowPath.apply_status(status='已驳回', keyWord=self.appText.get('cluePhone'))

    def test_follow_apply_06(self):
        """3、客户申请暂缓跟进-审核成功     已同意                 已同意"""
        self.flowPath.client_list_non_null()
        self.webApi.Audit_management(suspend=True, suspendLevel=1)  # 修改配置审核
        self.flowPath.suspend_follow()
        self.webApi.audit_List(keyWord=self.appText.get('cluePhone'))  # 审核列表
        self.webApi.auditApply(customerId=self.appApi.appText.get('customerId'),
                               endTime=time.strftime("%Y-%m-%d ") + '22:00:00')
        self.flowPath.apply_status(status='已同意', keyWord=self.appText.get('cluePhone'))
        self.appApi.client_exile_sea()
        self.flowPath.apply_status(status='已同意', keyWord=self.appText.get('cluePhone'))

    def test_follow_apply_10(self):
        """7、客户无效终止-待审核           申请中"""
        self.flowPath.client_list_non_null()
        self.webApi.Audit_management(customerStop=True, customerStopLevel=1)  # 修改配置审核
        self.appApi.client_exile_sea()
        try:
            self.flowPath.apply_status(status='申请中', keyWord=self.appText.get('cluePhone'))
        except:
            self.flowPath.apply_status(status='审核中', keyWord=self.appText.get('cluePhone'))
        """8、客户无效终止-审核成功         已同意"""
        self.webApi.audit_List(keyWord=self.appText.get('cluePhone'))  # 审核列表
        self.webApi.auditApply(customerId=self.appApi.appText.get('customerId'))
        self.flowPath.apply_status(status='已同意', keyWord=self.appText.get('cluePhone'))

    def test_follow_apply_12(self):
        """9、客户无效终止-审核失败         已驳回"""
        dome = time.strftime("%Y-%m-%d %H:%M:%S")
        self.flowPath.client_list_non_null()
        self.webApi.Audit_management(customerStop=True, customerStopLevel=1)  # 修改配置审核
        self.appApi.client_exile_sea()
        self.webApi.audit_List(keyWord=self.appText.get('cluePhone'))  # 审核列表
        self.webApi.auditApply(isAudit=False, auditRemark=dome + '客户无效终止审核失败')
        self.flowPath.apply_status(status='已驳回', keyWord=self.appText.get('cluePhone'))
        self.assertEqual(dome + '客户无效终止审核失败', self.appApi.appText.get('auditRemark'))

    def test_follow_apply_13(self):
        """ 1、客户申请暂缓跟进-待审核              申请中            已取消"""
        self.webApi.Audit_management(suspend=True, suspendLevel=2)  # 修改配置审核
        self.flowPath.client_list_non_null()
        self.flowPath.suspend_follow()
        try:
            self.flowPath.apply_status(status='申请中', keyWord=self.appText.get('cluePhone'))
        except:
            self.flowPath.apply_status(status='审核中', keyWord=self.appText.get('cluePhone'))

        """2、客户申请暂缓跟进-一级审核失败        已驳回            已驳回"""
        dome = time.strftime("%Y-%m-%d %H:%M:%S")
        self.webApi.audit_List(keyWord=self.appText.get('cluePhone'))  # 审核列表
        self.webApi.auditApply(customerId=self.appApi.appText.get('customerId'),
                               isAudit=False, auditRemark=dome + ' python-跟进申请不通过',
                               endTime=time.strftime("%Y-%m-%d ") + '22:00:00')
        self.flowPath.apply_status(status='已驳回', keyWord=self.appText.get('cluePhone'))
        self.assertEqual(dome + ' python-跟进申请不通过', self.appApi.appText.get('auditRemark'))
        self.appApi.client_exile_sea()
        self.flowPath.apply_status(status='已驳回', keyWord=self.appText.get('cluePhone'))

    def test_follow_apply_15(self):
        """3、客户申请暂缓跟进-一级审核成功        审核中            已取消"""
        self.webApi.Audit_management(suspend=True, suspendLevel=2)  # 修改配置审核
        self.flowPath.client_list_non_null()
        self.flowPath.suspend_follow()
        self.webApi.audit_List(keyWord=self.appText.get('cluePhone'))  # 审核列表
        self.webApi.auditApply(customerId=self.appApi.appText.get('customerId'),
                               endTime=time.strftime("%Y-%m-%d ") + '22:00:00')
        try:
            self.flowPath.apply_status(status='申请中', keyWord=self.appText.get('cluePhone'))
        except:
            self.flowPath.apply_status(status='审核中', keyWord=self.appText.get('cluePhone'))

        """4、客户申请暂缓跟进-二级审核失败        已驳回            已取消"""
        dome = time.strftime("%Y-%m-%d %H:%M:%S")
        self.webApi.audit_List(auditLevel=2)
        self.webApi.auditApply(customerId=self.appApi.appText.get('customerId'), isAudit=False,
                               auditRemark=dome + ' 暂申请不通过', vlue=2,
                               endTime=time.strftime("%Y-%m-%d ") + '22:00:00')
        self.flowPath.apply_status(status='已驳回', keyWord=self.appText.get('cluePhone'))
        self.assertEqual(dome + ' 暂申请不通过', self.appApi.appText.get('auditRemark'))
        self.appApi.client_exile_sea()
        self.flowPath.apply_status(status='已驳回', keyWord=self.appText.get('cluePhone'))

    def test_follow_apply_17(self):
        """5、客户申请暂缓跟进-二级审核成功        已同意            已同意"""
        self.webApi.Audit_management(suspend=True, suspendLevel=2)  # 修改配置审核
        self.flowPath.client_list_non_null()
        self.flowPath.suspend_follow()
        self.webApi.audit_List(keyWord=self.appText.get('cluePhone'))  # 审核列表
        self.webApi.auditApply(customerId=self.appApi.appText.get('customerId'),
                               endTime=time.strftime("%Y-%m-%d ") + '22:00:00')
        self.webApi.audit_List(auditLevel=2, keyWord=self.appText.get('cluePhone'))
        self.webApi.auditApply(customerId=self.appApi.appText.get('customerId'), vlue=2,
                               endTime=time.strftime("%Y-%m-%d ") + '22:00:00')
        self.flowPath.apply_status(status='已同意', keyWord=self.appText.get('cluePhone'))
        self.appApi.client_exile_sea()
        self.flowPath.apply_status(status='已同意', keyWord=self.appText.get('cluePhone'))

    def test_follow_apply_22(self):
        """  11、客户无效终止-待审核                 申请中"""
        self.flowPath.client_list_non_null()
        self.webApi.Audit_management(customerStop=True, customerStopLevel=2)  # 修改配置审核
        self.appApi.client_exile_sea()
        try:
            self.flowPath.apply_status(status='申请中', keyWord=self.appText.get('cluePhone'))
        except:
            self.flowPath.apply_status(status='审核中', keyWord=self.appText.get('cluePhone'))
        dome = time.strftime("%Y-%m-%d %H:%M:%S")

        """12、客户无效终止-一级审核失败           已驳回"""
        self.webApi.audit_List(keyWord=self.appText.get('cluePhone'))        # 审核列表
        self.webApi.auditApply(isAudit=False, auditRemark=dome + '客户无效终止审核失败')
        try:
            self.flowPath.apply_status(status='已驳回', vlue=1, keyWord=self.appText.get('cluePhone'))
        except:
            self.flowPath.apply_status(status='已驳回', keyWord=self.appText.get('cluePhone'))
        self.assertEqual(dome + '客户无效终止审核失败', self.appApi.appText.get('auditRemark'))

    def test_follow_apply_23(self):
        """13、客户无效终止-一级审核成功           审核中"""
        self.flowPath.clue_non_null()
        self.appApi.my_clue_list()
        self.appApi.ClueFollowList()
        self.appApi.ClueFollowSave(taskEndTime=time.strftime("%Y-%m-%d %H:%M:%S"))
        self.appApi.ClueInfo()
        self.appApi.ClientEntering(callName=self.appApi.RandomText(textArr=surname),
                                   loanSituation='这个是贷款情况')
        self.appApi.ClientList()
        self.webApi.Audit_management(customerStop=True, customerStopLevel=2)  # 修改配置审核
        self.appApi.client_exile_sea()


        try:
            self.flowPath.apply_status(status='申请中', keyWord=self.appText.get('cluePhone'))
        except:
            self.flowPath.apply_status(status='审核中', keyWord=self.appText.get('cluePhone'))
        dome = time.strftime("%Y-%m-%d %H:%M:%S")
        self.webApi.audit_List()        # 审核列表
        self.webApi.auditApply()


        try:
            self.flowPath.apply_status(status='申请中', keyWord=self.appText.get('cluePhone'))
        except:
            self.flowPath.apply_status(status='审核中', keyWord=self.appText.get('cluePhone'))

        """14、客户无效终止-二级审核失败           已驳回"""
        self.webApi.audit_List(auditLevel=2)        # 审核列表
        self.webApi.auditApply(vlue=2, isAudit=False, auditRemark=dome + '客户无效终止审核失败')
        self.flowPath.apply_status(status='已驳回', keyWord=self.appText.get('cluePhone'))
        self.assertEqual(dome + '客户无效终止审核失败', self.appApi.appText.get('auditRemark'))

    def test_follow_apply_24(self):
        """15、客户无效终止-二级审核成功           已同意"""
        self.flowPath.client_list_non_null()
        self.webApi.Audit_management(customerStop=True, customerStopLevel=2)  # 修改配置审核
        self.appApi.client_exile_sea()
        try:
            self.flowPath.apply_status(status='申请中', keyWord=self.appText.get('cluePhone'))
        except:
            self.flowPath.apply_status(status='审核中', keyWord=self.appText.get('cluePhone'))
        self.webApi.audit_List()        # 审核列表
        self.webApi.auditApply()
        try:
            self.flowPath.apply_status(status='申请中', keyWord=self.appText.get('cluePhone'))
        except:
            self.flowPath.apply_status(status='审核中', keyWord=self.appText.get('cluePhone'))

        """14、客户无效终止-二级审核失败           已驳回"""
        self.webApi.audit_List(auditLevel=2, keyWord=self.appText.get('cluePhone'))        # 审核列表
        self.webApi.auditApply(customerId=self.appApi.appText.get('customerId'),
                               vlue=2)
        self.flowPath.apply_status(status='已同意', keyWord=self.appText.get('cluePhone'))

    def test_follow_apply_26(self):
        """2、客户终止跟进审核中 ---不允许创建带看，不允许录成交，
        不允许暂缓，（无论是否开启审核，都不允许操作）"""
        self.flowPath.client_list_non_null()
        self.webApi.Audit_management(customerStop=True, customerStopLevel=1)  # 修改配置审核
        self.appApi.client_exile_sea()

        self.appApi.GetMatchingAreaHouse()
        dome = time.strftime("%Y-%m-%d %H:%M:%S")
        self.appApi.ClientVisitAdd(projectAId=self.appApi.appText.get('houseId'),
                                   appointmentTime=dome,
                                   seeingConsultant=self.appApi.appText.get('consultantId'),
                                   appointConsultant=self.appApi.appText.get('consultantId'))
        self.assertEqual('已申请客户终止,正在审核中!', self.appApi.appText.get('data'))

        self.appApi.GetMatchingAreaHouse()  # 匹配楼盘
        assert 0 != self.appApi.appText.get('total'), '匹配楼盘为空？'

        self.appApi.add_deal()  # 录入成交
        self.assertEqual('已申请客户终止,正在审核中!', self.appApi.appText.get('data'))

        self.appApi.ClientTaskPause()
        self.assertEqual('已申请客户终止,正在审核中!', self.appApi.appText.get('data'))

    def test_follow_apply_28(self):
        """暂停后再次申请暂停"""
        self.flowPath.client_list_non_null()
        self.webApi.Audit_management(suspend=True, suspendLevel=1)  # 修改配置审核
        self.flowPath.suspend_follow()
        self.webApi.audit_List(keyWord=self.appText.get('cluePhone'))  # 审核列表
        self.webApi.auditApply(customerId=self.appApi.appText.get('customerId'),
                               endTime=time.strftime("%Y-%m-%d ") + '22:00:00')
        self.appApi.ClientFollowList()
        self.appApi.ClueFollowSave(followType='客户', taskEndTime=time.strftime("%Y-%m-%d") + ' 22:00:00')
        self.appApi.ClientTaskPause()
        self.assertEqual(200, self.appApi.appText.get('code'))


