"""后台-财富值统计"""
from XFP.PubilcAPI.flowPath import *


class TestCase(unittest.TestCase):
    """客第壹后台——财富值统计"""

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
        cls.do_request = appApi()
        cls.appApi = cls.do_request
        cls.appApi.Login()
        cls.appApi.GetUserData()
        cls.request = webApi()
        cls.webApi = cls.request
        cls.webApi.Audit_management()

    def test_Statistics_web_wealth(self):
        """财富值统计"""
        self.webApi.statistics_wealth()
        self.appApi.my_Wealth()
        """后台与app数值上的对比"""
        if self.webText.get('web_clueCount') != self.appText.get('monthGetClueCount'):
            raise RuntimeError('兑换线索（总数）不一致（后台财富值与APP我的财富值）')
        dome2 = self.webText.get('web_clueCount')

        """通过财富值兑换线索与财富值统计兑换线索进行对比"""
        self.appApi.getWealthDetailList(startTime=self.appText.get('start_date'),
                                        endTime=time.strftime("%Y-%m-%d"),
                                        wealthType=self.appText.get('PTSH'),
                                        orderNo=None)

        if self.webText.get('web_clueCount') != self.appText.get('web_total'):
            raise RuntimeError('通过财富值兑换线索与财富值统计兑换线索进行对比')

        if self.webText.get('web_wealthClueSum') != self.appText.get('monthGetClueConsumeWealth'):
            raise RuntimeError('兑换线索（消耗财富值）不一致（后台财富值与APP我的财富值）')
        dome = self.webText.get('web_wealthClueSum')

        if self.webText.get('web_wealthConsume') != self.appText.get('monthConsumeWealth'):
            raise RuntimeError('消耗财富值不一致（后台财富值与APP我的财富值）')
        dome1 = self.webText.get('web_wealthConsume')

        if self.webText.get('web_wealthObtainSum') != self.appText.get('monthGetWealth'):
            raise RuntimeError('本月获得财富值不一致（后台财富值与APP我的财富值）')

        if self.webText.get('web_wealthSum') != self.appText.get('lastMonthWealthDifference'):
            raise RuntimeError('合计增减财富值（后台财富值与APP我的财富值）')

        # if self.webText.get('web_wealthSysDeduct') != self.appText.get('monthNotClueWealth'):
        #     raise RuntimeError('系统扣除不一致（后台财富值与APP我的财富值）')
        dome4 = self.webText.get('web_wealthSysDeduct')

        """判断合计增减是否计算错误"""
        if int(self.webText.get('web_wealthObtainSum')) + int(self.webText.get('web_wealthConsume')) \
                != int(self.appText.get('web_wealthSum')):
            raise RuntimeError('合计增减是否计算错误')
        """业绩奖励  系统奖励  需要通过计算可得"""

        """申诉返还"""
        dome3 = self.webText.get('web_clueApplyCount')
        if ApiXfpUrl == 'http://xfp.xfj100.com':
            pass
        else:
            self.appApi.Login(userName='admin', saasCode='admin', authCode='0')
            self.webApi.add_clue_admin(clueNickName=self.appApi.RandomText(textArr=surname))
            if self.appText.get('code') == 403:
                self.webApi.addGoldDetailInfo()
                self.webApi.add_clue_admin(clueNickName=self.appApi.RandomText(textArr=surname))
            self.appApi.Login()
            self.appApi.my_clue_list(keyWord=self.webText.get('cluePhone'))
            self.appApi.getWealthDetailList(startTime=time.strftime("%Y-%m-%d"),
                                            endTime=time.strftime("%Y-%m-%d"),
                                            wealthType=self.appText.get('PTSH'),
                                            orderNo=self.appText.get('orderNo'))
            self.webApi.statistics_wealth()
            if self.webText.get('web_wealthClueSum') != dome - 300:
                raise RuntimeError('我的财富值！ 平台上户后 线索扣除的财富值没有扣除')

            if self.webText.get('web_wealthConsume') != dome1 - 300:
                raise RuntimeError('我的财富值！ 平台上户后 消耗的财富值没有扣除')

            if self.webText.get('web_clueCount') != dome2 + 1:
                raise RuntimeError('我的财富值！ 平台上户后 兑换线索没有+1')

            """申诉操作"""
            self.appApi.getWealthDetailList(startTime=time.strftime("%Y-%m-%d"),
                                            endTime=time.strftime("%Y-%m-%d"),
                                            wealthType=self.appText.get('PTSH'),
                                            orderNo=self.appText.get('orderNo'))

            self.appApi.addWealthApply()
            self.webApi.getWealthApplyList(keyWord=self.appText.get('orderNo'))
            self.webApi.wealthApply()

            """申诉完成后财富值进行对比"""
            self.webApi.statistics_wealth()
            if self.webText.get('web_wealthSysDeduct') != dome4 + 300:
                raise RuntimeError('我的财富值！ 申诉后系统扣除没有加上返还')

            if self.webText.get('web_wealthConsume') != dome1:
                raise RuntimeError('我的财富值！ 平台上户后再上户消耗不变')

            if self.webText.get('web_clueApplyCount') != dome3 + 1:
                raise RuntimeError('我的财富值！ 平台上户后 申诉返还条数不一致')



        






