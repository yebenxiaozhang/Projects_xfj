# -*- coding: utf-8 -*-
# @Time    : 2020/3/30 20:47
# @Author  : 潘师傅
# @File    : Client_case.py

"""线索相关"""
from XFP.PubilcAPI.flowPath import *
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
        # 财富值类型
        cls.appApi.GetLabelList(labelNo='CFZLX', labelName='首电及时率', saasCode='admin')
        cls.appText.set_map('SDJSL', cls.appText.get('remark'))

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
        self.assertIn('将线索指派至', self.appText.get('followContent'))

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
