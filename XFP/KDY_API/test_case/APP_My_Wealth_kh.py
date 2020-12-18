# -*- coding: utf-8 -*-
# @Time    : 2020/3/21 11:08
# @Author  : 潘师傅
# @File    : My_Wealth_casc.py

"""客户-财富值相关"""
from XFP.PubilcAPI.flowPath import *
"""
带看相关
    1、准时完成带看        增加财富值
    2、超时完成带看        增加财富值并且扣除超时财富值
    3、取消带看            无变化
录入成交
    1、录入成交              审核成功后增加财富值
    2、修改成交              审核成功财富值无变化   
"""


class TestCase(unittest.TestCase):
    """客第壹——财富值相关"""

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
        cls.webApi.auditList()
        while cls.appApi.appText.get('web_total') != 0:
            cls.webApi.audit(auditStatue=2, auditRemark=' 审核失败')
            cls.webApi.auditList()
        cls.webApi.auditList(auditLevel=2)
        while cls.appApi.appText.get('web_total') != 0:
            cls.webApi.audit(auditStatue=2, auditRemark=' 审核失败')
            cls.webApi.auditList(auditLevel=2)

    def test_Wealth_01(self):
        """1、准时完成带看        增加财富值"""
        self.flowPath.add_visit()
        self.appApi.getWealthDetailList(startTime=time.strftime("%Y-%m-%d"),
                                        endTime=time.strftime("%Y-%m-%d"),
                                        wealthType=self.appText.get('YYDK'),
                                        orderNo=self.appText.get('orderNo'))
        dome = self.appText.get('vlue')
        self.flowPath.accomplish_visit()
        self.appApi.getWealthDetailList(startTime=time.strftime("%Y-%m-%d"),
                                        endTime=time.strftime("%Y-%m-%d"),
                                        wealthType=self.appText.get('YYDK'),
                                        orderNo=self.appText.get('orderNo'))
        if self.appText.get('vlue') != dome + 50:
            raise RuntimeError('及时完成带看没有加财富值')

    def test_Wealth_02(self):
        """2、超时完成带看        增加财富值并且扣除超时财富值"""
        dome1 = (datetime.datetime.now()+datetime.timedelta(days=-3)).strftime("%Y-%m-%d %H:%M:%S")
        self.flowPath.add_visit(dome=dome1)
        self.appApi.getWealthDetailList(startTime=time.strftime("%Y-%m-%d"),
                                        endTime=time.strftime("%Y-%m-%d"),
                                        wealthType=self.appText.get('YYDK'),
                                        orderNo=self.appText.get('orderNo'))
        dome = self.appText.get('vlue')
        self.appApi.ClientTask(taskType='3')
        if self.appApi.appText.get('total') < 1:
            raise RuntimeError(self.appApi.appText.get('ApiXfpUrl'))
        self.appApi.visit_info()

        self.appApi.VisitFlow1(agencyId=self.appApi.appText.get('DLGS'),
                               receptionName=self.appApi.RandomText(textArr=surname),
                               houseId=self.appApi.appText.get('houseId'),
                               receptionPhone='1' + str(int(time.time())))
        self.appApi.getWealthDetailList(startTime=time.strftime("%Y-%m-%d"),
                                        endTime=time.strftime("%Y-%m-%d"),
                                        wealthType=self.appText.get('YYDK'),
                                        orderNo=self.appText.get('orderNo'))
        if self.appText.get('vlue') != dome + 30:
            raise RuntimeError('2、超时完成带看奖励财富值与扣除财富值不之和不对')

    def test_Wealth_03(self):
        """3、取消带看            无变化"""
        self.flowPath.add_visit()
        self.appApi.getWealthDetailList(startTime=time.strftime("%Y-%m-%d"),
                                        endTime=time.strftime("%Y-%m-%d"),
                                        wealthType=self.appText.get('YYDK'),
                                        orderNo=self.appText.get('orderNo'))
        dome = self.appText.get('vlue')
        self.flowPath.advance_over_visit()
        self.appApi.getWealthDetailList(startTime=time.strftime("%Y-%m-%d"),
                                        endTime=time.strftime("%Y-%m-%d"),
                                        wealthType=self.appText.get('YYDK'),
                                        orderNo=self.appText.get('orderNo'))
        if self.appText.get('vlue') != dome:
            raise RuntimeError('及时完成带看没有加财富值')

    def test_Wealth_04(self):
        """1、录入成交              审核成功后增加财富值"""
        self.flowPath.client_list_non_null()
        self.appApi.getWealthDetailList(startTime=time.strftime("%Y-%m-%d"),
                                        endTime=time.strftime("%Y-%m-%d"),
                                        wealthType=self.appText.get('CJJL'),
                                        orderNo=self.appText.get('orderNo'))
        dome = self.appText.get('vlue')
        self.flowPath.add_visit()
        self.flowPath.accomplish_visit()
        self.appApi.visitProject_list()
        self.appApi.add_deal()
        self.appApi.getWealthDetailList(startTime=time.strftime("%Y-%m-%d"),
                                        endTime=time.strftime("%Y-%m-%d"),
                                        wealthType=self.appText.get('CJJL'),
                                        orderNo=self.appText.get('orderNo'))
        if self.appText.get('vlue') != int(dome):
            raise RuntimeError('录入成交后财务还没审核 加财富值？')

        """财务审核"""
        self.webApi.finance_deal_auditList(keyWord=self.appText.get('dealPhone'))
        self.webApi.finance_deal_audit()
        self.appApi.getWealthDetailList(startTime=time.strftime("%Y-%m-%d"),
                                        endTime=time.strftime("%Y-%m-%d"),
                                        wealthType=self.appText.get('CJJL'),
                                        orderNo=self.appText.get('orderNo'))
        if self.appText.get('vlue') != int(dome) + 5000:
            print('录入成交前财富值' + dome)
            print('录入成交后财富值' + self.appText.get('vlue'))
            raise RuntimeError('录入成交与设定成交值不符预设值')

        """2、修改成交              审核成功财富值无变化   """
        dome = self.appText.get('vlue')
        self.appApi.deal_List()
        self.webApi.detail()
        self.appApi.add_deal(Status=1, transTotalPrice='1000000')
        self.appApi.getWealthDetailList(startTime=time.strftime("%Y-%m-%d"),
                                        endTime=time.strftime("%Y-%m-%d"),
                                        wealthType=self.appText.get('CJJL'),
                                        orderNo=self.appText.get('orderNo'))
        if self.appText.get('vlue') != dome:
            raise RuntimeError('修改成交单不添加财富值')

        self.webApi.finance_deal_auditList(keyWord=self.appText.get('dealPhone'))
        self.webApi.finance_deal_audit()


