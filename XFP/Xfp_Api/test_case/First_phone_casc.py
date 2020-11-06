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


class FirstPhoneTestCase(unittest.TestCase):
    """客第壹——首电相关"""

    def __init__(self, *args, **kwargs):
        super(FirstPhoneTestCase, self).__init__(*args, **kwargs)
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
        self.appApi.TodayClue(keyWord=self.appText.get('cluePhone'))
        self.assertEqual(1, self.appText.get('isFirst'))
        # 检查待跟进状态
        self.appApi.GetUserAgenda(endTime=time.strftime("%Y-%m-%d"), keyWord=self.appText.get('cluePhone'))
        self.assertNotEqual(0, self.appText.get('total'))
        # 后台查看是否已首电
        globals()['clueId'] = self.appText.get('clueId')
        self.webApi.TodayClue()
        if self.webText.get('total') != 0:
            a = 0
            while a != self.webText.get('total') - 1:
                if self.webText.get('clueId') == globals()['clueId']:
                    # print(self.webApi.appText.get('notFirstCall'))
                    if str(self.webApi.webText.get('notFirstCall')) != 'False':
                        print("已首电-但后台提示未首电")
                        raise RuntimeError(self.webText.get('ApiXfpUrl'))
                a = a + 1
                time.sleep(1)
                self.webApi.TodayClue(vlue=a)

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
        self.appApi.TodayClue(keyWord=self.appText.get('cluePhone'))
        self.assertEqual(1, self.appText.get('isFirst'))
        self.flowPath.first_phone_non_null()
        # 呼出
        self.appApi.phone_log(callee_num=self.appText.get('cluePhone'), talk_time=12000,
                              call_time=time.strftime("%Y-%m-%d %H:%M:%S"))
        self.appApi.TodayClue(keyWord=self.appText.get('cluePhone'))
        self.assertEqual(1, self.appText.get('isFirst'))

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
        self.appApi.TodayClue(keyWord=self.appText.get('cluePhone'))
        self.assertEqual(1, self.appText.get('isFirst'))

    def test_first_phone_08(self):
        """4、他人打该线索"""
        self.flowPath.first_phone_non_null()
        self.appApi.phone_log(callee_num=self.appText.get('cluePhone'), wait_time=1200, is_me=2,
                              call_time=time.strftime("%Y-%m-%d %H:%M:%S"))
        self.appApi.TodayClue(keyWord=self.appText.get('cluePhone'))
        self.assertEqual(1, self.appText.get('isFirst'))
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
        self.appApi.ConsultantList()
        self.appApi.ClueChange()        # 线索转移
        self.appApi.TodayClue(keyWord=self.appText.get('cluePhone'))         # 转移后查看自己的列表
        # 登陆转移后账号进行查看
        self.assertEqual(0, self.appText.get('Total'))
        self.appApi.Login(userName=XfpUser1, password=XfpPwd1)
        self.appApi.TodayClue(keyWord=self.appText.get('cluePhone'))
        self.assertEqual(0, self.appText.get('isFirst'))

    def test_first_phone_12(self):
        """7、线索转移后B---无首电"""
        self.appApi.Login()
        self.appApi.GetUserData()
        self.test_first_phone_01()
        self.appApi.ConsultantList()
        self.appApi.ClueChange()        # 线索转移
        self.appApi.TodayClue(keyWord=self.appText.get('cluePhone'))         # 转移后查看自己的列表
        # 登陆转移后账号进行查看
        self.assertEqual(0, self.appText.get('Total'))
        self.appApi.Login(userName=XfpUser1, password=XfpPwd1)
        self.appApi.TodayClue(keyWord=self.appText.get('cluePhone'))
        self.assertEqual(1, self.appText.get('isFirst'))





