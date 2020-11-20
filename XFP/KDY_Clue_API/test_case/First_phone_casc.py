# -*- coding: utf-8 -*-
# @Time    : 2020/3/21 11:08
# @Author  : 潘师傅
# @File    : First_phone_casc.py

"""首电-相关"""
from XFP.PubilcAPI.flowPath import *

"""
首电：
    1、首电不管接通已否             --都算首电
    2、首电不管是呼入还是呼出       --都算首电
    3、他人打该线索也要有通话记录   
    4、他人打该线索
    5、线索转客户要将通话也一并转移
    6、未首电不允许转客户
    7、线索转移后B需要进行首电
    8、首电不算跟进
"""


class TestCase(unittest.TestCase):
    """客第壹——首电相关"""

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

    def test_first_phone_01(self):
        """8、首电不算跟进"""
        self.flowPath.first_phone_non_null()
        self.appApi.CluePhoneLog()
        self.webApi.CluePhoneLog()
        dome = self.appText.get('total')
        dome1 = self.appText.get('consultantName')
        webdome = self.webText.get('total')
        webdome1 = self.webText.get('consultantName')
        self.appApi.phone_log(callee_num=self.appText.get('cluePhone'), talk_time=12000,
                              call_time=time.strftime("%Y-%m-%d %H:%M:%S"))
        self.appApi.CluePhoneLog()
        self.webApi.CluePhoneLog()
        # 检查相关参数
        self.assertEqual(dome + 1, self.appText.get('total'))
        self.assertEqual('呼出', self.appText.get('isFlagCallStr'))
        self.assertEqual(dome1, self.appText.get('consultantName'))
        self.assertEqual(webdome + 1, self.webText.get('total'))
        self.assertEqual('呼出', self.webText.get('isFlagCallStr'))
        self.assertEqual(webdome1, self.webText.get('consultantName'))
        # 检查首页 待首电状态
        self.appApi.TodayClue(isFirst=1)
        dome1 = 0
        globals()['r.text'] = json.loads(json.dumps(self.appText.get('records')))
        while globals()['r.text'][dome1]['clueId'] != self.appText.get('clueId'):
            dome1 = dome1 + 1
        self.assertEqual('1', globals()['r.text'][dome1]['isFirst'])
        # 检查待跟进状态
        self.appApi.GetUserAgenda(keyWord=self.appText.get('cluePhone'))
        self.assertNotEqual(0, self.appText.get('total'))
        # 后台查看是否已首电
        globals()['clueId'] = self.appText.get('clueId')
        self.webApi.TodayClue()
        globals()['r.text'] = json.loads(self.webText.get('r.text'))
        if self.webText.get('total') != 0:
            a = 0
            while a != self.webText.get('total') - 1:
                if globals()['r.text']['data'][a]['clueId'] == globals()['clueId']:
                    if str(globals()['r.text']['data'][a]['notFirstCall']) != 'False':
                        print("已首电-但后台提示未首电")
                        raise RuntimeError(self.webText.get('ApiXfpUrl'))
                a = a + 1

        """7、线索转移后B---无首电"""
        self.appApi.ClueChange()        # 线索转移
        self.appApi.my_clue_list(keyWord=self.appText.get('cluePhone'))
        # 登陆转移后账号进行查看
        self.assertEqual(0, self.appText.get('total'))
        self.appApi.Login(userName=XfpUser1, password=XfpPwd1)
        self.appApi.TodayClue(isFirst=1)
        dome1 = 0
        globals()['r.text'] = json.loads(json.dumps(self.appText.get('records')))
        while globals()['r.text'][dome1]['clueId'] != self.appText.get('clueId'):
            dome1 = dome1 + 1
        self.assertEqual('1', globals()['r.text'][dome1]['isFirst'])
        self.appApi.Login()

    def test_first_phone_02(self):
        """5、线索转客户要将通话也一并转移"""
        self.flowPath.add_new_clue()
        self.appApi.phone_log(callee_num=self.appText.get('cluePhone'), talk_time=12000,
                              call_time=time.strftime("%Y-%m-%d %H:%M:%S"))
        self.appApi.ClientEntering(callName=self.appApi.RandomText(textArr=surname),
                                   loanSituation='这个是贷款情况')
        self.assertEqual('成功', self.appApi.appText.get('msg'))
        self.appApi.CluePhoneLog()
        self.assertEqual(1, self.appText.get('total'))
        self.appApi.phone_log(callee_num=self.appText.get('cluePhone'), talk_time=12000,
                              call_time=time.strftime("%Y-%m-%d %H:%M:%S"))
        self.appApi.CluePhoneLog()
        self.assertEqual(2, self.appText.get('total'))
        self.webApi.CluePhoneLog()
        self.assertEqual(2, self.webText.get('total'))

    def test_first_phone_03(self):
        """2、首电不管是呼入还是呼出       --都算首电"""
        self.flowPath.first_phone_non_null()
        self.appApi.phone_log(callee_num=self.appText.get('cluePhone'), is_own_call=0, talk_time=12000,
                              call_time=time.strftime("%Y-%m-%d %H:%M:%S"))

        self.appApi.TodayClue(isFirst=1)
        dome1 = 0
        globals()['r.text'] = json.loads(json.dumps(self.appText.get('records')))
        while globals()['r.text'][dome1]['clueId'] != self.appText.get('clueId'):
            dome1 = dome1 + 1
        self.assertEqual('1', globals()['r.text'][dome1]['isFirst'])
        self.flowPath.first_phone_non_null()
        # 呼出
        self.appApi.phone_log(callee_num=self.appText.get('cluePhone'), talk_time=12000,
                              call_time=time.strftime("%Y-%m-%d %H:%M:%S"))
        self.appApi.TodayClue(isFirst=1)
        dome1 = 0
        globals()['r.text'] = json.loads(json.dumps(self.appText.get('records')))
        while globals()['r.text'][dome1]['clueId'] != self.appText.get('clueId'):
            dome1 = dome1 + 1
        self.assertEqual('1', globals()['r.text'][dome1]['isFirst'])

    def test_first_phone_04(self):
        """呼入-计入在通话记录"""
        self.flowPath.clue_non_null()
        self.appApi.ClueInfo()
        self.appApi.phone_log(callee_num=self.appText.get('cluePhone'), is_own_call=0, talk_time=12000,
                              call_time=time.strftime("%Y-%m-%d %H:%M:%S"))
        self.appApi.CluePhoneLog()
        self.webApi.CluePhoneLog()
        self.assertEqual('呼入', self.appText.get('isFlagCallStr'))
        self.assertEqual('呼入', self.webText.get('isFlagCallStr'))

    def test_first_phone_05(self):
        """3、他人打该线索也要有通话记录 ---他人打该线索-呼出"""
        self.flowPath.clue_non_null()
        dome = self.appText.get('consultantName')
        self.appApi.ClueInfo()
        self.appApi.phone_log(callee_num=self.appText.get('cluePhone'), is_me=2, talk_time=12000,
                              call_time=time.strftime("%Y-%m-%d %H:%M:%S"))
        self.appApi.CluePhoneLog()
        self.webApi.CluePhoneLog()
        self.assertEqual('呼出', self.appText.get('isFlagCallStr'))
        self.assertEqual('呼出', self.webText.get('isFlagCallStr'))
        self.assertNotEqual(dome, self.appText.get('consultantName'))
        self.assertNotEqual(dome, self.webText.get('consultantName'))

    def test_first_phone_06(self):
        """3、他人打该线索也要有通话记录 ---他人打该线索-呼入"""
        self.flowPath.clue_non_null()
        self.appApi.GetUserData()
        dome = self.appText.get('consultantName')
        self.appApi.ClueInfo()
        self.appApi.phone_log(callee_num=self.appText.get('cluePhone'),
                              is_me=2, is_own_call=0, talk_time=12000,
                              call_time=time.strftime("%Y-%m-%d %H:%M:%S"))
        self.appApi.CluePhoneLog()
        self.webApi.CluePhoneLog()
        self.assertEqual('呼入', self.appText.get('isFlagCallStr'))
        self.assertEqual('呼入', self.webText.get('isFlagCallStr'))
        self.assertNotEqual(dome, self.appText.get('consultantName'))
        self.assertNotEqual(dome, self.webText.get('consultantName'))

    def test_first_phone_07(self):
        """1、首电不管接通已否--首电为未接通--算首电"""
        self.flowPath.first_phone_non_null()
        self.appApi.phone_log(callee_num=self.appText.get('cluePhone'), wait_time=1200,
                              call_time=time.strftime("%Y-%m-%d %H:%M:%S"))
        self.appApi.TodayClue(isFirst=1)
        dome1 = 0
        globals()['r.text'] = json.loads(json.dumps(self.appText.get('records')))
        while globals()['r.text'][dome1]['clueId'] != self.appText.get('clueId'):
            dome1 = dome1 + 1
        self.assertEqual('1', globals()['r.text'][dome1]['isFirst'])

    def test_first_phone_08(self):
        """4、他人打该线索"""
        self.flowPath.first_phone_non_null()
        self.appApi.phone_log(callee_num=self.appText.get('cluePhone'), wait_time=1200, is_me=2,
                              call_time=time.strftime("%Y-%m-%d %H:%M:%S"))
        self.appApi.TodayClue(isFirst=1)
        dome1 = 0
        globals()['r.text'] = json.loads(json.dumps(self.appText.get('records')))
        while globals()['r.text'][dome1]['clueId'] != self.appText.get('clueId'):
            dome1 = dome1 + 1
        self.assertEqual('1', globals()['r.text'][dome1]['isFirst'])
        self.appApi.phone_log(callee_num=self.appText.get('cluePhone'), talk_time=1200, is_me=2,
                              call_time=time.strftime("%Y-%m-%d %H:%M:%S"))
        self.appApi.CluePhoneLog()
        self.assertEqual(0, self.appText.get('isFirst'))

    def test_first_phone_09(self):
        """6、未首电不允许转客户--公海领取"""
        self.flowPath.first_phone_non_null()
        self.appApi.ClientEntering(callName=self.appApi.RandomText(textArr=surname),
                                   loanSituation='这个是贷款情况')
        self.assertEqual('该线索未首电,不能转为客户!', self.appText.get('data'))

    def test_first_phone_10(self):
        """6、未首电不允许转客户--新线索转客户"""
        self.appApi.ClueSave(clueNickName=self.appApi.RandomText(textArr=surname))
        self.appApi.ClientEntering(callName=self.appApi.RandomText(textArr=surname),
                                   loanSituation='这个是贷款情况')
        self.assertEqual('该线索未首电,不能转为客户!', self.appText.get('data'))

    def test_first_phone_11(self):
        """7、线索转移后B---有首电"""
        self.flowPath.first_phone_non_null()
        self.appApi.phone_log(callee_num=self.appText.get('cluePhone'), wait_time=1200, is_me=2,
                              call_time=time.strftime("%Y-%m-%d %H:%M:%S"))
        self.appApi.ClueChange()        # 线索转移
        self.appApi.my_clue_list(keyWord=self.appText.get('cluePhone'))
        # 登陆转移后账号进行查看
        self.assertEqual(0, self.appText.get('total'))
        self.appApi.ClueInfo()
        self.appApi.Login(userName=XfpUser1, password=XfpPwd1)
        self.appApi.GetUserData()
        self.appApi.my_clue_list(keyWord=self.appText.get('cluePhone'))
        self.appApi.CluePhoneLog()
        self.assertEqual(1, self.appText.get('total'))







