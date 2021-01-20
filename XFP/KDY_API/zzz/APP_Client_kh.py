# -*- coding: utf-8 -*-
# @Time    : 2020/3/21 11:08
# @Author  : 潘师傅
# @File    : Client_casc.py

"""客户相关"""
from PubilcAPI.flowPath import *


class ClientTestCase(unittest.TestCase):
    """客第壹——客户"""

    def __init__(self, *args, **kwargs):
        super(ClientTestCase, self).__init__(*args, **kwargs)
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
        登录经纪人 获取ID"""
        cls.do_request = appApi()
        cls.appApi = cls.do_request
        cls.appApi.Login()
        cls.appApi.GetUserData()
        cls.request = webApi()
        cls.webApi = cls.request
        cls.webApi.Audit_management()

    # def test_FollowSave(self):
    #     """客户跟进"""
    #     try:
    #         #  客户详情查看  及 列表是否有新增
    #         self.flowPath.client_list_non_null()
    #         self.appApi.ClientFollowList()
    #         time.sleep(1)
    #         self.appApi.ClueFollowSave(followType='客户', taskEndTime=time.strftime("%Y-%m-%d") + ' 22:00:00')
    #         self.appApi.ClientFollowList()
    #         self.assertEqual('python-线索/客户跟进，本次沟通记录', self.appText.get('followContent'))
    #         """客户跟进-下次跟进日期为明日---------首页待办会减少"""
    #         self.appApi.GetUserAgenda()
    #         dome = self.appText.get('total')
    #         """及时跟进--是否有添加财富值"""
    #         self.appApi.ClientList()
    #         self.appApi.getWealthDetailList(startTime=time.strftime("%Y-%m-%d"),
    #                                         endTime=time.strftime("%Y-%m-%d"),
    #                                         orderNo=self.appText.get('orderNo'))
    #         dome1 = self.appText.get('vlue')
    #         tomorrow = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
    #         self.appApi.ClientFollowList()
    #         self.appApi.ClueFollowSave(taskEndTime=tomorrow, followType='客户')
    #         # 验证下次跟进日期为明日 待办总数
    #         self.appApi.GetUserAgenda()
    #         self.assertEqual(dome - 1, self.appText.get('total'))
    #         # 验证及时跟进 有没有添加财富值
    #         self.appApi.getWealthDetailList(startTime=time.strftime("%Y-%m-%d"),
    #                                         endTime=time.strftime("%Y-%m-%d"),
    #                                         orderNo=self.appText.get('orderNo'))
    #         self.assertEqual(dome1 + 15, self.appText.get('vlue'))
    #
    #     except BaseException as e:
    #         print("断言错误，错误原因：%s" % e)
    #         raise RuntimeError(self.appText.get('ApiXfpUrl'))

    # def test_CompleteSettingTakeLook(self):
    #     """完成带看计划"""
    #     try:
    #         self.flowPath.add_visit()
    #         self.assertEqual(self.appApi.appText.get('code'), 200)
    #         self.appApi.ClientTask(taskType='3')
    #         if self.appText.get('total') < 1:
    #             raise RuntimeError(self.appText.get('ApiXfpUrl'))
    #         self.appApi.visit_info()
    #         self.appApi.VisitFlow1(agencyId=self.appApi.appText.get('DLGS'),
    #                                receptionName=self.appApi.RandomText(textArr=surname),
    #                                receptionPhone='1' + str(int(time.time())), attachmentIds='1')
    #         self.appApi.ClientTask()
    #         if self.appText.get('total') >= 2:
    #             raise RuntimeError(self.appText.get('ApiXfpUrl'))
    #
    #     except BaseException as e:
    #         print("断言错误，错误原因：%s" % e)
    #         raise RuntimeError(self.appText.get('ApiXfpUrl'))

    # def test_advance_over_visit(self):
    #     """取消带看"""
    #     try:
    #         self.flowPath.add_visit()
    #         self.flowPath.advance_over_visit()
    #         self.appApi.ClientTask()
    #         self.appApi.ClientFollowList()
    #         self.assertEqual('取消带看', self.appText.get('followContent')[-4:])
    #     except BaseException as e:
    #         print("断言错误，错误原因：%s" % e)
    #         raise RuntimeError(self.appText.get('ApiXfpUrl'))

    # def test_AddAgreement(self):
    #     """录入成交"""
    #     try:
    #         self.appApi.deal_List()
    #         dome = self.appText.get('total')
    #         self.flowPath.client_list_non_null()
    #         self.appApi.visitProject_list()
    #         if self.appApi.appText.get('web_total') == 0:
    #             self.flowPath.add_visit()
    #             self.flowPath.accomplish_visit()
    #             self.appApi.visitProject_list()
    #         self.appApi.add_deal()  # 录入成交
    #         self.appApi.deal_List()
    #         self.assertNotEqual(dome, self.appText.get('total'))
    #         self.webApi.finance_deal_auditList(keyWord=self.appText.get('dealPhone'))
    #         self.webApi.finance_deal_audit()
    #     except BaseException as e:
    #         print("断言错误，错误原因：%s" % e)
    #         raise RuntimeError(self.appText.get('ApiXfpUrl'))
    #
    # def test_SuspendFollow(self):
    #     """暂停跟进"""
    #     try:
    #         """申请暂缓过后首页以及客户待办依旧存在"""
    #         self.flowPath.client_list_non_null()
    #         self.appApi.ClientFollowList()
    #         self.appApi.ClueFollowSave(followType='客户', taskEndTime=time.strftime("%Y-%m-%d") + ' 22:00:00')
    #         self.appApi.GetUserAgenda()
    #         dome = self.appText.get('total')
    #         self.appApi.ClientList()
    #         self.flowPath.suspend_follow()
    #         self.appApi.ClientTask(taskType=2)       # 待办
    #         self.assertEqual('2', self.appText.get('taskType'))
    #         self.appApi.GetUserAgenda()
    #         self.assertEqual(dome, self.appText.get('total'))
    #         """暂缓过后进行客户转移"""
    #         # 登录咨询师04 查看任务待办
    #         self.appApi.Login(userName=XfpUser1)
    #         self.appApi.GetUserData()
    #         self.appApi.GetUserAgenda()
    #         zxs_04_db = self.appText.get('total')
    #         # 登录咨询师01 进行转移
    #         self.appApi.Login()
    #         self.appApi.GetUserData()
    #         self.appApi.ClientList()
    #         self.appApi.client_change()
    #         self.appApi.GetUserAgenda()
    #         self.assertEqual(dome - 1, self.appText.get('total'))
    #         # 登录咨询师04 查看待办是否新增
    #         self.appApi.Login(userName=XfpUser1)
    #         self.appApi.GetUserData()
    #         self.appApi.GetUserAgenda()
    #         self.assertEqual(zxs_04_db + 1, self.appText.get('total'))
    #     except BaseException as e:
    #         print("断言错误，错误原因：%s" % e)
    #         raise RuntimeError(self.appText.get('ApiXfpUrl'))
    #
    # def test_client_change(self):
    #     """客户转移-只有一个待办（客户跟进）"""
    #     self.appApi.Login(userName=XfpUser1)
    #     self.appApi.GetUserData()
    #     self.appApi.GetUserAgenda()
    #     dome3 = self.appText.get('total')
    #     self.appApi.Login()
    #     self.appApi.GetUserData()
    #     self.flowPath.client_list_non_null()
    #     self.appApi.ClientFollowList()
    #     self.appApi.ClueFollowSave(followType='客户', taskEndTime=time.strftime("%Y-%m-%d") + ' 22:00:00')
    #     dome = self.appText.get('total') + 1
    #     """首页待办转移过后是否在新的咨询师上是否在"""
    #     self.appApi.GetUserAgenda()
    #     dome1 = self.appText.get('total')
    #     self.appApi.client_change()
    #     self.appApi.Login(userName=XfpUser1)
    #     self.appApi.GetUserData()
    #     self.appApi.ClientList()
    #     self.appApi.ClientFollowList()
    #     self.assertEqual('客户转移', self.appText.get('followContent')[:4])
    #     if self.appText.get('total') != dome + 1:
    #         raise RuntimeError('客户转移后跟进记录的条数与转移前不一致')
    #     self.appApi.GetUserAgenda()
    #     self.assertEqual(dome3 + 1, self.appText.get('total'))
    #     self.appApi.Login()
    #     self.appApi.GetUserData()
    #     self.appApi.GetUserAgenda()
    #     self.assertEqual(dome1 - 1, self.appText.get('total'))

    # def test_client_exile_sea(self):
    #     """客户释放公海"""
    #     self.flowPath.client_list_non_null()
    #     self.appApi.ClientFollowList()
    #     self.appApi.ClueFollowSave(followType='客户', taskEndTime=time.strftime("%Y-%m-%d") + ' 22:00:00')
    #     self.appApi.GetUserAgenda()
    #     dome1 = self.appText.get('total')
    #     self.appApi.ClientList()
    #     """流放公海后首页待办是否减少"""
    #     self.appApi.client_exile_sea()
    #     self.appApi.GetUserAgenda()
    #     self.assertEqual(dome1 - 1, self.appText.get('total'))




