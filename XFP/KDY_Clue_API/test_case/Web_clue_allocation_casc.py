"""后台-线索分配"""
from XFP.PubilcAPI.flowPath import *
"""
    1、幸福币不足，分配失败
    2、无咨询师接受分配，会在待分配列表
    3、上户时间：分站分配时间
"""


class TestCase(unittest.TestCase):
    """客第壹——线索分配"""

    def __init__(self, *args, **kwargs):
        super(TestCase, self).__init__(*args, **kwargs)
        self.xfp_web = webApi()
        self.webApi = self.xfp_web

        self.xfp_app = appApi()
        self.appApi = self.xfp_app

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

    def test_all_allocation_1(self):
        """2、无咨询师接受分配，会在待分配列表"""
        if ApiXfpUrl == 'http://xfp.xfj100.com':
            pass
        else:
            self.webApi.consultant_allocition(isAppoint=0)
            self.appApi.my_clue_list()
            dome = self.appText.get('total')
            self.appApi.Login(userName='admin', saasCode='admin')
            self.webApi.add_clue_admin(clueNickName=self.appApi.RandomText(textArr=surname))
            self.appApi.Login()
            self.webApi.clue_await_allocition(keyWord=self.webText.get('cluePhone'))
            self.assertEqual(1, self.webText.get('total'))
            self.assertNotEqual(self.webText.get('receptionTime'), self.webText.get('createdTime'))
            """3、上户时间：分站分配时间"""
            self.webApi.clue_appoint()
            self.webApi.clue_await_allocition(keyWord=self.webText.get('cluePhone'))
            self.assertEqual(0, self.webText.get('total'))
            self.appApi.my_clue_list()
            self.assertNotEqual(dome, self.appText.get('total'))
            self.appApi.ClueInfo()
            self.assertNotEqual(self.webText.get('receptionTime'), self.webText.get('createdTime'))
            self.assertNotEqual(self.appText.get('receptionTime'), self.appText.get('createdTime'))
            self.assertEqual(self.webText.get('createdTime'), self.appText.get('createdTime'))
            self.webApi.consultant_allocition(isAppoint=1)



