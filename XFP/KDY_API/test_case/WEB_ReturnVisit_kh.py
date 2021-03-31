"""客第壹总站-回访"""
from PubilcAPI.flowPath import *
"""
回访：
    无审核：
        完成带看--->创建待回访任务         
                ！！！ APP_My_visit_kh.py-->test_my_visit_02
        录入成交--->创建待回访任务         
                ！！！ APP_My_Deal_kh.py-->test_my_deal_01
    有审核：
        审核失败、取消带看--->不创建回访任务
                ！！！ APP_My_visit_kh.py-->test_my_visit_06
                ！！！ APP_My_visit_kh.py-->test_my_visit_03
        审核成功--->创建回访任务
                ！！！ APP_My_visit_kh.py-->test_my_visit_07
        成交审核失败--->不创建回访任务
        审核成功、审核失败的再次提交--->创建待回访任务    
    
    回访带看--------取消带看回访
    回访成交--------取消成交回访
"""


class TestCase(unittest.TestCase):
    """客第壹总站-回访"""

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

    def test_ReturnVisit_001(self):
        """
        录入成交-审核失败不创建回访记录
        将原来审核失败的记录重新申请 则创建回访记录
        :return:
        """
        self.flowPath.client_list_non_null()
        self.appApi.visitProject_list()
        if self.appText.get('web_total') == 0:
            self.flowPath.add_visit()
            self.flowPath.accomplish_visit()
            self.appApi.visitProject_list()
        self.webApi.Audit_management(customerDeal=True, customerDealLevel=1)
        self.appApi.ClientList()
        self.webApi.repayTaskList(repayType=2)
        repay = self.appText.get('total')
        self.appApi.add_deal()
        self.webApi.repayTaskList(repayType=2)
        self.assertEqual(self.appText.get('total'), repay)

        self.webApi.auditList(phoneNum=self.appText.get('cluePhone'))
        self.webApi.audit(auditStatue=2, auditRemark=time.strftime("%Y-%m-%d %H:%M:%S") + ' 成交审核不通过')

        self.webApi.repayTaskList(repayType=2)
        self.assertEqual(self.appText.get('total'), repay)

        self.appApi.deal_List(ApplyStatus=2)
        self.webApi.detail()
        self.appApi.add_deal(Status=1)

        self.webApi.auditList(phoneNum=self.appText.get('cluePhone'))
        self.webApi.audit()

        self.webApi.repayTaskList(repayType=2)
        self.assertNotEqual(self.appText.get('total'), repay)

    def test_ReturnVisit_002(self):
        """
            回访带看--------取消带看回访
            回访成交--------取消成交回访
        :return:
        """
        a = 0
        while a != 4:
            if a < 2:
                self.webApi.repayTaskList()
            if a > 1:
                self.webApi.repayTaskList(repayType=2)
            dome = self.appText.get('total')
            if self.appText.get('total') != 0:
                if a == 0 or a == 2:
                    self.webApi.repayTask()         # 取消回访
                else:
                    self.webApi.repayTaskCancel()   # 回访
                self.webApi.repayTaskList()
                self.assertNotEqual(dome, self.appText.get('total'))
            a = a + 1

    def test_ReturnVisit_003(self):
        """设置开关为关闭---成交"""
        self.flowPath.client_list_non_null()
        self.appApi.visitProject_list()
        if self.appText.get('web_total') == 0:
            self.flowPath.add_visit()
            self.flowPath.accomplish_visit()
            self.appApi.visitProject_list()
        self.webApi.Audit_management(dealIRepaySwitch=False)
        self.appApi.ClientList()
        self.webApi.repayTaskList(repayType=2)
        repay = self.appText.get('total')
        self.appApi.add_deal()
        self.webApi.repayTaskList(repayType=2)
        self.assertEqual(self.appText.get('total'), repay)

    def test_ReturnVisit_004(self):
        """设置开关为关闭---带看"""
        self.flowPath.client_list_non_null()
        self.appApi.ClientTask(taskType='3')
        if self.appApi.appText.get('total') == 2:
            self.flowPath.advance_over_visit()
            if self.appApi.appText.get('code') != 200:
                self.flowPath.clue_non_null()
                self.appApi.ClientEntering(callName=self.appApi.RandomText(textArr=surname),
                                           loanSituation='这个是贷款情况')
                self.flowPath.client_list_non_null()
        self.appApi.ClientList()
        self.webApi.repayTaskList()
        dome = self.appText.get('total')
        self.webApi.Audit_management(visitIRepaySwitch=False)
        self.appApi.ClientVisitAdd(projectAId=self.appApi.appText.get('houseId'),
                                   appointmentTime=time.strftime("%Y-%m-%d %H:%M:%S"),
                                   seeingConsultant=self.appApi.appText.get('consultantId'),
                                   appointConsultant=self.appApi.appText.get('consultantId'))
        self.appApi.ClientTask(taskType='3')
        self.appApi.visit_info()

        self.appApi.VisitFlow1(agencyId=self.appApi.appText.get('DLGS'),
                               receptionName=self.appApi.RandomText(textArr=surname),
                               houseId=self.appApi.appText.get('houseId'),
                               receptionPhone='1' + str(int(time.time())))
        self.webApi.repayTaskList()
        self.assertEqual(dome, self.appText.get('total'))


