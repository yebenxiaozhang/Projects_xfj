"""跟进申请-相关（暂缓跟进）"""
from PubilcAPI.flowPath import *

"""
无审核-正常流程：·······现状态··············· 操作流放公海
  1、客户申请暂缓        已同意                 已同意

 一级审核-正常流程：···············现状态··················操作流放公海成功
  2、客户申请暂缓跟进-待审核       申请中 
  3、客户申请暂缓跟进-审核失败     已驳回                 已取消
  4、客户申请暂缓跟进-审核成功     已同意                 已同意

 二级审核-正常流程························现状态·········流放公海的状态
  5、客户申请暂缓跟进-待审核              申请中 
  6、客户申请暂缓跟进-一级审核失败        已驳回            已取消
  7、客户申请暂缓跟进-一级审核成功        审核中 
  8、客户申请暂缓跟进-二级审核失败        已驳回            已取消
  9、客户申请暂缓跟进-二级审核成功        已同意            已同意

 注意事项：
  10、客户暂缓审核中---不允许创建带看，不允许录成交，不允许流放公海（无论是否开启审核，都不允许操作） 
  11、暂停后再次申请暂停

"""


class TestCase(unittest.TestCase):
    """客第壹——跟进申请（暂缓）"""

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

    def test_Defer_01(self):
        """10、客户暂缓审核中---不允许创建带看，不允许录成交，不允许流放公海（无论是否开启审核，都不允许操作）"""
        self.flowPath.client_list_non_null()
        self.appApi.visitProject_list()
        if self.appApi.appText.get('web_total') == 0:
            self.flowPath.add_visit()
            self.flowPath.accomplish_visit()
            self.appApi.visitProject_list()
        self.webApi.Audit_management(suspend=True, suspendLevel=1)  # 修改配置审核

        self.flowPath.suspend_follow()
        dome = time.strftime("%Y-%m-%d %H:%M:%S")
        self.appApi.ClientVisitAdd(projectAId=self.appApi.appText.get('houseId'),
                                   appointmentTime=dome,
                                   seeingConsultant=self.appApi.appText.get('consultantId'),
                                   appointConsultant=self.appApi.appText.get('consultantId'))
        self.assertEqual('已申请暂缓跟进,正在审核中!', self.appApi.appText.get('data'))

        self.appApi.add_deal()  # 录入成交
        self.assertEqual('已申请暂缓跟进,正在审核中!', self.appApi.appText.get('data'))

        self.appApi.client_exile_sea()
        self.assertEqual('已申请暂缓跟进,正在审核中!', self.appApi.appText.get('data'))

        self.webApi.auditList(phoneNum=self.appText.get('cluePhone'))
        self.webApi.audit(auditStatue=2, auditRemark=time.strftime("%Y-%m-%d %H:%M:%S") + ' 审核失败')

    def test_Defer_02(self):
        """1、客户申请暂缓        已同意  """
        self.webApi.Audit_management()  # 修改配置审核
        self.flowPath.client_list_non_null()
        self.appApi.follow_apply(keyWord=self.appText.get('cluePhone'))
        dome = self.appText.get('total')
        """B-1 客户暂缓--无审核--跟进不变"""
        self.appApi.GetUserAgenda()
        zxs_01_db = self.appText.get('total')
        self.appApi.ClientList()
        self.appApi.ClueFollowSave(taskEndTime=time.strftime("%Y-%m-%d %H:%M:%S"), followType='客户')
        self.appApi.ClientTaskPause()
        self.appApi.ClientTask(taskType=2)  # 待办
        self.assertEqual(time.strftime("%Y-%m-%d"), self.appApi.appText.get('endTime')[:10])
        self.appApi.follow_apply(keyWord=self.appText.get('cluePhone'))
        if self.appText.get('total') != dome + 1:
            raise RuntimeError("无审核的情况下 客户申请暂缓没有多加一个跟进")
        self.appApi.GetUserAgenda()
        self.assertEqual(zxs_01_db, self.appText.get('total'))

    def test_Defer_03(self):
        """2、客户申请暂缓跟进-待审核       申请中"""
        # self.flowPath.client_list_non_null()
        self.flowPath.client_list_non_null()
        self.webApi.Audit_management(suspend=True, suspendLevel=1)  # 修改配置审核
        """    B-2 客户申请暂缓--审核中--跟进不变    """
        self.follow_front()
        self.appApi.ClientList()
        self.appApi.ClueFollowSave(taskEndTime=time.strftime("%Y-%m-%d %H:%M:%S"), followType='客户')
        """暂缓失败后进行查看任务待办是否有新增"""
        self.appApi.GetUserAgenda()
        zxs_01_db = self.appText.get('total')
        self.appApi.ClientList()
        self.appApi.ClientTaskPause()
        self.flowPath.apply_status(status='申请中', keyWord=self.appText.get('cluePhone'))
        self.follow_later()
        self.appApi.ClientList()
        """3、客户申请暂缓跟进-审核失败     已驳回                 已取消"""
        dome = time.strftime("%Y-%m-%d %H:%M:%S")
        self.webApi.auditList(phoneNum=self.appText.get('cluePhone'))
        self.webApi.audit(auditStatue=2, auditRemark=dome + ' 审核失败')

        self.flowPath.apply_status(status='已驳回', keyWord=self.appText.get('cluePhone'))
        self.assertEqual(dome + ' 审核失败', self.appApi.appText.get('auditRemark'))

        # 验证暂缓失败后是否有新增
        self.appApi.GetUserAgenda()
        self.assertEqual(zxs_01_db, self.appText.get('total'))

        self.appApi.ClientList()
        self.appApi.client_exile_sea()
        self.flowPath.apply_status(status='已驳回', keyWord=self.appText.get('cluePhone'), vlue=1)

        """首页待办-审核失败后进行流放公海- 待办减少"""
        self.appApi.GetUserAgenda()
        self.assertEqual(zxs_01_db - 1, self.appText.get('totol'))

    def test_Defer_04(self):
        """4、客户申请暂缓跟进-审核成功     已同意                 已同意"""
        self.flowPath.client_list_non_null()
        self.webApi.Audit_management(suspend=True, suspendLevel=1)  # 修改配置审核
        self.appApi.ClientFollowList()
        self.appApi.ClueFollowSave(taskEndTime=time.strftime("%Y-%m-%d %H:%M:%S"), followType='客户')
        # 暂缓前进行检查任务待办数目
        self.appApi.GetUserAgenda()
        dome = self.appText.get('total')
        self.appApi.ClientList()
        self.appApi.ClientTaskPause()

        """暂缓审核中进行"""
        self.webApi.auditList(phoneNum=self.appText.get('cluePhone'))
        self.webApi.audit()

        # 审核通过过进行验证
        self.appApi.GetUserAgenda()
        self.assertEqual(dome, self.appText.get('total'))
        self.flowPath.apply_status(status='已同意', keyWord=self.appText.get('cluePhone'))
        """首页待办-暂缓成功后  进行流放公海"""
        self.appApi.client_exile_sea()
        self.flowPath.apply_status(status='已同意', keyWord=self.appText.get('cluePhone'), vlue=1)
        self.appApi.GetUserAgenda()
        self.assertEqual(dome - 1, self.appText.get('total'))

    def test_Defer_05(self):
        """ 5、客户申请暂缓跟进-待审核              申请中            已取消"""
        self.webApi.Audit_management(suspend=True, suspendLevel=2)  # 修改配置审核
        self.flowPath.client_list_non_null()
        self.flowPath.suspend_follow()
        self.flowPath.apply_status(status='申请中', keyWord=self.appText.get('cluePhone'))

        """6、客户申请暂缓跟进-一级审核失败        已驳回            已驳回"""
        dome = time.strftime("%Y-%m-%d %H:%M:%S")
        self.webApi.auditList(phoneNum=self.appText.get('cluePhone'))
        self.webApi.audit(auditStatue=2, auditRemark=dome + ' 审核失败')

        self.flowPath.apply_status(status='已驳回', keyWord=self.appText.get('cluePhone'))
        self.assertEqual(dome + ' 审核失败', self.appApi.appText.get('auditRemark'))
        self.appApi.client_exile_sea()
        self.flowPath.apply_status(status='已驳回', keyWord=self.appText.get('cluePhone'), vlue=1)

    def test_Defer_06(self):
        """7、客户申请暂缓跟进-一级审核成功        审核中            已取消"""
        self.webApi.Audit_management(suspend=True, suspendLevel=2)  # 修改配置审核
        self.flowPath.client_list_non_null()
        self.flowPath.suspend_follow()
        self.webApi.auditList(phoneNum=self.appText.get('cluePhone'))
        self.webApi.audit()
        self.flowPath.apply_status(status='申请中', keyWord=self.appText.get('cluePhone'))

        """8、客户申请暂缓跟进-二级审核失败        已驳回            已取消"""
        self.webApi.auditList(phoneNum=self.appText.get('cluePhone'), auditLevel=2)
        self.webApi.audit(auditStatue=2, auditRemark=time.strftime("%Y-%m-%d %H:%M:%S") + ' 审核失败')
        self.flowPath.apply_status(status='已驳回', keyWord=self.appText.get('cluePhone'))
        self.appApi.client_exile_sea()
        self.flowPath.apply_status(status='已驳回', keyWord=self.appText.get('cluePhone'), vlue=1)

    def test_Defer_07(self):
        """9、客户申请暂缓跟进-二级审核成功        已同意            已同意"""
        self.webApi.Audit_management(suspend=True, suspendLevel=2)  # 修改配置审核
        self.flowPath.client_list_non_null()
        self.flowPath.suspend_follow()
        self.webApi.auditList(phoneNum=self.appText.get('cluePhone'))
        self.webApi.audit()

        self.webApi.auditList(phoneNum=self.appText.get('cluePhone'), auditLevel=2)
        self.webApi.audit()

        self.flowPath.apply_status(status='已同意', keyWord=self.appText.get('cluePhone'))
        self.appApi.client_exile_sea()
        self.flowPath.apply_status(status='已同意', keyWord=self.appText.get('cluePhone'), vlue=1)

    def test_Defer_08(self):
        """11、暂停后再次申请暂停"""
        self.flowPath.client_list_non_null()
        self.webApi.Audit_management(suspend=True, suspendLevel=1)  # 修改配置审核
        self.flowPath.suspend_follow()
        self.webApi.auditList(phoneNum=self.appText.get('cluePhone'))
        self.webApi.audit()

        self.appApi.ClientFollowList()
        self.appApi.ClueFollowSave(followType='客户', taskEndTime=time.strftime("%Y-%m-%d") + ' 22:00:00')
        self.appApi.ClientTaskPause()
        self.assertEqual(200, self.appApi.appText.get('code'))

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
