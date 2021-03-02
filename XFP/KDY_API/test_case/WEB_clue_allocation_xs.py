"""后台-线索分配"""
from PubilcAPI.flowPath import *
"""
    1、幸福币不足，分配失败
    2、无咨询师接受分配，会在待分配列表
    3、上户时间：分站分配时间
    4、通过总部分配的线索不允许修改来源
    5、待分配列表进行分配会有待首电的待办
"""


class TestCase(unittest.TestCase):
    """客第壹——线索分配"""

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

        # cls.do_request = appApi()
        # cls.appApi = cls.do_request
        # cls.appApi.Login()
        # cls.appApi.GetUserData()
        # cls.request = webApi()
        # cls.webApi = cls.request
        # cls.webApi.Audit_management()
        # cls.flow = flowPath()
        # cls.flowPath = cls.flow
        # cls.appText = GlobalMap()
        # """线索来源"""
        # cls.flowPath.get_label(labelNo='XSLY', labelName='线索来源',
        #                        newlabelName='百度小程序')
        # cls.appText.set_map('XSLY', cls.appText.get('labelId'))
        #
        # """线索来源_幸福派总部"""
        # cls.flowPath.get_label(labelNo='XSLY', labelName='线索来源',
        #                        newlabelName='幸福派总部', saasCode='admin')
        # cls.appText.set_map('XSLY_admin', cls.appText.get('labelId'))
        # """线索标签"""
        # cls.appApi.GetUserLabelList(userLabelType='线索标签')
        # if cls.appText.get('total') == 0:
        #     cls.appApi.AddUserLabel()
        #     cls.appApi.GetUserLabelList(userLabelType='线索标签')
        # cls.appText.set_map('XSBQ', cls.appText.get('labelData'))
        # """终止跟进"""
        # cls.flowPath.get_label(labelNo='SZGJYY', labelName='终止跟进原因',
        #                        newlabelName='客户已成交')
        # cls.appText.set_map('ZZGJ', cls.appText.get('labelId'))
        # """成交项"""
        # cls.flowPath.get_label(labelNo='CJX', labelName='成交项目',
        #                        newlabelName='认购')
        # cls.appText.set_map('CJX', cls.appText.get('labelId'))
        # """出行方式"""
        # cls.flowPath.get_label(labelNo='CXFS', labelName='出行方式',
        #                        newlabelName='自驾')
        # cls.appText.set_map('CXFS', cls.appText.get('labelId'))
        # """客户意向等级"""
        # cls.appApi.GetLabelList(labelNo='KHYXDJ')                       # 查询购房意向loanSituation
        # cls.appText.set_map('KHYXDJ', cls.appText.get('labelId'))
        # cls.appApi.GetLabelList(labelNo='ZJZZ')                         # 查询资金资质
        # cls.appText.set_map('ZJZZ', cls.appText.get('labelId'))
        # cls.appApi.GetLabelList(labelNo='GFMD')                         # 查询购房目的
        # cls.appText.set_map('GFMD', cls.appText.get('labelId'))
        # cls.appApi.GetLabelList(labelNo='WYSX')                         # 查询物业属性
        # cls.appText.set_map('WYSX', cls.appText.get('labelId'))
        # cls.appApi.GetLabelList(labelNo='GFZZ')                         # 查询购房资质
        # cls.appText.set_map('GFZZ', cls.appText.get('labelId'))
        # cls.appApi.GetLabelList(labelNo='SFSTF')                        # 查询是否首套
        # cls.appText.set_map('SFSTF', cls.appText.get('labelId'))
        # cls.appApi.GetMatchingArea()                                    # 查询匹配区域
        # cls.appApi.GetMatchingAreaHouse()                               # 匹配楼盘
        # cls.appApi.GetLabelList(labelNo='QTKHXQ')                       # 查询客户需求
        # cls.appText.set_map('QTKHXQ', cls.appText.get('labelId'))
        # cls.appApi.ConsultantList()                                     # 咨询师列表
        # cls.appApi.GetLabelList(labelNo='SQZHGJ', labelName='其他')
        # cls.appText.set_map('ZHGJ', cls.appText.get('labelId'))         # 暂缓跟进
        # cls.flowPath.get_label(labelNo='XXFL', labelName='信息分类',
        #                        newlabelName='信息分类一')
        # cls.appText.set_map('XXFL', cls.appText.get('labelId'))         # 信息分类
        # cls.flowPath.get_label(labelNo='DLGS', labelName='代理公司',
        #                        newlabelName='代理公司一')
        # cls.appText.set_map('DLGS', cls.appText.get('labelId'))         # 代理公司
        # cls.flowPath.get_label(labelNo='WDFL', labelName='问答分类',
        #                        newlabelName='问答分类一')
        # cls.appText.set_map('WDFL', cls.appText.get('labelId'))         # 问答分类
        # cls.webApi.consultant_allocition(isAppoint=1)
        #
        # cls.appApi.GetLabelList(labelNo='CFZLX', labelName='成交奖励', saasCode='admin')
        # cls.appText.set_map('CJJL', cls.appText.get('remark'))
        # cls.appApi.GetLabelList(labelNo='CFZLX', labelName='邀约带看', saasCode='admin')
        # cls.appText.set_map('YYDK', cls.appText.get('remark'))
        # cls.appApi.GetLabelList(labelNo='CFZLX', labelName='成交发放', saasCode='admin')
        # cls.appText.set_map('CJFF', cls.appText.get('remark'))
        # cls.webApi.get_group()
        # cls.appApi.GetLabelList(labelNo='CFZLX', labelName='平台上户', saasCode='admin')
        # cls.appText.set_map('PTSH', cls.appText.get('remark'))
        # cls.appApi.GetLabelList(labelNo='XSSPYY', labelName='电话空号', saasCode='admin')
        # cls.appText.set_map('DHWK', cls.appText.get('labelId'))
        # cls.appApi.get_current_month_start_and_end(date=time.strftime("%Y-%m-%d"))
        #
        # """审核-成交相关-财务"""
        # cls.webApi.finance_deal_auditList()
        # while cls.appText.get('web_total') != 0:
        #     cls.webApi.finance_deal_audit(auditStatue=2, remark=time.strftime("%Y-%m-%d %H:%M:%S") + '审核不通过')
        #     cls.webApi.finance_deal_auditList()
        #
        # """审核-成交相关-经理"""
        # cls.webApi.auditList()
        # while cls.appText.get('web_total') != 0:
        #     cls.webApi.audit(auditStatue=2, auditRemark=' 审核失败')
        #     cls.webApi.auditList()
        # cls.webApi.auditList(auditLevel=2)
        # while cls.appText.get('web_total') != 0:
        #     cls.webApi.audit(auditStatue=2, auditRemark=' 审核失败')
        #     cls.webApi.auditList(auditLevel=2)
        #
        # """去除一些客户及线索"""
        # cls.appApi.my_clue_list()
        # while cls.appText.get('total') >= 5:
        #     cls.flowPath.clue_exile_sea()
        #     cls.appApi.my_clue_list()
        #
        # cls.appApi.ClientList()
        # while cls.appText.get('total') >= 5:
        #     cls.appApi.client_exile_sea()
        #     cls.appApi.ClientList()

    def test_all_allocation_1(self):
        """2、无咨询师接受分配，会在待分配列表"""
        self.webApi.consultant_allocition(isAppoint=0)
        self.appApi.my_clue_list()
        dome = self.appText.get('total')
        self.appApi.Login(userName='admin', saasCode='admin', authCode=0)
        self.webApi.add_clue_admin(clueNickName=self.appApi.RandomText(textArr=surname))
        self.appApi.Login()
        self.webApi.clue_await_allocition(keyWord=self.webText.get('cluePhone'))
        self.assertEqual(1, self.webText.get('total'))
        self.assertNotEqual(self.webText.get('receptionTime'), self.webText.get('createdTime'))
        """3、上户时间：分站分配时间"""
        self.webApi.clue_appoint()
        self.webApi.clue_await_allocition(keyWord=self.webText.get('cluePhone'))
        self.assertEqual(0, self.webText.get('total'))
        self.appApi.my_clue_list()
        self.assertNotEqual(dome, self.appText.get('total'))
        self.appApi.ClueInfo()
        self.assertNotEqual(self.webText.get('receptionTime'), self.webText.get('createdTime'))
        self.assertNotEqual(self.appText.get('receptionTime'), self.appText.get('createdTime'))
        self.assertEqual(self.webText.get('createdTime'), self.appText.get('createdTime'))
        self.webApi.consultant_allocition(isAppoint=1)

        """留点记录"""
        self.webApi.clue_detail()
        if self.appText.get('remark') != '总站添加线索':
            print('线索存在留点记录，但是分派给咨询师后，留点记录为空')

        """总部分配到分站-分站无在线人员 通过手动分派人员 要扣除财富值"""
        self.appApi.getWealthDetailList(startTime=time.strftime("%Y-%m-%d"),
                                        endTime=time.strftime("%Y-%m-%d"),
                                        wealthType=self.appText.get('PTSH'),
                                        orderNo=self.appText.get('orderNo'))
        if self.appText.get('vlue') != -300:
            raise RuntimeError('总部分配到分站-分站无在线人员 通过手动分派人员 要扣除财富值')

    def test_repetition_compensation(self):
        """重复申请索赔"""
        # self.webApi.clue_list(myClue='N', sourceId=self.appText.get('XSLY_admin'))
        # self.appApi.ClueInfo()
        self.webApi.goldApply_addGoldApply()
        self.webApi.goldApply_addGoldApply()
        if self.appText.get('data') != '该线索已索赔，详情可查看索赔记录!':
            print(self.appText.get('data'))
            print(self.appText.get('orderNo'))
            raise RuntimeError('索赔提示文案不对？')

        """审核失败后 再次申请是否可以？"""
        self.webApi.getGoldApplyList()
        self.webApi.auditGoldApply(applyStatus=False)
        self.webApi.goldApply_addGoldApply()
        self.assertEqual(self.appText.get('data'), '该线索已索赔，详情可查看索赔记录!')

    def test_compensation(self):
        """索赔成功-后 总站线索列表应该显示为无效"""
        self.appApi.Login(userName='admin', saasCode='admin', authCode=0)
        self.webApi.add_clue_admin(clueNickName=self.appApi.RandomText(textArr=surname))
        self.appApi.Login()
        self.appApi.my_clue_list(keyWord=self.webText.get('cluePhone'))
        self.webApi.goldApply_addGoldApply()
        self.webApi.getGoldApplyList()
        self.webApi.auditGoldApply()
        self.webApi.clue_adminList(keyWord=self.appText.get('cluePhone'),
                                   isInvalid=1, saasCodeSys=0)
        if self.appText.get('web_total') != 1:
            raise RuntimeError('索赔成功-后 总站线索列表应该显示为无效')

    def test_adminRepetitionAllocationClue(self):
        """总部重复分派线索"""
        self.appApi.Login()
        self.webApi.clue_list(sourceId=self.appText.get('XSLY_admin_fb'), myClue='N', followStatus=3)
        self.appApi.ClueInfo()
        self.appApi.Login(userName='admin', saasCode='admin', authCode=0)
        self.webApi.clue_adminList(keyWord=self.appText.get('cluePhone'), saasCodeSys=0)
        dome = self.appText.get('web_total')
        self.webApi.clue_adminList(keyWord=self.appText.get('cluePhone'),
                                   isInvalid=1, saasCodeSys=0)
        dome1 = self.appText.get('web_total')
        self.webApi.add_clue_admin(clueNickName=self.appApi.RandomText(textArr=surname),
                                   cluePhone=self.appText.get('cluePhone'))
        self.assertEqual(self.webText.get('code'), 403)
        """重复分派会添加新线索"""
        self.webApi.clue_adminList(keyWord=self.appText.get('cluePhone'), saasCodeSys=0)
        if self.appText.get('web_total') != dome + 1:
            print('重复分派会添加新线索')
        else:
            """新建线索会干扰旧线索的有效无效显示"""
            self.webApi.clue_adminList(keyWord=self.appText.get('cluePhone'),
                                       isInvalid=1, saasCodeSys=0)
            if self.appText.get('web_total') == dome1:
                print('新建线索会干扰旧线索的有效无效显示')

    def test_001(self):
        """无论线索来源于总部 还是自由都不允许再次指派（包括线索是否释放公海）"""

    def test_admin_clue(self):
        """通过总部分配的线索不允许修改来源"""
        if ApiXfpUrl == 'http://xfp.xfj100.com':
            pass
        else:
            """总站分配待首电数量是否新增"""
            self.appApi.TodayClue(isFirst=0)
            dome = self.appText.get('Total')
            self.appApi.Login(userName='admin', saasCode='admin', authCode=0)
            self.webApi.add_clue_admin(clueNickName=self.appApi.RandomText(textArr=surname))
            if self.webText.get('code') != 200:
                self.webApi.addGoldDetailInfo()
                self.webApi.add_clue_admin(clueNickName=self.appApi.RandomText(textArr=surname))
            self.appApi.Login()
            self.appApi.my_clue_list()
            self.appApi.ClueInfo()
            self.appApi.ClueSave(Status=2,
                                 clueNickName=self.appApi.RandomText(textArr=surname),
                                 sourceId=self.appText.get('XSLY'))
            if self.appText.get('code') == 200:
                raise RuntimeError('总部分配过来的线索,线索来源不能修改')
            # 检验从总站分配过来的线索是否添加待办
            self.appApi.TodayClue(isFirst=0)
            self.assertNotEqual(dome, self.appText.get('Total'))
            self.assertEqual(dome + 1, self.appText.get('Total'))
            dome = self.appText.get('Total')
            """未首电进行转移"""
            self.appApi.ClueChange()  # 线索转移
            self.appApi.TodayClue(isFirst=0)
            self.assertNotEqual(dome, self.appText.get('Total'))
            self.assertEqual(dome - 1, self.appText.get('Total'))

    def test_ClueAllocation_05(self):
        """待分配列表进行分配会有待首电的待办"""
        self.webApi.clue_await_allocition()
        if self.webText.get('total') != 0:
            self.appApi.ClueInfo()
            self.webApi.clue_appoint()
            self.appApi.ClueTask()
            if self.appText.get('total') != 1:
                raise RuntimeError('线索待办数异常')

            if self.appText.get('taskRemark') != '添加线索首电联系':
                raise RuntimeError('线索待办跟进备注异常')




