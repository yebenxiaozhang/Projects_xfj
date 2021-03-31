"""后台-成交结算"""
from PubilcAPI.flowPath import *
"""
结算列表：
    1、底部统计-验证数据准确性---->WEB_Statistics_kh.py test_statistics_1
    
# 成交结算列表的显示：
#     无审核：
#         1、直接显示，后续无论审核成功与否  都显示
#     有审核：
#         1、首次审核通过后，后续无论审核成功与否  都显示
#         2、审核失败后 不显示 
#             认购审核通过后，后续无论审核成功与否 都显示
            

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

        """添加财务审核后 进行授予财富值"""
        self.webApi.Audit_management(wealthDetailSwitch=True)
        self.webApi.awardedWealthDetail()
        dome = self.appText.get('wealthValue')
        self.webApi.wealthAudit()
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
            # self.webApi.paymentRegister()
            self.webApi.requestAudit()
            self.webApi.TransactionSettlementStatisticalInfo()
            if dome + self.appText.get('paymentAmount') != self.appText.get('paidCommission'):
                print('发放佣金新加后没有在结算详情里面进行添加')

            """发佣列表总和比较"""
            self.webApi.paymentList()
            self.webApi.TransactionSettlementStatisticalInfo()
            if self.appText.get('paidCommission') != self.appText.get('vlue'):
                print('发佣列表总和比较与详情比较两个值不一样')

    # def test_DealAccount_002(self):
    #     """无审核情况下 录入成交 成交结算列表的变化"""
    #     self.flowPath.client_list_non_null()
    #     self.appApi.visitProject_list()
    #     if self.appText.get('web_total') == 0:
    #         self.flowPath.add_visit()
    #         self.flowPath.accomplish_visit()
    #         self.appApi.visitProject_list()
    #
    #     self.webApi.TransactionSettlementList()
    #     dome = self.appText.get('web_total')
    #     """创建成交  无审核的情况下 结算列表新增"""
    #     self.appApi.ClientList()
    #     self.appApi.add_deal()
    #     self.webApi.TransactionSettlementList()
    #     self.assertEqual(dome + 1, self.appText.get('web_total'))
    #
    #     """
    #     修改成交单---认购--- 审核失败
    #     修改成交单---网签--- 审核失败"""
    #     self.appApi.deal_List(keyWord=self.appText.get('dealPhone'))
    #     self.webApi.detail()
    #     self.webApi.Audit_management(customerDeal=True, customerDealLevel=1)
    #     A = 0
    #     while A != 2:
    #         if A == 1:
    #             self.flowPath.get_label(labelNo='CJX', labelName='成交项目',
    #                                     newlabelName='网签')
    #             self.appText.set_map('CJX', self.appText.get('labelId'))
    #         self.appApi.add_deal(Status=1)
    #
    #         self.webApi.auditList(phoneNum=self.appText.get('cluePhone'))
    #         self.webApi.audit(auditStatue=2, auditRemark=time.strftime("%Y-%m-%d %H:%M:%S") + ' 成交审核不通过')
    #         self.webApi.TransactionSettlementList()
    #         self.assertEqual(dome + 1, self.appText.get('web_total'))
    #         A = A + 1
    #
    # def test_DealAccount_003(self):
    #     """
    #         2、审核失败后 不显示
    #         认购审核通过后，后续无论审核成功与否 都显示
    #     :return:
    #     """
    #     self.webApi.TransactionSettlementList()
    #     dome = self.appText.get('web_total')
    #     A = 0
    #     while A != 4:
    #         print(A)
    #         if A == 0 or A == 3:
    #             if A == 0:
    #                 self.flowPath.get_label(labelNo='CJX', labelName='成交项目',
    #                                         newlabelName='认购')
    #             else:
    #                 self.flowPath.get_label(labelNo='CJX', labelName='成交项目',
    #                                         newlabelName='网签')
    #             self.appText.set_map('CJX', self.appText.get('labelId'))
    #
    #         if A == 0:
    #             self.appApi.add_deal()
    #             self.appApi.deal_List(keyWord=self.appText.get('dealPhone'))
    #             self.webApi.detail()
    #         else:
    #             self.appApi.add_deal(Status=1)
    #         self.webApi.auditList(phoneNum=self.appText.get('cluePhone'))
    #         if A == 1:
    #             self.webApi.audit()
    #         else:
    #             self.webApi.audit(auditStatue=2, auditRemark=time.strftime("%Y-%m-%d %H:%M:%S") + ' 成交审核不通过')
    #         self.webApi.TransactionSettlementList()
    #         if A == 0:
    #             self.assertEqual(dome, self.appText.get('web_total'))
    #         else:
    #             self.assertEqual(dome + 1, self.appText.get('web_total'))
    #         A = A + 1

        # self.webApi.auditList(phoneNum=self.appText.get('cluePhone'))
        # if A != 1:
        #     self.webApi.audit(auditStatue=2, auditRemark=dome + ' 成交审核不通过')
        # else:
        #     self.webApi.audit()
        # self.appApi.add_deal(Status=1)
        # self.webApi.TransactionSettlementList()
        # self.assertEqual(dome, self.appText.get('web_total'))
        #
        # """
        # 修改成交单---认购--- 审核失败
        # 修改成交单---网签--- 审核失败"""
        # self.appApi.deal_List(keyWord=self.appText.get('dealPhone'))
        # self.webApi.detail()
        # self.appApi.add_deal(Status=1)
        # self.webApi.auditList(phoneNum=self.appText.get('cluePhone'))
        # self.webApi.audit()
        # A = 0
        # while A != 2:
        #     if A == 1:
        #         self.flowPath.get_label(labelNo='CJX', labelName='成交项目',
        #                                 newlabelName='网签')
        #         self.appText.set_map('CJX', self.appText.get('labelId'))
        #     self.appApi.add_deal(Status=1)
        #
        #     self.webApi.auditList(phoneNum=self.appText.get('cluePhone'))
        #     self.webApi.audit(auditStatue=2, auditRemark=dome + ' 成交审核不通过')
        #     self.webApi.TransactionSettlementList()
        #     self.assertEqual(dome + 1, self.appText.get('web_total'))




