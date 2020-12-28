"""财富值-相关"""
from PubilcAPI.flowPath import *
"""
1、拨打时间在超时前---增加财富值(上传时间再超时后)
2、正常首电-----------增加财富值
3、超时首电-----------扣除财富值
4、线索转移过后------进行首电|跟进  不增加首电及时率财富值
5、公海领取--立即写一个跟进 --增加财富值
6、新增线索-立即写一个跟进
"""


class TestCase(unittest.TestCase):
    """客第壹——财富值"""

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
        cls.appApi.Login()
        cls.appApi.GetUserData()
        cls.request = webApi()
        cls.webApi = cls.request
        cls.webApi.Audit_management()
        cls.webApi.auditList()
        while cls.appApi.appText.get('web_total') != 0:
            cls.webApi.audit(auditStatue=2, auditRemark=' 审核失败')
            cls.webApi.auditList()
        cls.webApi.auditList(auditLevel=2)
        while cls.appApi.appText.get('web_total') != 0:
            cls.webApi.audit(auditStatue=2, auditRemark=' 审核失败')
            cls.webApi.auditList(auditLevel=2)
        cls.do_request = appApi()
        cls.appApi = cls.do_request
        cls.appApi.Login(authCode=1)

        cls.flow = flowPath()
        cls.flowPath = cls.flow
        cls.appText = GlobalMap()
        cls.request = webApi()
        cls.webApi = cls.request
        cls.appApi.GetUserData()
        cls.webApi.Audit_management()

        """去除一些客户及线索"""
        cls.appApi.my_clue_list()
        while cls.appText.get('total') >= 2:
            cls.flowPath.clue_exile_sea()
            cls.appApi.my_clue_list()

        cls.appApi.ClientList()
        while cls.appText.get('total') >= 2:
            cls.appApi.client_exile_sea()
            cls.appApi.ClientList()

    def test_wealth_01(self):
        """1、拨打时间在超时前---增加财富值(上传时间再超时后)"""
        self.appApi.ClueSave(clueNickName=self.appApi.RandomText(textArr=surname),
                             sourceId=self.appApi.appText.get('XSLY'),
                             keyWords=self.appApi.appText.get('XSBQ'))
        dome1 = time.strftime("%Y-%m-%d %H:%M:%S")
        time.sleep(60)
        self.appApi.phone_log(callee_num=self.appText.get('cluePhone'), talk_time=12000,
                              call_time=dome1)
        self.appApi.getWealthDetailList(startTime=time.strftime("%Y-%m-%d"),
                                        endTime=time.strftime("%Y-%m-%d"),
                                        wealthType=self.appText.get('SDJSL'),
                                        orderNo=self.appText.get('orderNo'))
        if self.appText.get('vlue') != 10:
            print(self.appText.get('orderNo'))
            raise RuntimeError('拨打再超时前，上传超时算首电及时')

    def test_wealth_02(self):
        """2、正常首电-----------增加财富值"""
        self.appApi.ClueSave(clueNickName=self.appApi.RandomText(textArr=surname),
                             sourceId=self.appApi.appText.get('XSLY'),
                             keyWords=self.appApi.appText.get('XSBQ'))
        dome1 = time.strftime("%Y-%m-%d %H:%M:%S")
        self.appApi.phone_log(callee_num=self.appText.get('cluePhone'), talk_time=12000,
                              call_time=dome1)
        self.appApi.getWealthDetailList(startTime=time.strftime("%Y-%m-%d"),
                                        endTime=time.strftime("%Y-%m-%d"),
                                        wealthType=self.appText.get('SDJSL'),
                                        orderNo=self.appText.get('orderNo'))
        if self.appText.get('vlue') != 10:
            print(self.appText.get('orderNo'))
            raise RuntimeError('2、正常首电-----------增加财富值')
        """4、线索转移过后------进行首电|跟进  不增加首电及时率财富值"""
        self.appApi.ClueChange()
        self.appApi.Login(userName=XfpUser1)
        self.appApi.GetUserData()
        dome1 = time.strftime("%Y-%m-%d %H:%M:%S")
        self.appApi.phone_log(callee_num=self.appText.get('cluePhone'), talk_time=12000,
                              call_time=dome1, is_me=2)
        self.appApi.getWealthDetailList(startTime=time.strftime("%Y-%m-%d"),
                                        endTime=time.strftime("%Y-%m-%d"),
                                        wealthType=self.appText.get('SDJSL'),
                                        orderNo=self.appText.get('orderNo'))
        if self.appText.get('vlue') != 0:
            print(self.appText.get('orderNo'))
            raise RuntimeError('已首电转移过后不能在加财富值')

    def test_wealth_03(self):
        """3、超时首电-----------扣除财富值"""
        self.appApi.Login()
        self.appApi.GetUserData()
        self.appApi.ClueSave(clueNickName=self.appApi.RandomText(textArr=surname),
                             sourceId=self.appApi.appText.get('XSLY'),
                             keyWords=self.appApi.appText.get('XSBQ'))
        dome = (datetime.datetime.now() + datetime.timedelta(minutes=2)).strftime("%Y-%m-%d %H:%M:%S")
        self.appApi.phone_log(callee_num=self.appText.get('cluePhone'), talk_time=12000,
                              call_time=dome)
        self.appApi.getWealthDetailList(startTime=time.strftime("%Y-%m-%d"),
                                        endTime=time.strftime("%Y-%m-%d"),
                                        wealthType=self.appText.get('SDJSL'),
                                        orderNo=self.appText.get('orderNo'))
        if self.appText.get('vlue') != -5:
            print(self.appText.get('orderNo'))
            raise RuntimeError('3、超时首电-----------扣除财富值')

    def test_wealth_04(self):
        """公海领取-首电|写跟进"""
        self.appApi.SeaList()  # 公海列表
        self.appApi.clue_Assigned()  # 领取线索
        self.appApi.my_clue_list()  # 线索列表
        self.appApi.ClueInfo()
        try:
            dome1 = time.strftime("%Y-%m-%d %H:%M:%S")
            self.appApi.phone_log(callee_num=self.appText.get('cluePhone'), talk_time=12000,
                                  call_time=dome1)
        except:
            self.appApi.ClueFollowList()
            self.appApi.ClueFollowSave(taskEndTime=time.strftime("%Y-%m-%d") + ' 22:00:00')

        self.appApi.getWealthDetailList(startTime=time.strftime("%Y-%m-%d"),
                                        endTime=time.strftime("%Y-%m-%d"),
                                        wealthType=self.appText.get('SDJSL'),
                                        orderNo=self.appText.get('orderNo'))
        if self.appText.get('vlue') != 10:
            print(self.appText.get('orderNo'))
            raise RuntimeError('公海领取-首电|写跟进 及时跟进 没有加财富值')

    def test_wealth_05(self):
        """在超时前写跟进 要有及时率奖励"""
        self.appApi.ClueSave(clueNickName=self.appApi.RandomText(textArr=surname),
                             sourceId=self.appApi.appText.get('XSLY'),
                             keyWords=self.appApi.appText.get('XSBQ'))
        self.appApi.my_clue_list()  # 线索列表
        self.appApi.ClueFollowList()
        time.sleep(20)
        self.appApi.ClueFollowSave(taskEndTime=time.strftime("%Y-%m-%d") + ' 22:00:00')
        self.appApi.getWealthDetailList(startTime=time.strftime("%Y-%m-%d"),
                                        endTime=time.strftime("%Y-%m-%d"),
                                        wealthType=self.appText.get('SDJSL'),
                                        orderNo=self.appText.get('orderNo'))
        if self.appText.get('vlue') != 10:
            print(self.appText.get('orderNo'))
            raise RuntimeError('首电及时率在超时前写跟进 要有及时率奖励')

    def test_wealth_06(self):
        """首电及时奖励为0 及时跟进"""
        self.webApi.Audit_management(firstCallDayWealth=0)
        self.appApi.ClueSave(clueNickName=self.appApi.RandomText(textArr=surname),
                             sourceId=self.appApi.appText.get('XSLY'),
                             keyWords=self.appApi.appText.get('XSBQ'))
        self.appApi.my_clue_list()  # 线索列表
        self.appApi.ClueFollowList()
        self.appApi.ClueFollowSave(taskEndTime=time.strftime("%Y-%m-%d") + ' 22:00:00')
        self.appApi.getWealthDetailList(startTime=time.strftime("%Y-%m-%d"),
                                        endTime=time.strftime("%Y-%m-%d"),
                                        wealthType=self.appText.get('SDJSL'),
                                        orderNo=self.appText.get('orderNo'))
        if self.appText.get('vlue') != 0:
            print(self.appText.get('orderNo'))
            raise RuntimeError('首电及时奖励为0 及时跟进 奖励应该为0')

    # def test_wealth_07(self):
    #     """首电及时奖励为0 30秒后跟进"""
    #     self.webApi.Audit_management(firstCallDayWealth=0)
    #     self.appApi.ClueSave(clueNickName=self.appApi.RandomText(textArr=surname),
    #                          sourceId=self.appApi.appText.get('XSLY'),
    #                          keyWords=self.appApi.appText.get('XSBQ'))
    #     self.appApi.my_clue_list()  # 线索列表
    #     self.appApi.ClueFollowList()
    #     time.sleep(35)
    #     self.appApi.ClueFollowSave(taskEndTime=time.strftime("%Y-%m-%d") + ' 22:00:00')
    #     self.appApi.getWealthDetailList(startTime=time.strftime("%Y-%m-%d"),
    #                                     endTime=time.strftime("%Y-%m-%d"),
    #                                     wealthType=self.appText.get('SDJSL'),
    #                                     orderNo=self.appText.get('orderNo'))
    #     if self.appText.get('vlue') != 0:
    #         print(self.appText.get('orderNo'))
    #         raise RuntimeError('首电及时奖励为0 超时前跟进 应该为0或者空')

    def test_wealth_08(self):
        """首电及时奖励为0 超时跟进"""
        self.webApi.Audit_management(firstCallDayWealth=0)
        self.appApi.ClueSave(clueNickName=self.appApi.RandomText(textArr=surname),
                             sourceId=self.appApi.appText.get('XSLY'),
                             keyWords=self.appApi.appText.get('XSBQ'))
        self.appApi.my_clue_list()  # 线索列表
        self.appApi.ClueFollowList()
        time.sleep(60)
        self.appApi.ClueFollowSave(taskEndTime=time.strftime("%Y-%m-%d") + ' 22:00:00')
        self.appApi.getWealthDetailList(startTime=time.strftime("%Y-%m-%d"),
                                        endTime=time.strftime("%Y-%m-%d"),
                                        wealthType=self.appText.get('SDJSL'),
                                        orderNo=self.appText.get('orderNo'))
        if self.appText.get('vlue') != -5:
            print(self.appText.get('orderNo'))
            raise RuntimeError('首电及时奖励为0 超时前跟进 应该为0或者空')
