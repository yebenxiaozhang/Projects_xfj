# -*- coding: utf-8 -*-
# @Time    : 2020/1/14 16:17
# @Author  : 潘师傅
# @File    : Seller_casc.py

# 第一步 导入unittest模块
from XFJ.PubilcAPI.FlowPath import *
# 第二步 编写测试用例
"""
绑定A类联盟商
解除A类联盟商
绑定C类联盟商
解除C类联盟商
"""


class SellerTestCase(unittest.TestCase):
    """联盟商"""

    def __init__(self, *args, **kwargs):
        super(SellerTestCase, self).__init__(*args, **kwargs)
        self.Agent = AgentApi()
        self.AgentRequest = self.Agent
        self.AgentTEXT = GlobalMap()

        self.Xm = XmApi()
        self.XmRequest = self.Xm
        self.XmTEXT = GlobalMap()

    @classmethod
    def setUpClass(cls):
        """登录经纪人账号"""
        cls.Xm = XmApi()
        cls.XmRequest = cls.Xm
        cls.XmRequest.ApiLogin()

    def setUp(self):
        self.tearDown()

    def tearDown(self):
        """解除绑定公司"""
        # 配置不需要审核 可以直接退出 也可以直接加入
        self.AgentRequest.LoginAgent(Uesr=AgentUser1)
        self.AgentRequest.getSellerJoinAndLeaveVerificationConfig()  # 查询配置
        if self.AgentTEXT.get('isCheck') == '0':
            pass
        else:
            self.AgentRequest.updateSellerConfig()  # 更新配置
            self.AgentRequest.getSellerJoinAndLeaveVerificationConfig()  # 查询配置
            self.assertEqual('0', self.AgentTEXT.get('isCheck'))
        # 我们要设置退出团队 不需要进行验证
        self.AgentRequest.getSellerJoinAndLeaveVerificationConfig(value=1)  # 查询配置
        if self.AgentTEXT.get('isCheck') == '0':
            pass
        else:
            self.AgentRequest.updateSellerConfig(configKey=2)
            self.AgentRequest.getSellerJoinAndLeaveVerificationConfig(value=1)  # 更新配置
            self.assertEqual('0', self.AgentTEXT.get('isCheck'))
        self.AgentRequest.LoginAgent(Uesr=AgentUser9)
        self.AgentRequest.LookSeller()
        if self.AgentTEXT.get('SellerNo') != SellerNo:
            if (self.AgentTEXT.get('SellerNo'))[3] != 'A':
                self.AgentRequest.BindingSeller(phone=AgentUser1)
                if self.AgentTEXT.get('XFKcontent') == '不能重复申请加入该团队':
                    self.AgentRequest.LoginAgent(Uesr=AgentUser1)
                    self.AgentRequest.SellerAgentApplyList()
                    self.AgentRequest.agreeSellerAgentApply()
                    try:
                        self.assertEqual(1, self.AgentTEXT.get('resultCode'))
                    except BaseException as e:
                        print(e)
                        raise RuntimeError(self.AgentTEXT.get('Agenturl'))
                    self.AgentRequest.LoginAgent(Uesr=AgentUser9)
                else:
                    self.assertEqual(1, self.AgentTEXT.get('resultCode'))
                time.sleep(1)
            # 解除绑定公司
            self.AgentRequest.LookSeller()
            time.sleep(1)
            self.AgentRequest.RelieveSeller()
            try:
                self.assertEqual(1, self.AgentTEXT.get('resultCode'))
            except BaseException as e:
                print(e, "解除绑定公司失败，可能以前申请过解除绑定")
                self.assertEqual(self.AgentTEXT.get('XFKcontent'), '不能重复申请退出该团队')
                self.AgentRequest.LoginAgent(Uesr=AgentUser1)
                self.AgentRequest.SellerAgentApplyList()                # 获取    加入 | 退出 审核列表
                self.AgentRequest.agreeSellerAgentApply(joinOrLeave=2)  # 同意    加入 | 退出 团队

    def test_BindingSeller(self):
        """绑定A类联盟商"""
        self.AgentRequest.LoginAgent(Uesr=AgentUser9)
        # 查询联盟商
        self.AgentRequest.GetSeller()
        # 通过手机号码绑定联盟商
        self.AgentRequest.BindingSeller(phone=AgentUser1)
        self.assertEqual(1, self.AgentTEXT.get('resultCode'))

    def test_BindingGroup(self):
        """绑定C类联盟商"""
        # 绑定C类
        self.AgentRequest.LoginAgent(Uesr=AgentUser7)
        self.AgentRequest.getSellerJoinAndLeaveVerificationConfig()
        if self.AgentTEXT.get('isCheck') == '0':
            pass
        else:
            self.AgentRequest.updateSellerConfig()
        self.AgentRequest.LoginAgent(Uesr=AgentUser9)
        self.AgentRequest.DddTeamInfo(phone=AgentUser7)
        self.assertEqual(1, self.AgentTEXT.get('resultCode'))

    def test_001(self):
        """加入团队A--->拒绝--->再次申请--->同意并且验证"""
        """退出团队A--->拒绝--->再次申请--->同意并且验证"""
        globals()['b'] = 1
        while globals()['b'] != 3:
            self.AgentRequest.LoginAgent(Uesr=AgentUser1)
            self.AgentRequest.getSellerJoinAndLeaveVerificationConfig(value=(globals()['b'] - 1))
            if self.AgentTEXT.get('isCheck') == '1':
                pass
            else:
                self.AgentRequest.updateSellerConfig(configKey=globals()['b'])
            globals()['a'] = 0
            while globals()['a'] != 2:
                # 登录普通经纪人账号-申请加入团队
                self.AgentRequest.LoginAgent(Uesr=AgentUser9)
                if globals()['b'] == 1:
                    self.AgentRequest.BindingSeller(phone=AgentUser1)   # 绑定公司
                    self.AgentRequest.BindingSeller(phone=AgentUser1)   # 绑定公司
                    self.assertEqual(self.AgentTEXT.get('XFKcontent'), '不能重复申请加入该团队')
                else:
                    self.AgentRequest.RelieveSeller()                   # 解除绑定
                    self.AgentRequest.RelieveSeller()                   # 解除绑定
                    self.assertEqual(self.AgentTEXT.get('XFKcontent'), '不能重复申请退出该团队')
                # 登录联盟商队长的账号-拒绝/同意该用户进入团队
                self.AgentRequest.LoginAgent(Uesr=AgentUser1)
                self.AgentRequest.SellerAgentApplyList()                # 获取加入 | 退出 审核列表
                if globals()['a'] == 0:
                    self.AgentRequest.refuseSellerAgentApply(joinOrLeave=globals()['b'])
                    # 拒绝加入 | 退出 团队
                    globals()['applyId'] = self.AgentTEXT.get('applyId')
                    self.AgentRequest.SellerAgentApplyList(processingStatus=2)
                    self.assertEqual(globals()['applyId'], self.AgentTEXT.get('applyId'))
                else:
                    globals()['applyId'] = self.AgentTEXT.get('applyId')
                    self.AgentRequest.agreeSellerAgentApply(joinOrLeave=globals()['b'])
                    self.AgentRequest.SellerAgentApplyList(processingStatus=2)
                    self.assertEqual(globals()['applyId'], self.AgentTEXT.get('applyId'))
                globals()['a'] = globals()['a'] + 1
                # 登录普通经纪人账号进行验证
            self.AgentRequest.LoginAgent(Uesr=AgentUser9)
            self.AgentRequest.LookSeller()
            if globals()['b'] == 1:
                self.assertNotEqual(self.AgentTEXT.get('SellerNo'), SellerNo)
            else:
                self.assertEqual(self.AgentTEXT.get('SellerNo'), SellerNo)
            globals()['b'] = globals()['b'] + 1

    def test_002(self):
        """加入团队C--->拒绝--->再次申请--->同意并且验证"""
        self.AgentRequest.LoginAgent(Uesr=AgentUser7)
        self.AgentRequest.getSellerJoinAndLeaveVerificationConfig()
        if self.AgentTEXT.get('isCheck') == '1':
            pass
        else:
            self.AgentRequest.updateSellerConfig()
        globals()['a'] = 0
        while globals()['a'] != 2:
            # 登录普通经纪人账号-申请加入团队
            self.AgentRequest.LoginAgent(Uesr=AgentUser9)
            self.AgentRequest.DddTeamInfo(phone=AgentUser7)   # 绑定公司
            # 登录联盟商队长的账号-拒绝/同意该用户进入团队
            self.AgentRequest.LoginAgent(Uesr=AgentUser7)
            self.AgentRequest.SellerAgentApplyList()                # 获取加入审核列表
            if globals()['a'] == 0:
                self.AgentRequest.refuseSellerAgentApply()          # 拒绝加入团队
                globals()['applyId'] = self.AgentTEXT.get('applyId')
                self.AgentRequest.SellerAgentApplyList(processingStatus=2)
                self.assertEqual(globals()['applyId'], self.AgentTEXT.get('applyId'))
            else:
                globals()['applyId'] = self.AgentTEXT.get('applyId')
                self.AgentRequest.agreeSellerAgentApply()
                try:
                    self.assertEqual(1, self.AgentTEXT.get('resultCode'))
                except BaseException as e:
                    print(e)
                    raise RuntimeError(self.AgentTEXT.get('Agenturl'))
                self.AgentRequest.SellerAgentApplyList(processingStatus=2)
                self.assertEqual(globals()['applyId'], self.AgentTEXT.get('applyId'))
            globals()['a'] = globals()['a'] + 1
            # 登录普通经纪人账号进行验证
        self.AgentRequest.LoginAgent(Uesr=AgentUser9)
        self.AgentRequest.LookSeller()
        self.assertNotEqual(self.AgentTEXT.get('SellerNo'), SellerNo)

    def test_003(self):
        """申请联盟商1后、去申请联盟商2"""
        user = [AgentUser1, AgentUser7]
        for i in user:
            # print(i)
            self.AgentRequest.LoginAgent(Uesr=i)
            self.AgentRequest.getSellerJoinAndLeaveVerificationConfig()
            if self.AgentTEXT.get('isCheck') == '1':
                pass
            else:
                self.AgentRequest.updateSellerConfig()
        # print('555')
        self.AgentRequest.LoginAgent(Uesr=AgentUser9)
        self.AgentRequest.BindingSeller(phone=user[0])  # 绑定公司
        self.AgentRequest.DddTeamInfo(phone=user[1])  # 绑定公司
        for z in user:
            self.AgentRequest.LoginAgent(Uesr=z)
            self.AgentRequest.SellerAgentApplyList()
            globals()['apply'] = self.AgentTEXT.get('applyId')
            if z == user[0]:
                self.AgentRequest.agreeSellerAgentApply()
                self.AgentRequest.SellerAgentApplyList(processingStatus=2)
                self.assertEqual(globals()['apply'], self.AgentTEXT.get('applyId'))
            else:
                self.AgentRequest.SellerAgentApplyList(processingStatus=2)
                self.assertNotEqual(globals()['apply'], self.AgentTEXT.get('applyId'))

    def test_004(self):
        """更换过联盟商队长"""

    # def test_005(self):
    #     """多数据---A类"""
    #     self.AgentRequest.LoginAgent(Uesr=AgentUser1)
    #     self.AgentRequest.getSellerJoinAndLeaveVerificationConfig()
    #     if self.AgentTEXT.get('isCheck') == '1':
    #         pass
    #     else:
    #         self.AgentRequest.updateSellerConfig(configKey=1)
    #     a = 10
    #     while a != 20:
    #         self.XmRequest.Search_C_USER(vlue=a)
    #         self.AgentRequest.LoginAgent(Uesr=self.XmTEXT.get('xmCPhone'))
    #         self.AgentRequest.BindingSeller(phone=AgentUser1)
    #         a = a + 1




