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
        cls.webApi.finance_deal_auditList()
        cls.appText = GlobalMap()
        while cls.appText.get('web_total') != 0:
            cls.webApi.finance_deal_audit(auditStatue=2, remark=time.strftime("%Y-%m-%d %H:%M:%S") + '审核不通过')
            cls.webApi.finance_deal_auditList()
        cls.webApi.auditList()
        while cls.appApi.appText.get('web_total') != 0:
            cls.webApi.audit(auditStatue=2, auditRemark=' 审核失败')
            cls.webApi.auditList()
        cls.webApi.auditList(auditLevel=2)
        while cls.appApi.appText.get('web_total') != 0:
            cls.webApi.audit(auditStatue=2, auditRemark=' 审核失败')
            cls.webApi.auditList(auditLevel=2)

    def test_await_first_phone_01(self):
        """1、平台分派              + 1"""
        if ApiXfpUrl == 'http://xfp.xfj100.com':
            pass
        else:
            self.appApi.TodayClue(isFirst=0)
            dome = self.appText.get('Total')
            self.appApi.Login(userName='admin', saasCode='admin', authCode=0)
            self.webApi.add_clue_admin(clueNickName=self.appApi.RandomText(textArr=surname))
            if self.webText.get('code') != 200:
                self.webApi.addGoldDetailInfo()
                self.webApi.add_clue_admin(clueNickName=self.appApi.RandomText(textArr=surname))
            self.assertEqual(200, self.webText.get('code'))
            self.appApi.Login()
            self.appApi.TodayClue(isFirst=0)
            self.assertNotEqual(dome, self.appText.get('Total'))
            self.assertEqual(dome + 1, self.appText.get('Total'))

    def test_await_first_phone_02(self):
        """2、添加线索              + 1"""
        self.appApi.TodayClue(isFirst=0)
        dome = self.appText.get('Total')
        self.appApi.ClueSave(clueNickName=self.appApi.RandomText(textArr=surname),
                             sourceId=self.appText.get('XSLY'),
                             keyWords=self.appText.get('XSBQ'))
        self.appApi.TodayClue(isFirst=0)
        self.assertNotEqual(dome, self.appText.get('Total'))
        self.assertEqual(dome + 1, self.appText.get('Total'))

    def test_await_first_phone_03(self):
        """3、领取线索              + 1"""
        self.appApi.TodayClue(isFirst=0)
        dome = self.appText.get('Total')
        self.appApi.SeaList()  # 公海列表
        self.appApi.clue_Assigned()  # 领取线索
        self.appApi.TodayClue(isFirst=0)
        self.assertNotEqual(dome, self.appText.get('Total'))
        self.assertEqual(dome + 1, self.appText.get('Total'))

    def test_await_first_phone_04(self):
        """4、线索转移（未首电）    - 1"""
        self.appApi.TodayClue(isFirst=0)
        dome = self.appText.get('Total')
        if dome < 1:
            self.flowPath.add_new_clue()
        self.appText.set_map('clueId', (json.loads(json.dumps(self.appText.get('records'))))[0]['clueId'])
        self.appApi.ClueChange()  # 线索转移
        self.appApi.TodayClue(isFirst=0)
        self.assertNotEqual(dome, self.appText.get('Total'))
        self.assertEqual(dome - 1, self.appText.get('Total'))

    def test_await_first_phone_05(self):
        """5、线索流放公海（未首电）   - 不支持该操作"""
        self.appApi.TodayClue(isFirst=0)
        dome = self.appText.get('Total')
        if dome < 1:
            self.flowPath.add_new_clue()
        self.appText.set_map('clueId', (json.loads(json.dumps(self.appText.get('records'))))[0]['clueId'])
        self.appApi.ExileSea()
        self.assertNotEqual(200, self.appText.get('code'))
        self.assertEqual('该线索未首电,不能终止跟进!', self.appText.get('data'))

    def test_await_follow_01(self):
        """1、新增线索（未首电）     + 1"""
        self.follow_front()
        self.appApi.ClueSave(clueNickName=self.appApi.RandomText(textArr=surname),
                             sourceId=self.appText.get('XSLY'),
                             keyWords=self.appText.get('XSBQ'))
        self.follow_later(0)
        self.appApi.ClueInfo()
        """2、新增线索（已首电）     + 1"""
        try:
            self.appApi.phone_log(callee_num=self.appApi.appText.get('cluePhone'),
                                  is_own_call=0, talk_time=12000,
                                  call_time=time.strftime("%Y-%m-%d %H:%M:%S"))
            self.follow_later()
        except:
            self.appApi.ClueFollowList()
            self.appApi.ClueFollowSave(taskEndTime=time.strftime("%Y-%m-%d %H:%M:%S"))
            self.follow_later(vlue=1)

    def test_await_follow_02(self):
        """3、线索转移               - 1"""
        self.flowPath.clue_non_null()
        self.appApi.my_clue_list()
        self.appApi.ClueFollowList()
        self.appApi.ClueFollowSave(taskEndTime=time.strftime("%Y-%m-%d %H:%M:%S"))
        self.follow_front()
        self.appApi.ClueChange()  # 线索转移
        self.appApi.GetUserAgenda()
        self.follow_later(vlue=-1)

    def test_await_follow_03(self):
        """4、线索转客户             + 0"""
        self.flowPath.clue_non_null()
        self.appApi.my_clue_list()
        self.appApi.ClueFollowList()
        self.appApi.ClueFollowSave(taskEndTime=time.strftime("%Y-%m-%d %H:%M:%S"))
        self.follow_front()
        self.appApi.ClueInfo()
        self.appApi.ClientEntering(callName=self.appApi.RandomText(textArr=surname),
                                   loanSituation='这个是贷款情况')
        self.follow_later()

    # def test_await_follow_09(self):
    #     """11、线索流放公海（无需审核）   - 1"""
    #     self.webApi.Audit_management()  # 修改配置审核
    #     self.clue_front()
    #     self.follow_front()
    #     self.flowPath.clue_exile_sea()
    #     self.follow_later(vlue=-1)
    #
    # def test_await_follow_10(self):
    #     """12、线索流放公海（审核中）     - 0"""
    #     self.clue_front()
    #     self.webApi.Audit_management(clueStop=True, clueStopLevel=1)
    #     self.follow_front()
    #     self.flowPath.clue_exile_sea()
    #     self.follow_later()
    #     """13、线索流放公海（审核失败）   - 0"""
    #     self.webApi.auditList(phoneNum=self.appText.get('cluePhone'))
    #     self.webApi.audit(auditStatue=2, auditRemark=time.strftime("%Y-%m-%d %H:%M:%S") + ' 审核失败')
    #     # self.webApi.audit_List()  # 审核列表
    #     # self.webApi.auditApply(isAudit=False)
    #     self.follow_later()
    #
    # def test_await_follow_11(self):
    #     """14、线索流放公海（审核成功）   - 1"""
    #     self.clue_front()
    #     self.webApi.Audit_management(clueStop=True, clueStopLevel=1)
    #     self.follow_front()
    #     self.flowPath.clue_exile_sea()
    #     self.webApi.auditList(phoneNum=self.appText.get('cluePhone'))
    #     self.webApi.audit()
    #     self.follow_later(vlue=-1)

    def test_await_follow_18(self):
        """25、线索跟进（下次跟进日期为明日）      - 1"""
        self.flowPath.clue_non_null()
        self.appApi.my_clue_list()
        self.appApi.ClueFollowList()
        self.appApi.ClueFollowSave(taskEndTime=time.strftime("%Y-%m-%d %H:%M:%S"))
        self.follow_front()
        tomorrow = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
        self.appApi.ClueFollowSave(taskEndTime=tomorrow)
        self.follow_later(vlue=-1)

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



