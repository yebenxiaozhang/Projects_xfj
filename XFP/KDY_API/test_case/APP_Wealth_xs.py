"""财富值-相关"""
from XFP.PubilcAPI.flowPath import *
"""
1、拨打时间在超时前---增加财富值(上传时间再超时后)
2、正常首电-----------增加财富值
3、超时首电-----------扣除财富值
4、线索转移过后------进行首电|跟进  不增加首电及时率财富值
"""


class TestCase(unittest.TestCase):
    """客第壹——财富值"""

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
        cls.appApi.ping_admin()
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
        cls.appApi.GetLabelList(labelNo='CFZLX', labelName='首电及时率', saasCode='admin')
        cls.appText.set_map('SDJSL', cls.appText.get('remark'))

    def test_wealth_01(self):
        """1、拨打时间在超时前---增加财富值(上传时间再超时后)"""
        self.appApi.ClueSave(clueNickName=self.appApi.RandomText(textArr=surname),
                             sourceId=self.appApi.appText.get('XSLY'),
                             keyWords=self.appApi.appText.get('XSBQ'))
        dome1 = time.strftime("%Y-%m-%d %H:%M:%S")
        time.sleep(60)
        self.appApi.phone_log(callee_num=self.appText.get('cluePhone'), talk_time=12000,
                              call_time=dome1)
        self.appApi.getWealthDetailList(startTime=time.strftime("%Y-%m-%d"),
                                        endTime=time.strftime("%Y-%m-%d"),
                                        wealthType=self.appText.get('SDJSL'),
                                        orderNo=self.appText.get('orderNo'))
        if self.appText.get('vlue') != 10:
            raise RuntimeError('拨打再超时前，上传超时算首电及时')

    def test_wealth_02(self):
        """2、正常首电-----------增加财富值"""
        self.appApi.ClueSave(clueNickName=self.appApi.RandomText(textArr=surname),
                             sourceId=self.appApi.appText.get('XSLY'),
                             keyWords=self.appApi.appText.get('XSBQ'))
        dome1 = time.strftime("%Y-%m-%d %H:%M:%S")
        self.appApi.phone_log(callee_num=self.appText.get('cluePhone'), talk_time=12000,
                              call_time=dome1)
        self.appApi.getWealthDetailList(startTime=time.strftime("%Y-%m-%d"),
                                        endTime=time.strftime("%Y-%m-%d"),
                                        wealthType=self.appText.get('SDJSL'),
                                        orderNo=self.appText.get('orderNo'))
        if self.appText.get('vlue') != 10:
            raise RuntimeError('2、正常首电-----------增加财富值')
        """4、线索转移过后------进行首电|跟进  不增加首电及时率财富值"""
        self.appApi.ClueChange()
        self.appApi.Login(userName=XfpUser1)
        self.appApi.GetUserData()
        dome1 = time.strftime("%Y-%m-%d %H:%M:%S")
        self.appApi.phone_log(callee_num=self.appText.get('cluePhone'), talk_time=12000,
                              call_time=dome1, is_me=2)
        self.appApi.getWealthDetailList(startTime=time.strftime("%Y-%m-%d"),
                                        endTime=time.strftime("%Y-%m-%d"),
                                        wealthType=self.appText.get('SDJSL'),
                                        orderNo=self.appText.get('orderNo'))
        if self.appText.get('vlue') != 0:
            raise RuntimeError('已首电转移过后不能在加财富值')

    def test_wealth_03(self):
        """3、超时首电-----------扣除财富值"""
        self.appApi.ClueSave(clueNickName=self.appApi.RandomText(textArr=surname),
                             sourceId=self.appApi.appText.get('XSLY'),
                             keyWords=self.appApi.appText.get('XSBQ'))
        dome = (datetime.datetime.now() + datetime.timedelta(minutes=2)).strftime("%Y-%m-%d %H:%M:%S")
        self.appApi.phone_log(callee_num=self.appText.get('cluePhone'), talk_time=12000,
                              call_time=dome)
        self.appApi.getWealthDetailList(startTime=time.strftime("%Y-%m-%d"),
                                        endTime=time.strftime("%Y-%m-%d"),
                                        wealthType=self.appText.get('SDJSL'),
                                        orderNo=self.appText.get('orderNo'))
        if self.appText.get('vlue') != -5:
            raise RuntimeError('3、超时首电-----------扣除财富值')










