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

    def test_await_first_phone_01(self):
        """1、平台分派              + 1"""
        if ApiXfpUrl == 'http://xfp.xfj100.com':
            pass
        else:
            self.appApi.TodayClue(isFirst=0)
            dome = self.appText.get('Total')
            self.appApi.Login(userName='admin', saasCode='admin')
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



