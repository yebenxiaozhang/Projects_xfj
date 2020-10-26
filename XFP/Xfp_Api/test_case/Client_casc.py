# -*- coding: utf-8 -*-
# @Time    : 2020/3/21 11:08
# @Author  : 潘师傅
# @File    : Client_casc.py

"""客户相关"""
from XFP.PubilcAPI.flowPath import *


class ClientTestCase(unittest.TestCase):
    """客第壹——客户列表"""

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

    def test_FollowSave(self):
        """客户跟进"""
        try:
            #  客户详情查看  及 列表是否有新增
            self.flowPath.client_list_non_null()
            self.appApi.ClientFollowList()
            self.appApi.ClueFollowSave(followType='客户', taskEndTime=time.strftime("%Y-%m-%d") + ' 22:00:00')
            self.appApi.ClientFollowList()
            try:
                self.assertEqual('python-线索/客户跟进，本次沟通记录', self.appText.get('followContent'))
            except BaseException as e:
                print("断言错误，错误原因：%s" % e)
                self.appApi.ClientFollowList(value=1)
                self.assertEqual('python-线索/客户跟进，本次沟通记录', self.appText.get('followContent'))
            self.appApi.ClientList()
            """在首页待办任务进行查询"""
            self.appApi.GetUserAgenda(endTime=time.strftime("%Y-%m-%d"))
        except BaseException as e:
            print("断言错误，错误原因：%s" % e)
            raise RuntimeError(self.appText.get('ApiXfpUrl'))

    def test_SettingTakeLook(self):
        """设定带看计划"""
        self.flowPath.add_visit()
        self.assertEqual(self.appApi.appText.get('code'), 200)

    def test_AlterSettingTakeLook(self):
        """修改带看计划"""
        try:
            self.flowPath.add_visit()
            self.appApi.ClientTask(taskType='3')
            if self.appApi.appText.get('total') < 1:
                print('创建带看至少有一个任务')
                raise RuntimeError(self.appText.get('ApiXfpUrl'))
            self.appApi.GetMatchingAreaHouse()
            self.appApi.UpdateVisitAdd(projectAId=self.appText.get('houseId'))
        except BaseException as e:
            print("断言错误，错误原因：%s" % e)
            raise RuntimeError(self.appText.get('ApiXfpUrl'))

    def test_CompleteSettingTakeLook(self):
        """完成带看计划"""
        try:
            self.flowPath.add_visit()
            self.appApi.ClientTask(taskType='3')
            if self.appText.get('total') < 1:
                raise RuntimeError(self.appText.get('ApiXfpUrl'))
            self.appApi.visit_info()
            self.appApi.VisitFlow1()
            self.appApi.ClientTask()
            if self.appText.get('total') >= 2:
                raise RuntimeError(self.appText.get('ApiXfpUrl'))

        except BaseException as e:
            print("断言错误，错误原因：%s" % e)
            raise RuntimeError(self.appText.get('ApiXfpUrl'))

    def test_advance_over_visit(self):
        """提前结束带看代办"""
        try:
            self.flowPath.add_visit()
            self.flowPath.advance_over_visit()
            self.appApi.ClientTask()
            self.appApi.ClientFollowList()
            self.assertEqual('提前结束带看', self.appText.get('followContent'))
        except BaseException as e:
            print("断言错误，错误原因：%s" % e)
            raise RuntimeError(self.appText.get('ApiXfpUrl'))

    def test_AddAgreement(self):
        """录入成交"""
        try:
            self.appApi.deal_List()
            dome = self.appText.get('total')
            self.flowPath.client_list_non_null()
            self.flowPath.add_deal()
            self.appApi.deal_List()
            self.assertNotEqual(dome, self.appText.get('total'))
        except BaseException as e:
            print("断言错误，错误原因：%s" % e)
            raise RuntimeError(self.appText.get('ApiXfpUrl'))

    def test_SuspendFollow(self):
        """暂停跟进"""
        try:
            self.flowPath.suspend_follow()
            self.appApi.ClientTask()       # 待办
            if self.appText.get('total') == 1:
                if self.appText.get('taskTypeStr') != '带看行程':
                    raise RuntimeError(self.appText.get('ApiXfpUrl'))
        except BaseException as e:
            print("断言错误，错误原因：%s" % e)
            raise RuntimeError(self.appText.get('ApiXfpUrl'))






