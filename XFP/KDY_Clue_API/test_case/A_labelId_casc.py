"""标签-相关"""
from XFP.PubilcAPI.flowPath import *


class TestCase(unittest.TestCase):

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

    def test_config_01(self):
        """项目大于3个"""
        self.appApi.AllBuildingUpdate()
        while self.appText.get('total') < 3:
            dome = time.strftime("%Y-%m-%d %H:%M:%S")
            self.webApi.add_house(houseName=dome)
            self.appApi.AllBuildingUpdate()

    def test_config_02(self):
        """资料信息"""
        self.appApi.Information()
        while self.appText.get('total') < 1:
            self.webApi.add_house_data(data='楼盘内容'+ time.strftime("%Y-%m-%d %H:%M:%S"))
            self.appApi.Information()

    def test_config_03(self):
        """商务信息"""
        self.appApi.BusinessInformation()
        while self.appText.get('total') < 1:
            self.webApi.add_house_business_information()
            self.appApi.BusinessInformation()

    def test_config_04(self):
        """楼盘问答"""
        self.appApi.HouseQA()
        while self.appText.get('total') < 1:
            self.webApi.add_house_questions()
            self.appApi.HouseQA()




