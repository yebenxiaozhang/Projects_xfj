# -*- coding: utf-8 -*-
# @Time    : 2020/3/21 10:48
# @Author  : 潘师傅
# @File    : Hone_casc.py

"""首页相关"""
from XFP.PubilcAPI.flowPath import *
from datetime import date, timedelta

"""
待首电：
    1、平台分派              + 1
    2、添加线索              + 1
    3、领取线索              + 1
    4、线索转移（未首电）    - 1
    5、线索流放公海（未首电）   - 不支持该操作
待跟进-（默认创建为当日）
                                        | 客户、线索转移  | 客户暂缓  |   释放公海    |    转客户

    1、新增线索（未首电）     + 1
    2、新增线索（已首电）     + 1
    3、线索转移               - 1
    4、线索转客户             + 0
    5、客户转移（未申请暂缓） - 1
    6、客户转移（暂缓审核中） - 1
    7、客户转移（已暂缓）     + 0
    8、客户暂缓（审核中）     + 0
    9、客户暂缓（审核通过）   - 1
    10、客户暂缓（审核失败）  + 0
    11、线索流放公海（无需审核）   - 1
    12、线索流放公海（审核中）     - 0
    13、线索流放公海（审核失败）   - 0
    14、线索流放公海（审核成功）   - 1
    15、客户流放公海（未申请暂缓 | 无需审核）     - 1
    16、客户流放公海（未申请暂缓 | 审核中）       - 0
    17、客户流放公海（未申请暂缓 | 审核失败）     - 0
    18、客户流放公海（未申请暂缓 | 审核成功）     - 1
    19、客户流放公海（已暂缓 | 无需审核）     - 0
    20、客户流放公海（已暂缓 | 审核中）       - 0
    21、客户流放公海（已暂缓 | 审核失败）     - 1
    22、客户流放公海（已暂缓 | 审核成功）     - 0
    23、客户创建带看       - 0
    24、客户录入成交       - 0
    25、线索跟进（下次跟进日期为明日）      - 1
    26、客户跟进（下次跟进日期为明日）      - 1

即将带看：
    1、录入带看（无需审核）    + 1
    2、录入带看（审核中）      + 1
    3、录入带看（审核失败）    + 0
    4、客户转移（有带看）      - 1
    5、客户转移（无带看）      - 0
    6、客户流放公海（有带看）  - 1
    7、客户流放公海（无带看）  - 0
    8、客户暂缓跟进            - 0
    8、客户录入客户            - 0
    9、录入客户带看（七天内）  + 1
    10、录入客户带看（七天后） + 0

"""


