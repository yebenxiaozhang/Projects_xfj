# -*- coding: utf-8 -*-
# @Time    : 2020/3/30 20:47
# @Author  : 潘师傅
# @File    : Client_case.py

"""线索相关"""
from XFP.PubilcAPI.flowPath import *
# 通过总部分配的线索不允许修改来源


class ClueTestCase(unittest.TestCase):
    """幸福派APP——线索"""

    def __init__(self, *args, **kwargs):
        super(ClueTestCase, self).__init__(*args, **kwargs)
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

    def test_FollowClue(self):
        """跟进线索"""
        self.flowPath.clue_non_null()
        self.appApi.ClueFollowList()
        self.appApi.ClueFollowSave(taskEndTime=time.strftime("%Y-%m-%d") + ' 22:00:00')
        time.sleep(1)
        self.appApi.ClueFollowList()
        try:
            self.assertEqual('python-线索/客户跟进，本次沟通记录', self.appText.get('followContent'))
            """查看今日上户是否已首电"""
        except BaseException as e:
            print("断言错误，错误原因：%s" % e)
            self.appApi.ClueFollowList(value=1)
            self.assertEqual('python-线索/客户跟进，本次沟通记录', self.appText.get('followContent'))

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
        self.assertEqual(self.appText.get('followContent')[:6], '线索流放公海')

    def test_ChangeClient(self):
        """线索转为客户"""
        self.flowPath.clue_non_null()
        self.appApi.ClueFollowList()
        self.appApi.ClueFollowSave(taskEndTime=time.strftime("%Y-%m-%d") + ' 22:00:00')
        self.appApi.ClueInfo()
        self.appApi.ClientEntering(callName=self.appApi.RandomText(textArr=surname),
                                   loanSituation='这个是贷款情况')
        self.assertEqual(200, self.appText.get('code'))
        # 转化为客户后，在首页进行验证

    def test_ClueShift(self):
        """线索转移"""
        self.flowPath.clue_non_null()
        dome2 = self.appText.get('cluePhone')
        self.appApi.my_clue_list()         # 转移后查看自己的列表
        dome = self.appText.get('total')
        self.appApi.ClueChange()        # 线索转移
        self.appApi.my_clue_list()         # 转移后查看自己的列表
        self.assertEqual(dome-1, self.appText.get('total'))
        # 登陆转移后账号进行查看
        self.appApi.Login(userName=XfpUser1, password=XfpPwd1)
        self.appApi.my_clue_list(keyWord=dome2)
        self.assertEqual(1, self.appText.get('total'))
        self.appApi.ClueFollowList()
        self.assertEqual('线索转移', self.appText.get('followContent')[:4])

    def test_clue_ChangeClient(self):
        """未首电转客户"""
        self.appApi.SeaList()  # 公海列表
        self.appApi.clue_Assigned()  # 领取线索
        self.appApi.my_clue_list()
        self.appApi.ClueInfo()
        self.appApi.ClientEntering(callName=self.appApi.RandomText(textArr=surname),
                                   loanSituation='这个是贷款情况')
        self.assertNotEqual(200, self.appText.get('code'))
        self.assertEqual('该线索未首电,不能转为客户!', self.appText.get('data'))

    def test_admin_clue(self):
        """通过总部分配的线索不允许修改来源"""
        if ApiXfpUrl == 'http://xfp.xfj100.com':
            pass
        else:
            self.appApi.Login(userName='admin', saasCode='admin')
            self.webApi.add_clue_admin(clueNickName=self.appApi.RandomText(textArr=surname))
            self.appApi.Login()
            self.appApi.my_clue_list()
            self.appApi.ClueInfo()
            self.appApi.ClueSave(Status=2,
                                 clueNickName=self.appApi.RandomText(textArr=surname),
                                 sourceId=self.appText.get('XSLY'))
            self.assertNotEqual(200, self.appText.get('code'))
            self.assertEqual('总部分配过来的线索,线索来源不能修改', self.appText.get('data'))
