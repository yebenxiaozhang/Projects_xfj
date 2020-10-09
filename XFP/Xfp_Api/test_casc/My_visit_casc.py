# -*- coding: utf-8 -*-
# @Time    : 2020/3/21 11:08
# @Author  : 潘师傅
# @File    : My_visit_casc.py

"""我的带看-相关"""
from XFP.PubilcAPI.webApi import *
"""
无审核-正常流程：····························· 流放公海状态
    1、创建带看          进行中                   已取消
    2、完成带看          已完成                   已完成
    3、提前结束带看      已取消                   已取消

一级审核-正常流程：·····································流放公海的状态
    1、创建带看-待审核                   审核中             已取消
    2、创建带看-审核成功                 进行中             已取消
    3、创建带看-审核失败                 已驳回             已驳回
    4、审核成功-完成带看                 已完成             已完成
    5、审核成功-提前结束带看             已取消             已取消

二级审核-正常流程······································流放公海的状态
    1、创建带看-待审核          申请中                     已取消
    2、创建带看-一级审核失败    已驳回                     已驳回
    3、创建带看-一级审核成功    审核中                     已取消
    4、创建带看-二级审核失败    已驳回                     已驳回
    5、创建带看-二级审核成功    进行中                     已取消
    6、审核成功-完成带看        已完成                     已完成
    7、审核成功-提前结束带看    已取消                     已取消
    
操作事项：
    1、审核失败的带看---不允许操作
    2、提前结束的带看---不允许操作
    3、审核中的带看  ---不允许操作
"""


class MyVisitTestCase(unittest.TestCase):
    """幸福派——我的带看"""

    def __init__(self, *args, **kwargs):
        super(MyVisitTestCase, self).__init__(*args, **kwargs)
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
        cls.app_api = cls.do_request
        cls.app_api.Login()
        cls.app_api.GetUserData()
        cls.request = webApi()
        cls.webApi = cls.request
        cls.webApi.Audit_management()

    def test_01(self):
        """1、创建带看          进行中                   已取消"""
        #  创建带看并且完成
        self.appApi.ClientList()
        dome = time.strftime("%Y-%m-%d %H:%M:%S")
        self.appApi.GetMatchingAreaHouse()
        self.appApi.ClientVisitAdd(projectAId=self.appText.get('houseId'), appointmentTime=dome)
        self.appApi.ClientTask(taskTypeStr='带看行程')
        if self.appText.get('total') < 1:
            raise RuntimeError(self.appText.get('ApiXfpUrl'))
        self.appApi.visit_info()
        self.appApi.VisitFlow1()
        self.appApi.ClientTask()
        if self.appText.get('total') >= 2:
            raise RuntimeError(self.appText.get('ApiXfpUrl'))
        self.appApi.Task_Visit_List(appointmentTime=dome)
        self.assertEqual(self.appText.get('visiteStatus'), '1')
        self.assertEqual(self.appText.get('visiteStatusStr'), '已完成')
        # 完成后流放公海
        self.appApi.GetLabelList(labelNo='SZGJYY', labelName='客户已成交')
        self.appApi.client_exile_sea(labelId=self.appText.get('labelId'))
        self.appApi.Task_Visit_List(appointmentTime=dome)
        self.assertEqual(self.appText.get('visiteStatus'), '1')
        self.assertEqual(self.appText.get('visiteStatusStr'), '已完成')

    def test_02(self):
        """流放公海未完成的带看     - 已取消"""
        #  创建带看不完成
        self.appApi.ClientList()
        dome = time.strftime("%Y-%m-%d %H:%M:%S")
        self.appApi.GetMatchingAreaHouse()
        self.appApi.ClientVisitAdd(projectAId=self.appText.get('houseId'))
        self.appApi.ClientTask(taskTypeStr='带看行程')
        if self.appText.get('total') < 1:
            raise RuntimeError(self.appText.get('ApiXfpUrl'))
        self.appApi.Task_Visit_List(appointmentTime=dome)
        self.assertEqual(self.appText.get('visiteStatus'), '0')
        self.assertEqual(self.appText.get('visiteStatusStr'), '进行中')
        # 流放公海
        self.appApi.GetLabelList(labelNo='SZGJYY', labelName='客户已成交')
        self.appApi.client_exile_sea(labelId=self.appText.get('labelId'))
        self.appApi.Task_Visit_List(appointmentTime=dome)
        self.assertEqual(self.appText.get('visiteStatus'), '1')
        self.assertEqual(self.appText.get('visiteStatusStr'), '已取消')

    def test_03(self):
        """流放公海提前结束的带看  - 已取消"""
        self.appApi.ClientList()
        dome = time.strftime("%Y-%m-%d %H:%M:%S")
        self.appApi.GetMatchingAreaHouse()
        self.appApi.ClientVisitAdd(projectAId=self.appText.get('houseId'))
        self.appApi.ClientTask(taskTypeStr='带看行程')
        if self.appText.get('total') < 1:
            raise RuntimeError(self.appText.get('ApiXfpUrl'))
        self.appApi.Task_Visit_List(appointmentTime=dome)
        self.assertEqual(self.appText.get('visiteStatus'), '0')
        self.assertEqual(self.appText.get('visiteStatusStr'), '进行中')
        # 提前结束带看
        self.appApi.ClientTask(taskTypeStr='带看行程')
        self.app_api.visit_info()
        self.app_api.OverVisit()  # 提前结束代办
        self.appApi.Task_Visit_List(appointmentTime=dome)
        self.assertEqual(self.appText.get('visiteStatus'), '0')
        self.assertEqual(self.appText.get('visiteStatusStr'), '已取消')
        # 流放公海
        self.appApi.GetLabelList(labelNo='SZGJYY', labelName='客户已成交')
        self.appApi.client_exile_sea(labelId=self.appText.get('labelId'))
        self.appApi.Task_Visit_List(appointmentTime=dome)
        self.assertEqual(self.appText.get('visiteStatus'), '1')
        self.assertEqual(self.appText.get('visiteStatusStr'), '已取消')

    def test_04(self):
        """流放公海申请中的带看     - 已取消"""
        self.webApi.Audit_management(customerVisit=True, customerVisitLevel=1)
        self.appApi.ClientList()
        dome = time.strftime("%Y-%m-%d %H:%M:%S")
        self.appApi.GetMatchingAreaHouse()
        self.appApi.ClientVisitAdd(projectAId=self.appText.get('houseId'))
        self.appApi.ClientTask(taskTypeStr='带看行程')
        if self.appText.get('total') < 1:
            raise RuntimeError(self.appText.get('ApiXfpUrl'))
        self.appApi.Task_Visit_List(appointmentTime=dome)
        self.assertEqual(self.appText.get('visiteStatus'), '0')
        self.assertEqual(self.appText.get('visiteStatusStr'), '进行中')
        # 流放公海
        self.appApi.GetLabelList(labelNo='SZGJYY', labelName='客户已成交')
        self.appApi.client_exile_sea(labelId=self.appText.get('labelId'))
        self.appApi.Task_Visit_List(appointmentTime=dome)
        self.assertEqual(self.appText.get('visiteStatus'), '1')
        self.assertEqual(self.appText.get('visiteStatusStr'), '已取消')

    def test_05(self):
        """流放公海审核失败的带看   - 已驳回"""