class TestCase(unittest.TestCase):
    """首页——相关指标"""

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

    def setUp(self):
        """残留审核 失败！！！"""
        self.webApi.audit_List()
        while self.webApi.webText.get('total') != 0:
            self.webApi.auditApply(isAudit=False,
                                   auditRemark='客户流放公海', customerId=self.webText.get('customerId'))
            self.webApi.audit_List()
        self.webApi.audit_List(auditLevel=2)
        while self.webApi.webText.get('total') != 0:
            self.webApi.auditApply(isAudit=False,
                                   auditRemark='客户流放公海', customerId=self.webText.get('customerId'))
            self.webApi.audit_List()

    def test_await_follow_04(self):
        """5、客户转移（未申请暂缓） - 1"""
        self.flowPath.client_list_non_null()
        self.appApi.ClientFollowList()
        self.appApi.ClueFollowSave(taskEndTime=time.strftime("%Y-%m-%d %H:%M:%S"), followType='客户')
        self.follow_front()
        self.appApi.client_change()
        self.follow_later(vlue=-1)

    def test_await_follow_05(self):
        """6、客户转移（暂缓审核中） - 1"""
        self.flowPath.client_list_non_null()
        self.appApi.ClientFollowList()
        self.appApi.ClueFollowSave(taskEndTime=time.strftime("%Y-%m-%d %H:%M:%S"), followType='客户')
        self.webApi.Audit_management(suspend=True, suspendLevel=1)  # 修改配置审核
        self.follow_front()
        self.appApi.ClientTaskPause()
        self.follow_later()
        self.appApi.client_change()
        self.assertNotEqual(200, self.appText.get('code'))

    def test_await_follow_06(self):
        """7、客户转移（已暂缓）     + 0"""
        self.flowPath.client_list_non_null()
        self.appApi.ClientFollowList()
        self.appApi.ClueFollowSave(taskEndTime=time.strftime("%Y-%m-%d %H:%M:%S"), followType='客户')
        self.webApi.Audit_management()  # 修改配置审核
        self.appApi.ClientTaskPause()
        self.follow_front()
        self.appApi.client_change()
        self.follow_later()

    def test_await_follow_07(self):
        """8、客户暂缓（审核中）     + 0"""
        self.flowPath.client_list_non_null()
        self.appApi.ClientFollowList()
        self.appApi.ClueFollowSave(taskEndTime=time.strftime("%Y-%m-%d %H:%M:%S"), followType='客户')
        self.webApi.Audit_management(suspend=True, suspendLevel=1)  # 修改配置审核
        self.follow_front()
        self.appApi.ClientTaskPause()
        self.follow_later()
        """9、客户暂缓（审核通过）   - 1"""
        self.webApi.audit_List()  # 审核列表
        self.webApi.auditApply(customerId=self.appText.get('customerId'),
                               endTime=time.strftime("%Y-%m-%d %H:%M:%S"))
        self.follow_later(vlue=-1)

    def test_await_follow_08(self):
        """10、客户暂缓（审核失败）  + 0"""
        self.flowPath.client_list_non_null()
        self.appApi.ClientFollowList()
        self.appApi.ClueFollowSave(taskEndTime=time.strftime("%Y-%m-%d %H:%M:%S"), followType='客户')
        self.webApi.Audit_management(suspend=True, suspendLevel=1)  # 修改配置审核
        self.follow_front()
        self.appApi.ClientTaskPause()
        self.webApi.audit_List()  # 审核列表
        self.webApi.auditApply(customerId=self.appText.get('customerId'), isAudit=False,
                               endTime=time.strftime("%Y-%m-%d %H:%M:%S"))
        self.follow_later()

    def test_await_follow_12(self):
        """15、客户流放公海（未申请暂缓 | 无需审核）     - 1"""
        self.client_front()
        self.webApi.Audit_management()
        self.follow_front()
        self.appApi.client_exile_sea()
        self.follow_later(vlue=-1)

    def test_await_follow_13(self):
        """16、客户流放公海（未申请暂缓 | 审核中）       - 0"""
        self.client_front()
        self.webApi.Audit_management(customerStop=True, customerStopLevel=1)  # 修改配置审核
        self.follow_front()
        self.appApi.client_exile_sea()
        self.follow_later()
        """17、客户流放公海（未申请暂缓 | 审核失败）     - 0"""
        self.webApi.audit_List()  # 审核列表
        self.webApi.auditApply(isAudit=False, customerId=self.appText.get('customerId'))
        self.follow_later()
        """18、客户流放公海（未申请暂缓 | 审核成功）     - 1"""
        self.appApi.client_exile_sea()
        self.webApi.audit_List()  # 审核列表
        self.webApi.auditApply(customerId=self.appText.get('customerId'))
        self.follow_later(vlue=-1)

    def test_await_follow_14(self):
        """19、客户流放公海（已暂缓 | 无需审核）     - 0"""
        self.flowPath.client_list_non_null()
        self.appApi.ClientTaskPause()
        self.follow_front()
        self.webApi.Audit_management()  # 修改配置审核
        self.appApi.client_exile_sea()
        self.follow_later()

    def test_await_follow_15(self):
        """20、客户流放公海（已暂缓 | 审核中）       - 0"""
        self.flowPath.client_list_non_null()
        self.appApi.ClientFollowList()
        self.appApi.ClueFollowSave(followType='客户', taskEndTime=time.strftime("%Y-%m-%d") + ' 22:00:00')
        self.webApi.Audit_management(suspend=True, suspendLevel=1)  # 修改配置审核
        self.appApi.ClientTaskPause()
        self.follow_front()
        self.appApi.client_exile_sea()
        self.assertNotEqual(200, self.appText.get('code'))
        """21、客户流放公海（已暂缓 | 审核失败）     - 1"""
        self.webApi.audit_List()  # 审核列表
        self.webApi.auditApply(isAudit=False, customerId=self.appText.get('customerId'))
        self.appApi.client_exile_sea()
        self.follow_later(vlue=-1)

    def test_await_follow_16(self):
        """22、客户流放公海（已暂缓 | 审核成功）     - 0"""
        self.flowPath.client_list_non_null()
        self.appApi.ClientFollowList()
        self.appApi.ClueFollowSave(followType='客户', taskEndTime=time.strftime("%Y-%m-%d") + ' 22:00:00')
        self.webApi.Audit_management(suspend=True, suspendLevel=1)  # 修改配置审核
        self.appApi.ClientTaskPause()
        self.webApi.audit_List()  # 审核列表
        self.webApi.auditApply(customerId=self.appText.get('customerId'),
                               endTime=time.strftime("%Y-%m-%d %H:%M:%S"))
        self.follow_front()
        self.appApi.client_exile_sea()
        self.follow_later()

    def test_await_follow_17(self):
        """23、客户创建带看       - 0"""
        self.flowPath.clue_non_null()
        self.appApi.my_clue_list()
        self.appApi.ClueFollowList()
        self.appApi.ClueFollowSave(taskEndTime=time.strftime("%Y-%m-%d %H:%M:%S"))
        self.follow_front()
        self.appApi.GetMatchingAreaHouse()
        self.appApi.ClientVisitAdd(projectAId=self.appApi.appText.get('houseId'),
                                   appointmentTime=time.strftime("%Y-%m-%d %H:%M:%S"),
                                   seeingConsultant=self.appApi.appText.get('consultantId'),
                                   appointConsultant=self.appApi.appText.get('consultantId'))
        self.follow_later()
        """24、客户录入成交       - 0"""
        self.flowPath.add_deal()
        self.follow_later()

    def test_await_follow_19(self):
        """26、客户跟进（下次跟进日期为明日）      - 1"""
        self.flowPath.client_list_non_null()
        self.appApi.ClientFollowList()
        self.appApi.ClueFollowSave(followType='客户', taskEndTime=time.strftime("%Y-%m-%d") + ' 22:00:00')
        self.follow_front()
        tomorrow = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
        self.appApi.ClueFollowSave(taskEndTime=tomorrow, followType='客户')
        self.follow_later(vlue=-1)

    def test_await_visit_01(self):
        """1、录入带看（无需审核）    + 1"""
        self.webApi.Audit_management()  # 修改配置审核
        self.visit_front()
        self.visit_later(vlue=1)

    def test_await_visit_02(self):
        """2、录入带看（审核中）      + 1"""
        self.webApi.Audit_management(customerVisit=True, customerVisitLevel=1)  # 修改配置审核
        self.visit_front()
        self.visit_later(vlue=1)
        """3、录入带看（审核失败）    + 0"""
        self.webApi.audit_List()  # 审核列表
        self.webApi.auditApply(isAudit=False, customerId=self.appText.get('customerId'))
        self.visit_later()

    def test_await_visit_03(self):
        """4、客户转移（有带看）      - 1"""
        self.webApi.Audit_management()  # 修改配置审核
        self.visit_front()
        self.appApi.client_change()
        self.visit_later()

    def test_await_visit_04(self):
        """5、客户转移（无带看）      - 0"""
        self.visit_front(vlue=0)
        self.appApi.client_change()
        self.visit_later()

    def test_await_visit_05(self):
        """6、客户流放公海（有带看）  - 1"""
        self.visit_front()
        self.appApi.client_exile_sea()
        self.visit_later()

    def test_await_visit_06(self):
        """7、客户流放公海（无带看）  - 0"""
        self.visit_front(vlue=0)
        self.appApi.client_exile_sea()
        self.visit_later()

    def test_await_visit_07(self):
        """客户暂缓跟进"""
        self.visit_front(vlue=0)
        self.appApi.ClientTaskPause()
        self.visit_later()

    def test_await_visit_08(self):
        """8、客户录入客户            - 0"""
        self.visit_front(vlue=0)
        self.flowPath.add_deal()
        self.visit_later()

    def test_await_visit_09(self):
        """10、录入客户带看（七天后） + 0"""
        self.visit_front(vlue1=2)
        self.visit_later()

    def visit_front(self, vlue=1, vlue1=0):
        """带看前"""
        self.flowPath.clue_non_null()
        self.appApi.my_clue_list()
        self.appApi.ClueFollowList()
        if vlue1 != 0:
            days = 9
        else:
            days = 1
        self.appApi.ClueFollowSave(taskEndTime=time.strftime("%Y-%m-%d %H:%M:%S"))
        self.appApi.ClueInfo()
        self.appApi.ClientEntering(callName=self.appApi.RandomText(textArr=surname),
                                   loanSituation='这个是贷款情况')
        tomorrow = (date.today() + timedelta(days=days)).strftime("%Y-%m-%d %H:%M:%S")
        tomorrow1 = (date.today() + timedelta(days=7)).strftime("%Y-%m-%d")
        self.appApi.Task_Visit_List(endTime=tomorrow1 + ' 23:59:59', visiteStatus=0)
        globals()['dome'] = self.appText.get('total')
        self.appApi.ClientList()  # 客户列表
        if vlue == 1:
            self.appApi.ClueInfo()
            self.appApi.ClientVisitAdd(projectAId=self.appApi.appText.get('houseId'),
                                       appointmentTime=tomorrow,
                                       seeingConsultant=self.appApi.appText.get('consultantId'),
                                       appointConsultant=self.appApi.appText.get('consultantId'))

    def visit_later(self, vlue=0):
        """带看后"""
        tomorrow = (date.today() + timedelta(days=7)).strftime("%Y-%m-%d")
        self.appApi.Task_Visit_List(endTime=tomorrow + ' 23:59:59', visiteStatus=0)
        if vlue == 0:
            self.assertEqual(globals()['dome'], self.appText.get('total'))
        else:
            self.assertNotEqual(globals()['dome'], self.appText.get('total'))
            if vlue == -1:
                self.assertEqual(globals()['dome'] - 1, self.appText.get('total'))
            else:
                self.assertEqual(globals()['dome'] + 1, self.appText.get('total'))

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

    def client_front(self):
        """客户前"""
        self.flowPath.client_list_non_null()
        self.appApi.ClientFollowList()
        self.appApi.ClueFollowSave(taskEndTime=time.strftime("%Y-%m-%d %H:%M:%S"), followType='客户')



