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
        cls.webApi.consultant_allocition(isAppoint=1)

        cls.appApi.GetLabelList(labelNo='CFZLX', labelName='成交奖励', saasCode='admin')
        cls.appText.set_map('CJJL', cls.appText.get('remark'))
        cls.appApi.GetLabelList(labelNo='CFZLX', labelName='邀约带看', saasCode='admin')
        cls.appText.set_map('YYDK', cls.appText.get('remark'))
        cls.webApi.get_group()
        cls.appApi.GetLabelList(labelNo='CFZLX', labelName='平台上户', saasCode='admin')
        cls.appText.set_map('PTSH', cls.appText.get('remark'))
        cls.appApi.get_current_month_start_and_end(date=time.strftime("%Y-%m-%d"))
        cls.webApi.audit_List()
        while cls.webApi.webText.get('total') != 0:
            cls.webApi.auditApply(isAudit=False, auditRemark='客户流放公海')
            cls.webApi.audit_List()
        cls.webApi.audit_List(auditLevel=2)
        while cls.webApi.webText.get('total') != 0:
            cls.webApi.auditApply(isAudit=False, auditRemark='客户流放公海')
            cls.webApi.audit_List()

        cls.appApi.my_clue_list()
        while cls.appText.get('total') >= 1:
            cls.flowPath.clue_exile_sea()
            cls.appApi.my_clue_list()

        cls.appApi.ClientList()
        while cls.appText.get('total') >= 1:
            cls.appApi.client_exile_sea()
            cls.appApi.ClientList()

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
        self.flowPath.add_visit()
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
        self.visit_later(vlue=1)

    def test_await_visit_03(self):
        """4、客户转移（有带看）      - 1"""
        self.webApi.Audit_management()  # 修改配置审核
        self.visit_front()
        self.appApi.client_change()
        self.visit_later(vlue=1)

    def test_await_visit_04(self):
        """5、客户转移（无带看）      - 0"""
        self.visit_front(vlue=0)
        self.appApi.client_change()
        self.visit_later()

    def test_await_visit_05(self):
        """6、客户流放公海（有带看）  - 1"""
        self.visit_front()
        self.appApi.client_exile_sea()
        self.visit_later(vlue=1)

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
        self.appApi.GetUserAgenda(tesk=2)
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



