# 第一步 导入unittest模块
from XFJ.PubilcAPI.FlowPath import *

# 第二步 编写测试用例


class FlowTestCase(unittest.TestCase):
    """我的测试用例类"""

    def __init__(self, *args, **kwargs):
        super(FlowTestCase, self).__init__(*args, **kwargs)
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

    # 测试用例方法必须用test开头

    def test_001_attache_list(self):
        """获取专员列表"""
        # 开始时间、结束时间、第几页、等级、状态、时间：3、7、15、 历史条数
        self.XfkRequest.AttacheList()
        self.assertNotEqual(self.XfkTEXT.get('XFKTotal'), 0)

    def test_002_recommend_new(self):
        """推荐新房"""
        self.AgentRequest.RecommendNew()

    def test_003_guest_status_attache_1(self):
        """查看刚报名的数据：状态是否为：待处理"""
        self.XfkRequest.AttacheList()
        self.assertNotEqual(self.XfkTEXT.get('XFKTotal'), 0)
        globals()['applyId'] = self.XfkTEXT.get('applyId')
        self.XfkRequest.AttacheList(Status='1')
        self.assertNotEqual(self.XfkTEXT.get('XFKTotal'), 0)
        self.assertEqual(globals()['applyId'], self.XfkTEXT.get('applyId'))

    def test_004_level_select(self):
        """等级的筛选
            随机选择:a、b、c"""
        self.XfkRequest.AttacheList()
        self.assertNotEqual(self.XfkTEXT.get('XFKTotal'), 0)
        globals()['applyId'] = self.XfkTEXT.get('applyId')
        self.XfkRequest.RandomString(['a', 'b', 'c'])
        self.XfkRequest.AttacheOperation(content='修改等级状态',
                                         Level=self.XfkTEXT.get('Random'))
        self.assertEqual("操作成功", self.XfkTEXT.get('content'))
        self.XfkRequest.AttacheList(Level=self.XfkTEXT.get('Random'))
        self.assertEqual(globals()['applyId'], self.XfkTEXT.get('applyId'))

    def test_005_guest_status_attache_2(self):
        """修改好状态后：待处理及待上门都有最新推荐的信息"""
        self.XfkRequest.AttacheList(Status='2')
        globals()['applyId'] = self.XfkTEXT.get('applyId')
        self.XfkRequest.AttacheList()
        self.assertEqual(self.XfkTEXT.get('applyId'), globals()['applyId'])

    def test_006_days_select(self):
        """时间的筛选
        随机选择：3天、7天、15天"""
        self.XfkRequest.AttacheList()
        globals()['applyId'] = self.XfkTEXT.get('applyId')
        self.XfkRequest.RandomString(['3', '7', '15'])
        self.XfkRequest.AttacheList(Days=self.XfkTEXT.get('Random'))
        self.assertEqual(self.XfkTEXT.get('applyId'), globals()['applyId'])

    def test_007_diy_time(self):
        """自定义时间的选择：当前年月日"""
        self.XfkRequest.AttacheList()
        applyid = self.XfkTEXT.get('applyId')
        self.XfkRequest.AttacheList(StartTime=time.strftime('%Y-%m-%d'), EndTime=time.strftime('%Y-%m-%d'))
        self.assertEqual(applyid, self.XfkTEXT.get('applyId'))

    def test_008_follow_guest_content_is_null(self):
        """验客跟进：内容为空"""
        self.XfkRequest.AttacheList()
        self.XfkRequest.AttacheOperation(content='')
        self.assertEqual("内容不能为空", self.XfkTEXT.get('content'))

    def test_009_follow_guest_content_is_long(self):
        """验客跟进：内容过长"""
        self.XfkRequest.AttacheOperation(content=ContentLong)
        self.assertEqual("跟进内容过长", self.XfkTEXT.get('content'))

    def test_010_follow_guest_content_is_(self):
        """验客跟进：内容不能为特殊字符"""
        self.XfkRequest.AttacheOperation(content='✿.｡.:*')
        self.assertEqual("不能含有表情等特殊字符", self.XfkTEXT.get('content'))

    def test_011_follpw_guest_content_is_true(self):
        """验客跟进：正常验客"""
        self.XfkRequest.AttacheOperation()
        self.assertEqual("操作成功", self.XfkTEXT.get('content'))

    def test_012_verification_follow_guest(self):
        """查看跟进内容是否以之前一致"""
        self.XfkRequest.AttacheList()
        self.XfkRequest.ExamineClientParticulars()
        self.assertEqual('测试数据', self.XfkTEXT.get('content'))

    def test_013_allocation_houses(self):
        """报备分配"""
        self.XfkRequest.AttacheOperation(content='报备分配', SalesId=self.XfkTEXT.get('xfkSalesId'))
        self.XfkRequest.ExamineClientParticulars()
        self.assertEqual('报备分配', self.XfkTEXT.get('content'))

    def test_014_guest_status_attache_3(self):
        """查看刚分配的状态"""
        self.XfkRequest.AttacheList(Status='2')
        globals()['applyId'] = self.XfkTEXT.get('applyId')
        self.XfkRequest.AttacheList(Status='3')
        self.assertNotEqual(globals()['applyId'], self.XfkTEXT.get('applyId'))

    def test_015_houses_list_status(self):
        """验证售楼员列表"""
        self.XfkRequest.HousesList()
        globals()['applyId'] = self.XfkTEXT.get('applyId')
        self.XfkRequest.HousesList(Status='2')
        self.assertEqual(globals()['applyId'], self.XfkTEXT.get('applyId'))

    def test_016_phone_follow_house(self):
        """电话跟进"""
        self.XfkRequest.HousesOperation(content='电话跟进', FollowType=1)
        self.XfkRequest.ExamineClientParticulars()
        self.assertEqual('电话跟进', self.XfkTEXT.get('content'))

    def test_017_verification_status_1(self):
        """验证状态"""
        self.XfkRequest.HousesList()
        globals()['applyId'] = self.XfkTEXT.get('applyId')
        self.XfkRequest.HousesList(Status=2)
        self.assertEqual(self.XfkTEXT.get('applyId'), globals()['applyId'])

    def test_018_visit_follow(self):
        """上门跟进"""
        self.XfkRequest.HousesOperation(content='上门跟进')
        self.XfkRequest.ExamineClientParticulars()
        self.assertEqual('上门跟进', self.XfkTEXT.get('content'))

    def test_019_verification_status_2(self):
        """验证状态：分别在专员列表、售楼员列表"""
        self.XfkRequest.AttacheList()
        globals()['applyId'] = self.XfkTEXT.get('applyId')
        self.XfkRequest.AttacheList(Status=3)
        self.assertEqual(self.XfkTEXT.get('applyId'), globals()['applyId'])
        self.XfkRequest.HousesList()
        self.assertEqual(self.XfkTEXT.get('applyId'), globals()['applyId'])
        self.XfkRequest.HousesList(3)
        self.assertEqual(self.XfkTEXT.get('applyId'), globals()['applyId'])

    def test_020_contract(self):
        """签约"""
        self.XfkRequest.ProjectExpect()
        self.XfkRequest.HouseType()
        self.XfkRequest.ContractAgo()
        self.XfkRequest.AttacheContract()

    def test_021_contract_later_verify_state(self):
        """签约之后 验证状态"""
        self.XfkRequest.AttacheList()
        globals()['applyid'] = self.XfkTEXT.get('applyId')
        self.XfkRequest.AttacheList(Status=4)
        globals()['applyid1'] = self.XfkTEXT.get('applyId')
        self.XfkRequest.HousesList(Status=4)
        self.assertEqual(globals()['applyid'], self.XfkTEXT.get('applyId'), globals()['applyid1'])

    def test_022_contract_later_verify_state_5(self):
        """签约之后  验证是否为已结佣"""
        print('签约之后  验证是否为已结佣  暂未写入')

    def test_verify_state_is_termination(self):
        """验证跟进 无效处理 并且进行验证"""
        self.AgentRequest.RecommendNew()
        self.XfkRequest.AttacheList()
        globals()['applyId'] = self.XfkTEXT.get('applyId')
        self.XfkRequest.AttacheOperation(content='无效终止', FollowConclusion=0)
        self.XfkRequest.AttacheList(Status=6)
        self.assertEqual(self.XfkTEXT.get('applyId'), globals()['applyId'])

    def test_Report_not_approved(self):
        """报备不通过, 在售楼员列表验证是否存在"""
        self.AgentRequest.RecommendNew()
        self.XfkRequest.AttacheList()
        globals()['applyId'] = self.XfkTEXT.get('applyId')
        self.XfkRequest.AttacheOperation(content='报备分配不通过', FollowConclusion=0)
        self.XfkRequest.ExamineClientParticulars()
        self.assertEqual('报备分配不通过', self.XfkTEXT.get('content'))
        self.XfkRequest.HousesList()
        self.assertNotEqual(globals()['applyId'], self.XfkTEXT.get('applyId'))

    def test_Phone_not_approved(self):
        """电话跟进，无效终止"""
        self.AgentRequest.RecommendNew()
        self.XfkRequest.AttacheList()
        self.XfkRequest.ExamineClientParticulars()
        self.XfkRequest.AttacheOperation(SalesId=self.XfkTEXT.get('xfkSalesId'))
        self.XfkRequest.HousesOperation(content='电话跟进，无效终止', FollowConclusion=0, FollowType=1)
        self.XfkRequest.ExamineClientParticulars()
        self.assertEqual('电话跟进，无效终止', self.XfkTEXT.get('content'))

    def test_door_not_approved(self):
        """上门跟进，无效终止"""
        self.AgentRequest.RecommendNew()
        self.XfkRequest.AttacheList()
        self.XfkRequest.ExamineClientParticulars()
        self.XfkRequest.AttacheOperation(SalesId=self.XfkTEXT.get('xfkSalesId'))
        self.XfkRequest.HousesOperation(content='上门跟进，无效终止', FollowConclusion=0, FollowType=2)
        self.XfkRequest.ExamineClientParticulars()
        self.assertEqual('上门跟进，无效终止', self.XfkTEXT.get('content'))
