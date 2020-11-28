# -*- coding: utf-8 -*-
# @Time    : 2020/3/21 11:08
# @Author  : 潘师傅
# @File    : Client_casc.py

"""客户相关"""
from XFP.PubilcAPI.flowPath import *


class ClientTestCase(unittest.TestCase):
    """客第壹——客户"""

    def __init__(self, *args, **kwargs):
        super(ClientTestCase, self).__init__(*args, **kwargs)
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
        while cls.appText.get('total') >= 5:
            cls.flowPath.clue_exile_sea()
            cls.appApi.my_clue_list()

        cls.appApi.ClientList()
        while cls.appText.get('total') >= 5:
            cls.appApi.client_exile_sea()
            cls.appApi.ClientList()

    def test_FollowSave(self):
        """客户跟进"""
        try:
            #  客户详情查看  及 列表是否有新增
            self.flowPath.client_list_non_null()
            self.appApi.ClientFollowList()
            self.appApi.ClueFollowSave(followType='客户', taskEndTime=time.strftime("%Y-%m-%d") + ' 22:00:00')
            self.appApi.ClientFollowList()
            try:
                self.assertEqual('python-线索/客户跟进，本次沟通记录', self.appText.get('followContent'))
            except BaseException as e:
                print("断言错误，错误原因：%s" % e)
                self.appApi.ClientFollowList(value=1)
                self.assertEqual('python-线索/客户跟进，本次沟通记录', self.appText.get('followContent'))
        except BaseException as e:
            print("断言错误，错误原因：%s" % e)
            raise RuntimeError(self.appText.get('ApiXfpUrl'))

    def test_SettingTakeLook(self):
        """设定带看计划"""
        self.flowPath.add_visit()
        self.assertEqual(self.appApi.appText.get('code'), 200)

    def test_CompleteSettingTakeLook(self):
        """完成带看计划"""
        try:
            self.flowPath.add_visit()
            self.appApi.ClientTask(taskType='3')
            if self.appText.get('total') < 1:
                raise RuntimeError(self.appText.get('ApiXfpUrl'))
            self.appApi.visit_info()
            self.appApi.VisitFlow1(agencyId=self.appApi.appText.get('DLGS'),
                                   receptionName=self.appApi.RandomText(textArr=surname),
                                   receptionPhone='1' + str(int(time.time())), attachmentIds='1')
            self.appApi.ClientTask()
            if self.appText.get('total') >= 2:
                raise RuntimeError(self.appText.get('ApiXfpUrl'))

        except BaseException as e:
            print("断言错误，错误原因：%s" % e)
            raise RuntimeError(self.appText.get('ApiXfpUrl'))

    def test_advance_over_visit(self):
        """取消带看"""
        try:
            self.flowPath.add_visit()
            self.flowPath.advance_over_visit()
            self.appApi.ClientTask()
            self.appApi.ClientFollowList()
            self.assertEqual('取消带看', self.appText.get('followContent')[-4:])
        except BaseException as e:
            print("断言错误，错误原因：%s" % e)
            raise RuntimeError(self.appText.get('ApiXfpUrl'))

    def test_AddAgreement(self):
        """录入成交"""
        try:
            self.appApi.deal_List()
            dome = self.appText.get('total')
            self.flowPath.client_list_non_null()
            self.flowPath.add_deal()
            self.appApi.deal_List()
            self.assertNotEqual(dome, self.appText.get('total'))
        except BaseException as e:
            print("断言错误，错误原因：%s" % e)
            raise RuntimeError(self.appText.get('ApiXfpUrl'))

    def test_SuspendFollow(self):
        """暂停跟进"""
        try:
            self.flowPath.suspend_follow()
            self.appApi.ClientTask(taskType=2)       # 待办
            self.assertEqual('2', self.appText.get('taskType'))
        except BaseException as e:
            print("断言错误，错误原因：%s" % e)
            raise RuntimeError(self.appText.get('ApiXfpUrl'))

    def test_client_change(self):
        """客户转移"""
        self.flowPath.client_list_non_null()
        self.appApi.ClientFollowList()
        dome = self.appText.get('total')
        self.appApi.client_change()
        self.appApi.Login(userName=XfpUser1)
        self.appApi.GetUserData()
        self.appApi.ClientList()
        self.appApi.ClientFollowList()
        self.assertEqual('客户转移', self.appText.get('followContent')[:4])
        if self.appText.get('total') != dome + 1:
            raise RuntimeError('客户转移后跟进记录的条数与转移前不一致')




