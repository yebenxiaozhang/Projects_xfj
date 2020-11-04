"""幸福小秘---客户
    幸福小秘---业绩报表"""
# 第一步 导入unittest模块
from XFJ.PubilcAPI.FlowPath import *
# 第二步 编写测试用例
"""客户列表的需求
推荐 无任何要求 
上门 上门失败不记录在此  算在推荐
成交 挞定过的不记录在此  算在上门
"""
"""
新增一条推荐 查看客户列表是否有新增
推荐后无效客户  查看客户列表是否有新增
新增一条上门 查看客户列表是否有新增
上门无效  查看客户列表是否有新增
新增一条成交 查看客户列表是否有新增
成交挞定  查看客户列表是否有新增
一个成交的客户是否存在上门列表、推荐列表
一个上门列表 是否也存在推荐列表
是否存在  一个在推荐也在成交 不会存在上门的列表
"""


class ClientTestCase(unittest.TestCase):
    """小秘——客户列表"""

    def __init__(self, *args, **kwargs):
        super(ClientTestCase, self).__init__(*args, **kwargs)
        self.XM_request = XmApi()
        self.XFK_request = XfkApi()
        self.XmTEXT = GlobalMap()
        self.XfkTEXT = GlobalMap()
        self.Flow = FlowPath()
        self.FlowPath = self.Flow

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
        cls.xfk = XfkApi()
        cls.XFKRequest = cls.xfk
        cls.XFKRequest.LoginXfk()

    def test_ClientList(self):
        """新增一条推荐 查看客户列表是否有新增 及业绩汇总"""
        self.WhetherPlusOneAgo(clientType=1, keyWork='推荐')
        """登录幸福客、获取专员列表、获取报名团ID"""
        self.XFK_request.AttacheList(StartTime='', EndTime='', Page='1', Level='', Status='', Days='')
        """推荐报名"""
        self.AgentRequest.RecommendNew()
        try:
            self.assertEqual('报名成功！', self.XfkTEXT.get('Agentcontent'))
        except BaseException as e:
            print("断言错误，错误原因：%s" % e)
            raise RuntimeError(self.XmTEXT.get('xmurl'))
        self.WhetherPlusOneRear(clientType=1, keyWork='推荐', Value=1)

    def test_Recommend_Disable(self):
        """推荐后无效客户  查看客户列表是否有新增"""
        self.WhetherPlusOneAgo(clientType=1, keyWork='推荐')
        """登录幸福客、获取专员列表、验客失败"""
        self.XFK_request.AttacheList(StartTime='', EndTime='', Page='1', Level='', Status='', Days='')
        self.XFK_request.AttacheOperation(content='验客跟进:无效终止',
                                          FollowConclusion=0, Level='a', SalesId=None, TureOrFalse=None)
        time.sleep(1)
        self.WhetherPlusOneRear(clientType=1, keyWork='推荐', Value=0)

    def test_Recommend_Visit(self):
        """新增一条上门 查看客户列表是否有新增"""
        self.WhetherPlusOneAgo(clientType=2, keyWork='上门')
        """登录幸福客、获取专员列表、获取报名团ID"""
        self.XFK_request.AttacheList(StartTime='', EndTime='', Page='1', Level='', Status='', Days='')
        """推荐报名"""
        try:
            self.AgentRequest.RecommendNew()
            self.assertEqual('报名成功！', self.XfkTEXT.get('Agentcontent'))
        except BaseException as e:
            print("断言错误，错误原因：%s" % e)
            raise RuntimeError(self.XmTEXT.get('xmurl'))
        """获取专员列表、查看客户详情（读取售楼员ID）、报备分配"""
        self.XFK_request.AttacheList(StartTime='', EndTime='', Page='1', Level='', Status='', Days='')
        self.XFK_request.ExamineClientParticulars()
        self.XFK_request.AttacheOperation(content='报备分配->成功',
                                          FollowConclusion=1,
                                          Level='a',
                                          SalesId=self.XfkTEXT.get('xfkSalesId'),
                                          TureOrFalse=1)
        """上门跟进"""
        self.XFK_request.HousesOperation(content='上门跟进->成功', FollowConclusion=1,
                                         Level='a', FollowType=2)
        self.WhetherPlusOneRear(clientType=2, keyWork='上门', Value=1)

    def test_Recommend_Visit_Disable(self):
        """上门无效  查看客户列表是否有新增"""
        self.WhetherPlusOneAgo(clientType=2, keyWork='上门')
        """登录幸福客、获取专员列表、获取报名团ID"""
        self.XFK_request.AttacheList(StartTime='', EndTime='', Page='1', Level='', Status='', Days='')
        """推荐报名"""
        self.AgentRequest.RecommendNew()
        self.assertEqual('报名成功！', self.XfkTEXT.get('Agentcontent'))
        """获取专员列表、查看客户详情（读取售楼员ID）、报备分配"""
        self.XFK_request.AttacheList(StartTime='', EndTime='', Page='1', Level='', Status='', Days='')
        self.XFK_request.ExamineClientParticulars()
        self.XFK_request.AttacheOperation(content='报备分配->成功',
                                          FollowConclusion=1,
                                          Level='a',
                                          SalesId=self.XfkTEXT.get('xfkSalesId'),
                                          TureOrFalse=1)
        """上门跟进"""
        self.XFK_request.HousesOperation(content='上门跟进->失败', FollowConclusion=0,
                                         Level='a', FollowType=2)
        self.WhetherPlusOneRear(clientType=2, keyWork='上门', Value=0)

    def test_Add_Contract(self):
        """新增一条成交 查看客户列表是否有新增"""
        self.WhetherPlusOneAgo(clientType=3, keyWork='成交')
        self.FlowPath.TheNewDeal()
        self.WhetherPlusOneRear(clientType=3, keyWork='成交', Value=1)

    def test_Contract_Tart_set(self):
        """成交挞定  查看客户列表是否有新增"""
        self.WhetherPlusOneAgo(clientType=3, keyWork='成交')
        self.FlowPath.TheNewDeal()
        self.XmRequest.DealTicketList()
        self.XmRequest.DealCancellation(checkingRemark='小秘挞定' + time.strftime("%Y-%m-%d"))
        self.assertEqual(1, self.XmTEXT.get('resultCode'))
        self.WhetherPlusOneRear(clientType=3, keyWork='成交', Value=0)

    def test_List_Issue(self):
        """
        一个成交的客户是否存在上门列表、推荐列表
        一个上门列表 是否也存在推荐列表
        一个成交的客户是否存在上门列表、推荐列表"""
        x = 3
        y = 2
        z = 0
        while z != 2:
            self.XM_request.Client_list(clientType=x)
            globals()['r.text'] = json.loads(self.XmTEXT.get('xmtext'))
            globals()['agentId'] = globals()['r.text']['extend']['sources'][0]['agentId']
            self.XM_request.Client_list(clientType=y)
            globals()['r.text'] = json.loads(self.XmTEXT.get('xmtext'))
            a = 0
            while globals()['agentId'] != globals()['r.text']['extend']['sources'][a]['agentId']:
                a = a + 1
                if self.XmTEXT.get('xmcount') == a:
                    break
                pass
            z = z + 1
            x = x - 1
            y = y - 1
        print('是否存在  一个在推荐也在成交 不会存在上门的列表、尚未写入自动化')

    def WhetherPlusOneAgo(self, clientType, keyWork):
        """是否加1前"""
        if keyWork == '上门':
            parameter = 'xmvisitCount'
            pass
        elif keyWork == '成交':
            parameter = 'xmdealCount'
        else:
            parameter = 'xmapplyCount'
        self.XM_request.Client_list(clientType=clientType)
        globals()['count-a'] = self.XmTEXT.get('xmcount')
        self.XM_request.ResultsSummary(keyWork=keyWork)
        globals()['xmday-a'] = self.XmTEXT.get('xmday')
        self.XM_request.UnionMonthly()
        self.XmTEXT.get(f'{parameter}')
        globals()[f'{parameter}-a'] = self.XmTEXT.get(f'{parameter}')
        self.XM_request.ProjectMonthly()
        globals()[f'{parameter}-b'] = self.XmTEXT.get(f'{parameter}')

    def WhetherPlusOneRear(self, clientType, keyWork, Value):
        """是否加1后"""
        """客户列表、业绩汇总、联盟商月报、项目月报"""
        try:
            """客户列表---7天内"""
            self.XM_request.Client_list(clientType=clientType)
            self.assertEqual((globals()['count-a'] + Value),
                             self.XmTEXT.get('xmcount'))
            """业绩汇总---今日"""
            self.XM_request.ResultsSummary(keyWork=keyWork)
            self.assertEqual(globals()['xmday-a'] + Value, self.XmTEXT.get('xmday'))
            if keyWork == '上门':
                parameter = 'xmvisitCount'
                pass
            elif keyWork == '成交':
                parameter = 'xmdealCount'
            else:
                parameter = 'xmapplyCount'
            """联盟商月报---总数"""
            self.XM_request.UnionMonthly()
            self.assertEqual(globals()[f'{parameter}-a'] + Value, self.XmTEXT.get(f'{parameter}'))
            """项目月报---总数"""
            self.XM_request.ProjectMonthly()
            self.assertEqual(globals()[f'{parameter}-b'] + Value, self.XmTEXT.get(f'{parameter}'))
        except BaseException as e:
            print("断言错误，错误原因：%s" % e)
            raise RuntimeError(self.XmTEXT.get('xmurl'))

