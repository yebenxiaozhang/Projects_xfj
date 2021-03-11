# -*- coding: utf-8 -*-
# @Time    : 2020/3/21 11:08
# @Author  : 潘师傅
# @File    : First_phone_casc.py

"""首电-相关"""
from PubilcAPI.flowPath import *
import requests
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
        """1、直接添加线索  首页待办是否新增"""
        self.appApi.TodayClue(isFirst=0)
        dome = self.appText.get('Total')

        self.flowPath.add_new_clue()

        # 验证首页待办是否新增
        self.appApi.TodayClue(isFirst=0)
        self.assertNotEqual(dome, self.appText.get('Total'))
        self.assertEqual(dome + 1, self.appText.get('Total'))

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
        """1、新增线索（未首电）客户待办 不会+ 1"""
        self.appApi.GetUserAgenda()
        dome = self.appText.get('total')
        self.flowPath.first_phone_non_null()

        dome2 = self.appText.get('clueId')
        # 验证新增线索 待办是否有添加
        self.appApi.GetUserAgenda()
        self.assertEqual(dome, self.appText.get('total'))
        self.appApi.phone_log(callee_num=self.appText.get('cluePhone'), wait_time=1200, is_me=2,
                              call_time=time.strftime("%Y-%m-%d %H:%M:%S"))
        """2、首电过后 客户待办会加 + 1"""
        self.appApi.GetUserAgenda()
        self.assertEqual(dome + 1, self.appText.get('total'))
        self.appApi.TodayClue(isFirst=1)
        dome1 = 0
        globals()['r.text'] = json.loads(json.dumps(self.appText.get('records')))
        while globals()['r.text'][dome1]['clueId'] != dome2:
            dome1 = dome1 + 1
        self.assertEqual('1', globals()['r.text'][dome1]['isFirst'])
        # self.appApi.phone_log(callee_num=self.appText.get('cluePhone'), talk_time=1200, is_me=2,
        #                       call_time=time.strftime("%Y-%m-%d %H:%M:%S"))
        self.appApi.CluePhoneLog(clueId=dome2)
        self.assertEqual(1, self.appText.get('isFirst'))

    def test_first_phone_09(self):
        """6、未首电不允许转客户--公海领取"""
        self.flowPath.first_phone_non_null()
        self.appApi.ClientEntering(callName=self.appApi.RandomText(textArr=surname),
                                   loanSituation='这个是贷款情况')
        self.assertEqual('该线索未首电,不能转为客户!', self.appText.get('data'))

    def test_first_phone_10(self):
        """1、未首电转客户"""
        """2、从公海领取-待办列表是否有新增"""
        self.appApi.TodayClue(isFirst=0)
        dome = self.appText.get('Total')
        self.appApi.SeaList()  # 公海列表
        self.appApi.clue_Assigned()  # 领取线索
        # 验证从公海领取 待首电是否有新增
        self.appApi.TodayClue(isFirst=0)
        self.assertNotEqual(dome, self.appText.get('Total'))
        self.assertEqual(dome + 1, self.appText.get('Total'))

        self.appApi.my_clue_list()
        self.appApi.ClueInfo()
        self.appApi.ClientEntering(callName=self.appApi.RandomText(textArr=surname),
                                   loanSituation='这个是贷款情况')
        if '该线索未首电,不能转为客户!' != self.appText.get('data'):
            print(self.appText.get('data'))
            self.appApi.ClueFollowList()
            print(self.appText.get('data'))
            raise RuntimeError('该线索未首电,不能转为客户!')

        self.appApi.ExileSea()
        self.assertNotEqual(200, self.appText.get('code'))
        self.assertEqual('该线索未首电,不能终止跟进!', self.appText.get('data'))

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
        """任务待办会显示为今日24:00"""
        self.appApi.ClueTask()
        self.assertEqual(self.appText.get('endTime'), time.strftime("%Y-%m-%d 23:59:59"))





