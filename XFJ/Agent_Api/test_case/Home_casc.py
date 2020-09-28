"""经纪人首页"""
# 第一步 导入unittest模块
from XFJ.PubilcAPI.AgentAPI import *
import unittest
import json

# 第二步 编写测试用例


class HomeTestCase(unittest.TestCase):
    """经纪人首页"""

    def __init__(self, *args, **kwargs):
        super(HomeTestCase, self).__init__(*args, **kwargs)
        self.Agent = AgentApi()
        self.AgentRequest = self.Agent
        self.AgentTEXT = GlobalMap()

    @classmethod
    def setUpClass(cls):
        """登陆经纪人"""
        cls.Agent = AgentApi()
        cls.AgentRequest = cls.Agent
        cls.AgentRequest.LoginAgent()

    def tearDown(self):
        pass

    def test_NewHouseListAndParticulars(self):
        """获取新房列表和详情---本地--海外--全国---周边"""
        dome = ['local', 'overseas', 'whole', 'periphery']
        z = 0
        while z < len(dome):
            self.AgentRequest.ForRegistrationID(type=dome[z])
            self.AgentRequest.NewHouseParticulars()
            z = z + 1

    def test_AssignNewHouseParticulars(self):
        """指定的新房详情"""
        self.AgentRequest.ForRegistrationID()
        self.AgentRequest.NewHouseParticulars()
        response = json.loads(json.dumps(json.loads(self.AgentTEXT.get('extend')),
                                         indent=4, sort_keys=False, ensure_ascii=False))
        """验证图片/佣金是否可见/报名人数/剩余天数/报备规则"""
        self.assertNotEqual(response['photoList'], None)
        self.assertNotEqual(response['commissionContent'], None)
        self.assertNotEqual(response['joinCount'], None)
        self.assertNotEqual(response['endDateStr'], None)
        self.assertNotEqual(response['projectProtectedPeriod'], None)
        """/亮点展示/户型与价格/楼盘参数+周边配套"""
        self.assertNotEqual(response['houseContentMobile'], None)
        self.assertNotEqual(response['projectApartmentDisplays'], None)
        self.assertNotEqual(response['projectParam'], None)
        """/项目地图（经纬度）、项目推荐"""
        self.assertNotEqual(response['latitude'], None)
        self.assertNotEqual(response['longitude'], None)
        self.assertNotEqual(response['recommendList'], None)
        """拓客工具、专员列表"""
        self.assertNotEqual(response['extensionCustomerTool'], None)
        self.assertNotEqual(response['sales'], None)

    def test_AdvertisingByAndParticulars(self):
        """广告轮播图及详情"""
        self.AgentRequest.AdvertisingBy()
        self.AgentRequest.AdvertisingForDetails()

    def test_WealthStory(self):
        """财富故事"""
        self.AgentRequest.WealthStory()

    def test_WealthStoryParticulars(self):
        """财富故事详情"""
        self.AgentRequest.WealthStory()
        self.AgentRequest.WealthStoryParticulars()

    def test_TheSoundOfHappinessOrTheVoiceOfTheCityAndParticulars(self):
        """获取幸福之声和者城市之声-----及详情"""
        dome = ['0', cityId]
        z = 0
        while z < len(dome):
            self.AgentRequest.TheSoundOfHappinessOrTheVoiceOfTheCity(cityId=dome[z])
            self.AgentRequest.TheSoundOfHappinessOrTheVoiceOfTheCityParticulars()
            z = z + 1

    def test_HappySchool(self):
        """幸福学堂"""
        self.AgentRequest.HappySchool()

    def test_Activity(self):
        """活动"""
        self.AgentRequest.Activity()

    def test_TheCityData(self):
        """获取城市数据"""
        self.AgentRequest.TheCityData()

    def test_HomeHouseList(self):
        """首页显示列表（财富故事/本地新房/全国旅居/海外地产/活动海报）"""
        self.AgentRequest.HomeHouseList()

    def test_KeywordNewHouse(self):
        """关键字搜索新房"""
        self.AgentRequest.KeywordNewHouse()

    def test_HappinessHeadlines(self):
        """幸福头条"""
        self.AgentRequest.HappinessHeadlines()

    def test_TheHeadlineForDetails(self):
        """头条详情"""
        self.AgentRequest.HappinessHeadlines()
        self.AgentRequest.TheHeadlineForDetails()
