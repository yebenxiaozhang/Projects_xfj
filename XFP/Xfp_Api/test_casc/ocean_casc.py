# -*- coding: utf-8 -*-
# @Time    : 2020/3/21 11:07
# @Author  : 潘师傅
# @File    : Ocean_casc.py

"""公海相关"""
# 线索流放公海
# 客户流放公海
# 领取线索


from XFP.PubilcAPI.webApi import *


class OceanTestCase(unittest.TestCase):
    """小秘——公海相关"""

    def __init__(self, *args, **kwargs):
        super(OceanTestCase, self).__init__(*args, **kwargs)
        self.appApi = appApi()
        self.appText = GlobalMap()
        self.webApi = webApi()
        self.webText = GlobalMap()

    @classmethod
    def setUpClass(cls):
        """登录幸福派 只执行一次
        登录经纪人 获取ID"""
        cls.do_request = appApi()
        cls.XmRequest = cls.do_request
        cls.XmRequest.Login()
        cls.request = webApi()
        cls.webApi = cls.request
        cls.webApi.Audit_management()

    def test_clue_orcan(self):
        """线索流放公海"""
        try:
            self.appApi.my_clue_list()
            if self.appText.get('total') == 0:
                ClueTestCase.test_1_AddNewClue(self)    # 新增线索
                self.appApi.my_clue_list()
            ClueTestCase.test_4_ExileSea(self)          # 流放公海
        except BaseException as e:
                print("错误，错误原因：%s" % e)
                raise RuntimeError(self.appText.get('ApiXfpUrl'))

    def test_client_orcan(self):
        """客户流放公海"""
        try:
            self.appApi.ClientList()
            if self.appText.get('total') == 0:

                #     ClueTestCase.test_1_AddNewClue(self)    # 新增客户
            #     self.appApi.my_clue_list()
            # ClueTestCase.test_4_ExileSea(self)          # 流放公海
                pass

        except BaseException as e:
                print("错误，错误原因：%s" % e)
                raise RuntimeError(self.appText.get('ApiXfpUrl'))

    def test_clue_Assigned(self):
        """线索领取"""
        try:
            self.appApi.SeaList()
            if self.appText.get('total') == 0:
                self.test_clue_orcan()
                self.appApi.SeaList()
            self.appApi.clue_Assigned()     # 领取线索
        except BaseException as e:
                print("错误，错误原因：%s" % e)
                raise RuntimeError(self.appText.get('ApiXfpUrl'))
