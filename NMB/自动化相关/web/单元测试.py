# 开始前需要运行web_server

# 第一步 导入unittest模块
import unittest
import requests


# 第二步 编写测试用例
class LoginTestCase(unittest.TestCase):
    """登录的测试用例类"""

    # 测试用例方法必须用test开头

    def test_login_pass(self):
        # 1、 准备请求数据
        url = "http://127.0.0.1:5000/login"
        data = {"user": "python01", "pwd": "lemonban"}
        # 2、发送请求，获取接口的返回内容
        response = requests.post(url=url, data=data)
        res = response.json()
        excepted = {'code': '1', 'data': None, 'msg': '成功'}
        # 3、比较结果和预期
        self.assertEqual(excepted, res)

    def test_user_is_null(self):
        url = "http://127.0.0.1:5000/login"
        data = {"user": None, "pwd": "lemonban"}
        # 2、发送请求，获取接口的返回内容
        response = requests.post(url=url, data=data)
        res = response.json()
        excepted = {'code': "0", "data": None, "msg": "账号不能为空"}
        # 3、比较结果和预期
        self.assertEqual(excepted, res)

    def test_pwd_is_null(self):
        url = "http://127.0.0.1:5000/login"
        data = {"user": 'python01', "pwd": None}
        # 2、发送请求，获取接口的返回内容
        response = requests.post(url=url, data=data)
        res = response.json()
        excepted = {'code': "0", "data": None, "msg": "密码不能为空"}
        # 3、比较结果和预期
        self.assertEqual(excepted, res)

    def test_pwd_fiald(self):
        url = "http://127.0.0.1:5000/login"
        data = {"user": 'python01', "pwd": '123456'}
        # 2、发送请求，获取接口的返回内容
        response = requests.post(url=url, data=data)
        res = response.json()
        excepted = {'code': "0", "data": None, "msg": "密码有误"}
        # 3、比较结果和预期
        self.assertEqual(excepted, res)


# 第三 创建测试套件
suite = unittest.TestSuite()

# 添加测试用例到套件
loader = unittest.TestLoader()
suite.addTests(loader.loadTestsFromTestCase(LoginTestCase))


# 第四步：执行测试用例
runner = unittest.TextTestRunner()
runner.run(suite)

