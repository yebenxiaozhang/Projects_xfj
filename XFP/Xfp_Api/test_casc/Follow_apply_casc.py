# -*- coding: utf-8 -*-
# @Time    : 2020/3/21 11:08
# @Author  : 潘师傅
# @File    : Follow_apply_casc.py

"""跟进申请-相关"""
from XFP.PubilcAPI.flowPath import *

"""
无审核-正常流程：····························· 流放公海状态
    1、客户申请暂缓        已同意                 已同意
    2、线索无效终止        已同意
    3、客户无效终止        已同意
    
一级审核-正常流程：·····································流放公海的状态
    1、客户申请暂缓跟进-待审核       申请中                 已取消
    2、客户申请暂缓跟进-审核失败     已驳回                 已取消
    3、客户申请暂缓跟进-审核成功     已同意                 已同意
    4、线索无效终止-待审核           申请中                 已取消
    5、线索无效终止-审核失败         已驳回                 已取消
    6、线索无效终止-审核成功         已同意                 已同意
    7、客户无效终止-待审核           申请中                 已取消
    8、客户无效终止-审核成功         已同意                 已同意
    9、客户无效终止-审核失败         已驳回                 已驳回
    
二级审核-正常流程······································流放公海的状态
    1、客户申请暂缓跟进-待审核              申请中            已取消
    2、客户申请暂缓跟进-一级审核失败        已驳回            已取消
    3、客户申请暂缓跟进-一级审核成功        审核中            已取消
    4、客户申请暂缓跟进-二级审核失败        已驳回            已取消
    5、客户申请暂缓跟进-二级审核成功        已同意            已同意
    6、线索无效终止-待审核                  申请中            已取消
    7、线索无效终止-一级审核失败            已驳回            已取消
    8、线索无效终止-一级审核成功            审核中            已取消
    9、线索无效终止-二级审核失败            已驳回            已取消
    10、线索无效终止-二级审核成功           已同意            已同意
    11、客户无效终止-待审核                 申请中            已取消
    12、客户无效终止-一级审核失败           已驳回            已取消
    13、客户无效终止-一级审核成功           审核中            已取消
    14、客户无效终止-二级审核失败           已驳回            已取消
    15、客户无效终止-二级审核成功           已同意            已同意
           
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

    def test_follow_apply_01(self):
        """1、客户申请暂缓        已同意                 已同意"""
        self.flowPath.client_list_non_null()
        self.flowPath.suspend_follow()
        self.appApi.ClientTask()  # 待办
        if self.appApi.appText.get('total') == 1:
            if self.appApi.appText.get('taskTypeStr') != '带看行程':
                raise RuntimeError(self.appApi.appText.get('ApiXfpUrl'))
        self.flowPath.apply_status(status='已同意')
        self.flowPath.client_exile_sea()
        self.flowPath.apply_status(status='已同意')

    def test_follow_apply_02(self):
        """2、线索无效终止        已同意"""
        self.flowPath.client_list_non_null()
        self.flowPath.clue_exile_sea()
        self.flowPath.apply_status(status='已同意')

    def test_follow_apply_03(self):
        """3、客户无效终止        已同意"""
        self.flowPath.client_list_non_null()
        self.flowPath.client_exile_sea()
        self.flowPath.apply_status(status='已同意')






















