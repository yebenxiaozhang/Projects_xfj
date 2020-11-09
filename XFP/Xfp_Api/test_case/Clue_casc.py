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
        cls.flow = flowPath()
        cls.flowPath = cls.flow
        cls.appText = GlobalMap()
        # 线索来源
        cls.flowPath.get_label(labelNo='XSLY', labelName='线索来源',
                               newlabelName='百度小程序')
        cls.appText.set_map('XSLY', cls.appText.get('labelId'))
        # 线索标签
        cls.appApi.GetUserLabelList(userLabelType='线索标签')
        if cls.appText.get('total') == 0:
            cls.appApi.AddUserLabel()
            cls.appApi.GetUserLabelList(userLabelType='线索标签')
        cls.appText.set_map('XSBQ', cls.appText.get('labelData'))

    def test_1_AddNewClue(self):
        """新增一条线索"""
        try:
            self.appApi.ClueSave(clueNickName=self.appApi.RandomText(textArr=surname),
                                 sourceId=self.appText.get('labelId'),
                                 keyWords=self.appText.get('labelData'))
            # 在搜索列表进行查找
            globals()['cluePhone'] = self.appText.get('cluePhone')
            self.appApi.ClueList(keyWord=(self.appText.get('cluePhone')))
            self.assertEqual(self.appText.get('cluePhone'), globals()['cluePhone'])
            """今日上户上进行查看"""
            self.appApi.TodayClue(keyWord=self.appText.get('cluePhone'))
            self.assertEqual(1, self.appText.get('Total'))
            self.assertEqual(0, self.appText.get('isFirst'))        # 是否首电
            time.sleep(2)
            # self.test_4_ExileSea()
        except BaseException as e:
                print("错误，错误原因：%s" % e)
                raise RuntimeError(self.appText.get('ApiXfpUrl'))

    def test_2_FollowClue(self):
        """跟进线索"""
        self.appApi.my_clue_list()
        self.appApi.ClueFollowList()
        self.appApi.ClueFollowSave(taskEndTime=time.strftime("%Y-%m-%d") + ' 22:00:00')
        time.sleep(1)
        self.appApi.ClueFollowList()
        try:
            self.assertEqual('python-线索/客户跟进，本次沟通记录', self.appText.get('followContent'))
            """查看今日上户是否已首电"""
            self.appApi.TodayClue(keyWord=self.appText.get('cluePhone'))
            # self.assertEqual(1, self.appText.get('isFirst'))
        except BaseException as e:
            print("断言错误，错误原因：%s" % e)
            self.appApi.ClueFollowList(value=1)
            self.assertEqual('python-线索/客户跟进，本次沟通记录', self.appText.get('followContent'))
            self.appApi.TodayClue(keyWord=self.appText.get('cluePhone'))
            # self.assertEqual(1, self.appText.get('isFirst'))

    def test_3_AlterClueMessage(self):
        """修改线索信息"""
        self.flowPath.clue_non_null()
        self.appApi.my_clue_list()
        self.appApi.GetUserLabelList(userLabelType='线索标签')
        self.appApi.GetLabelList(labelNo='XSLY', labelName='百度小程序')
        globals()['cluePhone'] = self.appText.get('cluePhone')
        self.appApi.ClueSave(Status=2,
                             clueNickName=self.appApi.RandomText(textArr=surname),
                             sourceId=self.appText.get('labelId'), keyWords=self.appText.get('labelData'))
        self.appApi.ClueInfo()
        self.assertNotEqual(globals()['cluePhone'], self.appText.get('cluePhone'))

    def test_4_ExileSea(self):
        """流放公海"""
        self.flowPath.clue_non_null()
        self.appApi.my_clue_list()
        self.appApi.GetLabelList(labelNo='SZGJYY', labelName='客户已成交')
        self.appApi.ExileSea(labelId=self.appText.get('labelId'))
        # 流放公海 在首页进行验证
        self.appApi.GetUserAgenda(keyWord=self.appText.get('cluePhone'), endTime=time.strftime("%Y-%m-%d"))
        # 跟进进行验证
        self.appApi.ClueFollowList()
        self.assertEqual(self.appText.get('followContent')[:6], '线索流放公海')

    def test_ChangeClient(self):
        """线索转为客户"""
        self.flowPath.clue_non_null()
        self.appApi.my_clue_list()
        self.appApi.ClueFollowList()
        self.appApi.ClueFollowSave(taskEndTime=time.strftime("%Y-%m-%d") + ' 22:00:00')
        self.appApi.ClueInfo()
        self.appApi.ClientEntering(callName=self.appApi.RandomText(textArr=surname),
                                   loanSituation='这个是贷款情况')
        self.assertEqual(200, self.appText.get('code'))
        # 转化为客户后，在首页进行验证

    def test_ClueShift(self):
        """线索转移"""
        self.test_1_AddNewClue()
        self.appApi.ConsultantList()
        self.appApi.ClueChange()        # 线索转移
        self.appApi.TodayClue(keyWord=self.appText.get('cluePhone'))         # 转移后查看自己的列表
        # 登陆转移后账号进行查看
        self.assertEqual(0, self.appText.get('Total'))
        self.appApi.Login(userName=XfpUser1, password=XfpPwd1)
        self.appApi.TodayClue(keyWord=self.appText.get('cluePhone'))
        self.assertEqual(1, self.appText.get('Total'))

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
            self.appApi.GetLabelList(labelNo='XSLY', labelName='幸福派总部')
            self.webApi.add_clue_admin(clueNickName=self.appApi.RandomText(textArr=surname))
            self.appApi.Login()
            self.appApi.my_clue_list()
            self.appApi.ClueInfo()
            self.appApi.GetLabelList(labelNo='XSLY', labelName='百度小程序')
            self.appApi.ClueSave(Status=2,
                                 clueNickName=self.appApi.RandomText(textArr=surname),
                                 sourceId=self.appText.get('labelId'))
            self.assertNotEqual(200, self.appText.get('code'))
            self.assertEqual('总部分配过来的线索,线索来源不能修改', self.appText.get('data'))

    # def test_1_AddNewClue1(self):
    #     """新增一条线索"""
    #     self.webApi.clue_list(myClue='N', vlue=12)
    #     self.appApi.ClueInfo()
    #     self.appApi.ClueFollowList()
    #     dome = self.appText.get('total')
    #     dome1 = 1
    #     dome2 = self.appApi.appText.get('cluePhone')
    #     while dome != 0:
    #         dome = dome - 1
    #         self.appApi.Login()
    #         time.sleep(1)
    #         self.webApi.clue_list(myClue='N', vlue=12)
    #         self.appApi.ClueFollowList(value=dome)
    #         test = self.appText.get('followContent')
    #         print(self.appText.get('followContent'))
    #         self.appApi.Login(userName='13000000005', saasCode='000006')     # 登录咨询师B
    #         self.appApi.GetUserData()
    #         if dome1 == 1:
    #             self.appApi.GetLabelList(labelNo='XSLY', labelName='百度小程序', saasCode='000006')
    #             if self.appText.get('labelId') is None:
    #                 self.webApi.add_label(labelName='百度小程序', labelId=self.appText.get('LabelId'),
    #                                       pid=self.appText.get('LabelId'), saasCode='000006')
    #                 self.appApi.GetLabelList(labelNo='XSLY', labelName='百度小程序', saasCode='000006')
    #             self.appApi.GetUserLabelList(userLabelType='线索标签', saasCode='000006')
    #             if self.appText.get('total') == 0:
    #                 self.appApi.AddUserLabel(saasCode='000006')
    #                 self.appApi.GetUserLabelList(userLabelType='线索标签', saasCode='000006')
    #             self.appApi.ClueSave(clueNickName=self.appApi.RandomText(textArr=surname),
    #                                  sourceId=self.appText.get('labelId'),
    #                                  keyWords=self.appText.get('labelData'),
    #                                  cluePhone=dome2, saasCode='000006')
    #
    #         else:
    #             self.appApi.my_clue_list(saasCode='000006')
    #             self.appApi.ClueFollowList(saasCode='000006')
    #             time.sleep(2)
    #             self.appApi.ClueFollowSave(taskEndTime=time.strftime("%Y-%m-%d %H:%M:%S"),
    #                                        followContent=test,
    #                                        taskRemark=test, saasCode='000006')
    #         dome1 = dome1 + 1
    #
    # def test_002(self):
    #     """11"""
    #     # self.appApi.Login(userName='13726224607', password='12345678', saasCode='000010')
    #     self.appApi.GetLabelList(labelNo='XSLY', labelName='百度小程序')
    #     if self.appText.get('labelId') is None:
    #         self.webApi.add_label(labelName='百度小程序', labelId=self.appText.get('LabelId'),
    #                               pid=self.appText.get('LabelId'))
    #         self.appApi.GetLabelList(labelNo='XSLY', labelName='百度小程序')
    #     self.appApi.GetUserLabelList(userLabelType='线索标签')
    #     if self.appText.get('total') == 0:
    #         self.appApi.AddUserLabel()
    #         self.appApi.GetUserLabelList(userLabelType='线索标签')
    #     dome = 0
    #     while dome != 20:
    #         self.appApi.ClueSave(clueNickName=self.appApi.RandomText(textArr=surname),
    #                              sourceId=self.appText.get('labelId'),
    #                              keyWords=self.appText.get('labelData'))
    #
    #         self.appApi.my_clue_list()
    #         self.appApi.ClueFollowList()
    #         self.appApi.ClueFollowSave(taskEndTime=time.strftime("%Y-%m-%d") + ' 22:00:00')
    #         self.appApi.my_clue_list()
    #         self.appApi.ClueInfo()
    #         self.appApi.ClientEntering(callName=self.appApi.RandomText(textArr=surname),
    #                                    loanSituation='这个是贷款情况')
    #         dome = dome + 1

    # def test_003(self):
    #     """总部新增线索并分派"""
    #     self.appApi.Login()
    #     self.webApi.add_clue_admin(clueNickName=self.appApi.RandomText(textArr=surname))



