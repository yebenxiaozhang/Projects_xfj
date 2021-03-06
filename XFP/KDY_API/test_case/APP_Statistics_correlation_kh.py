# -*- coding: utf-8 -*-
# @Time    : 2020/3/21 11:08
# @Author  : 潘师傅
# @File    : Statistics_correlation_casc.py

"""客第壹——统计相关"""
from PubilcAPI.flowPath import *

"""
首电及时率: 例上户时间为：08:00:00    一分钟超时  超时的时间为08:01:00
    1、在08:00:00-08:01:00 拨打再超时之前上传录音    -首电及时
    2、在08:00:00-08:01:00 拨打再超时之后上传录音    -首电及时
    3、在08:01:00之后拨打                            -首电超时
    4、在08:00:59拨打                                -首电及时
    5、在08:01:00拨打                                -首电超时
    6、在08:01:01拨打                                -首电超时

跟进及时率：（客户跟进，与线索跟进）  超过规定时间6小时 算超时
    1、线索跟进
        - 查看线索规定时间跟进 超过6小时      跟进及时率下降
        - 查看线索规定时间跟进 未过6小时      跟进及时率增加
        - 无线索-新增线索      -跟进          跟进及时率增加
    2、客户跟进
        - 查看客户规定时间跟进 超过6小时      跟进及时率下降
        - 查看线索规定时间跟进 未过6小时      跟进及时率增加
        - 无客户-新增客户      -跟进          跟进及时率增加

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


class TestCase(unittest.TestCase):
    """客第壹——统计相关"""

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
        cls.webApi.auditList()
        while cls.appApi.appText.get('web_total') != 0:
            cls.webApi.audit(auditStatue=2, auditRemark=' 审核失败')
            cls.webApi.auditList()
        cls.webApi.auditList(auditLevel=2)
        while cls.appApi.appText.get('web_total') != 0:
            cls.webApi.audit(auditStatue=2, auditRemark=' 审核失败')
            cls.webApi.auditList(auditLevel=2)

        cls.flow = flowPath()
        cls.flowPath = cls.flow
        cls.appText = GlobalMap()
        cls.flowPath.get_label(labelNo='CJX', labelName='成交项目',
                               newlabelName='认购')
        cls.appText.set_map('CJX', cls.appText.get('labelId'))

    def test_client_visit_rate_01(self):
        """1、创建带看，                 -邀约率不变"""
        self.flowPath.client_list_non_null()
        self.appApi.getConsultantCount()
        dome = self.appApi.appText.get('visitRatio')
        self.flowPath.add_visit()
        self.appApi.getConsultantCount()
        self.assertEqual(dome, self.appApi.appText.get('visitRatio'))
        """2、提前结束带看，             -邀约率不变"""
        self.flowPath.advance_over_visit()
        self.appApi.getConsultantCount()
        self.assertEqual(dome, self.appApi.appText.get('visitRatio'))

    def test_client_visit_rate_02(self):
        """3、完成带看，                 -邀约率提高"""
        self.flowPath.client_list_non_null()
        self.appApi.getConsultantCount()
        dome = self.appApi.appText.get('visitRatio')
        self.flowPath.add_visit()
        self.flowPath.accomplish_visit()
        self.appApi.getConsultantCount()
        if self.appApi.appText.get('visitRatio') <= dome:
            print('3、完成带看，                 -邀约率提高')
            raise RuntimeError(self.appApi.appText.get('ApiXfpUrl'))
        dome = self.appApi.appText.get('visitRatio')
        """4、完成带看后，转移客户，     -邀约率提高"""
        self.appApi.client_change()
        self.appApi.getConsultantCount()
        if self.appApi.appText.get('visitRatio') != dome:
            print('4、完成带看后，转移客户，     -邀约率提高')
            raise RuntimeError(self.appApi.appText.get('ApiXfpUrl'))

    def test_deal_rate_01(self):
        """1、录入成交（需要审核）         -成交率不变"""
        self.webApi.Audit_management(customerDeal=True, customerDealLevel=1)
        self.flowPath.client_list_non_null()
        self.appApi.visitProject_list()
        if self.appText.get('web_total') == 0:
            self.flowPath.add_visit()
            self.flowPath.accomplish_visit()
            self.appApi.visitProject_list()

        self.appApi.getConsultantCount()
        dome = self.appApi.appText.get('dealRatio')
        self.appApi.add_deal()
        self.appApi.getConsultantCount()
        if self.appApi.appText.get('dealRatio') != dome:
            print('1、录入成交（需要审核）         -成交率不变')
            raise RuntimeError(self.appApi.appText.get('ApiXfpUrl'))

        """2、审核成功                     -成交率提高"""
        self.webApi.auditList(phoneNum=self.appText.get('cluePhone'))
        self.webApi.audit()

        self.appApi.getConsultantCount()
        if self.appApi.appText.get('dealRatio') <= dome:
            raise RuntimeError('2、审核成功                     -成交率提高')

        """4、录入成交，审核成功后转移     -成交率提高"""
        dome = self.appApi.appText.get('dealRatio')
        self.appApi.client_change()
        self.appApi.getConsultantCount()
        if self.appApi.appText.get('dealRatio') != dome:
            raise RuntimeError('4、录入成交，审核成功后转移     -成交率提高')

    def test_deal_rate_02(self):
        """3、审核失败                     -成交率不变"""
        self.webApi.Audit_management(customerDeal=True, customerDealLevel=1)
        self.flowPath.client_list_non_null()
        self.appApi.visitProject_list()
        if self.appApi.appText.get('web_total') == 0:
            self.flowPath.add_visit()
            self.flowPath.accomplish_visit()
            self.appApi.visitProject_list()
        self.appApi.getConsultantCount()
        dome = self.appApi.appText.get('dealRatio')
        self.appApi.add_deal()  # 录入成交

        self.webApi.auditList(phoneNum=self.appText.get('cluePhone'))
        self.webApi.audit(auditStatue=2,
                          auditRemark=time.strftime("%Y-%m-%d %H:%M:%S") + '审核不通过')
        self.appApi.getConsultantCount()
        if self.appApi.appText.get('dealRatio') != dome:
            print('3、审核失败                     -成交率不变')
            raise RuntimeError(self.appApi.appText.get('ApiXfpUrl'))

    def test_follow_rete_02(self):
        """
            1、跟进及时率-客户
            2、写入跟进后 查看跟进列表是否有新增
            3、写入跟进后 财富值前后的变化
        """
        self.flowPath.client_list_non_null()        # 客户列表不能为空
        self.appApi.getConsultantCount()            # 查看本月概况
        dome = self.appText.get('followRatio')
        self.appApi.ClientTask(taskType=2)          # 获取任务待办截止时间

        self.appApi.time_difference()
        if int(self.appText.get('vlue')) > 1:       # 判断时间是否超时
            GJ_vlue = -10
        else:
            GJ_vlue = 15

        """财富值跟进前后对比"""
        self.appApi.getWealthDetailList(startTime=time.strftime("%Y-%m-%d"),
                                        endTime=time.strftime("%Y-%m-%d"),
                                        orderNo=self.appText.get('orderNo'))
        vlue = self.appText.get('vlue')
        self.appApi.ClientFollowList()
        if self.appText.get('taskId') is None:
            self.appApi.ClientTask(taskType=2)  # 获取任务待办截止时间
        self.appApi.ClueFollowSave(followType='客户', taskEndTime=time.strftime("%Y-%m-%d") + ' 22:00:00')
        time.sleep(1)
        """跟进后 查看跟进列表是否有新增"""
        self.appApi.ClientFollowList()
        self.assertEqual('python-线索/客户跟进，本次沟通记录', self.appText.get('followContent'))
        self.appApi.getConsultantCount()
        if dome == self.appText.get('followRatio') and float(dome) == 1:
            pass
        else:
            if GJ_vlue == -10:
                if self.appText.get('followRatio') >= dome:
                    print('查看线索规定时间跟进 超过1小时      跟进及时率下降')
            else:
                if self.appText.get('followRatio') <= dome:
                    print('查看线索规定时间跟进 未超过1小时      跟进及时率上降')
        self.appApi.getWealthDetailList(startTime=time.strftime("%Y-%m-%d"),
                                        endTime=time.strftime("%Y-%m-%d"),
                                        orderNo=self.appText.get('orderNo'))
        self.assertEqual(vlue + GJ_vlue, self.appText.get('vlue'))

















