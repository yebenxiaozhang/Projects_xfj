# -*- coding: utf-8 -*-
# @Time    : 2020/9/1 16:25
# @Author  : 潘师傅
# @File    : Houses_casc.py

from XFP.PubilcAPI.flowPath import *
"""楼盘相关"""


class HousesTestCase(unittest.TestCase):
    """幸福派APP——楼盘相关"""

    def __init__(self, *args, **kwargs):
        super(HousesTestCase, self).__init__(*args, **kwargs)
        self.xfp_web = webApi()
        self.web_api = self.xfp_web

        self.xfp_app = appApi()
        self.app_api = self.xfp_app

        self.flow = flowPath()
        self.flowPath = self.flow

        self.appText = GlobalMap()
        self.webText = GlobalMap()

    @classmethod
    def setUpClass(cls):
        """登录幸福派 只执行一次"""
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

    def test_AllBuildingUpdate(self):
        """全部楼盘"""
        try:
            self.app_api.AllBuildingUpdate()
            globals()['total'] = self.appText.get('total')
            self.app_api.AllBuildingUpdate(keyWord='ABCDEFG')
            self.assertNotEqual(globals()['total'], self.appText.get('total'))
        except BaseException as e:
                print("错误，错误原因：%s" % e)
                raise RuntimeError(self.appText.get('ApiXfpUrl'))

    def test_BusinessInformation(self):
        """商务信息"""
        try:
            self.app_api.BusinessInformation()
            globals()['total'] = self.appText.get('total')
            self.app_api.BusinessInformation(keyWord='ABCDEFG')
            self.assertNotEqual(globals()['total'], self.appText.get('total'))
        except BaseException as e:
            print("错误，错误原因：%s" % e)
            raise RuntimeWarning(self.appText.get('ApiXfpUrl'))

    def test_Information(self):
        """资料信息"""
        try:
            self.app_api.Information()
            globals()['total'] = self.appText.get('total')
            self.app_api.Information(keyWord='ABCDEFG')
            self.assertNotEqual(globals()['total'], self.appText.get('total'))
        except BaseException as e:
            print("错误，错误原因：%s" % e)
            raise RuntimeWarning(self.appText.get('ApiXfpUrl'))

    def test_HouseQA(self):
        """楼盘QA"""
        try:
            self.app_api.HouseQA()
            globals()['total'] = self.appText.get('total')
            self.app_api.HouseQA(keyWord='ABCDEFG')
            self.assertNotEqual(globals()['total'], self.appText.get('total'))
        except BaseException as e:
            print("错误，错误原因：%s" % e)
            raise RuntimeWarning(self.appText.get('ApiXfpUrl'))


