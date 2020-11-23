# -*- coding: utf-8 -*-
# @Time    : 2020/3/21 11:08
# @Author  : 潘师傅
# @File    : My_Wealth_casc.py

"""客户相关"""
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
    """客第壹——客户列表"""

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
        cls.appApi.GetLabelList(labelNo='CFZLX', labelName='成交奖励', saasCode='admin')
        cls.appText.set_map('CJJL', cls.appText.get('remark'))
        cls.appApi.GetLabelList(labelNo='CFZLX', labelName='邀约带看', saasCode='admin')
        cls.appText.set_map('YYDK', cls.appText.get('remark'))

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
        self.appApi.add_deal()
        self.appApi.getWealthDetailList(startTime=time.strftime("%Y-%m-%d"),
                                        endTime=time.strftime("%Y-%m-%d"),
                                        wealthType=self.appText.get('CJJL'),
                                        orderNo=self.appText.get('orderNo'))
        if self.appText.get('vlue') != dome + 5000:
            raise RuntimeError('录入成交与设定成交值不符预设值：5000' + '计算值：' + self.appText.get('vlue'))
        """2、修改成交              审核成功财富值无变化   """
        dome = self.appText.get('vlue')
        self.appApi.deal_List()
        self.appApi.add_deal(Status=1, transTotalPrice='1000000')
        self.appApi.getWealthDetailList(startTime=time.strftime("%Y-%m-%d"),
                                        endTime=time.strftime("%Y-%m-%d"),
                                        wealthType=self.appText.get('CJJL'),
                                        orderNo=self.appText.get('orderNo'))
        if self.appText.get('vlue') != dome:
            raise RuntimeError('修改成交单不添加财富值')



