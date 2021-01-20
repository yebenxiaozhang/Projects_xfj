"""客户终止跟进-跟进申请"""
from PubilcAPI.flowPath import *

"""
无审核-正常流程：·······现状态··············· 操作流放公海
  1、客户无效终止        已同意
    C-1 客户释放公海--无审核--跟进减少

 一级审核-正常流程：···············现状态··················操作流放公海成功
  2、客户无效终止-待审核           申请中
      C-2 客户释放公海--审核中--跟进不变   
  3、客户无效终止-审核成功         已同意
      C-3 客户释放公海--审核失败--跟进不变
  4、客户无效终止-审核失败         已驳回
      C-4 客户释放公海--审核成功--跟进减少

 二级审核-正常流程························现状态·········流放公海的状态
  5、客户无效终止-待审核                 申请中
  6、客户无效终止-一级审核失败           已驳回
  7、客户无效终止-一级审核成功           审核中
  8、客户无效终止-二级审核失败           已驳回
  9、客户无效终止-二级审核成功           已同意

 注意事项：
  10、客户终止跟进审核中 ---不允许创建带看，不允许录成交，不允许暂缓，不允许流放公海（无论是否开启审核，都不允许操作）
"""


class TestCase(unittest.TestCase):
    """客第壹——跟进申请（客户终止跟进）"""

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

        """审核-成交相关-财务"""
        cls.webApi.finance_deal_auditList()
        while cls.appApi.appText.get('web_total') != 0:
            cls.webApi.finance_deal_audit(auditStatue=2, remark=time.strftime("%Y-%m-%d %H:%M:%S") + '审核不通过')
            cls.webApi.finance_deal_auditList()

        """审核-成交相关-经理"""
        cls.webApi.auditList()
        while cls.appApi.appText.get('web_total') != 0:
            cls.webApi.audit(auditStatue=2, auditRemark=' 审核失败')
            cls.webApi.auditList()
        cls.webApi.auditList(auditLevel=2)
        while cls.appApi.appText.get('web_total') != 0:
            cls.webApi.audit(auditStatue=2, auditRemark=' 审核失败')
            cls.webApi.auditList(auditLevel=2)

    def test_ExileSea_01(self):
        """10、客户终止跟进审核中 ---不允许创建带看，不允许录成交，
        不允许暂缓，（无论是否开启审核，都不允许操作）"""
        self.flowPath.client_list_non_null()
        self.appApi.visitProject_list()
        if self.appApi.appText.get('web_total') == 0:
            self.flowPath.add_visit()
            self.flowPath.accomplish_visit()
            self.appApi.visitProject_list()
        self.webApi.Audit_management(customerStop=True, customerStopLevel=1)  # 修改配置审核
        self.appApi.client_exile_sea()

        dome = time.strftime("%Y-%m-%d %H:%M:%S")
        self.appApi.ClientVisitAdd(projectAId=self.appApi.appText.get('houseId'),
                                   appointmentTime=dome,
                                   seeingConsultant=self.appApi.appText.get('consultantId'),
                                   appointConsultant=self.appApi.appText.get('consultantId'))
        self.assertEqual('已申请客户终止,正在审核中!', self.appApi.appText.get('data'))

        self.appApi.add_deal()  # 录入成交
        self.assertEqual('已申请客户终止,正在审核中!', self.appApi.appText.get('data'))

        self.appApi.ClientTaskPause()
        self.assertEqual('已申请客户终止,正在审核中!', self.appApi.appText.get('data'))

        self.webApi.auditList(phoneNum=self.appText.get('cluePhone'))
        self.webApi.audit(auditStatue=2, auditRemark=time.strftime("%Y-%m-%d %H:%M:%S") + ' 审核失败')

    def test_ExileSea_02(self):
        """1、客户无效终止        已同意"""
        self.webApi.Audit_management()
        """客户释放公海--无审核--跟进减少"""
        """客户释放公海--客户待办--会清空"""
        self.flowPath.client_list_non_null()
        self.appApi.ClientFollowList()
        self.appApi.ClueFollowSave(followType='客户', taskEndTime=time.strftime("%Y-%m-%d") + ' 22:00:00')
        self.appApi.ClientTask()
        kh_db = self.appText.get('total')
        self.appApi.follow_apply(keyWord=self.appText.get('cluePhone'))
        dome = self.appText.get('total')
        self.appApi.GetUserAgenda()
        sy_db = self.appText.get('total')
        self.appApi.ClientList()
        self.appApi.client_exile_sea()
        """11、无审核跟进内容为：线索终止跟进"""
        self.appApi.ClueFollowList()
        self.assertEqual(self.appText.get('followContent'),
                         '客户终止跟进</br>原因:客户已成交</br>备注:python-客户释放公海')
        self.appApi.follow_apply(keyWord=self.appText.get('cluePhone'))
        if dome + 1 != self.appText.get('total'):
            raise RuntimeError("无审核的情况下 客户终止会没有添加一个跟进申请")
        self.appApi.ClientTask()
        if 0 != self.appText.get('total'):
            raise RuntimeError("无效终止后，客户待办应该为空")
        self.appApi.GetUserAgenda()
        if sy_db - kh_db != self.appText.get('total'):
            raise RuntimeError("无效终止后，首页待办应该减少")

    def test_ExileSea_03(self):
        """2、客户无效终止-待审核           申请中"""
        # self.flowPath.client_list_non_null()
        self.webApi.Audit_management(customerStop=True, customerStopLevel=1)  # 修改配置审核
        """    C-2 客户释放公海--审核中--跟进不变    """
        self.client_front()
        self.follow_front()
        self.appApi.ClientList()
        self.appApi.client_exile_sea()
        self.appApi.ClueFollowList()
        self.assertEqual(self.appText.get('followContent'),
                         '申请客户终止跟进</br>原因:客户已成交</br>备注:python-客户释放公海')
        self.flowPath.apply_status(status='申请中', keyWord=self.appText.get('cluePhone'))
        self.follow_later()
        """3、客户无效终止-审核成功         已同意"""
        """    A-4 线客户放公海--审核成功--跟进减少"""
        self.webApi.auditList(phoneNum=self.appText.get('cluePhone'))
        self.webApi.audit()

        self.flowPath.apply_status(status='已同意', keyWord=self.appText.get('cluePhone'))
        self.follow_later(vlue=-1)

    def test_ExileSea_04(self):
        """4、客户无效终止-审核失败         已驳回"""
        dome = time.strftime("%Y-%m-%d %H:%M:%S")
        # self.flowPath.client_list_non_null()
        self.webApi.Audit_management(customerStop=True, customerStopLevel=1)  # 修改配置审核
        self.client_front()
        self.follow_front()
        self.appApi.client_exile_sea()
        self.webApi.auditList(phoneNum=self.appText.get('cluePhone'))
        self.webApi.audit(auditStatue=2,
                          auditRemark=dome + ' 客户无效终止审核失败')

        self.follow_later()
        self.flowPath.apply_status(status='已驳回', keyWord=self.appText.get('cluePhone'))
        self.assertEqual(dome + ' 客户无效终止审核失败', self.appApi.appText.get('auditRemark'))

    def test_ExileSea_05(self):
        """5、客户无效终止-待审核                 申请中"""
        self.flowPath.client_list_non_null()
        self.webApi.Audit_management(customerStop=True, customerStopLevel=2)  # 修改配置审核
        self.appApi.ClientFollowList()
        self.appApi.ClueFollowSave(taskEndTime=time.strftime("%Y-%m-%d %H:%M:%S"), followType='客户')
        """首页待办-客户释放公海-审核中"""
        self.appApi.GetUserAgenda()
        dome = self.appText.get('total')
        self.appApi.ClientList()
        self.appApi.client_exile_sea()
        self.flowPath.apply_status(status='申请中', keyWord=self.appText.get('cluePhone'))

        """6、客户无效终止-一级审核失败           已驳回"""
        self.webApi.auditList(phoneNum=self.appText.get('cluePhone'))
        self.webApi.audit(auditStatue=2, auditRemark=time.strftime("%Y-%m-%d %H:%M:%S") + ' 审核失败')
        self.flowPath.apply_status(status='已驳回', keyWord=self.appText.get('cluePhone'))

        """首页待办-客户释放公海-审核失败"""
        self.appApi.GetUserAgenda()
        self.assertEqual(dome, self.appText.get('total'))

    def test_ExileSea_06(self):
        """7、客户无效终止-一级审核成功           审核中"""
        self.flowPath.client_list_non_null()
        self.webApi.Audit_management(customerStop=True, customerStopLevel=2)  # 修改配置审核
        self.appApi.client_exile_sea()

        self.flowPath.apply_status(status='申请中', keyWord=self.appText.get('cluePhone'))

        self.webApi.auditList(phoneNum=self.appText.get('cluePhone'))
        self.webApi.audit()
        self.flowPath.apply_status(status='申请中', keyWord=self.appText.get('cluePhone'))

        """8、客户无效终止-二级审核失败           已驳回"""
        self.webApi.auditList(phoneNum=self.appText.get('cluePhone'), auditLevel=2)
        self.webApi.audit(auditStatue=2, auditRemark=time.strftime("%Y-%m-%d %H:%M:%S") + ' 审核失败')

        self.flowPath.apply_status(status='已驳回', keyWord=self.appText.get('cluePhone'))

    def test_ExileSea_07(self):
        """9、客户无效终止-二级审核成功           已同意"""
        self.flowPath.client_list_non_null()
        self.webApi.Audit_management(customerStop=True, customerStopLevel=2)  # 修改配置审核
        """首页待办-客户流放公海-审核中"""
        self.appApi.ClientFollowList()
        self.appApi.ClueFollowSave(taskEndTime=time.strftime("%Y-%m-%d %H:%M:%S"), followType='客户')
        self.appApi.GetUserAgenda()
        dome = self.appText.get('total')

        self.appApi.ClientList()
        self.appApi.client_exile_sea()
        self.flowPath.apply_status(status='申请中', keyWord=self.appText.get('cluePhone'))

        self.webApi.auditList(phoneNum=self.appText.get('cluePhone'))
        self.webApi.audit()

        self.appApi.GetUserAgenda()
        self.assertEqual(dome, self.appText.get('total'))

        self.flowPath.apply_status(status='申请中', keyWord=self.appText.get('cluePhone'))

        self.webApi.auditList(phoneNum=self.appText.get('cluePhone'), auditLevel=2)
        self.webApi.audit()

        self.flowPath.apply_status(status='已同意', keyWord=self.appText.get('cluePhone'))

        self.appApi.GetUserAgenda()
        self.assertEqual(dome - 1, self.appText.get('total'))

    def follow_front(self):
        """跟进前"""
        self.appApi.GetUserAgenda(tesk=2)
        globals()['dome'] = self.appText.get('total')

    def follow_later(self, vlue=0):
        """跟进后"""
        self.appApi.GetUserAgenda()
        if vlue == 0:
            self.assertEqual(globals()['dome'], self.appText.get('total'))
        else:
            self.assertNotEqual(globals()['dome'], self.appText.get('total'))
            if vlue == -1:
                self.assertEqual(globals()['dome'] - 1, self.appText.get('total'))
            else:
                self.assertEqual(globals()['dome'] + 1, self.appText.get('total'))

    def client_front(self):
        """客户前"""
        self.flowPath.client_list_non_null()
        self.appApi.ClientFollowList()
        self.appApi.ClueFollowSave(taskEndTime=time.strftime("%Y-%m-%d %H:%M:%S"), followType='客户')
