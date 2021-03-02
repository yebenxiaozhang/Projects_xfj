"""设备管理-相关"""
from PubilcAPI.flowPath import *
DeviceId = '1' + str(int(time.time()))
"""
设备管理：
    1、未绑定设备
        1、登录失败
    2、已绑定设备
        1、登录成功

"""


class TestCase(unittest.TestCase):
    """客第壹——设备管理"""

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
        cls.appApi.Login(authCode=1)
    #     cls.appApi.GetUserData()
    #     cls.request = webApi()
    #     cls.webApi = cls.request
    #     cls.webApi.Audit_management()

    def test_Device_01(self):
        """添加设备进行登录"""
        self.webApi.DeptUserListPage(deviceNo=DeviceId)
        self.webApi.configList(keyWord='check_device_switch')
        self.webApi.configSave(configValue=1)
        self.webApi.DeptUserListPage(deviceNo=DeviceId)
        while self.appText.get('web_total') != 0:
            """删除设备"""
            self.webApi.DelDeviceInfo()
            self.webApi.DeptUserListPage(deviceNo=DeviceId)
        """添加设备"""
        self.webApi.addDeviceInfo(deviceName='设备', deviceNo=DeviceId)
        """重复添加设备"""
        self.webApi.addDeviceInfo(deviceName='设备', deviceNo=DeviceId)
        self.assertEqual('设备已存在,请勿重复添加!', self.appText.get('data'))
        """尝试登录"""
        self.appApi.Login(userName='13062200320')
        self.assertEqual('用户暂无设备授权,登录失败!', self.appText.get('resultStr'))
        """绑定设备"""
        self.appApi.Login(userName='13332978000', authCode=1)
        self.webApi.DeptUserListPage(deviceNo=DeviceId)
        self.webApi.UserIdList(keyWord='13062200320')
        self.webApi.DeviceBinding()
        self.appApi.Login(userName='13062200320')
        self.assertEqual(self.appText.get('msg'), '成功')
        self.webApi.configSave(configValue=0)

    def test_Device_02(self):
        """添加默认设备人员"""
        self.appApi.Login(authCode=1, userName='13332978000')
        self.webApi.DeptUserListPage(deviceNo=DeviceId)
        self.webApi.UserIdList(keyWord=XfpUser1)
        dome = self.appText.get('userId')
        self.webApi.UserIdList(keyWord='13062200320')
        dome1 = self.appText.get('userId')
        self.webApi.UserIdList(keyWord=XfpUser)
        dome2 = self.appText.get('userId')
        userId = [dome, dome1, dome2]
        self.webApi.DeviceBinding(userId=userId)

    def test_Device_03(self):
        """恢复默认 将设备进行删除"""
        self.webApi.DeptUserListPage(deviceNo=DeviceId)
        while self.appText.get('web_total') != 0:
            """删除设备"""
            self.webApi.DelDeviceInfo()
            self.webApi.DeptUserListPage(deviceNo=DeviceId)
        self.webApi.configList(keyWord='check_device_switch')
        self.webApi.configSave(configValue=0)

