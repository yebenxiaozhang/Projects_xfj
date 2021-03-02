"""客第壹总站-回访"""
from PubilcAPI.flowPath import *
"""
回访：
    无审核：
        完成带看--->创建待回访任务         
                ！！！ APP_My_visit_kh.py-->test_my_visit_02
        录入成交--->创建待回访任务         
                ！！！ APP_My_Deal_kh.py-->test_my_deal_01
    有审核：
        审核失败、取消带看--->不创建回访任务
                ！！！ APP_My_visit_kh.py-->test_my_visit_06
                ！！！ APP_My_visit_kh.py-->test_my_visit_03
        审核成功--->创建回访任务
                ！！！ APP_My_visit_kh.py-->test_my_visit_07
        成交审核失败--->不创建回访任务
        审核成功、审核失败的再次提交--->创建待回访任务    
    
    回访带看--------取消带看回访
    回访成交--------取消成交回访
"""


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
        登录幸福派 获取ID"""
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
        cls.flowPath.get_label(labelNo='XSLY', labelName='线索来源',
                               newlabelName='幸福派总部',)
        cls.appText.set_map('XSLY_admin_fb', cls.appText.get('labelId'))
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
        cls.appApi.GetLabelList(labelNo='CFZLX', labelName='成交发放', saasCode='admin')
        cls.appText.set_map('CJFF', cls.appText.get('remark'))
        cls.appApi.GetLabelList(labelNo='QXHF', saasCode='admin')
        cls.appText.set_map('QXHF', cls.appText.get('remark'))
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

        cls.appApi.ClientList()
        while cls.appText.get('total') >= 5:
            cls.appApi.client_exile_sea()
            cls.appApi.ClientList()

    def test_ReturnVisit_001(self):
        """
        录入成交-审核失败不创建回访记录
        将原来审核失败的记录重新申请 则创建回访记录
        :return:
        """
        self.flowPath.client_list_non_null()
        self.appApi.visitProject_list()
        if self.appText.get('web_total') == 0:
            self.flowPath.add_visit()
            self.flowPath.accomplish_visit()
            self.appApi.visitProject_list()
        self.webApi.Audit_management(customerDeal=True, customerDealLevel=1)
        self.appApi.ClientList()
        self.webApi.repayTaskList(repayType=2)
        repay = self.appText.get('total')
        self.appApi.add_deal()
        self.webApi.repayTaskList(repayType=2)
        self.assertEqual(self.appText.get('total'), repay)

        self.webApi.auditList(phoneNum=self.appText.get('cluePhone'))
        self.webApi.audit(auditStatue=2, auditRemark=time.strftime("%Y-%m-%d %H:%M:%S") + ' 成交审核不通过')

        self.webApi.repayTaskList(repayType=2)
        self.assertEqual(self.appText.get('total'), repay)

        self.appApi.deal_List(ApplyStatus=2)
        self.webApi.detail()
        self.appApi.add_deal(Status=1)

        self.webApi.auditList(phoneNum=self.appText.get('cluePhone'))
        self.webApi.audit()

        self.webApi.repayTaskList(repayType=2)
        self.assertNotEqual(self.appText.get('total'), repay)

    def test_ReturnVisit_002(self):
        """
            回访带看--------取消带看回访
            回访成交--------取消成交回访
        :return:
        """
        a = 0
        while a != 4:
            if a < 2:
                self.webApi.repayTaskList()
            if a > 1:
                self.webApi.repayTaskList(repayType=2)
            dome = self.appText.get('total')
            if self.appText.get('total') != 0:
                if a == 0 or a == 2:
                    self.webApi.repayTask()         # 取消回访
                else:
                    self.webApi.repayTaskCancel()   # 回访
                self.webApi.repayTaskList()
                self.assertNotEqual(dome, self.appText.get('total'))
            a = a + 1

