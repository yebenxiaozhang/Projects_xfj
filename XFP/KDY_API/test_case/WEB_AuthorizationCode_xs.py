"""后台-授权码"""
from PubilcAPI.flowPath import *
"""
授权码：(只考虑是否正常登录，不考虑时效)
    1、不输入授权码                                登录失败
    2、输入授权码                                  登录成功
    3、输入授权码（已失效）| 上一个授权码          登录失败
"""


class TestCase(unittest.TestCase):
    """授权码"""

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
        cls.do_request = appApi()
        cls.appApi = cls.do_request
        cls.appApi.Login(userName=XfpUser11)
        cls.appApi.GetUserData()
        cls.request = webApi()
        cls.webApi = cls.request
        cls.webApi.Audit_management()

    def test_AuthorizationCode_1(self):
        """1、不输入授权码                                登录失败"""
        self.appApi.generateAuthCode()
        self.appApi.Login(userName=XfpUser11, authCode='')
        self.assertEqual('请输入授权码!', self.appText.get('resultStr'))

    def test_AuthorizationCode_2(self):
        """2、输入授权码（失效前）                        登录成功"""
        self.appApi.Login(userName=XfpUser11)
        self.appApi.generateAuthCode()
        self.appApi.Login(userName=XfpUser11, authCode=self.appText.get('code'))
        self.assertEqual('授权码验证成功!', self.appText.get('resultStr'))

    def test_AuthorizationCode_4(self):
        """4、输入授权码（已失效）   登录失败"""
        self.appApi.Login(userName=XfpUser11)
        self.appApi.generateAuthCode()
        time.sleep(30)
        self.appApi.Login(userName=XfpUser11, authCode=self.appText.get('code'))
        self.assertEqual('授权码已过期或授权码错误!', self.appText.get('resultStr'))




