"""幸福小秘-成交跟踪
需求：只能输入成交的客户、或者经纪人手机号4位数
"""
from XFJ.PubilcAPI.FlowPath import *
# 第二步 编写测试用例
"""
1、输入成交的客户、是否可以查询结果
2、输入成交的经纪人手机号4位  是否可以查询到结果
3、输入未成交的客户、
4、输入挞定的客户
5、输入非数字 是否有相应的提示
6、输入数字过长 是否有相应的提示

"""


class TestCase(unittest.TestCase):
    """小秘——成交跟踪"""

    def __init__(self, *args, **kwargs):
        super(TestCase, self).__init__(*args, **kwargs)
        self.XM_request = XmApi()
        self.XFK_request = XfkApi()
        self.XmTEXT = GlobalMap()
        self.XfkTEXT = GlobalMap()
        self.Flow = FlowPath()
        self.FlowPath = self.Flow
        self.Agent = AgentApi()
        self.AgentRequest = self.Agent
        self.AgentTEXT = GlobalMap()

    @classmethod
    def setUpClass(cls):
        """登录小秘 只执行一次
        登录经纪人 获取ID"""
        cls.do_request = XmApi()
        cls.XmRequest = cls.do_request
        cls.XmRequest.ApiLogin()
        cls.request = AgentApi()
        cls.AgentRequest = cls.request
        cls.AgentRequest.LoginAgent()
        cls.AgentRequest.ForRegistrationID()
        cls.do_request = XfkApi()
        cls.to_request = cls.do_request
        cls.to_request.LoginXfk()

    def test_SignedTail_is_OK(self):
        """输入成交的客户、是否可以查询结果"""
        self.FlowPath.TheNewDeal()
        self.FlowPath.DealTicket()
        self.XFK_request.AttacheList(StartTime='', EndTime='', Page=1, Level='', Status=4, Days='')
        try:
            self.XM_request.SignedTail(keyWord=(self.AgentTEXT.get('ClientPhone'))[-4:])
            self.assertEqual(1, self.XmTEXT.get('resultCode'))
        except BaseException as e:
            print("断言错误，错误原因：%s" % e)
            raise RuntimeError(self.XmTEXT.get('xmurl'))

    def test_SignedTail_is_AgentPhone(self):
        """输入成交的经纪人手机号4位  是否可以查询到结果"""
        try:
            self.XM_request.SignedTail(keyWord=AgentUesr[-4:])
            self.assertNotEqual(0, self.XmTEXT.get('xmcount'))
        except BaseException as e:
            print("断言错误，错误原因：%s" % e)
            raise RuntimeError(self.XmTEXT.get('xmurl'))

    def test_Unclinched_Client(self):
        """输入未成交的客户、"""
        a = 0
        self.XFK_request.AttacheList(StartTime='', EndTime='', Page=1, Level='', Status=2, Days='', vlue=a)
        self.XM_request.SignedTail(keyWord=self.XfkTEXT.get('xfkcustomerTel')[-4:])
        try:
            while self.XmTEXT.get('xmcount') != 0:
                a = a + 1
                self.XFK_request.AttacheList(StartTime='', EndTime='', Page=1, Level='', Status=2, Days='', vlue=a)
                self.XM_request.SignedTail(keyWord=self.XfkTEXT.get('xfkcustomerTel')[-4:])
                if a == 10:
                    break
        except BaseException as e:
            print("断言错误，错误原因：%s" % e)
            raise RuntimeError(self.XmTEXT.get('xmurl'))

    def test_Invalid_Client(self):
        """输入挞定的客户"""
        try:
            self.XM_request.DealTicketList()
            self.XM_request.DealCancellation()
            self.XM_request.SignedTail(keyWord=self.XmTEXT.get('customerMobile')[-4:])
            while self.XmTEXT.get('xmcount') != 0:
                self.XM_request.DealTicketList()
                self.XM_request.DealCancellation()
                self.XM_request.SignedTail(keyWord=self.XmTEXT.get('customerMobile')[-4:])
        except BaseException as e:
            print("断言错误，错误原因：%s" % e)
            raise RuntimeError(self.XmTEXT.get('xmurl'))

    def test_Non_Numeric(self):
        """输入非数字 是否有相应的提示"""
        try:
            self.XM_request.SignedTail(keyWord="hehe")
            self.assertEqual('搜索值不对！', self.XmTEXT.get('xmcontent'))
        except BaseException as e:
            print("断言错误，错误原因：%s" % e)
            raise RuntimeError(self.XmTEXT.get('xmurl'))

    def test_Input_Long(self):
        """输入数字过长 是否有相应的提示"""
        try:
            self.XM_request.SignedTail(keyWord=AgentUesr[-5:])
            self.assertEqual('搜索值不对！', self.XmTEXT.get('xmcontent'))
        except BaseException as e:
            print("断言错误，错误原因：%s" % e)
            raise RuntimeError(self.XmTEXT.get('xmurl'))




