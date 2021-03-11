"""转移-相关"""
from PubilcAPI.flowPath import *
import requests

"""
线索：
    1、已首电转移             APP_First_phone_xs.py  - test_first_phone_11
    2、线索待办为今天以前
    3、线索待办为今天
    4、线索待办为今天以后

客户跟进待办：
    1、待办为今日以前
    2、待办为今日
    3、待办为今日以后

客户暂缓待办
    1、待办为今日以前
    2、待办为今日
    3、待办为今日以后
    
客户带看待办
    1、待办为今日以前
    2、待办为今日
    3、待办为今日以后
"""


class TestCase(unittest.TestCase):
    """客第壹——首电相关"""

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
        cls.appApi.time_()

    def test_ClueChange(self):
        """
        2、线索待办为今天以前
        3、线索待办为今天
        4、线索待办为今天以后
        :return:
        """
        dome = -1
        while dome != 2:
            self.appApi.Login()
            self.appApi.GetUserData()
            self.flowPath.clue_non_null()
            self.appApi.ClueFollowList()
            if dome == -1:
                self.appApi.ClueFollowSave(taskEndTime=self.appText.get('yesterday'))
            elif dome == 0:
                self.appApi.ClueFollowSave(taskEndTime=time.strftime("%Y-%m-%d %H:%M:%S"))
            else:
                self.appApi.ClueFollowSave(taskEndTime=self.appText.get('tomorrow'))
            self.appApi.ClueChange()
            self.appApi.Login(userName=XfpUser1)
            self.appApi.GetUserData()
            self.appApi.ClueTask()
            self.assertEqual(self.appText.get('endTime'), time.strftime("%Y-%m-%d 23:59:59"))
            dome = dome + 1

    def test_ClientChange(self):
        """
        1、待办为今日以前
        2、待办为今日
        3、待办为今日以后"""

        dome = -1
        while dome != 2:
            self.appApi.Login()
            self.appApi.GetUserData()
            self.flowPath.client_list_non_null()
            self.appApi.ClueFollowList()
            if dome == -1:
                self.appApi.ClueFollowSave(taskEndTime=self.appText.get('yesterday'), followType='客户')
            elif dome == 0:
                self.appApi.ClueFollowSave(taskEndTime=time.strftime("%Y-%m-%d %H:%M:%S"), followType='客户')
            else:
                self.appApi.ClueFollowSave(taskEndTime=self.appText.get('tomorrow'), followType='客户')
            self.appApi.client_change()
            self.appApi.Login(userName=XfpUser1)
            self.appApi.GetUserData()
            self.appApi.ClientTask(taskType=2)
            self.assertEqual(self.appText.get('endTime'), time.strftime("%Y-%m-%d 23:59:59"))
            dome = dome + 1

    def test_ClientChange_Defer(self):
        """
            1、待办为今日以前
            2、待办为今日
            3、待办为今日以后
        """

        dome = -1
        while dome != 2:
            self.appApi.Login()
            self.appApi.GetUserData()
            self.flowPath.client_list_non_null()

            self.appApi.ClientFollowList()
            self.appApi.ClueFollowSave(followType='客户', taskEndTime=time.strftime("%Y-%m-%d") + ' 22:00:00')
            self.appApi.ClientFollowList()

            if dome == -1:
                self.appApi.ClientTaskPause(endTime=self.appText.get('yesterday'))
            elif dome == 0:
                self.appApi.ClientTaskPause()
            else:
                self.appApi.ClientTaskPause(endTime=self.appText.get('yesterday'))
            self.appApi.client_change()
            self.appApi.Login(userName=XfpUser1)
            self.appApi.GetUserData()
            self.appApi.ClientTask(taskType=2)
            self.assertEqual(self.appText.get('endTime'), time.strftime("%Y-%m-%d 23:59:59"))
            dome = dome + 1

    def test_ClientChange_visit(self):
        """
        1、待办为今日以前
        2、待办为今日
        3、待办为今日以后"""

        dome = -1
        while dome != 2:
            self.appApi.Login()
            self.appApi.GetUserData()
            self.flowPath.client_list_non_null()
            self.appApi.ClientList()
            self.appApi.ClientTask(taskType='3')
            if self.appApi.appText.get('total') == 2:
                self.flowPath.advance_over_visit()
                if self.appApi.appText.get('code') != 200:
                    self.flowPath.clue_non_null()
                    self.appApi.ClientEntering(callName=self.appApi.RandomText(textArr=surname),
                                               loanSituation='这个是贷款情况')
                    self.flowPath.client_list_non_null()
            self.appApi.ClientList()
            if dome == -1:
                self.appApi.ClientVisitAdd(projectAId=self.appApi.appText.get('houseId'),
                                           appointmentTime=self.appText.get('yesterday'),
                                           seeingConsultant=self.appApi.appText.get('consultantId'),
                                           appointConsultant=self.appApi.appText.get('consultantId'))

            elif dome == 0:
                self.appApi.ClientVisitAdd(projectAId=self.appApi.appText.get('houseId'),
                                           appointmentTime=time.strftime("%Y-%m-%d %H:%M:%S"),
                                           seeingConsultant=self.appApi.appText.get('consultantId'),
                                           appointConsultant=self.appApi.appText.get('consultantId'))
            else:
                self.appApi.ClientVisitAdd(projectAId=self.appApi.appText.get('houseId'),
                                           appointmentTime=self.appText.get('tomorrow'),
                                           seeingConsultant=self.appApi.appText.get('consultantId'),
                                           appointConsultant=self.appApi.appText.get('consultantId'))
            self.appApi.client_change()
            self.appApi.Login(userName=XfpUser1)
            self.appApi.GetUserData()
            self.appApi.ClientTask(taskType=3)
            self.assertEqual(self.appText.get('endTime'), time.strftime("%Y-%m-%d 23:59:59"))
            dome = dome + 1

    def test_config_05(self):
        self.appApi.Login(userName=XfpUser1)
        self.appApi.GetUserData()

        self.appApi.my_clue_list()
        while self.appText.get('total') >= 1:
            self.flowPath.clue_exile_sea()
            self.appApi.my_clue_list()

        self.appApi.ClientList()
        while self.appText.get('total') >= 1:
            self.appApi.client_exile_sea()
            self.appApi.ClientList()
