# -*- coding: utf-8 -*-
# @Time    : 2020/9/1 16:25
# @Author  : 潘师傅
# @File    : Houses_casc.py

from XFP.PubilcAPI.webApi import *
"""楼盘相关"""


class HousesTestCase(unittest.TestCase):
    """幸福派APP——楼盘相关"""

    def __init__(self, *args, **kwargs):
        super(HousesTestCase, self).__init__(*args, **kwargs)
        self.xfp_web = webApi()
        self.web_api = self.xfp_web

        self.xfp_app = appApi()
        self.app_api = self.xfp_app

        self.appText = GlobalMap()
        self.webText = GlobalMap()

    @classmethod
    def setUpClass(cls):
        """登录幸福派 只执行一次"""
        cls.do_request = appApi()
        cls.Request = cls.do_request
        cls.Request.Login()

    def test_AllBuildingUpdate(self):
        """全部楼盘"""
        try:
            self.app_api.AllBuildingUpdate()
            if self.appText.get('total') == 0:
                self.app_api.GetLabelList(labelNo='XXFL', labelName='信息分类一')
                if self.appText.get('labelId') is not None:
                    pass        # 存在标签---不创建
                else:
                    self.web_api.add_label(labelName='信息分类一', labelId=self.appText.get('LabelId'),
                                           pid=self.appText.get('LabelId'))
                    self.app_api.GetLabelList(labelNo='XXFL', labelName='信息分类一')
                self.web_api.house_list()
                self.assertEqual(self.webText.get('total'), 0)
                self.web_api.add_house(houseName='项目' + time.strftime("%Y-%m-%d"))
                self.web_api.house_list()
                self.assertNotEqual(self.webText.get('total'), 0)
                self.web_api.add_house_data(data='这是楼盘内容')
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
            if self.appText.get('total') == 0:
                self.app_api.GetLabelList(labelNo='DLGS', labelName='代理公司一')
                if self.appText.get('labelId') is not None:
                    pass        # 存在标签---不创建
                else:
                    self.web_api.add_label(labelName='代理公司一', labelId=self.appText.get('LabelId'),
                                           pid=self.appText.get('LabelId'))
                    self.app_api.GetLabelList(labelNo='DLGS', labelName='代理公司一')
                self.web_api.house_list()
                if self.webText.get('total') == 0:
                    self.web_api.add_house(houseName='项目' + time.strftime("%Y-%m-%d"))
                    self.web_api.house_list()
                self.web_api.add_house_business_information()
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
            if self.appText.get('total') == 0:
                self.app_api.GetLabelList(labelNo='XXFL', labelName='信息分类一')
                if self.appText.get('labelId') is not None:
                    pass        # 存在标签---不创建
                else:
                    self.web_api.add_label(labelName='信息分类一', labelId=self.appText.get('LabelId'),
                                           pid=self.appText.get('LabelId'))
                    self.app_api.GetLabelList(labelNo='XXFL', labelName='信息分类一')
                self.web_api.house_list()
                if self.webText.get('total') == 0:
                    self.web_api.add_house(houseName='项目' + time.strftime("%Y-%m-%d"))
                    self.web_api.house_list()
                self.assertNotEqual(self.webText.get('total'), 0)
                self.web_api.add_house_data(data='这是楼盘内容')
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
            if self.appText.get('total') == 0:
                self.app_api.GetLabelList(labelNo='WDFL', labelName='问答分类一')
                if self.appText.get('labelId') is not None:
                    pass  # 存在标签---不创建
                else:
                    self.web_api.add_label(labelName='问答分类一', labelId=self.appText.get('LabelId'),
                                           pid=self.appText.get('LabelId'))
                    self.app_api.GetLabelList(labelNo='WDFL', labelName='问答分类一')
                self.web_api.house_list()
                if self.webText.get('total') == 0:
                    self.web_api.add_house(houseName='项目' + time.strftime("%Y-%m-%d"))
                    self.web_api.house_list()
                self.web_api.add_house_questions()
                self.app_api.HouseQA()
            globals()['total'] = self.appText.get('total')
            self.app_api.HouseQA(keyWord='ABCDEFG')
            self.assertNotEqual(globals()['total'], self.appText.get('total'))
        except BaseException as e:
            print("错误，错误原因：%s" % e)
            raise RuntimeWarning(self.appText.get('ApiXfpUrl'))

    def test_Rank(self):
        """各个列表验证排序"""
        self.app_api.AllBuildingUpdate()
        globals()['r.text'] = self.appText.get('records')
        a = 0
        while a != 3:
            globals()['a'] = 0
            while globals()['r.text'][globals()['a']]['houseType'] != a:
                time.sleep(0.1)
                globals()['a'] = globals()['a'] + 1
            if a == 0:
                self.app_api.BusinessInformation(
                    keyWord=globals()['r.text'][globals()['a']]['saasHouseBusinessInfoVo']['houseName'])
                self.assertEqual(globals()['r.text'][globals()['a']]['saasHouseBusinessInfoVo']['houseName'],
                                 self.appText.get('houseName'))
            elif a == 1:
                if globals()['a'] > 30:
                    pass
                else:
                    self.app_api.Information(keyWord=globals()['r.text'][globals()['a']]['saasHouseInfo']['houseName'])
                    self.assertEqual(globals()['r.text'][globals()['a']]['saasHouseInfo']['houseName'],
                                     self.appText.get('houseName'))
            elif a == 2:
                self.app_api.HouseQA(keyWord=globals()['r.text'][globals()['a']]['houseQuestionVo']['houseName'])
                self.assertEqual(globals()['r.text'][globals()['a']]['houseQuestionVo']['houseName'],
                                 self.appText.get('houseName'))
            a = a + 1

