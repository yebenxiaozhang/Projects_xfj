"""经纪人---推荐新房"""
# 第一步 导入unittest模块
from XFJ.PubilcAPI.AgentAPI import *
import unittest
from XFJ.PubilcAPI.XfkApi import *
"""
非全号是否推荐成功
全号是否推荐成功
不输入姓名是否推荐成功
不输入手机号码是否推荐成功
输入的手机号码异常（非数字）是否有相应的提示
重复推荐是否有相应的提示

"""


class RecommendTestCase(unittest.TestCase):
    """推荐新房"""

    def __init__(self, *args, **kwargs):
        super(RecommendTestCase, self).__init__(*args, **kwargs)
        self.do_request = AgentApi()
        self.to_request = self.do_request
        self.AgentTEXT = GlobalMap()
        self.Xfk_do_request = XfkApi()
        self.Xfk_to_request = self.Xfk_do_request
        self.XfkTEXT = GlobalMap()

    @classmethod
    def setUpClass(cls):
        """登录小秘 只执行一次"""
        cls.do_request = AgentApi()
        cls.to_request = cls.do_request
        cls.to_request.LoginAgent()
        cls.Xfk_do_request = XfkApi()
        cls.Xfk_to_request = cls.Xfk_do_request
        cls.Xfk_to_request.LoginXfk()

    @classmethod
    def tearDownClass(cls):
        """所用用例执行之后的操作"""
        pass

    def setUp(self):
        """用例开始前"""
        self.to_request.ForRegistrationID()
        self.to_request.Client(status=0)

    def tearDown(self):
        """用例执行之后"""
        try:
            self.Xfk_to_request.AttacheList(StartTime='', EndTime='', Page=1, Level='', Status=None, Days=None)
            self.Xfk_to_request.AttacheOperation(content='报名后立即终止',
                                                 FollowConclusion=0, Level='c', SalesId=None, TureOrFalse='0')

            self.assertEqual('操作成功', self.XfkTEXT.get('content'))
        except BaseException as e:
            print("断言错误：%s" % e)
            raise RuntimeError(self.AgentTEXT.get('Agenturl'))

    def test_HoneKongNo(self):
        """香港非全号---后4"""
        try:
            self.to_request.RecommendNew(phone=(str(852) + '***' +
                                                (str(self.AgentTEXT.get('applyId'))[-5:])))
            self.assertEqual('报名成功！', self.AgentTEXT.get('Agentcontent'))

        except BaseException as e:
            print("断言错误：%s" % e)
            raise RuntimeError(self.AgentTEXT.get('Agenturl'))
    #
    # def test_HoneKongNo1(self):
    #     """香港非全号---前二后3"""
    #     try:
    #         self.to_request.RecommendNew(
    #                                      phone=(str(852) + str(18) + '***' +
    #                                             (str(self.AgentTEXT.get('applyId'))[-3:])))
    #         self.assertEqual('报名成功！', self.AgentTEXT.get('Agentcontent'))
    #
    #     except BaseException as e:
    #         print("断言错误：%s" % e)
    #         raise RuntimeError(self.AgentTEXT.get('Agenturl'))

    def test_HoneKong(self):
        """香港全号"""
        try:
            self.to_request.RecommendNew(
                                         phone=((str(852) + str(PhoneFront[:4])) +
                                                (str(self.AgentTEXT.get('applyId'))[-4:])))
            self.assertEqual('报名成功！', self.AgentTEXT.get('Agentcontent'))

        except BaseException as e:
            print("断言错误：%s" % e)
            raise RuntimeError(self.AgentTEXT.get('Agenturl'))

    def test_MacaoNo(self):
        """澳门非全号------后4"""
        try:
            self.to_request.RecommendNew(
                                         phone=(str(853) + '****' +
                                                (str(self.AgentTEXT.get('applyId'))[-4:])))
            self.assertEqual('报名成功！', self.AgentTEXT.get('Agentcontent'))

        except BaseException as e:
            print("断言错误：%s" % e)
            raise RuntimeError(self.AgentTEXT.get('Agenturl'))

    def test_Macao(self):
        """澳门全号"""
        try:
            self.to_request.RecommendNew(
                                         phone=((str(852) + str(PhoneFront[:4])) +
                                                (str(self.AgentTEXT.get('applyId'))[-4:])))
            self.assertEqual('报名成功！', self.AgentTEXT.get('Agentcontent'))

        except BaseException as e:
            print("断言错误：%s" % e)
            raise RuntimeError(self.AgentTEXT.get('Agenturl'))

    def test_MainlandNo(self):
        """大陆非全号---前三后5"""
        try:
            self.to_request.RecommendNew(
                                         phone=(str(PhoneFront[:3])) + '***' +
                                               (str(self.AgentTEXT.get('applyId'))[-5:]))
            self.assertEqual('报名成功！', self.AgentTEXT.get('Agentcontent'))

        except BaseException as e:
            print("断言错误：%s" % e)
            raise RuntimeError(self.AgentTEXT.get('Agenturl'))

    def test_Mainland(self):
        """大陆全号"""
        try:
            self.to_request.RecommendNew(
                                         phone=PhoneFront + str(self.AgentTEXT.get('applyId')))
            self.assertEqual('报名成功！', self.AgentTEXT.get('Agentcontent'))

        except BaseException as e:
            print("断言错误：%s" % e)
            raise RuntimeError(self.AgentTEXT.get('Agenturl'))

    def test_LessThanEleven(self):
        """小于11位"""
        try:
            self.to_request.RecommendNew(
                                         phone=((str(852) + str(PhoneFront[:2])) + '**' +
                                                (str(self.AgentTEXT.get('applyId'))[-3:])))
            self.assertEqual('请使用：手机号8位报备、手机号后5位报备',
                             self.AgentTEXT.get('Agentcontent'))
            self.to_request.RecommendNew(
                                         phone=(str(PhoneFront[:3])) + '****' +
                                               (str(self.AgentTEXT.get('applyId'))[-3:]))
            self.assertEqual('请使用：手机号11位报备、手机号前3后5报备',
                             self.AgentTEXT.get('Agentcontent'))

        except BaseException as e:
            print("断言错误：%s" % e)
            raise RuntimeError(self.AgentTEXT.get('Agenturl'))

    def test_GreaterThanEleven(self):
        """大于11位"""
        try:
            self.to_request.RecommendNew(
                                         phone=(str(852) + '****' +
                                                (str(self.AgentTEXT.get('applyId'))[-5:])))
            self.assertEqual('请使用：手机号11位报备、手机号前后4报备、手机号前2后3报备',
                             self.AgentTEXT.get('Agentcontent'))
            self.to_request.RecommendNew(
                                         phone=(str(PhoneFront[:3])) + '****' +
                                               (str(self.AgentTEXT.get('applyId'))[-5:]))
            self.assertEqual('请使用：手机号11位报备、手机号前3后5报备',
                             self.AgentTEXT.get('Agentcontent'))

        except BaseException as e:
            print("断言错误：%s" % e)
            raise RuntimeError(self.AgentTEXT.get('Agenturl'))

    def test_PhoneIsNull(self):
        """手机号为空"""
        try:
            self.to_request.RecommendNew(phone='')
            self.assertEqual('手机号不能为空', self.AgentTEXT.get('Agentcontent'))

        except BaseException as e:
            print("断言错误：%s" % e)
            raise RuntimeError(self.AgentTEXT.get('Agenturl'))

    def test_PhoneEroor(self):
        """手机号异常（非数字）"""
        try:
            self.to_request.RecommendNew(
                                         phone='呵呵哒')
            self.assertEqual('请使用：手机号11位报备、手机号前3后5报备',
                             self.AgentTEXT.get('Agentcontent'))
            self.to_request.RecommendNew(
                                         phone='(*￣︶￣)')
            self.assertEqual('请使用：手机号11位报备、手机号前3后5报备',
                             self.AgentTEXT.get('Agentcontent'))
            self.to_request.RecommendNew(
                                         phone='😘')
            self.assertEqual('请使用：手机号11位报备、手机号前3后5报备',
                             self.AgentTEXT.get('Agentcontent'))

        except BaseException as e:
            print("断言错误：%s" % e)
            raise RuntimeError(self.AgentTEXT.get('Agenturl'))

    def test_RepeatTheRegistration(self):
        """重复报名"""
        try:
            self.to_request.RecommendNew(
                                         phone=PhoneFront + str(self.AgentTEXT.get('applyId')))
            self.assertEqual('报名成功！', self.AgentTEXT.get('Agentcontent'))
            self.to_request.RecommendNew(
                                         phone=PhoneFront + str(self.AgentTEXT.get('applyId')))
            self.assertEqual('已经报名！', self.AgentTEXT.get('Agentcontent'))

        except BaseException as e:
            print("断言错误：%s" % e)
            raise RuntimeError(self.AgentTEXT.get('Agenturl'))








