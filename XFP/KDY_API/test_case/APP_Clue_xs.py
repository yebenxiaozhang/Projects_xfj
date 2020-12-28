# -*- coding: utf-8 -*-
# @Time    : 2020/3/30 20:47
# @Author  : 潘师傅
# @File    : Client_case.py

"""线索相关"""
from PubilcAPI.flowPath import *

# 通过总部分配的线索不允许修改来源


class TestCase(unittest.TestCase):
    """幸福派APP——线索"""

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
        登录经纪人 获取ID"""
        cls.do_request = appApi()
        cls.appApi = cls.do_request
        cls.appApi.Login()
        cls.appApi.GetUserData()
        cls.request = webApi()
        cls.webApi = cls.request
        cls.webApi.Audit_management()
        cls.webApi.auditList()
        while cls.appApi.appText.get('web_total') != 0:
            cls.webApi.audit(auditStatue=2, auditRemark=' 审核失败')
            cls.webApi.auditList()
        cls.webApi.auditList(auditLevel=2)
        while cls.appApi.appText.get('web_total') != 0:
            cls.webApi.audit(auditStatue=2, auditRemark=' 审核失败')
            cls.webApi.auditList(auditLevel=2)

    def test_FollowClue(self):
        """1、跟进线索"""
        self.flowPath.clue_non_null()
        self.appApi.ClueFollowList()
        time.sleep(1)
        self.appApi.ClueFollowSave(taskEndTime=time.strftime("%Y-%m-%d") + ' 22:00:00')
        """2、查看线索跟进后的跟进日志"""
        self.appApi.ClueFollowList()
        self.assertEqual('python-线索/客户跟进，本次沟通记录', self.appText.get('followContent'))
        """3、线索跟进（下次跟进日期为明日）"""
        # 先查看今日待办有多少 | 查看财富值今日多少
        self.appApi.GetUserAgenda()
        dome = self.appText.get('total')
        self.appApi.getWealthDetailList(startTime=time.strftime("%Y-%m-%d"),
                                        endTime=time.strftime("%Y-%m-%d"),
                                        orderNo=self.appText.get('orderNo'))
        vlue = self.appText.get('vlue')
        tomorrow = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
        self.appApi.ClueFollowSave(taskEndTime=tomorrow)
        self.appApi.GetUserAgenda()
        self.assertEqual(dome - 1, self.appText.get('total'))
        self.appApi.getWealthDetailList(startTime=time.strftime("%Y-%m-%d"),
                                        endTime=time.strftime("%Y-%m-%d"),
                                        orderNo=self.appText.get('orderNo'))
        self.assertEqual(vlue + 15, self.appText.get('vlue'))

    def test_AlterClueMessage(self):
        """修改线索信息"""
        self.flowPath.clue_non_null()
        globals()['cluePhone'] = self.appText.get('cluePhone')
        self.appApi.ClueSave(Status=2,
                             clueNickName=self.appApi.RandomText(textArr=surname),
                             sourceId=self.appText.get('sourceId'), keyWords=self.appText.get('XSBQ'))
        self.appApi.ClueInfo()
        self.assertNotEqual(globals()['cluePhone'], self.appText.get('cluePhone'))

    def test_ExileSea(self):
        """流放公海"""
        self.flowPath.clue_non_null()
        self.flowPath.clue_exile_sea()
        # 跟进进行验证
        self.appApi.ClueFollowList()
        self.assertEqual(self.appText.get('followContent')[:6], '线索终止跟进')

    def test_ChangeClient(self):
        """1、线索转为客户"""
        self.flowPath.clue_non_null()
        self.appApi.ClueFollowList()
        self.appApi.ClueFollowSave(taskEndTime=time.strftime("%Y-%m-%d") + ' 22:00:00')
        self.appApi.ClueInfo()
        self.appApi.GetUserAgenda()
        dome = self.appText.get('total')
        self.appApi.my_clue_list()
        self.appApi.ClientEntering(callName=self.appApi.RandomText(textArr=surname),
                                   loanSituation='这个是贷款情况')
        self.assertEqual(200, self.appText.get('code'))
        # 转化为客户后，任务是否有新增
        self.appApi.GetUserAgenda()
        self.assertEqual(dome, self.appText.get('total'))

    def test_ClueShift(self):
        """线索转移"""
        self.flowPath.clue_non_null()
        dome2 = self.appText.get('cluePhone')
        self.appApi.ClueFollowList()
        self.appApi.ClueFollowSave(taskEndTime=time.strftime("%Y-%m-%d %H:%M:%S"))
        self.appApi.GetUserAgenda()
        dome3 = self.appText.get('total')
        self.appApi.my_clue_list()         # 转移后查看自己的列表
        dome = self.appText.get('total')
        self.appApi.ClueChange()        # 线索转移
        self.appApi.my_clue_list()         # 转移后查看自己的列表
        self.assertEqual(dome-1, self.appText.get('total'))
        # 登陆转移后账号进行查看
        self.appApi.Login(userName=XfpUser1, password=XfpPwd1)
        self.appApi.GetUserData()
        self.appApi.my_clue_list(keyWord=dome2)
        self.assertEqual(1, self.appText.get('total'))
        self.appApi.ClueFollowList()
        self.assertIn('将线索指派至', self.appText.get('followContent'))
        self.appApi.Login()
        self.appApi.GetUserData()
        """转移过后查看自己的待办是否有新增"""
        self.appApi.GetUserAgenda()
        self.assertEqual(dome3 - 1, self.appText.get('total'))

    def test_clue_ChangeClient(self):
        """1、未首电转客户"""
        """2、从公海领取-待办列表是否有新增"""
        self.appApi.TodayClue(isFirst=0)
        dome = self.appText.get('Total')
        self.appApi.SeaList()  # 公海列表
        self.appApi.clue_Assigned()  # 领取线索
        # 验证从公海领取 待首电是否有新增
        self.appApi.TodayClue(isFirst=0)
        self.assertNotEqual(dome, self.appText.get('Total'))
        self.assertEqual(dome + 1, self.appText.get('Total'))

        self.appApi.my_clue_list()
        self.appApi.ClueInfo()
        self.appApi.ClientEntering(callName=self.appApi.RandomText(textArr=surname),
                                   loanSituation='这个是贷款情况')
        if '该线索未首电,不能转为客户!' != self.appText.get('data'):
            print(self.appText.get('data'))
            self.appApi.ClueFollowList()
            print(self.appText.get('data'))
            raise RuntimeError('该线索未首电,不能转为客户!')

        self.appApi.ExileSea()
        self.assertNotEqual(200, self.appText.get('code'))
        self.assertEqual('该线索未首电,不能终止跟进!', self.appText.get('data'))

    def test_admin_clue(self):
        """通过总部分配的线索不允许修改来源"""
        if ApiXfpUrl == 'http://xfp.xfj100.com':
            pass
        else:
            """总站分配待首电数量是否新增"""
            self.appApi.TodayClue(isFirst=0)
            dome = self.appText.get('Total')
            self.appApi.Login(userName='admin', saasCode='admin', authCode=0)
            self.webApi.add_clue_admin(clueNickName=self.appApi.RandomText(textArr=surname))
            if self.webText.get('code') != 200:
                self.webApi.addGoldDetailInfo()
                self.webApi.add_clue_admin(clueNickName=self.appApi.RandomText(textArr=surname))
            self.appApi.Login()
            self.appApi.my_clue_list()
            self.appApi.ClueInfo()
            self.appApi.ClueSave(Status=2,
                                 clueNickName=self.appApi.RandomText(textArr=surname),
                                 sourceId=self.appText.get('XSLY'))
            if self.appText.get('code') == 200:
                raise RuntimeError('总部分配过来的线索,线索来源不能修改')
            # 检验从总站分配过来的线索是否添加待办
            self.appApi.TodayClue(isFirst=0)
            self.assertNotEqual(dome, self.appText.get('Total'))
            self.assertEqual(dome + 1, self.appText.get('Total'))
            dome = self.appText.get('Total')
            """未首电进行转移"""
            self.appApi.ClueChange()  # 线索转移
            self.appApi.TodayClue(isFirst=0)
            self.assertNotEqual(dome, self.appText.get('Total'))
            self.assertEqual(dome - 1, self.appText.get('Total'))



