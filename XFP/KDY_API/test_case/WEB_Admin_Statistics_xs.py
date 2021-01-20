"""后台-总站相关统计"""
from PubilcAPI.flowPath import *


class TestCase(unittest.TestCase):
    """客第壹后台——总站相关统计"""

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
        登录经纪人 获取ID"""
        cls.do_request = appApi()
        cls.appApi = cls.do_request
        cls.appApi.Login(userName='admin', saasCode='admin', authCode=0)
        if ApiXfpUrl == 'http://xfp.xfj100.com':
            print('正式站不跑')

    def test_Statistics_01(self):
        """储值单位统计（幸福币管理）与全部线索（线索管理）进行比较"""
        # 测试所有的新增
        self.webApi.GoldDetailCountList()
        self.webApi.clue_adminList()
        self.assertEqual(self.appText.get('web_total'), self.appText.get('goldClueCount'))

        # 查看本月
        self.appApi.get_current_month_start_and_end(date=time.strftime("%Y-%m-%d"))
        self.webApi.GoldDetailCountList(startTime=self.appText.get('start_date'),
                                        endTime=self.appText.get('end_date'))
        self.webApi.clue_adminList(startTime=self.appText.get('start_date'),
                                   endTime=self.appText.get('end_date'))
        self.assertEqual(self.appText.get('web_total'), self.appText.get('goldClueCount'))

        """线索及消耗统计与全部线索进行比较---当月新增"""
        self.webApi.clue_adminList(startTime=self.appText.get('start_date'),
                                   endTime=self.appText.get('end_date'),
                                   saasCodeSys=0, isInvalid=1)
        self.webApi.admin_report_clue()
        self.assertEqual(self.appText.get('monthNewNum'), self.appText.get('web_total'))

        """线索及消耗统计与全部线索进行比较---当月有效"""
        self.webApi.clue_adminList(startTime=self.appText.get('start_date'),
                                   endTime=self.appText.get('end_date'), saasCodeSys=0, isInvalid=1)
        if self.appText.get('monthValidNum') != self.appText.get('web_total'):
            print('索及消耗统计与全部线索进行比较---当月有效---两个值不相等 有可能存在未分配的线索')
