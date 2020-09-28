# 第一步 导入unittest模块
from XFJ.PubilcAPI.AgentAPI import *
import unittest
# 第二步 编写测试用例


class NewsTestCase(unittest.TestCase):
    """消息列表"""

    def __init__(self, *args, **kwargs):
        super(NewsTestCase, self).__init__(*args, **kwargs)
        self.Agent = AgentApi()
        self.AgentRequest = self.Agent
        self.AgentTEXT = GlobalMap()

    @classmethod
    def setUpClass(cls):
        """登陆经纪人"""
        cls.Agent = AgentApi()
        cls.AgentRequest = cls.Agent
        cls.AgentRequest.LoginAgent()

    def test_TheTaskOfIntegral(self):
        """任务积分"""
        self.AgentRequest.TheTaskOfIntegral()

    def test_PersonalPayments(self):
        """个人收支"""
        self.AgentRequest.PersonalPayments()

    def test_SystemMessages(self):
        """系统消息"""
        self.AgentRequest.SystemMessages()

