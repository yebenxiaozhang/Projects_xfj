# 第一步 导入unittest模块
from XFJ.PubilcAPI.FlowPath import *
import unittest
# 第二步 编写测试用例


class LonInTestCase(unittest.TestCase):
    """我的测试用例类"""

    def __init__(self, *args, **kwargs):
        super(LonInTestCase, self).__init__(*args, **kwargs)
        self.Xfk_request = XfkApi()
        self.XfkRequest = self.Xfk_request
        self.XfkTEXT = GlobalMap()
    # 测试用例方法必须用test开头

    def test_login_pass(self):
        self.XfkRequest.LoginXfk()
        self.assertEqual('登录成功', self.XfkTEXT.get('Content'))

    def test_user_is_null(self):
        self.XfkRequest.LoginXfk(user=None)
        self.assertEqual('手机或密码不能为空', self.XfkTEXT.get('Content'))

    def test_pwd_is_null(self):
        self.XfkRequest.LoginXfk(pwd=None)
        self.assertEqual('手机或密码不能为空', self.XfkTEXT.get('Content'))

    def test_pwd_fiald(self):
        self.XfkRequest.LoginXfk(pwd='123')
        self.assertEqual('密码不正确', self.XfkTEXT.get('Content'))


# # 第三 创建测试套件
# suite = unittest.TestSuite()
#
# # 添加测试用例到套件
# loader = unittest.TestLoader()
# suite.addTests(loader.loadTestsFromTestCase(LonInTestCase))
#
#
# # 第四步：执行测试用例
# runner = unittest.TextTestRunner()
# runner.run(suite)

