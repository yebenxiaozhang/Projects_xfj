"""后台-统计相关"""
from PubilcAPI.flowPath import *


class TestCase(unittest.TestCase):
    """客第壹后台——带看成交统计"""

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
        cls.appApi.Login()
        cls.appApi.GetUserData()
        cls.request = webApi()
        cls.webApi = cls.request
        cls.webApi.Audit_management()

    def test_statistics_01(self):
        """带看成交统计"""
        self.webApi.visit_deal_statistics()
        """上户数量对比"""
        self.appApi.getConsultantCount()
        if self.webText.get('web_newClueCount') != self.appText.get('newClueCount'):
            print('带看成交统计上户数量与APP本月概况上户数量不一致')

        """带看数量对比"""
        self.webApi.visit_list()
        if self.webText.get('web_visitOnTimeCount') != self.appText.get('web_total'):
            print('带看成交统计的带看次数与后台带看次数不一致')

        if self.webText.get('web_visitCount') != self.appText.get('visitCount'):
            print('带看成交统计的带看次数与APP本月概况带看次数不一致')

        """上户邀约率"""
        if self.webText.get('web_visitRatio') != self.webText.get('visitRatio'):
            print('带看成交统计的成交与APP本月概况上户邀约率不一致')

        """带看成交率"""
        if self.webText.get('web_transactionRatio') != self.webText.get('dealRatio'):
            print('带看成交统计的成交与APP本月概况带看成交率不一致')

        """成交套数对比"""
        self.webApi.deal_list(transTime='认购')             # 后台查看已完成成交次数
        if self.webText.get('web_transactionCount') != self.webText.get('web_total'):
            print('带看成交统计的成交与后台成交总套数不一致')

        if self.webText.get('web_transactionCount') != self.webText.get('dealCount'):
            print('带看成交统计的成交与APP本月概况成交套数不一致')

        """网签套数对比"""
        self.webApi.deal_list(transType=2, transTime='网签')             # 后台查看已完成成交次数
        if self.webText.get('web_total') != self.webText.get('web_subscribeConvertSigning'):
            print('带看成交统计中网签套数与后台成交套数不一致')

        """带看成交统计与成交结算底部统计进行比较"""
        self.webApi.TransactionSettlementStatistical()
        if self.appText.get('rgCount') != self.webText.get('web_transactionCount'):
            print('带看成交统计与成交结算底部统计进行比较---认购套数--审核通过的')

        if self.appText.get('wqCount') != self.webText.get('web_subscribeConvertSigning'):
            print('带看成交统计与成交结算底部统计进行比较---网签套数--审核通过的')

        # self.webApi.deal_list(transType=3, transTime='认购')  # 后台查看已完成成交次数
        # if self.appText.get('hkCount') != self.webText.get('web_total'):
        #     print('带看成交统计与成交结算底部统计进行比较---回款套数--审核通过的')

        if self.appText.get('verificationResults') != self.webText.get('web_transactionResults'):
            print('带看成交统计与成交结算底部统计进行比较---审核业绩--审核通过的')

        """业绩对比"""
        dome = self.webText.get('web_transactionResults')
        self.webApi.deal_list()             # 后台查看已完成成交次数
        if self.webText.get('web_total') != 0:
            self.webApi.detail()
            self.appApi.ClueInfo()
            dome1 = self.appText.get('transYeji')
            self.appApi.add_deal(Status=1, transYeji=float(dome1) + float(500))
            self.webApi.visit_deal_statistics()
            if self.webText.get('web_transactionResults') != float(dome) + float(500):
                print('带看成交统计中业绩与成交业绩不一致')

    def test_Statistics_02(self):
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

    def test_Statistics_03(self):
        """咨询师工作统计"""
        self.webApi.work_statistics()
        """上户数量   ！   首电及时率         ！ 跟进及时率"""
        self.appApi.getConsultantCount()
        if self.webText.get('web_newClueCount') != self.appText.get('newClueCount'):
            raise RuntimeError('咨询师工作统计上户数量与APP本月概况上户数量不一致')
        if self.webText.get('web_firstCallRatio') != self.appText.get('firstCallRatio'):
            raise RuntimeError('咨询师工作统计首电及时率与APP本月概况首电及时率不一致')
        if self.webText.get('web_followRatio') != self.appText.get('followRatio'):
            raise RuntimeError('咨询师工作统计跟进及时率与APP本月概况首电及时率不一致')

        """通话记录"""
        self.webApi.phoneLogList()
        if self.appText.get('web_total') != self.webText.get('web_callCount'):
            print('咨询师工作统计与通话记录中的通话次数不一致')

        """公海领取"""
        dome = self.webText.get('web_seaClaimClueCount')
        self.appApi.SeaList()  # 公海列表
        if self.appApi.appText.get('total') != 0:
            self.appApi.clue_Assigned()  # 领取线索
            if dome + 1 == self.webText.get('web_seaClaimClueCount'):
                print('咨询师工作统计中领取线索后 没有加1（公海领取）')

        """释放公海批次"""
        if self.webText.get('web_seaClueCount') != self.appText.get('seaClueCount'):
            print('咨询师工作统计中释放公海批次与APP本月概况释放批次不一致')

    def test_Statistics_04(self):
        """客第壹后台---队长---关键指标"""

        """关键指标与APP本月概况进行比较"""
        self.appApi.getConsultantCount()
        self.webApi.ConsultantCountList()

        if self.appText.get('newClueCount') != self.appText.get('web_newClueCount'):
            print('上户数量不一致---APP本月概况与客第壹后台关键指标--队长')

        if self.appText.get('seaClueCount') != self.appText.get('web_seaClueCounth'):
            print('释放公海批数---APP本月概况与客第壹后台关键指标--队长')

        if self.appText.get('firstCallRatio') != self.appText.get('web_firstCallRatio'):
            print('首电及时率---APP本月概况与客第壹后台关键指标--队长')

        if self.appText.get('followRatio') != self.appText.get('web_followRatio'):
            print('跟进及时率---APP本月概况与客第壹后台关键指标--队长')

        if self.appText.get('visitCount') != self.appText.get('web_visitCount'):
            print('带看总数---APP本月概况与客第壹后台关键指标--队长')

        if self.appText.get('visitRatio') != self.appText.get('web_visitRatio'):
            print('上户邀约率---APP本月概况与客第壹后台关键指标--队长')

        if self.appText.get('dealCount') != self.appText.get('web_dealCount'):
            print('成交总数---APP本月概况与客第壹后台关键指标--队长')

        if self.appText.get('dealRatio') != self.appText.get('web_dealRatio'):
            print('带看邀约率---APP本月概况与客第壹后台关键指标--队长')

        """带看成交统计与工作台中业绩进行比较"""
        self.webApi.visit_deal_statistics()
        if self.webText.get('web_transactionResults') != self.appText.get('web_transactionSum'):
            print('成交业绩---APP本月概况与客第壹后台关键指标--队长')



