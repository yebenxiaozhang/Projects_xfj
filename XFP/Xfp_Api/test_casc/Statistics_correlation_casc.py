# -*- coding: utf-8 -*-
# @Time    : 2020/3/21 11:08
# @Author  : 潘师傅
# @File    : Statistics_correlation_casc.py

"""客第壹——统计相关"""
from XFP.PubilcAPI.flowPath import *

"""
首电及时率: 例上户时间为：08:00:00    一分钟超时  超时的时间为08:01:00
    1、在08:00:00-08:01:00 拨打再超时之前上传录音    -首电及时
    2、在08:00:00-08:01:00 拨打再超时之后上传录音    -首电及时
    3、在08:01:00之后拨打                            -首电超时
    4、在08:00:59拨打                                -首电及时
    5、在08:01:00拨打                                -首电超时
    6、在08:01:01拨打                                -首电超时
跟进及时率：

上户邀约率：
    1、创建带看，                 -邀约率不变
    2、提前结束带看，             -邀约率不变
    3、完成带看，                 -邀约率提高
    4、完成带看后，转移客户，     -邀约率提高
    
带看成交率：
    1、录入成交（需要审核）         -成交率不变
    2、审核成功                     -成交率提高
    3、审核失败                     -成交率不变
    4、录入成交，审核成功后转移     -成交率提高
"""


class StatisticsCorrelationTestCase(unittest.TestCase):
    """客第壹——统计相关"""

    def __init__(self, *args, **kwargs):
        super(StatisticsCorrelationTestCase, self).__init__(*args, **kwargs)
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
        cls.app_api = cls.do_request
        cls.app_api.Login()
        cls.app_api.GetUserData()
        cls.request = webApi()
        cls.webApi = cls.request
        cls.webApi.Audit_management()

    def test_first_phone_TimelinessRate_01(self):
        """1、在08:00:00-08:01:00 拨打再超时之前上传录音    -首电及时"""
        self.flowPath.add_new_clue()
        self.appApi.getConsultantCount()
        dome = self.appApi.appText.get('firstCallRatio')
        try:
            self.appApi.phone_log(callee_num=self.appText.get('cluePhone'), talk_time=12000,
                                  call_time=time.strftime("%Y-%m-%d %H:%M:%S"))
        except:
            self.appApi.ClueFollowList()
            self.appApi.ClueFollowSave(taskEndTime=time.strftime("%Y-%m-%d") + ' 22:00:00')
        self.appApi.getConsultantCount()
        if dome < self.appApi.appText.get('firstCallRatio'):
            pass
        else:
            print('在规定时间首电，不算超时')
            raise RuntimeError(self.appApi.appText.get('ApiXfpUrl'))
        self.appApi.ClientEntering(callName=self.appApi.RandomText(textArr=surname),
                                   loanSituation='这个是贷款情况')
        self.assertEqual('成功', self.appApi.appText.get('msg'))

    def test_first_phone_TimelinessRate_02(self):
        """2、在08:00:00-08:01:00 拨打再超时之后上传录音    -首电及时"""
        self.flowPath.add_new_clue()
        self.appApi.getConsultantCount()
        dome = self.appApi.appText.get('firstCallRatio')
        dome1 = time.strftime("%Y-%m-%d %H:%M:%S")
        time.sleep(60)
        self.appApi.phone_log(callee_num=self.appText.get('cluePhone'), talk_time=12000,
                              call_time=dome1)
        self.appApi.getConsultantCount()
        if dome < self.appApi.appText.get('firstCallRatio'):
            pass
        else:
            print('2、在08:00:00-08:01:00 拨打再超时之后上传录音    -首电及时')
            raise RuntimeError(self.appApi.appText.get('ApiXfpUrl'))

    def test_first_phone_TimelinessRate_03(self):
        """3、在08:01:00之后拨打                            -首电超时"""
        self.flowPath.add_new_clue()
        self.appApi.getConsultantCount()
        dome = self.appApi.appText.get('firstCallRatio')
        time.sleep(60)
        dome1 = time.strftime("%Y-%m-%d %H:%M:%S")
        self.appApi.phone_log(callee_num=self.appText.get('cluePhone'), talk_time=12000,
                              call_time=dome1)
        self.appApi.getConsultantCount()
        if dome == self.appApi.appText.get('firstCallRatio'):
            pass
        else:
            print('3、在08:01:00之后拨打                            -首电超时')
            raise RuntimeError(self.appApi.appText.get('ApiXfpUrl'))

    def test_first_phone_TimelinessRate_04(self):
        """4、在08:00:59拨打                                -首电及时"""
        self.flowPath.add_new_clue()
        self.appApi.getConsultantCount()
        dome = self.appApi.appText.get('firstCallRatio')
        self.appApi.time_add(second=59)
        self.appApi.phone_log(callee_num=self.appText.get('cluePhone'), talk_time=12000,
                              call_time=self.appText.get('time_add'))
        self.appApi.getConsultantCount()
        if dome < self.appApi.appText.get('firstCallRatio'):
            pass
        else:
            print('4、在08:00:59拨打                                -首电及时')
            raise RuntimeError(self.appApi.appText.get('ApiXfpUrl'))

    def test_first_phone_TimelinessRate_05(self):
        """5、在08:01:00拨打                                -首电超时"""
        self.flowPath.add_new_clue()
        self.appApi.getConsultantCount()
        time.sleep(2)
        self.appApi.time_add(second=60)
        dome = self.appApi.appText.get('firstCallRatio')
        self.appApi.phone_log(callee_num=self.appText.get('cluePhone'), talk_time=12000,
                              call_time=self.appText.get('time_add'))
        self.appApi.getConsultantCount()
        if dome == self.appApi.appText.get('firstCallRatio'):
            pass
        else:
            print('5、在08:01:00拨打                                -首电超时')
            raise RuntimeError(self.appApi.appText.get('ApiXfpUrl'))

    def test_first_phone_TimelinessRate_06(self):
        """5、在08:01:00拨打                                -首电超时"""
        self.flowPath.add_new_clue()
        self.appApi.getConsultantCount()
        self.appApi.time_add(second=61)
        dome = self.appApi.appText.get('firstCallRatio')
        self.appApi.phone_log(callee_num=self.appText.get('cluePhone'), talk_time=12000,
                              call_time=self.appText.get('time_add'))
        self.appApi.getConsultantCount()
        if dome == self.appApi.appText.get('firstCallRatio'):
            pass
        else:
            print('5、在08:01:00拨打                                -首电超时')
            raise RuntimeError(self.appApi.appText.get('ApiXfpUrl'))























