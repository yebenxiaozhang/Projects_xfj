"""带看-相关"""
from XFP.PubilcAPI.flowPath import *

"""
新增：
    1、约见时间只能在此之后
    2、约见地点
    3、邀约人默认是登录人也可以选其他咨询师
    4、带看人可多选最多3
    5、带看路线 一定要选一个目标楼盘 可选两个非目标楼盘
    6、出行方式，单选
    7、备注，最多可以填写200个字
    8、客户情况 核心诉求 核心抗性  应对方案 最多可填写200个字
    
完成带看：
    1、带看楼盘可以替换
    2、对接平台单选
    3、接待人及电话、手机号可以是微信长度不得超过20，名字不能超过5个字
    4、报备截图至多9张
    5、可以删除单个带看楼盘
    6、可以添加带看楼盘
    7、可以添加楼盘QA 并且在楼盘QA会新增
    8、带看总结，不允许超过200个字
    9、除了完成的带看 任何情况下都可以取消带看

取消带看：
    1、备注不得超过50个字

"""


class VisitTestCase(unittest.TestCase):
    """幸福派——我的带看"""

    def __init__(self, *args, **kwargs):
        super(VisitTestCase, self).__init__(*args, **kwargs)
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
        cls.app_api = cls.do_request
        cls.app_api.Login()
        cls.app_api.GetUserData()
        cls.request = webApi()
        cls.webApi = cls.request
        cls.webApi.Audit_management()

    # def setUp(self):
    #     pass

    def setUp(self):
        """残留审核 失败！！！"""
        self.webApi.audit_List()
        while self.webApi.webText.get('total') != 0:
            self.webApi.auditApply(isAudit=False, auditRemark='客户流放公海')
            self.webApi.audit_List()
        self.webApi.audit_List(auditLevel=2)
        while self.webApi.webText.get('total') != 0:
            self.webApi.auditApply(isAudit=False, auditRemark='客户流放公海')
            self.webApi.audit_List()
        self.appApi.GetLabelList(labelNo='CXFS', labelName='自驾')
        if self.appText.get('labelId') is None:
            self.webApi.add_label(labelName='自驾', labelId=self.appText.get('LabelId'),
                                  pid=self.appText.get('LabelId'))
            self.appApi.GetLabelList(labelNo='CXFS', labelName='自驾')
        self.flowPath.client_list_non_null()
        self.appApi.GetMatchingAreaHouse()
        globals()['dome'] = time.strftime("%Y-%m-%d %H:%M:%S")
        self.appApi.ClientTask(taskType='3')
        if self.appApi.appText.get('total') == 2:
            self.flowPath.advance_over_visit()
            if self.appApi.appText.get('code') != 200:
                self.flowPath.clue_non_null()
                self.appApi.ClientEntering(callName=self.appApi.RandomText(textArr=surname),
                                           loanSituation='这个是贷款情况')

    def test_visit_01(self):
        """3、邀约人默认是登录人也可以选其他咨询师"""
        self.appApi.ClientVisitAdd(projectAId=self.appApi.appText.get('houseId'),
                                   appointmentTime=globals()['dome'],
                                   seeingConsultant=self.appText.get('consultantId'),
                                   appointConsultant=self.appText.get('consultantId'))
        self.assertEqual(200, self.appApi.appText.get('code'))

    def test_visit_02(self):
        """3、邀约人默认是登录人也可以选其他咨询师"""
        self.webApi.consultant_list()
        self.appApi.ClientVisitAdd(projectAId=self.appApi.appText.get('houseId'),
                                   appointmentTime=globals()['dome'],
                                   seeingConsultant=self.appText.get('consultantId'),
                                   appointConsultant=self.webText.get('consultantId'))
        self.assertEqual(200, self.appApi.appText.get('code'))

    def test_visit_03(self):
        """4、带看人可多选最多3"""
        self.webApi.consultant_list()
        dome = self.webApi.webText.get('total')
        dome1 = 0
        dome2 = []
        while dome > dome1:
            # print(dome1, self.appText.get('consultantId'))
            self.webApi.consultant_list(vlue=dome1)
            dome2.append(self.appText.get('consultantId'))
            self.appApi.ClientVisitAdd(projectAId=self.appApi.appText.get('houseId'),
                                       appointmentTime=globals()['dome'],
                                       seeingConsultant=(str(dome2))[1:-1],
                                       appointConsultant=self.webText.get('consultantId'))
            if dome1 + 1 == dome or dome1 >= 3:
                self.assertNotEqual(200, self.appApi.appText.get('code'))
            else:
                self.assertEqual(200, self.appApi.appText.get('code'))
            dome1 = dome1 + 1
            self.setUp()

    def test_visit_04(self):
        """5、带看路线 一定要选一个目标楼盘 可选两个非目标楼盘"""
        self.appApi.ClientVisitAdd(projectAId=None,
                                   appointmentTime=globals()['dome'],
                                   seeingConsultant=self.appText.get('consultantId'),
                                   appointConsultant=self.appText.get('consultantId'))
        self.assertNotEqual(200, self.appApi.appText.get('code'))

    def test_visit_05(self):
        """7、备注，最多可以填写200个字
    8、客户情况 核心诉求 核心抗性  应对方案 最多可填写200个字"""
        self.appApi.ClientVisitAdd(projectAId=self.appApi.appText.get('houseId'),
                                   appointmentTime=globals()['dome'],
                                   seeingConsultant=self.appText.get('consultantId'),
                                   appointConsultant=self.appText.get('consultantId'),
                                   visitRemark=(str(surname))[1:-1])
        self.assertNotEqual(200, self.appApi.appText.get('code'))
        self.appApi.ClientVisitAdd(projectAId=self.appApi.appText.get('houseId'),
                                   appointmentTime=globals()['dome'],
                                   seeingConsultant=self.appText.get('consultantId'),
                                   appointConsultant=self.appText.get('consultantId'),
                                   beforeTakingA=(str(surname))[1:-1])
        self.assertNotEqual(200, self.appApi.appText.get('code'))
        self.appApi.ClientVisitAdd(projectAId=self.appApi.appText.get('houseId'),
                                   appointmentTime=globals()['dome'],
                                   seeingConsultant=self.appText.get('consultantId'),
                                   appointConsultant=self.appText.get('consultantId'),
                                   beforeTakingB=(str(surname))[1:-1])
        self.assertNotEqual(200, self.appApi.appText.get('code'))
        self.appApi.ClientVisitAdd(projectAId=self.appApi.appText.get('houseId'),
                                   appointmentTime=globals()['dome'],
                                   seeingConsultant=self.appText.get('consultantId'),
                                   appointConsultant=self.appText.get('consultantId'),
                                   beforeTakingC=(str(surname))[1:-1])
        self.assertNotEqual(200, self.appApi.appText.get('code'))
        self.appApi.ClientVisitAdd(projectAId=self.appApi.appText.get('houseId'),
                                   appointmentTime=globals()['dome'],
                                   seeingConsultant=self.appText.get('consultantId'),
                                   appointConsultant=self.appText.get('consultantId'),
                                   beforeTakingD=(str(surname))[1:-1])
        self.assertNotEqual(200, self.appApi.appText.get('code'))

    def test_visit_06(self):
        """完成带看的一些限制"""
        self.test_visit_01()
        self.appApi.ClientTask(taskType='3')
        if self.appApi.appText.get('total') < 1:
            raise RuntimeError(self.appApi.appText.get('ApiXfpUrl'))
        self.appApi.visit_info()
        self.appApi.GetLabelList(labelNo='DLGS')
        """接待人姓名超过5位数"""
        self.appApi.VisitFlow1(agencyId=self.appText.get('labelId'), receptionName=(str(surname))[1:-1])
        self.assertNotEqual(200, self.appText.get('code'))

        """带看总结不允许超过200个字"""
        self.appApi.VisitFlow1(agencyId=self.appText.get('labelId'),
                               receptionName=self.appApi.RandomText(textArr=surname),
                               receptionPhone='1' + str(int(time.time())), visitSummary=(str(surname))[1:-1])
        self.assertNotEqual(200, self.appText.get('code'))
        """报备截图最多9张"""
        self.appApi.VisitFlow1(agencyId=self.appText.get('labelId'),
                               receptionName=self.appApi.RandomText(textArr=surname),
                               receptionPhone='1' + str(int(time.time())),
                               attachmentIds='1,2,3,4,5,6,7,8,9,10')
        self.assertNotEqual(200, self.appText.get('code'))

    def test_visit_07(self):
        """楼盘QA的一些限制"""
        self.test_visit_01()
        self.appApi.ClientTask(taskType='3')
        if self.appApi.appText.get('total') < 1:
            raise RuntimeError(self.appApi.appText.get('ApiXfpUrl'))
        self.appApi.visit_info()
        self.appApi.GetLabelList(labelNo='DLGS')
        """标题过长"""
        self.appApi.VisitFlow1(agencyId=self.appText.get('labelId'),
                               receptionName=self.appApi.RandomText(textArr=surname),
                               receptionPhone='1' + str(int(time.time())), title=(str(surname))[1:-1],
                               is_QA=1)
        self.assertNotEqual(200, self.appText.get('code'))
        """标题不能重复"""
        self.appApi.HouseQA()
        if self.appText.get('total') != 0:
            self.appApi.VisitFlow1(agencyId=self.appText.get('labelId'),
                                   receptionName=self.appApi.RandomText(textArr=surname),
                                   receptionPhone='1' + str(int(time.time())),
                                   is_QA=1,
                                   title=self.appText.get('title'))
            self.assertNotEqual(200, self.appText.get('code'))
        """答案不能超过200个字"""
        self.appApi.VisitFlow1(agencyId=self.appText.get('labelId'),
                               receptionName=self.appApi.RandomText(textArr=surname),
                               receptionPhone='1' + str(int(time.time())), is_QA=1,
                               title='楼盘问答 ' + time.strftime("%Y-%m-%d %H:%M:%S"),
                               answer=(str(surname))[1:-1])
        self.assertNotEqual(200, self.appText.get('code'))

    def test_visit_08(self):
        """完成带看后要是有楼盘问答则在列表会显示"""
        self.test_visit_01()
        self.appApi.ClientTask(taskType='3')
        if self.appApi.appText.get('total') < 1:
            raise RuntimeError(self.appApi.appText.get('ApiXfpUrl'))
        self.appApi.visit_info()
        self.appApi.GetLabelList(labelNo='DLGS')
        dome = '楼盘问答 ' + time.strftime("%Y-%m-%d %H:%M:%S")
        self.appApi.VisitFlow1(agencyId=self.appText.get('labelId'),
                               receptionName=self.appApi.RandomText(textArr=surname),
                               receptionPhone='1' + str(int(time.time())),
                               attachmentIds='1', is_QA=1,
                               answer='答案 ' + time.strftime("%Y-%m-%d %H:%M:%S"),
                               title=dome)
        self.assertEqual(200, self.appText.get('code'))
        self.app_api.HouseQA(keyWord=dome)
        self.assertNotEqual(1, self.appText.get('total'))

    def test_visit_09(self):
        """取消带看备注过长"""
        self.appApi.ClientVisitAdd(projectAId=self.appApi.appText.get('houseId'),
                                   appointmentTime=globals()['dome'],
                                   seeingConsultant=self.appText.get('consultantId'),
                                   appointConsultant=self.appText.get('consultantId'))
        self.assertEqual(200, self.appApi.appText.get('code'))
        self.appApi.ClientTask(taskType='3')
        if self.appApi.appText.get('total') < 1:
            raise RuntimeError(self.appApi.appText.get('ApiXfpUrl'))
        self.appApi.visit_info()
        self.appApi.visit_cancel(cancelRemark=(str(surname))[1:-1])
        self.assertNotEqual(200, self.appText.get('code'))
        """正常取消"""

        self.appApi.visit_cancel()
        self.assertEqual(200, self.appText.get('code'))

