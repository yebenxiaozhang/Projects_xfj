"""后台-线索分配"""
from PubilcAPI.flowPath import *
"""
    1、幸福币不足，分配失败
    2、无咨询师接受分配，会在待分配列表
    3、上户时间：分站分配时间
"""


class TestCase(unittest.TestCase):
    """客第壹——线索分配"""

    def __init__(self, *args, **kwargs):
        super(TestCase, self).__init__(*args, **kwargs)
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
        cls.appApi = cls.do_request
        cls.appApi.Login()
        cls.appApi.GetUserData()
        cls.request = webApi()
        cls.webApi = cls.request
        cls.webApi.Audit_management()

    def test_all_allocation_1(self):
        """2、无咨询师接受分配，会在待分配列表"""
        if ApiXfpUrl == 'http://xfp.xfj100.com':
            pass
        else:
            self.webApi.consultant_allocition(isAppoint=0)
            self.appApi.my_clue_list()
            dome = self.appText.get('total')
            self.appApi.Login(userName='admin', saasCode='admin', authCode=0)
            self.webApi.add_clue_admin(clueNickName=self.appApi.RandomText(textArr=surname))
            self.appApi.Login()
            self.webApi.clue_await_allocition(keyWord=self.webText.get('cluePhone'))
            self.assertEqual(1, self.webText.get('total'))
            self.assertNotEqual(self.webText.get('receptionTime'), self.webText.get('createdTime'))
            """3、上户时间：分站分配时间"""
            self.webApi.clue_appoint()
            self.webApi.clue_await_allocition(keyWord=self.webText.get('cluePhone'))
            self.assertEqual(0, self.webText.get('total'))
            self.appApi.my_clue_list()
            self.assertNotEqual(dome, self.appText.get('total'))
            self.appApi.ClueInfo()
            self.assertNotEqual(self.webText.get('receptionTime'), self.webText.get('createdTime'))
            self.assertNotEqual(self.appText.get('receptionTime'), self.appText.get('createdTime'))
            self.assertEqual(self.webText.get('createdTime'), self.appText.get('createdTime'))
            self.webApi.consultant_allocition(isAppoint=1)

            """留点记录"""
            self.webApi.clue_detail()
            if self.appText.get('remark') != '总站添加线索':
                print('线索存在留点记录，但是分派给咨询师后，留点记录为空')

            """总部分配到分站-分站无在线人员 通过手动分派人员 要扣除财富值"""
            self.appApi.getWealthDetailList(startTime=time.strftime("%Y-%m-%d"),
                                            endTime=time.strftime("%Y-%m-%d"),
                                            wealthType=self.appText.get('PTSH'),
                                            orderNo=self.appText.get('orderNo'))
            if self.appText.get('vlue') != -300:
                raise RuntimeError('总部分配到分站-分站无在线人员 通过手动分派人员 要扣除财富值')

    def test_repetition_compensation(self):
        """重复申请索赔"""
        if ApiXfpUrl == 'http://xfp.xfj100.com':
            pass
        else:
            # self.webApi.clue_list(myClue='N', sourceId=self.appText.get('XSLY_admin'))
            # self.appApi.ClueInfo()
            self.webApi.goldApply_addGoldApply()
            self.webApi.goldApply_addGoldApply()
            if self.appText.get('data') != '该线索已索赔，详情可查看索赔记录!':
                print(self.appText.get('data'))
                print(self.appText.get('orderNo'))
                raise RuntimeError('索赔提示文案不对？')

            """审核失败后 再次申请是否可以？"""
            self.webApi.getGoldApplyList()
            self.webApi.auditGoldApply(applyStatus=False)
            self.webApi.goldApply_addGoldApply()
            self.assertEqual(self.appText.get('data'), '该线索已索赔，详情可查看索赔记录!')

    def test_adminRepetitionAllocationClue(self):
        """总部重复分派线索"""
        self.appApi.Login()
        self.webApi.clue_list(sourceId=self.appText.get('XSLY_admin'), myClue='N')
        self.appApi.ClueInfo()
        self.appApi.Login(userName='admin', saasCode='admin', authCode=0)
        self.webApi.add_clue_admin(clueNickName=self.appApi.RandomText(textArr=surname),
                                   cluePhone=self.appText.get('cluePhone'))
        self.assertEqual(self.webText.get('code'), 403)



