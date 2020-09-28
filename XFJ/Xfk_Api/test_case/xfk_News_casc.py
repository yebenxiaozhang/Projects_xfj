# 第一步 导入unittest模块
from XFJ.PubilcAPI.FlowPath import *

# 第二步 编写测试用例


class NewsTestCase(unittest.TestCase):
    """幸福客消息列表"""

    def __init__(self, *args, **kwargs):
        super(NewsTestCase, self).__init__(*args, **kwargs)
        self.do_request = XmApi()
        self.XmRequest = self.do_request
        self.XmTEXT = GlobalMap()
        self.AgentRequest = AgentApi()
        self.ToAgentRequest = self.AgentRequest
        self.AgentTEXT = GlobalMap()
        self.Xfk_request = XfkApi()
        self.XfkRequest = self.Xfk_request
        self.XfkTEXT = GlobalMap()
        self.FlowPath = FlowPath()
        self.FlowPath = self.FlowPath

    @classmethod
    def setUpClass(cls):
        """登录小秘 只执行一次
        登录经纪人 获取ID"""
        cls.request = AgentApi()
        cls.AgentRequest = cls.request
        cls.AgentRequest.LoginAgent()
        cls.AgentRequest.ForRegistrationID()
        cls.do_request = XfkApi()
        cls.to_request = cls.do_request
        cls.to_request.LoginXfk()

    def test_100_recommend_news(self):
        """验证报名新房推送的信息"""
        self.AgentRequest.ForRegistrationID()
        self.AgentRequest.RecommendNew()
        content = '推荐信息：' + ProjectName
        self.XfkRequest.NewsList()
        self.assertEqual(self.XfkTEXT.get('push_title'), content)

    def test_101_timeout_new(self):
        """验证超时的信息 时间为5分钟"""
        import time
        time.sleep(310)
        self.XfkRequest.NewsList()
        self.assertEqual(self.XfkTEXT.get('push_title'), '任务即将超时')

    def test_102_allocation(self):
        """验证报备分配的文案"""
        self.XfkRequest.AttacheList()
        self.XfkRequest.ExamineClientParticulars()
        self.XfkRequest.AttacheOperation(SalesId=self.XfkTEXT.get('xfkSalesId'))
        self.XfkRequest.NewsList()
        self.assertEqual(self.XfkTEXT.get('push_title'), '接客啦')

    def test_timeout_list(self):
        """查看超时列表"""
        self.XfkRequest.TimeoutClient()

