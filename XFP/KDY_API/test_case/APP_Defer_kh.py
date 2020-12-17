"""跟进申请-相关（暂缓跟进）"""
from XFP.PubilcAPI.flowPath import *

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
        cls.webApi.auditList()
        while cls.appText.get('web_total') != 0:
            cls.webApi.audit(auditStatue=2, auditRemark=' 审核失败')
            cls.webApi.auditList()
        cls.webApi.auditList(auditLevel=2)
        while cls.appText.get('web_total') != 0:
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
        self.follow_front()
        self.flowPath.suspend_follow()
        self.appApi.ClientTask(taskType=2)  # 待办
        self.assertEqual(time.strftime("%Y-%m-%d"), self.appApi.appText.get('endTime')[:10])
        self.appApi.follow_apply(keyWord=self.appText.get('cluePhone'))
        if self.appText.get('total') != dome + 1:
            raise RuntimeError("无审核的情况下 客户申请暂缓没有多加一个跟进")
        self.follow_later()

    def test_Defer_03(self):
        """2、客户申请暂缓跟进-待审核       申请中"""
        # self.flowPath.client_list_non_null()
        self.flowPath.client_list_non_null()
        self.webApi.Audit_management(suspend=True, suspendLevel=1)  # 修改配置审核
        """    B-2 客户申请暂缓--审核中--跟进不变    """
        self.follow_front()
        self.appApi.ClientList()
        self.flowPath.suspend_follow()
        self.flowPath.apply_status(status='申请中', keyWord=self.appText.get('cluePhone'))
        self.follow_later()
        self.appApi.ClientList()
        """3、客户申请暂缓跟进-审核失败     已驳回                 已取消"""
        dome = time.strftime("%Y-%m-%d %H:%M:%S")
        self.webApi.auditList(phoneNum=self.appText.get('cluePhone'))
        self.webApi.audit(auditStatue=2, auditRemark=dome + ' 审核失败')

        self.flowPath.apply_status(status='已驳回', keyWord=self.appText.get('cluePhone'))
        self.assertEqual(dome + ' 审核失败', self.appApi.appText.get('auditRemark'))
        self.appApi.client_exile_sea()
        self.flowPath.apply_status(status='已驳回', keyWord=self.appText.get('cluePhone'), vlue=1)

    def test_Defer_04(self):
        """4、客户申请暂缓跟进-审核成功     已同意                 已同意"""
        self.flowPath.client_list_non_null()
        self.webApi.Audit_management(suspend=True, suspendLevel=1)  # 修改配置审核
        self.flowPath.suspend_follow()
        self.webApi.auditList(phoneNum=self.appText.get('cluePhone'))
        self.webApi.audit()

        self.flowPath.apply_status(status='已同意', keyWord=self.appText.get('cluePhone'))
        self.appApi.client_exile_sea()
        self.flowPath.apply_status(status='已同意', keyWord=self.appText.get('cluePhone'), vlue=1)

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