"""后台-授予财富值"""
from PubilcAPI.flowPath import *
"""
财务总监审核-关：
    授予财富值
    扣除财富值

审核开关    开
    授予财富值   审核成功
                 审核失败
    扣除财富值   审核成功
                 审核失败

"""


class TestCase(unittest.TestCase):
    """客第壹后台——带看成交统计"""

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

    def test_EndowWealth_01(self):
        """
        财务总监审核-关：
                授予财富值
                扣除财富值
        :return:
        """
        a = 1
        while a != 3:
            self.webApi.consultantWealthChange(Type=a)
            dome = self.appText.get('vlue')
            self.appApi.getWealthDetailList(startTime=time.strftime("%Y-%m-%d"),
                                            endTime=time.strftime("%Y-%m-%d"),
                                            wealthType=None,
                                            orderNo=None)
            self.assertEqual(dome, self.appText.get('vlue1'))
            a = a + 1

    def test_EndowWealth_02(self):
        """审核开关    开
           授予财富值   审核成功
                        审核失败
           扣除财富值   审核成功
                        审核失败"""
        self.webApi.Audit_management(wealthDetailSwitch=True)
        dome2 = 1
        while dome2 != 3:
            a = 1
            while a != 3:
                self.webApi.consultantWealthChange(Type=dome2)
                dome = self.appText.get('vlue')
                self.webApi.getWealthAuditList()
                if self.appText.get('total') == 0:
                    if dome == 1:
                        raise RuntimeError('授予财富值（有审核）在财务总监审核列表没有体现')
                    else:
                        raise RuntimeError('扣除财富值（有审核）在财务总监审核列表没有体现')
                if a == 1:
                    self.webApi.wealthAudit()
                else:
                    self.webApi.wealthAudit(auditType=False)
                self.appApi.getWealthDetailList(startTime=time.strftime("%Y-%m-%d"),
                                                endTime=time.strftime("%Y-%m-%d"),
                                                wealthType=None,
                                                orderNo=None)
                if a == 1:
                    self.assertEqual(dome, self.appText.get('vlue1'))
                else:
                    self.assertNotEqual(dome, self.appText.get('vlue1'))
                a = a + 1
            dome2 = dome2 + 1

