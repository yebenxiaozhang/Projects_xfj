"""后台-带看成交统计"""
from XFP.PubilcAPI.flowPath import *


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

    def test_visit_deal_statistics(self):
        """带看成交统计"""
        self.webApi.visit_deal_statistics()
        """上户数量对比"""
        self.appApi.getConsultantCount()
        if self.webText.get('web_newClueCount') != self.appText.get('newClueCount'):
            print('带看成交统计上户数量与APP本月概况上户数量不一致')

        """带看数量对比"""
        self.webApi.visit_list()
        if self.webText.get('web_visitOnTimeCount') != self.appText.get('web_total'):
            raise RuntimeError('带看成交统计的带看次数与后台带看次数不一致')

        if self.webText.get('web_visitCount') != self.appText.get('visitCount'):
            print('带看成交统计的带看次数与APP本月概况带看次数不一致')
            # raise RuntimeError('带看成交统计的带看次数与APP本月概况带看次数不一致')
        """上户邀约率"""
        if self.webText.get('web_visitRatio') != self.webText.get('visitRatio'):
            print('带看成交统计的成交与APP本月概况上户邀约率不一致')
            # raise RuntimeError('带看成交统计的成交与APP本月概况上户邀约率不一致')
        """带看成交率"""
        if self.webText.get('web_transactionRatio') != self.webText.get('dealRatio'):
            print('带看成交统计的成交与APP本月概况带看成交率不一致')
            # raise RuntimeError('带看成交统计的成交与APP本月概况带看成交率不一致')

        """成交套数对比"""
        self.webApi.deal_list()             # 后台查看已完成成交次数
        if self.webText.get('web_transactionCount') != self.webText.get('web_total'):
            print('带看成交统计的成交与后台成交总套数不一致')
            # raise RuntimeError('带看成交统计的成交与后台成交总套数不一致')
        if self.webText.get('web_transactionCount') != self.webText.get('dealCount'):
            print('带看成交统计的成交与APP本月概况成交套数不一致')
            # raise RuntimeError('带看成交统计的成交与APP本月概况成交套数不一致')

        # """网签套数对比"""
        # self.flowPath.get_label(labelNo='CJX', labelName='成交项目',
        #                         newlabelName='网签')
        # self.webApi.deal_list(transType=self.appText.get('labelId'))             # 后台查看已完成成交次数
        # if self.webText.get('web_total') != self.webText.get('web_subscribeConvertSigning'):
        #     raise RuntimeError('带看成交统计中网签套数与后台成交套数不一致')

        """业绩对比"""
        dome = self.webText.get('web_transactionResults')
        self.webApi.deal_list()             # 后台查看已完成成交次数
        if self.webText.get('web_total') != 0:
            self.webApi.detail()
            dome1 = self.appText.get('transYeji')
            self.appApi.add_deal(Status=1, transYeji=float(dome1) + float(500))
            self.webApi.finance_deal_auditList(keyWord=self.appText.get('dealPhone'))
            self.webApi.finance_deal_audit()
            self.webApi.visit_deal_statistics()
            if self.webText.get('web_transactionResults') != float(dome) + float(500):
                raise RuntimeError('带看成交统计中业绩与成交业绩不一致')






