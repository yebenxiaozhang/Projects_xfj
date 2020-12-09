# # -*- coding: utf-8 -*-
# # @Time    : 2020/3/30 20:47
# # @Author  : 潘师傅
# # @File    : Client_case.py
#
# """线索相关"""
# from XFP.PubilcAPI.flowPath import *
# # 通过总部分配的线索不允许修改来源
#
#
# class ClueTestCase(unittest.TestCase):
#     """幸福派APP——线索"""
#
#     def __init__(self, *args, **kwargs):
#         super(ClueTestCase, self).__init__(*args, **kwargs)
#         self.xfp_web = webApi()
#         self.webApi = self.xfp_web
#
#         self.xfp_app = appApi()
#         self.appApi = self.xfp_app
#
#         self.flow = flowPath()
#         self.flowPath = self.flow
#
#         self.appText = GlobalMap()
#         self.webText = GlobalMap()
#
#     @classmethod
#     def setUpClass(cls):
#         """登录幸福派 只执行一次
#         登录经纪人 获取ID"""
#         cls.do_request = appApi()
#         cls.appApi = cls.do_request
#         cls.appApi.Login()
#         cls.appApi.GetUserData()
#         cls.request = webApi()
#         cls.webApi = cls.request
#         cls.webApi.Audit_management()
#         cls.flow = flowPath()
#         cls.flowPath = cls.flow
#         cls.appText = GlobalMap()
#         """线索来源"""
#         cls.flowPath.get_label(labelNo='XSLY', labelName='线索来源',
#                                newlabelName='百度小程序')
#         cls.appText.set_map('XSLY', cls.appText.get('labelId'))
#
#         """线索来源_幸福派总部"""
#         cls.flowPath.get_label(labelNo='XSLY', labelName='线索来源',
#                                newlabelName='幸福派总部')
#         cls.appText.set_map('XSLY_admin', cls.appText.get('labelId'))
#         """线索标签"""
#         cls.appApi.GetUserLabelList(userLabelType='线索标签')
#         if cls.appText.get('total') == 0:
#             cls.appApi.AddUserLabel()
#             cls.appApi.GetUserLabelList(userLabelType='线索标签')
#         cls.appText.set_map('XSBQ', cls.appText.get('labelData'))
#         """终止跟进"""
#         cls.flowPath.get_label(labelNo='SZGJYY', labelName='终止跟进原因',
#                                newlabelName='客户已成交')
#         cls.appText.set_map('ZZGJ', cls.appText.get('labelId'))
#         """成交项"""
#         cls.flowPath.get_label(labelNo='CJX', labelName='成交项目',
#                                newlabelName='认购')
#         cls.appText.set_map('CJX', cls.appText.get('labelId'))
#         """出行方式"""
#         cls.flowPath.get_label(labelNo='CXFS', labelName='出行方式',
#                                newlabelName='自驾')
#         cls.appText.set_map('CXFS', cls.appText.get('labelId'))
#         """客户意向等级"""
#         cls.appApi.GetLabelList(labelNo='KHYXDJ')                       # 查询购房意向loanSituation
#         cls.appText.set_map('KHYXDJ', cls.appText.get('labelId'))
#         cls.appApi.GetLabelList(labelNo='ZJZZ')                         # 查询资金资质
#         cls.appText.set_map('ZJZZ', cls.appText.get('labelId'))
#         cls.appApi.GetLabelList(labelNo='GFMD')                         # 查询购房目的
#         cls.appText.set_map('GFMD', cls.appText.get('labelId'))
#         cls.appApi.GetLabelList(labelNo='WYSX')                         # 查询物业属性
#         cls.appText.set_map('WYSX', cls.appText.get('labelId'))
#         cls.appApi.GetLabelList(labelNo='GFZZ')                         # 查询购房资质
#         cls.appText.set_map('GFZZ', cls.appText.get('labelId'))
#         cls.appApi.GetLabelList(labelNo='SFSTF')                        # 查询是否首套
#         cls.appText.set_map('SFSTF', cls.appText.get('labelId'))
#         cls.appApi.GetMatchingArea()                                    # 查询匹配区域
#         cls.appApi.GetMatchingAreaHouse()                               # 匹配楼盘
#         cls.appApi.GetLabelList(labelNo='QTKHXQ')                       # 查询客户需求
#         cls.appText.set_map('QTKHXQ', cls.appText.get('labelId'))
#         cls.appApi.ConsultantList()                                     # 咨询师列表
#         cls.appApi.GetLabelList(labelNo='SQZHGJ', labelName='其他')
#         cls.appText.set_map('ZHGJ', cls.appText.get('labelId'))         # 暂缓跟进
#         cls.flowPath.get_label(labelNo='XXFL', labelName='信息分类',
#                                newlabelName='信息分类一')
#         cls.appText.set_map('XXFL', cls.appText.get('labelId'))         # 信息分类
#         cls.flowPath.get_label(labelNo='DLGS', labelName='代理公司',
#                                newlabelName='代理公司一')
#         cls.appText.set_map('DLGS', cls.appText.get('labelId'))         # 代理公司
#         cls.flowPath.get_label(labelNo='WDFL', labelName='问答分类',
#                                newlabelName='问答分类一')
#         cls.appText.set_map('WDFL', cls.appText.get('labelId'))         # 问答分类
#
#     def test_1_AddNewClue(self):
#         """新增一条线索"""
#         try:
#             self.appApi.ClueSave(clueNickName=self.appApi.RandomText(textArr=surname),
#                                  sourceId=self.appText.get('XSLY'),
#                                  keyWords=self.appText.get('XSBQ'))
#             # 在搜索列表进行查找
#             globals()['cluePhone'] = self.appText.get('cluePhone')
#             self.appApi.ClueList(keyWord=(self.appText.get('cluePhone')))
#             self.assertEqual(self.appText.get('cluePhone'), globals()['cluePhone'])
#             """今日上户上进行查看"""
#             self.appApi.TodayClue()
#             dome1 = 0
#             globals()['r.text'] = json.loads(json.dumps(self.appText.get('records')))
#             while globals()['r.text'][dome1]['clueId'] != self.appText.get('clueId'):
#                 dome1 = dome1 + 1
#             self.assertEqual('0', globals()['r.text'][dome1]['isFirst'])
#             time.sleep(1)
#             # self.test_4_ExileSea()
#         except BaseException as e:
#                 print("错误，错误原因：%s" % e)
#                 raise RuntimeError(self.appText.get('ApiXfpUrl'))
#
#     def test_2_FollowClue(self):
#         """跟进线索"""
#         self.appApi.my_clue_list()
#         self.appApi.ClueFollowList()
#         self.appApi.ClueFollowSave(taskEndTime=time.strftime("%Y-%m-%d") + ' 22:00:00')
#         time.sleep(1)
#         self.appApi.ClueFollowList()
#         try:
#             self.assertEqual('python-线索/客户跟进，本次沟通记录', self.appText.get('followContent'))
#             """查看今日上户是否已首电"""
#         except BaseException as e:
#             print("断言错误，错误原因：%s" % e)
#             self.appApi.ClueFollowList(value=1)
#             self.assertEqual('python-线索/客户跟进，本次沟通记录', self.appText.get('followContent'))
#
#     def test_3_AlterClueMessage(self):
#         """修改线索信息"""
#         self.flowPath.clue_non_null()
#         self.appApi.my_clue_list()
#         globals()['cluePhone'] = self.appText.get('cluePhone')
#         self.appApi.ClueSave(Status=2,
#                              clueNickName=self.appApi.RandomText(textArr=surname),
#                              sourceId=self.appText.get('XSLY'), keyWords=self.appText.get('XSBQ'))
#         self.appApi.ClueInfo()
#         self.assertNotEqual(globals()['cluePhone'], self.appText.get('cluePhone'))
#
#     def test_4_ExileSea(self):
#         """流放公海"""
#         self.flowPath.clue_non_null()
#         self.appApi.my_clue_list()
#         self.appApi.ExileSea()
#         # 流放公海 在首页进行验证
#         self.appApi.GetUserAgenda(keyWord=self.appText.get('cluePhone'))
#         # 跟进进行验证
#         self.appApi.ClueFollowList()
#         self.assertEqual(self.appText.get('followContent')[:6], '线索流放公海')
#
#     def test_ChangeClient(self):
#         """线索转为客户"""
#         self.flowPath.clue_non_null()
#         self.appApi.my_clue_list()
#         self.appApi.ClueFollowList()
#         self.appApi.ClueFollowSave(taskEndTime=time.strftime("%Y-%m-%d") + ' 22:00:00')
#         self.appApi.ClueInfo()
#         self.appApi.ClientEntering(callName=self.appApi.RandomText(textArr=surname),
#                                    loanSituation='这个是贷款情况')
#         self.assertEqual(200, self.appText.get('code'))
#         # 转化为客户后，在首页进行验证
#
#     def test_ClueShift(self):
#         """线索转移"""
#         self.test_1_AddNewClue()
#         self.appApi.Login(userName=XfpUser1, password=XfpPwd1)
#         self.appApi.GetUserData()
#         self.appApi.my_clue_list()         # 转移后查看自己的列表
#         dome1 = self.appText.get('total')
#         self.appApi.Login()
#         self.appApi.GetUserData()
#         self.appApi.my_clue_list()         # 转移后查看自己的列表
#         dome = self.appText.get('total')
#         self.appApi.ClueChange()        # 线索转移
#         self.appApi.my_clue_list()         # 转移后查看自己的列表
#         self.assertEqual(dome-1, self.appText.get('total'))
#         # 登陆转移后账号进行查看
#         self.appApi.Login(userName=XfpUser1, password=XfpPwd1)
#         self.appApi.my_clue_list()
#         self.assertEqual(dome1 + 1, self.appText.get('total'))
#         self.appApi.ClueFollowList()
#         self.assertEqual('线索转移', self.appText.get('followContent')[:4])
#
#     def test_clue_ChangeClient(self):
#         """未首电转客户"""
#         self.appApi.SeaList()  # 公海列表
#         self.appApi.clue_Assigned()  # 领取线索
#         self.appApi.my_clue_list()
#         self.appApi.ClueInfo()
#         self.appApi.ClientEntering(callName=self.appApi.RandomText(textArr=surname),
#                                    loanSituation='这个是贷款情况')
#         self.assertNotEqual(200, self.appText.get('code'))
#         self.assertEqual('该线索未首电,不能转为客户!', self.appText.get('data'))
#
#     def test_admin_clue(self):
#         """通过总部分配的线索不允许修改来源"""
#         if ApiXfpUrl == 'http://xfp.xfj100.com':
#             pass
#         else:
#             self.appApi.Login(userName='admin', saasCode='admin')
#             self.webApi.add_clue_admin(clueNickName=self.appApi.RandomText(textArr=surname))
#             self.appApi.Login()
#             self.appApi.my_clue_list()
#             self.appApi.ClueInfo()
#             self.appApi.ClueSave(Status=2,
#                                  clueNickName=self.appApi.RandomText(textArr=surname),
#                                  sourceId=self.appText.get('XSLY'))
#             self.assertNotEqual(200, self.appText.get('code'))
#             self.assertEqual('总部分配过来的线索,线索来源不能修改', self.appText.get('data'))
#
#
#     # def test_002(self):
#     #     """11"""
#     #     # self.appApi.Login(userName='13726224607', password='12345678', saasCode='000010')
#     #     # self.appApi.GetLabelList(labelNo='XSLY', labelName='百度小程序')
#     #     # if self.appText.get('labelId') is None:
#     #     #     self.webApi.add_label(labelName='百度小程序', labelId=self.appText.get('LabelId'),
#     #     #                           pid=self.appText.get('LabelId'))
#     #     #     self.appApi.GetLabelList(labelNo='XSLY', labelName='百度小程序')
#     #     # self.appApi.GetUserLabelList(userLabelType='线索标签')
#     #     # if self.appText.get('total') == 0:
#     #     #     self.appApi.AddUserLabel()
#     #     #     self.appApi.GetUserLabelList(userLabelType='线索标签')
#     #     dome = 0
#     #     while dome != 10:
#     #         self.appApi.ClueSave(clueNickName=self.appApi.RandomText(textArr=surname),
#     #                              sourceId=self.appText.get('labelId'),
#     #                              keyWords=self.appText.get('labelData'))
#     #
#     #         # self.appApi.my_clue_list()
#     #         # self.appApi.ClueFollowList()
#     #         # self.appApi.ClueFollowSave(taskEndTime=time.strftime("%Y-%m-%d") + ' 22:00:00')
#     #         # self.appApi.my_clue_list()
#     #         # self.appApi.ClueInfo()
#     #         # self.appApi.ClientEntering(callName=self.appApi.RandomText(textArr=surname),
#     #         #                            loanSituation='这个是贷款情况')
#     #         # self.appApi.ClientList()
#     #         # self.flowPath.add_visit()
#     #         # dome = dome + 1
#
# residentInfo = '0313+11111111111'
#
# dome = 1
# while residentInfo[0:dome] == '+':
#     print(dome)
#     dome = dome + 1

# import time
# NowYear = time.localtime()[0]
# NowMonth = time.localtime()[1]
# LastMonth = NowMonth - 1
# if NowMonth == 1:
#     LastMonth = 12
#     NowYear = NowYear - 1
# result = "%s-%s-%d" % (NowYear, LastMonth, 1)
# TimeStamp=time.mktime(time.strptime(result, '%Y-%m-%d'))    # 日期转换为时间戳
# LocalTime = time.localtime(TimeStamp)   # 将日期时间戳转换为localtime
# print(time.strftime('%Y-%m-%d', LocalTime))

import time
import datetime

# 先获得时间数组格式的日期
threeDayAgo = (datetime.datetime.now() - datetime.timedelta(days=60))
# 转换为时间戳
timeStamp = int(time.mktime(threeDayAgo.timetuple()))
# 转换为其他字符串格式
otherStyleTime = threeDayAgo.strftime("%Y-%m-%d 00:00:00")
print(otherStyleTime)