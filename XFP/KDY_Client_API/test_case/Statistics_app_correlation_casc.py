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

    def setUp(self):
        """残留审核 失败！！！"""
        self.webApi.audit_List()
        while self.webApi.webText.get('total') != 0:
            self.webApi.auditApply(isAudit=False, auditRemark='客户流放公海')
            self.webApi.audit_List()
        self.webApi.audit_List(auditLevel=2)
        while self.webApi.webText.get('total') != 0:
            self.webApi.auditApply(isAudit=False, auditRemark='客户流放公海')
            self.webApi.audit_List()

    def test_client_visit_rate_01(self):
        """1、创建带看，                 -邀约率不变"""
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
        self.appApi.getConsultantCount()
        dome = self.appApi.appText.get('dealRatio')
        self.flowPath.add_deal()
        self.appApi.getConsultantCount()
        if self.appApi.appText.get('dealRatio') != dome:
            print('1、录入成交（需要审核）         -成交率不变')
            raise RuntimeError(self.appApi.appText.get('ApiXfpUrl'))
        """2、审核成功                     -成交率提高"""
        self.webApi.audit_List()
        self.webApi.auditApply(customerId=self.appApi.appText.get('customerId'))
        self.appApi.getConsultantCount()
        if self.appApi.appText.get('dealRatio') <= dome:
            print('2、审核成功                     -成交率提高')
            raise RuntimeError(self.appApi.appText.get('ApiXfpUrl'))
        """4、录入成交，审核成功后转移     -成交率提高"""
        dome = self.appApi.appText.get('dealRatio')
        self.appApi.client_change()
        self.appApi.getConsultantCount()
        if self.appApi.appText.get('dealRatio') != dome:
            print('4、录入成交，审核成功后转移     -成交率提高')
            raise RuntimeError(self.appApi.appText.get('ApiXfpUrl'))

    def test_deal_rate_02(self):
        """3、审核失败                     -成交率不变"""
        self.webApi.Audit_management(customerDeal=True, customerDealLevel=1)
        self.appApi.getConsultantCount()
        dome = self.appApi.appText.get('dealRatio')
        self.flowPath.add_deal()
        self.webApi.audit_List()
        self.webApi.auditApply(customerId=self.appApi.appText.get('customerId'), isAudit=False)
        self.appApi.getConsultantCount()
        if self.appApi.appText.get('dealRatio') != dome:
            print('3、审核失败                     -成交率不变')
            raise RuntimeError(self.appApi.appText.get('ApiXfpUrl'))

    def test_follow_rete_02(self):
        """ 2、客户跟进
                - 查看客户规定时间跟进 超过6小时      跟进及时率下降
                - 查看客户规定时间跟进 未过6小时      跟进及时率增加
                - 无客户-新增客户      -跟进          跟进及时率增加"""
        self.appApi.ClientList()
        if self.appText.get('total') != 0:
            self.appApi.getConsultantCount()
            dome = self.appText.get('followRatio')
            self.appApi.ClientTask(taskType='2')
            self.appApi.time_difference()
            if int(self.appText.get('vlue')) >= 1:
                """查看客户规定时间跟进 超过6小时      跟进及时率下降"""
                self.appApi.ClientFollowList()
                self.appApi.ClueFollowSave(followType='客户', taskEndTime=time.strftime("%Y-%m-%d %H:%M:%S"))
                time.sleep(1)
                self.appApi.getConsultantCount()
                if float(dome) == 1:
                    pass
                else:
                    if self.appText.get('followRatio') >= dome:
                        print('查看客户规定时间跟进 超过6小时      跟进及时率下降')
                        raise RuntimeError(self.appApi.appText.get('ApiXfpUrl'))
            else:
                self.appApi.ClientFollowList()
                self.appApi.ClueFollowSave(followType='客户', taskEndTime=time.strftime("%Y-%m-%d %H:%M:%S"))
                time.sleep(1)
                self.appApi.getConsultantCount()
                if float(dome) == 1:
                    pass
                else:
                    if self.appText.get('followRatio') <= dome:
                        print('- 查看客户规定时间跟进 未过1小时      跟进及时率增加')
                        raise RuntimeError(self.appApi.appText.get('ApiXfpUrl'))
        else:
            """-无客户-新增客户      -跟进          跟进及时率增加"""
            self.flowPath.client_list_non_null()
            self.appApi.getConsultantCount()
            dome = self.appText.get('followRatio')
            self.appApi.ClientFollowList()
            self.appApi.ClueFollowSave(followType='客户', taskEndTime=time.strftime("%Y-%m-%d %H:%M:%S"))
            time.sleep(1)
            self.appApi.getConsultantCount()
            if float(dome) == 1:
                pass
            else:
                if self.appText.get('followRatio') < dome:
                    print('- 无客户-新增客户      -跟进          跟进及时率增加')
                    raise RuntimeError(self.appApi.appText.get('ApiXfpUrl'))















