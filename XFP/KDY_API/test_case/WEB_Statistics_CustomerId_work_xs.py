"""后台-咨询师工作统计"""
from PubilcAPI.flowPath import *


class TestCase(unittest.TestCase):
    """客第壹后台——咨询师工作统计"""

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
        登录经纪人 获取ID"""
        cls.do_request = appApi()
        cls.appApi = cls.do_request
        cls.appApi.Login()
        cls.appApi.GetUserData()
        cls.request = webApi()
        cls.webApi = cls.request
        cls.webApi.Audit_management()

    def test_CustomerId_work_statistics(self):
        """咨询师工作统计"""
        self.webApi.work_statistics()
        """上户数量   ！   首电及时率         ！ 跟进及时率"""
        self.appApi.getConsultantCount()
        if self.webText.get('web_newClueCount') != self.appText.get('newClueCount'):
            raise RuntimeError('咨询师工作统计上户数量与APP本月概况上户数量不一致')
        if self.webText.get('web_firstCallRatio') != self.appText.get('firstCallRatio'):
            raise RuntimeError('咨询师工作统计首电及时率与APP本月概况首电及时率不一致')
        if self.webText.get('web_followRatio') != self.appText.get('followRatio'):
            raise RuntimeError('咨询师工作统计跟进及时率与APP本月概况首电及时率不一致')

        """通话记录"""
        self.webApi.phoneLogList()
        if self.appText.get('web_total') != self.webText.get('web_callCount'):
            print('咨询师工作统计与通话记录中的通话次数不一致')

        """公海领取"""
        dome = self.webText.get('web_seaClaimClueCount')
        self.appApi.SeaList()  # 公海列表
        if self.appApi.appText.get('total') != 0:
            self.appApi.clue_Assigned()  # 领取线索
            if dome + 1 == self.webText.get('web_seaClaimClueCount'):
                print('咨询师工作统计中领取线索后 没有加1（公海领取）')

        """释放公海批次"""
        if self.webText.get('web_seaClueCount') != self.appText.get('seaClueCount'):
            print('咨询师工作统计中释放公海批次与APP本月概况释放批次不一致')





