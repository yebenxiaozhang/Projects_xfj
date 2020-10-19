# -*- coding: utf-8 -*-
# @Time    : 2020/3/21 11:08
# @Author  : 潘师傅
# @File    : Client_casc.py

"""客户相关"""
from XFP.PubilcAPI.webApi import *


class ClientTestCase(unittest.TestCase):
    """幸福派——客户列表"""

    def __init__(self, *args, **kwargs):
        super(ClientTestCase, self).__init__(*args, **kwargs)
        self.xfp_web = webApi()
        self.web_api = self.xfp_web

        self.xfp_app = appApi()
        self.app_api = self.xfp_app

        self.appText = GlobalMap()
        self.webText = GlobalMap()

    @classmethod
    def setUpClass(cls):
        """登录幸福派 只执行一次
        登录幸福派 获取ID"""
        cls.do_request = appApi()
        cls.app_api = cls.do_request
        cls.app_api.Login()
        cls.app_api.GetUserData()
        cls.request = webApi()
        cls.webApi = cls.request
        cls.webApi.Audit_management()

    def test_addClientSave(self):
        """直接新增客户"""
        try:
            self.app_api.GetLabelList(labelNo='KHYXDJ', labelName='A-现在买，紧迫性高')
            # B-要买，还没确定什么时候     |   C-了解一下，还没确定买不买  |   D-不需要，随便看看
            GFYX = self.appText.get('labelId')
            self.app_api.GetLabelList(labelNo='ZJZZ', labelName='双资')
            # 有资质无资金  |   双无   |    双资
            ZJZZ = self.appText.get('labelId')
            self.app_api.GetLabelList(labelNo='XSLY', labelName='百度信息流')
            if self.appText.get('labelId') is None:
                self.web_api.add_label(labelName='百度信息流', labelId=self.appText.get('LabelId'),
                                       pid=self.appText.get('LabelId'))
                self.app_api.GetLabelList(labelNo='XSLY', labelName='百度信息流')
            XSLY = self.appText.get('labelId')
            self.app_api.GetMatchingArea()       # 匹配区域
            self.app_api.GetMatchingAreaHouse()      # 匹配楼盘
            while self.appText.get('total') < 3:
                self.web_api.add_house(houseName='项目' + time.strftime("%Y-%m-%d %H:%M:%S"))
                self.app_api.GetMatchingAreaHouse()  # 匹配楼盘
            # 新增客户
            self.app_api.ClientSave(clueNickName=self.app_api.RandomText(textArr=surname),
                                    GFYX=GFYX, ZJZZ=ZJZZ, areaId=self.appText.get('PPQY'), XSLY=XSLY)
            """新增成功后再今日上户，进行查看"""
            self.app_api.TodayClue(keyWord=self.appText.get('CluePhone'))
            self.assertEqual(0, self.appText.get('isFirst'))  # 是否首电
            # self.app_api.LookHistoryFollow()
        except BaseException as e:
            print("断言错误，错误原因：%s" % e)
            raise RuntimeError(self.appText.get('ApiXfpUrl'))

    def test_FollowSave(self):
        """客户跟进"""
        try:
            #  客户详情查看  及 列表是否有新增
            self.add_client()
            self.app_api.ClientFollowList()
            self.app_api.ClueFollowSave(followType='客户', taskEndTime=time.strftime("%Y-%m-%d") + ' 22:00:00')
            self.app_api.ClientFollowList()
            try:
                self.assertEqual('python-线索/客户跟进，本次沟通记录', self.appText.get('followContent'))
            except BaseException as e:
                print("断言错误，错误原因：%s" % e)
                self.app_api.ClientFollowList(value=1)
                self.assertEqual('python-线索/客户跟进，本次沟通记录', self.appText.get('followContent'))
            self.app_api.ClientList()
            """在首页待办任务进行查询"""
            self.app_api.GetUserAgenda(endTime=time.strftime("%Y-%m-%d"))
        except BaseException as e:
            print("断言错误，错误原因：%s" % e)
            raise RuntimeError(self.appText.get('ApiXfpUrl'))

    def test_SettingTakeLook(self):
        """设定带看计划"""
        self.app_api.ClientList()
        if self.appText.get('total') == 0:  # 没有客户
            self.test_addClientSave()
            self.app_api.ClientList()
            self.assertEqual(1, self.appText.get('total'))
        self.app_api.GetMatchingAreaHouse()
        self.app_api.ClientVisitAdd(projectAId=self.appText.get('houseId'))

    def test_AlterSettingTakeLook(self):
        """修改带看计划"""
        try:
            self.test_DelSettingTakeLook()  # 删除原有的带看计划
            self.test_SettingTakeLook()     # 创建新的带看计划
            self.app_api.ClientTask(taskTypeStr='带看行程')
            self.assertEqual(2, self.appText.get('total'))
            self.app_api.GetMatchingAreaHouse()
            self.app_api.UpdateVisitAdd(projectAId=self.appText.get('houseId'))
        except BaseException as e:
            print("断言错误，错误原因：%s" % e)
            raise RuntimeError(self.appText.get('ApiXfpUrl'))

    def test_DelSettingTakeLook(self):
        """删除带看计划"""
        try:
            self.app_api.ClientList()
            if self.appText.get('total') == 0:  # 没有客户
                self.test_addClientSave()
                self.app_api.ClientList()
            self.assertNotEqual(0, self.appText.get('total'))
            self.app_api.ClientTask()
            if self.appText.get('total') == 2:  # 有带看计划
                self.app_api.ClientTask(taskTypeStr='带看行程')
                self.app_api.DelVisit()  # 删除带看
                self.app_api.ClientTask()
                self.assertNotEqual(2, self.appText.get('total'))
                self.app_api.ClientFollowList()
                self.assertEqual('删除带看代办', self.appText.get('followContent'))
            # else:
            #     self.test_SettingTakeLook()
            #     self.app_api.ClientTask(taskTypeStr='带看行程')
            # if self.appText.get('visitId') is None:
            #     print(self.appText.get('ApiXfpUrl'), '接口没有返回 visitId')
            #     self.app_api.visit_info()
            # self.app_api.DelVisit()             # 删除带看
            # self.app_api.ClientTask()
            # self.assertNotEqual(2, self.appText.get('total'))
            # self.app_api.ClientFollowList()
            # self.assertEqual('删除带看代办', self.appText.get('followContent'))
        except BaseException as e:
            print("断言错误，错误原因：%s" % e)
            raise RuntimeError(self.appText.get('ApiXfpUrl'))

    def test_CompleteSettingTakeLook(self):
        """完成带看计划"""
        try:
            self.test_DelSettingTakeLook()  # 删除原有的带看计划
            self.test_SettingTakeLook()     # 创建新的带看计划
            self.app_api.ClientTask(taskTypeStr='带看行程')
            if self.appText.get('total') < 1:
                raise RuntimeError(self.appText.get('ApiXfpUrl'))
            self.app_api.visit_info()
            self.app_api.VisitFlow1()
            self.app_api.ClientTask()
            if self.appText.get('total') >= 2:
                raise RuntimeError(self.appText.get('ApiXfpUrl'))

        except BaseException as e:
            print("断言错误，错误原因：%s" % e)
            raise RuntimeError(self.appText.get('ApiXfpUrl'))

    def test_advance_over_visit(self):
        """提前结束带看代办"""
        try:
            self.test_DelSettingTakeLook()  # 删除原有的带看计划
            self.test_SettingTakeLook()     # 创建新的带看计划
            self.app_api.ClientTask(taskTypeStr='带看行程')
            self.app_api.visit_info()
            self.app_api.OverVisit()        # 提前结束代办
            self.app_api.ClientTask()
            self.app_api.ClientFollowList()
            self.assertEqual('提前结束带看', self.appText.get('followContent'))
        except BaseException as e:
            print("断言错误，错误原因：%s" % e)
            raise RuntimeError(self.appText.get('ApiXfpUrl'))

    def test_AddAgreement(self):
        """录入成交"""
        try:
            self.app_api.TransactionList()
            dome = self.appText.get('total')
            self.add_client()
            self.app_api.GetMatchingAreaHouse()             # 匹配楼盘
            self.assertNotEqual(0, self.appText.get('total'))
            self.app_api.GetLabelList(labelNo='CJX', labelName='认购')
            self.app_api.TransactionSave()                  # 录入成交
            self.app_api.TransactionList()
            self.assertNotEqual(dome, self.appText.get('total'))
        except BaseException as e:
            print("断言错误，错误原因：%s" % e)
            raise RuntimeError(self.appText.get('ApiXfpUrl'))

    def test_SuspendFollow(self):
        """暂停跟进"""
        try:
            self.add_client()
            self.app_api.GetLabelList(labelNo='SQZHGJ', labelName='其他')
            self.app_api.ClientTaskPause()
            while self.appText.get('data') == '该客户已被暂缓!':
                self.app_api.GetLabelList(labelNo='SZGJYY', labelName='客户已成交')
                self.app_api.ExileSea(labelId=self.appText.get('labelId'))
                self.add_client()
                self.app_api.GetLabelList(labelNo='SQZHGJ', labelName='其他')
                self.app_api.ClientTaskPause()
            self.app_api.ClientTask()       # 待办
            if self.appText.get('total') == 1:
                if self.appText.get('taskTypeStr') != '带看行程':
                    raise RuntimeError(self.appText.get('ApiXfpUrl'))
        except BaseException as e:
            print("断言错误，错误原因：%s" % e)
            raise RuntimeError(self.appText.get('ApiXfpUrl'))

    def add_client(self):
        """新增客户"""
        try:
            self.app_api.ClientList()               # 客户列表
            if self.appText.get('total') == 0:      # 客户列表为空
                self.app_api.SeaList()              # 公海列表
                if self.appText.get('total') == 0:  # 公海列表为空
                    self.test_addClientSave()       # 直接新增客户
                else:
                    self.app_api.clue_Assigned()    # 领取线索
                    self.app_api.ClientEntering(callName=self.app_api.RandomText(textArr=surname),
                                                loanSituation='这个是贷款情况')  # 线索转客户
                self.app_api.ClientList()  # 客户列表
                self.assertNotEqual(0, self.appText.get('total'))
        except BaseException as e:
            print("断言错误，错误原因：%s" % e)



