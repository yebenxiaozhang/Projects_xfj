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
        cls.flow = flowPath()
        cls.flowPath = cls.flow
        cls.appText = GlobalMap()
        """线索来源"""
        cls.flowPath.get_label(labelNo='XSLY', labelName='线索来源',
                               newlabelName='百度小程序')
        cls.appText.set_map('XSLY', cls.appText.get('labelId'))

        """线索来源_幸福派总部"""
        cls.flowPath.get_label(labelNo='XSLY', labelName='线索来源',
                               newlabelName='幸福派总部')
        cls.appText.set_map('XSLY_admin', cls.appText.get('labelId'))
        """线索标签"""
        cls.appApi.GetUserLabelList(userLabelType='线索标签')
        if cls.appText.get('total') == 0:
            cls.appApi.AddUserLabel()
            cls.appApi.GetUserLabelList(userLabelType='线索标签')
        cls.appText.set_map('XSBQ', cls.appText.get('labelData'))
        """终止跟进"""
        cls.flowPath.get_label(labelNo='SZGJYY', labelName='终止跟进原因',
                               newlabelName='客户已成交')
        cls.appText.set_map('ZZGJ', cls.appText.get('labelId'))
        """成交项"""
        cls.flowPath.get_label(labelNo='CJX', labelName='成交项目',
                               newlabelName='认购')
        cls.appText.set_map('CJX', cls.appText.get('labelId'))
        """出行方式"""
        cls.flowPath.get_label(labelNo='CXFS', labelName='出行方式',
                               newlabelName='自驾')
        cls.appText.set_map('CXFS', cls.appText.get('labelId'))
        """客户意向等级"""
        cls.appApi.GetLabelList(labelNo='KHYXDJ')                       # 查询购房意向loanSituation
        cls.appText.set_map('KHYXDJ', cls.appText.get('labelId'))
        cls.appApi.GetLabelList(labelNo='ZJZZ')                         # 查询资金资质
        cls.appText.set_map('ZJZZ', cls.appText.get('labelId'))
        cls.appApi.GetLabelList(labelNo='GFMD')                         # 查询购房目的
        cls.appText.set_map('GFMD', cls.appText.get('labelId'))
        cls.appApi.GetLabelList(labelNo='WYSX')                         # 查询物业属性
        cls.appText.set_map('WYSX', cls.appText.get('labelId'))
        cls.appApi.GetLabelList(labelNo='GFZZ')                         # 查询购房资质
        cls.appText.set_map('GFZZ', cls.appText.get('labelId'))
        cls.appApi.GetLabelList(labelNo='SFSTF')                        # 查询是否首套
        cls.appText.set_map('SFSTF', cls.appText.get('labelId'))
        cls.appApi.GetMatchingArea()                                    # 查询匹配区域
        cls.appApi.GetMatchingAreaHouse()                               # 匹配楼盘
        cls.appApi.GetLabelList(labelNo='QTKHXQ')                       # 查询客户需求
        cls.appText.set_map('QTKHXQ', cls.appText.get('labelId'))
        cls.appApi.ConsultantList()                                     # 咨询师列表
        cls.appApi.GetLabelList(labelNo='SQZHGJ', labelName='其他')
        cls.appText.set_map('ZHGJ', cls.appText.get('labelId'))         # 暂缓跟进
        cls.flowPath.get_label(labelNo='XXFL', labelName='信息分类',
                               newlabelName='信息分类一')
        cls.appText.set_map('XXFL', cls.appText.get('labelId'))         # 信息分类
        cls.flowPath.get_label(labelNo='DLGS', labelName='代理公司',
                               newlabelName='代理公司一')
        cls.appText.set_map('DLGS', cls.appText.get('labelId'))         # 代理公司
        cls.flowPath.get_label(labelNo='WDFL', labelName='问答分类',
                               newlabelName='问答分类一')
        cls.appText.set_map('WDFL', cls.appText.get('labelId'))         # 问答分类
        cls.webApi.consultant_allocition(isAppoint=1)

        cls.appApi.GetLabelList(labelNo='CFZLX', labelName='成交奖励', saasCode='admin')
        cls.appText.set_map('CJJL', cls.appText.get('remark'))
        cls.appApi.GetLabelList(labelNo='CFZLX', labelName='邀约带看', saasCode='admin')
        cls.appText.set_map('YYDK', cls.appText.get('remark'))
        cls.webApi.get_group()
        cls.appApi.GetLabelList(labelNo='CFZLX', labelName='平台上户', saasCode='admin')
        cls.appText.set_map('PTSH', cls.appText.get('remark'))
        cls.appApi.get_current_month_start_and_end(date=time.strftime("%Y-%m-%d"))

        """残余审核"""
        cls.webApi.audit_List()
        while cls.webApi.webText.get('total') != 0:
            cls.webApi.auditApply(isAudit=False, auditRemark='客户流放公海')
            cls.webApi.audit_List()
        cls.webApi.audit_List(auditLevel=2)
        while cls.webApi.webText.get('total') != 0:
            cls.webApi.auditApply(isAudit=False, auditRemark='客户流放公海')
            cls.webApi.audit_List()

        """去除一些客户及线索"""
        cls.appApi.my_clue_list()
        while cls.appText.get('total') >= 5:
            cls.flowPath.clue_exile_sea()
            cls.appApi.my_clue_list()

        cls.appApi.ClientList()
        while cls.appText.get('total') >= 5:
            cls.appApi.client_exile_sea()
            cls.appApi.ClientList()

    def test_visit_deal_statistics(self):
        """带看成交统计"""
        self.webApi.visit_deal_statistics()
        """上户数量对比"""
        self.appApi.getConsultantCount()
        if self.webText.get('web_newClueCount') != self.appText.get('newClueCount'):
            raise RuntimeError('带看成交统计上户数量与APP本月概况上户数量不一致')

        """带看数量对比"""
        self.webApi.visit_list()
        if self.webText.get('web_visitOnTimeCount') != self.appText.get('web_total'):
            raise RuntimeError('带看成交统计的带看次数与后台带看次数不一致')

        if self.webText.get('web_visitCount') != self.appText.get('visitCount'):
            raise RuntimeError('带看成交统计的带看次数与APP本月概况带看次数不一致')
        """上户邀约率"""
        if self.webText.get('web_visitRatio') != self.webText.get('visitRatio'):
            raise RuntimeError('带看成交统计的成交与APP本月概况上户邀约率不一致')
        """带看成交率"""
        if self.webText.get('web_transactionRatio') != self.webText.get('dealRatio'):
            raise RuntimeError('带看成交统计的成交与APP本月概况带看成交率不一致')

        """成交套数对比"""
        self.webApi.deal_list()             # 后台查看已完成成交次数
        if self.webText.get('web_transactionCount') != self.webText.get('web_total'):
            raise RuntimeError('带看成交统计的成交与后台成交总套数不一致')
        if self.webText.get('web_transactionCount') != self.webText.get('dealCount'):
            raise RuntimeError('带看成交统计的成交与APP本月概况成交套数不一致')

        # """网签套数对比"""
        # self.flowPath.get_label(labelNo='CJX', labelName='成交项目',
        #                         newlabelName='网签')
        # self.webApi.deal_list(transType=self.appText.get('labelId'))             # 后台查看已完成成交次数
        # if self.webText.get('web_total') != self.webText.get('web_subscribeConvertSigning'):
        #     raise RuntimeError('带看成交统计中网签套数与后台成交套数不一致')

        """业绩对比"""
        dome = self.webText.get('web_transactionResults')
        self.webApi.deal_list()             # 后台查看已完成成交次数
        dome1 = self.appText.get('transYeji')
        self.appApi.add_deal(Status=1, transYeji=float(dome1) + float(500))
        self.webApi.visit_deal_statistics()
        if self.webText.get('web_transactionResults') != float(dome) + float(500):
            raise RuntimeError('带看成交统计中业绩与成交业绩不一致')






