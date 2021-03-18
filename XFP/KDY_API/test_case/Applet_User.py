"""用户相关"""
from PubilcAPI.appletApi import *


"""
验证码登录：
    1、正常登录
    2、手机号码为空
    3、验证码为空
    4、手机号码及验证码都为空
    5、用户名不正确
    6、验证码错误
    7、手机号及验证码都错误

发送验证码：
    1、正确的手机号
    2、异常手机号  



"""


class UserTestCase(unittest.TestCase):
    """幸福派——用户相关"""

    def __init__(self, *args, **kwargs):
        super(UserTestCase, self).__init__(*args, **kwargs)
        self.AppletRequest = appletApi()
        self.AppletTEXT = GlobalMap()

    @classmethod
    def setUpClass(cls):
        """登录幸云 只执行一次"""

    # def test_Login_Pass(self):
    #     """登录"""
    #     self.AppletRequest.Login()
    #     self.assertEqual(self.AppletTEXT.get('msg'), '成功')

    def test_UserIsNone(self):
        """用户名为空"""
        self.AppletRequest.Login(userName='')
        self.assertEqual(self.AppletTEXT.get('data'), "用户信息不存在 ''")

    def test_PwdIsNone(self):
        """密码为空"""
        self.AppletRequest.Login(code='')
        self.assertEqual(self.AppletTEXT.get('data'), '验证码有误！')

    def test_UserAndPwdNone(self):
        """用户名密码都为空"""
        self.AppletRequest.Login(userName='', code='')
        self.assertEqual(self.AppletTEXT.get('data'), "用户信息不存在 ''")

    # def test_UserError(self):
    #     """用户名不正确"""
    #     self.AppletRequest.Login(userName='11111111111')
    #     self.assertEqual(self.AppletTEXT.get('data'), '用户名或密码不正确')

    def test_PsdError(self):
        """密码错误"""
        self.AppletRequest.Login(code='11111111')
        self.assertEqual(self.AppletTEXT.get('data'), '验证码有误！')

    # def test_UserAndPwdError(self):
    #     """用户名密码都错误"""
    #     self.AppletRequest.Login(userName='11111111111', code='11111111')
    #     self.assertEqual(self.AppletTEXT.get('data'), '用户名或密码不正确')

    def test_Applet_User_201(self):
        """获取验证码-正常手机号码"""
        self.AppletRequest.sendCodeWeiXin(userName=XfpUser)
        self.assertEqual(self.AppletTEXT.get('msg'), '成功')

    def test_Applet_User_202(self):
        """获取验证码-异常手机号码"""
        self.AppletRequest.sendCodeWeiXin(userName='1306220030')
        self.assertEqual(self.AppletTEXT.get('data'), "用户信息不存在 '1306220030'")


