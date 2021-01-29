"""后台-成交结算"""
from PubilcAPI.flowPath import *
"""
结算列表：
    1、底部统计-验证数据准确性---->WEB_Statistics_kh.py test_statistics_1
    

"""


class TestCase(unittest.TestCase):
    """客第壹——成交结算"""

    def __init__(self, *args, **kwargs):
        super(TestCase, self).__init__(*args, **kwargs)
        self.xfp_web = webApi()
        self.webApi = self.xfp_web

        self.xfp_app = appApi()
        self.appApi = self.xfp_app

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
        if ApiXfpUrl == 'http://xfp.xfj100.com':
            raise RuntimeError('正式站不跑')

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
                               newlabelName='幸福派总部', saasCode='admin')
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
        """发佣类型"""
        cls.flowPath.get_label(labelNo='YJLX', labelName='佣金类型',
                               newlabelName='认购网签')
        cls.appText.set_map('YJLX', cls.appText.get('labelId'))
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
        cls.appApi.GetLabelList(labelNo='CFZLX', labelName='成交发放', saasCode='admin')
        cls.appText.set_map('CJFF', cls.appText.get('remark'))
        cls.webApi.get_group()
        cls.appApi.GetLabelList(labelNo='CFZLX', labelName='平台上户', saasCode='admin')
        cls.appText.set_map('PTSH', cls.appText.get('remark'))
        cls.appApi.GetLabelList(labelNo='XSSPYY', labelName='电话空号', saasCode='admin')
        cls.appText.set_map('DHWK', cls.appText.get('labelId'))
        cls.appApi.get_current_month_start_and_end(date=time.strftime("%Y-%m-%d"))

        """审核-成交相关-财务"""
        cls.webApi.finance_deal_auditList()
        while cls.appText.get('web_total') != 0:
            cls.webApi.finance_deal_audit(auditStatue=2, remark=time.strftime("%Y-%m-%d %H:%M:%S") + '审核不通过')
            cls.webApi.finance_deal_auditList()

        """审核-成交相关-经理"""
        cls.webApi.auditList()
        while cls.appText.get('web_total') != 0:
            cls.webApi.audit(auditStatue=2, auditRemark=' 审核失败')
            cls.webApi.auditList()
        cls.webApi.auditList(auditLevel=2)
        while cls.appText.get('web_total') != 0:
            cls.webApi.audit(auditStatue=2, auditRemark=' 审核失败')
            cls.webApi.auditList(auditLevel=2)

        """去除一些客户及线索"""
        cls.appApi.my_clue_list()
        while cls.appText.get('total') >= 5:
            cls.flowPath.clue_exile_sea()
            cls.appApi.my_clue_list()

        """审核-成交相关-财务"""
        cls.webApi.finance_deal_auditList()
        while cls.appText.get('web_total') != 0:
            cls.webApi.finance_deal_audit(auditStatue=2, remark=time.strftime("%Y-%m-%d %H:%M:%S") + '审核不通过')
            cls.webApi.finance_deal_auditList()

        """审核-成交相关-经理"""
        cls.webApi.auditList()
        while cls.appText.get('web_total') != 0:
            cls.webApi.audit(auditStatue=2, auditRemark=' 审核失败')
            cls.webApi.auditList()
        cls.webApi.auditList(auditLevel=2)
        while cls.appText.get('web_total') != 0:
            cls.webApi.audit(auditStatue=2, auditRemark=' 审核失败')
            cls.webApi.auditList(auditLevel=2)

        """去除一些客户及线索"""
        cls.appApi.my_clue_list()
        while cls.appText.get('total') >= 5:
            cls.flowPath.clue_exile_sea()
            cls.appApi.my_clue_list()

        cls.appApi.ClientList()
        while cls.appText.get('total') >= 5:
            cls.appApi.client_exile_sea()
            cls.appApi.ClientList()

    def test_DealAccount_001(self):
        """结算列表-添加回款信息"""
        self.webApi.TransactionSettlementList()

        """添加回款记录"""
        self.webApi.addOrUpdateReceivableRecords()
        dome = self.appText.get('returnMoney')
        self.webApi.TransReturnList()
        if dome != self.appText.get('returnMoney'):
            print('结算----添加回款记录与回款记录单次金额不一致')
        self.webApi.TransactionSettlementStatisticalInfo()
        if self.appText.get('receivableAmount') != self.appText.get('vlue'):
            print('结算----回款金额与回款记录列表总额不一致')

        """回款进度  待收金额 -- 详情"""
        if float(self.appText.get('debtCollectionSchedule')) != \
                round(self.appText.get('receivableAmount') / self.appText.get('transYeji'), 2):
            print('结算详情---回款进度计算错误')
        if self.appText.get('amountToBeCollected') != \
                self.appText.get('transYeji') - self.appText.get('receivableAmount'):
            print('结算详情---待收金额计算错误')

        """回款进度  待收金额 -- 合计"""
        self.webApi.TransReturnStatistical()
        if self.appText.get('debtCollectionSchedule') != self.appText.get('percentage'):
            print('结算详情--回款进度计算与底部合计计算不一致')
        if self.appText.get('vlue') != self.appText.get('returnMoney'):
            print('结算详情--回款总额计算与底部合计计算不一致')
        if self.appText.get('amountToBeCollected') != self.appText.get('forReceivable'):
            print('结算详情--待回款总额计算与底部合计计算不一致')

        """添加开票记录"""
        self.webApi.addOrUpdateReceivableRecords(returnType=2)
        dome = self.appText.get('returnMoney')
        self.webApi.TransReturnList(returnType=2)
        if dome != self.appText.get('returnMoney'):
            print('结算详情----添加开票记录与开票记录单次金额不一致')
        self.webApi.TransactionSettlementStatisticalInfo()
        if self.appText.get('printedInvoiceAmount') != self.appText.get('vlue'):
            print('结算详情---开票金额与开票记录列表总额不一致')

        """开票进度  待收金额 -- 合计"""
        self.webApi.TransReturnStatistical(returnType=2)
        if round(self.appText.get('vlue') / self.appText.get('transYeji'), 2) != \
                float(self.appText.get('percentage')):
            print('结算详情--开票进度计算与底部合计计算不一致')
        if self.appText.get('vlue') != self.appText.get('returnMoney'):
            print('结算详情--开票总额计算与底部合计计算不一致')
        if self.appText.get('transYeji') - self.appText.get('vlue') != \
                self.appText.get('forReceivable'):
            print('结算详情--待开票总额计算与底部合计计算不一致')

        """添加授予财富值"""
        self.webApi.awardedWealthDetail()
        dome = self.appText.get('wealthValue')
        self.webApi.WealthDetailList()
        if dome != self.appText.get('wealthValue'):
            print('结算----授予财富值与授予财富值记录单次金额不一致')
        self.webApi.TransactionSettlementStatisticalInfo()
        if self.appText.get('paidWealth') != self.appText.get('vlue'):
            print('结算----授予财富值与授予财富值列表总额不一致')

        if ApiXfpUrl == 'http://xfp.xfj100.com':
            raise RuntimeError('正式站不跑')
        else:
            """发佣"""
            # 新建发佣申请并且审核通过
            self.webApi.TransactionSettlementStatisticalInfo()
            dome = self.appText.get('paidCommission')
            self.webApi.paymentRequest()
            self.webApi.requestList(keyWord=self.appText.get('CJDH'))
            self.webApi.paymentRegister()
            self.webApi.requestAudit()
            self.webApi.TransactionSettlementStatisticalInfo()
            if dome + self.appText.get('paymentAmount') != self.appText.get('paidCommission'):
                print('发放佣金新加后没有在结算详情里面进行添加')

            """发佣列表总和比较"""
            self.webApi.paymentList()
            self.webApi.TransactionSettlementStatisticalInfo()
            if self.appText.get('paidCommission') != self.appText.get('vlue'):
                print('发佣列表总和比较与详情比较两个值不一样')






