# -*- coding: utf-8 -*-
# @Time    : 2019/11/2 10:37
# @Author  : 潘师傅
# @File    : Xm_MB_casc.py
from XFJ.PubilcAPI.FlowPath import *
from XFJ.PubilcAPI.XmApi import *
"""陌拜必填项有：
shopName：门店名称
shopCompany：归属公司
shopAddress：具体位置
shopAgentName：店长姓名
shopAgentTel：店长电话
默认项：
industryType：类型 中介、电销、平台、其他
其他
shopMainName：关键联系人
shopMainTel：关键联系人电话
shopType： 主营方向
shopAgentCount：员工人数
shopYears：开业年限
shopRemark：备注
mainArea：主营区域
shopImgs：附件
"""


class MBTestCace(unittest.TestCase):
    """小秘----陌拜"""
    def __init__(self, *args, **kwargs):
        super(MBTestCace, self).__init__(*args, **kwargs)
        self.do_request = XmApi()
        self.XmRequest = self.do_request
        self.XmTEXT = GlobalMap()

    @classmethod
    def setUpClass(cls):
        """登录小秘 只执行一次"""
        cls.do_request = XmApi()
        cls.to_request = cls.do_request
        cls.to_request.ApiLogin()

    @classmethod
    def tearDownClass(cls):
        """所用用例执行之后的操作==>注销刚刚创建的联盟商"""
        cls.do_request = XmApi()
        cls.XmRequest = cls.do_request
        cls.XmTEXT = GlobalMap()
        cls.city = LogIn()
        cls.City = cls.city
        cls.Web = WebTools()
        cls.WebTooles = cls.Web
        cls.WebTooles.Openbrowser()
        cls.city.LogIn(method='City', d=cls.WebTooles.driver)
        dome = cls.WebTooles.driver.find_element_by_css_selector('#showCityName').text
        while dome != XmSellerCityName:
            cls.WebTooles.driver.find_element_by_css_selector('#showCityName').click()
            time.sleep(0.5)
            cls.WebTooles.driver.find_element_by_link_text(SellerCityName).click()
            time.sleep(2)
            dome = cls.WebTooles.driver.find_element_by_css_selector('#showCityName').text

        cls.WebTooles.Click(type='link_text', value='联盟商管理')
        cls.WebTooles.Click(type='link_text', value='团队管理')
        cls.WebTooles.Input(type='id', value='keyWord2', inputvalue=cls.XmTEXT.get('xmCPhone'))
        cls.WebTooles.Click(type='id', value='searchSeller')
        dome = cls.WebTooles.driver.find_element_by_id('sortTable_info').text
        try:
            assert '显示第 1 至 1 项结果，共 1 项', dome
        except BaseException as e:
            print("断言错误，错误原因：%s" % e)
            raise RuntimeError(cls.XmTEXT.get('xmurl'))
        cls.WebTooles.Click(type='xpath', value='//*[@id="sortTable"]/tbody/tr/td[16]/a[4]/i')
        cls.WebTooles.Click(type='id', value='button-0')
        time.sleep(5)

        # 下面是总站的操作
        cls.city.LogIn(method='admin', d=cls.WebTooles.driver)
        cls.WebTooles.Click(type='link_text', value='联盟商管理')
        cls.WebTooles.Click(type='link_text', value='联盟商注销管理')
        cls.WebTooles.Input(type='id', value='keyWord1', inputvalue=cls.XmTEXT.get('xmCPhone'))
        cls.WebTooles.Click(type='id', value='searchSeller1')
        dome = cls.WebTooles.driver.find_element_by_id('dealTable1_info').text
        try:
            assert '显示第 1 至 1 项结果，共 1 项', dome
        except BaseException as e:
            print("断言错误，错误原因：%s" % e)
            raise RuntimeError(cls.XmTEXT.get('xmurl'))
        cls.WebTooles.Click(type='xpath', value='//*[@id="dealTable1"]/tbody/tr/td[17]/a')
        # cls.WebTooles.Click(type='link_text', value='确认注销联盟商')
        cls.WebTooles.Click(type='id', value='sureHandleSellerBtn')
        time.sleep(10)
        dome = cls.WebTooles.driver.find_element_by_id('dealTable1_info').text
        try:
            assert '显示第 0 至 0 项结果，共 0 项', dome
        except BaseException as e:
            print("断言错误，错误原因：%s" % e)
            raise RuntimeError(cls.XmTEXT.get('xmurl'))









        pass

    def test_1_EstablishMB(self):
        """创建陌拜"""
        try:
            self.XmRequest.Client_list()
            self.XmRequest.MB(shopName=time.strftime("%Y-%m-%d %H:%M:%S"),
                              shopCompany='测试归属公司',
                              shopAgentName='陌拜店长',
                              shopAgentTel='1' + (str(time.time()))[:10])
            self.assertEqual('陌拜资料登记成功！', self.XmTEXT.get('xmcontent'))

        except BaseException as e:
            print("断言错误，错误原因：%s" % e)
            raise RuntimeError(self.XmTEXT.get('xmurl'))

    def test_2_MBList(self):
        """修改陌拜"""
        now = int(time.time())
        self.XmRequest.MBList()
        self.XmRequest.MBParticulars()
        self.XmRequest.AlterMB(shopName=('测试' + time.strftime("%Y-%m-%d")),
                               shopCompany='测试归属公司',
                               shopAgentName='店长',
                               shopAgentTel='1' + str(now),
                               shopMainName='关键联系人',
                               shopMainTel='1' + str(now),
                               shopType='本地新房，二手房',
                               shopAgentCount='100人以上',
                               shopYears='3年以上',
                               shopRemark='1',
                               mainArea='主营区域',
                               shopImgs='/uploads/2019/0930/1f62b001-2547-4193-a1e8-1d695790f4c4.png',
                               industryType='电销')

    def test_3_MBEstablishSeller(self):
        """陌拜创建联盟商"""
        self.XmRequest.MBList()
        try:
            """判断是否为正式站 要是是 则为自己的手机号码
            要是否 则系统随机取一个"""
            if ApiXmUrl == 'http://api.xfj100.com':
                print('正式站咱暂不创建联盟商')
            else:
                self.XmRequest.Search_C_USER()
                self.XmRequest.SellerPrincipalPhone(
                    sellerType='a',         # 联盟商类型
                    sellerName=time.strftime("%Y-%m-%d"),       # 联盟商名称
                    sellerFullName='全称' + time.strftime("%Y-%m-%d"),     # 联盟商全称
                    agentId=self.XmTEXT.get('xmCAgentId'),          # 队长的ID
                    agentName=self.XmTEXT.get('xmCAgentName'),     # 队长的名字
                    mainPerson=None,            # 关键联系人
                    mainPersonTel=None,         # 关键联系人手机号
                    sellerShopType='本地新房，二手房',  # 主营方向
                    sellerAgentCount='21～50人',      # 人数
                    sellerYears='3年以上',     # 门店营业执照
                    sellerUserIdcards=None,     # 负责人身份证
                    sellerLicensePics=None,     # 营业执照
                    showPic=None,       # 门店照片
                    sellerBackbook=None,    # 备案证书
                    sellerAgreement=None        # 联盟商协议
                )
        except BaseException as e:
            print("断言错误，错误原因：%s" % e)
            raise RuntimeError(self.XmTEXT.get('xmurl'))





