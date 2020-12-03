"""后台-线索分配"""
from XFP.PubilcAPI.flowPath import *
"""
    1、幸福币不足，分配失败
    2、无咨询师接受分配，会在待分配列表
    3、上户时间：分站分配时间
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
        # 财富值类型
        cls.appApi.GetLabelList(labelNo='CFZLX', labelName='首电及时率', saasCode='admin')
        cls.appText.set_map('SDJSL', cls.appText.get('remark'))
        cls.appApi.GetLabelList(labelNo='CFZLX', labelName='平台上户', saasCode='admin')
        cls.appText.set_map('PTSH', cls.appText.get('remark'))
        cls.webApi.get_group()
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

    def test_all_allocation_1(self):
        """2、无咨询师接受分配，会在待分配列表"""
        if ApiXfpUrl == 'http://xfp.xfj100.com':
            pass
        else:
            self.webApi.consultant_allocition(isAppoint=0)
            self.appApi.my_clue_list()
            dome = self.appText.get('total')
            self.appApi.Login(userName='admin', saasCode='admin')
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



