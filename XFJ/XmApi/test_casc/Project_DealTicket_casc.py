# -*- coding: utf-8 -*-
# @Time    : 2019/11/5 17:23
# @Author  : 潘师傅
# @File    : Project_DealTicket_casc.py
"""项目---成交确认/挞定"""
from XFJ.PubilcAPI.FlowPath import *
import json
"""
客户的主要性质有：本地  异地
主要账户类型有：A类联盟商队长， A类联盟商队员  C类联盟商队长 C类联盟商队员
"""


class DealTicketTestCace(unittest.TestCase):
    """小秘----成交确认"""
    def __init__(self, *args, **kwargs):
        super(DealTicketTestCace, self).__init__(*args, **kwargs)
        self.do_request = XmApi()
        self.XmRequest = self.do_request
        self.XmTEXT = GlobalMap()
        self.Agent_request = AgentApi()
        self.AgentRequest = self.Agent_request
        self.AgentTEXT = GlobalMap()
        self.Xfk_request = XfkApi()
        self.XfkRequest = self.Xfk_request
        self.XfkTEXT = GlobalMap()
        self.NRTEXT = HandleRequest()
        self.TEXT = self.NRTEXT
        self.TEXT = GlobalMap()
        self.FlowPath = FlowPath()
        self.FlowPath = self.FlowPath

    @classmethod
    def setUpClass(cls):
        """登录小秘、幸福客 只执行一次"""
        cls.do_request = XmApi()
        cls.to_request = cls.do_request
        cls.to_request.ApiLogin()
        cls.do_request = XfkApi()
        cls.to_request = cls.do_request
        cls.to_request.LoginXfk()

    @classmethod
    def tearDownClass(cls):
        """所用用例执行之后的操作"""
        pass

    def test_RandomUserAlterDeal(self):
        """随机账户---修改成交单"""
        AGENTUSER = [AgentUser1, AgentUser3, AgentUser5, AgentUser7, AgentUser9]
        dome = self.XmRequest.RandomText(AGENTUSER)
        """修改后进行确认、账号有异地A 异地C、本地A、本地C、默认团队C"""
        self.FlowPath.TheNewDeal(user=dome)
        # print(self.XfkTEXT.get('sellerYJRete'))
        # print(self.XfkTEXT.get('sellerYJAmount'))
        # print(self.XfkTEXT.get('sellerXJJRete'))
        # print(self.XfkTEXT.get('sellerXJJAmount'))
        #
        # print(self.XfkTEXT.get('XFJYJRete'))
        # print(self.XfkTEXT.get('XFJYJAmount'))
        # print(self.XfkTEXT.get('XFJXJJRete'))
        # print(self.XfkTEXT.get('XFJXJJAmount'))
        if ApiXmUrl == 'http://api.xfj100.com':
            demo = ['50~100套', '两房', '三房', '复式', '别墅']
        else:
            demo = ['一房', '两房', '三房', '复式', '商铺']
        demo1 = ['分期付款', '不限定', '按揭贷款', '分期付款', '不限定']
        for x, y in zip(demo, demo1):
            self.XmRequest.DealTicketList()
            self.XfkRequest.ProjectExpect()
            self.XfkRequest.HouseType(houseTypeName=x)
            """修改签约单"""
            test1 = random.randint(100000, 1000000)
            test2 = random.randint(20, 300)
            test3 = random.randint(10000000000, 19999999999)
            self.XmRequest.AlterDealTicket(roomNoStr=self.XfkTEXT.get('roomNoStr'),
                                           houseTypeId=self.XfkTEXT.get('houseTypeId'),
                                           squareBuilding=test2,   # 面积
                                           roomPriceTotal=float(test1),    # 总价
                                           houseTypeName=x,
                                           commissionRate=self.XfkTEXT.get('XFJYJRete'),
                                           commissionRatePrice=self.XfkTEXT.get('XFJYJAmount'),
                                           XFJMoneyRate=self.XfkTEXT.get('XFJXJJRete'),
                                           XFJMoneyRatePrice=self.XfkTEXT.get('XFJXJJAmount'),
                                           proportion=self.XfkTEXT.get('sellerYJRete'),
                                           addAmount=self.XfkTEXT.get('sellerYJAmount'),
                                           LMSMoneyRate=self.XfkTEXT.get('sellerXJJRete'),
                                           LMSMoneyRatePrice=self.XfkTEXT.get('sellerXJJAmount'),
                                           paymentMethod=y,
                                           customerMobile=test3,
                                           customerName='客户' + x)
            if self.XmTEXT.get('resultCode') == 0 and x == '三房':
                pass
            else:
                self.XmRequest.DealTicketParticulars()          # 获取客户类型 A或者C
                response = json.loads(json.dumps(json.loads(self.XmTEXT.get('extend')),
                                                 indent=4, sort_keys=False, ensure_ascii=False))
                """户型、面积、总价、户型名称、应收比例、额外应收、应付比例、额外应付、应收总额、应付总额"""
                self.assertEqual(response['houseTypeId'], self.XfkTEXT.get('houseTypeId'))
                self.assertEqual(response['squareBuilding'], str(test2))
                self.assertEqual(response['houseTypeName'], x)
                # 付款方式、业主姓名、业主电话
                self.assertEqual(response['paymentMethod'], y)
                self.assertEqual(response['customerName'], '客户' + x)
                self.assertEqual(float(response['customerMobile']), float(test3))

    def test_IdenticalRoomNoStr2(self):
        """先挞定，然后修改签约单，房号为挞定的房号"""
        try:
            """先获取第二个房号、在首位进行修改成第二个房号"""
            self.XmRequest.DealTicketList()
            dome = self.XmTEXT.get('roomNoStr')
            self.XmRequest.DealCancellation(checkingRemark='小秘挞定' + time.strftime("%Y-%m-%d"))
            self.assertEqual(1, self.XmTEXT.get('resultCode'))
            """挞定成功后 查看幸福客客户详情的历史跟进"""
            self.XfkRequest.ExamineClientParticulars()
            globals()['xfktext'] = json.loads(json.dumps(json.loads(self.XmTEXT.get('XFKtext')),
                                                         indent=4, sort_keys=False, ensure_ascii=False))
            self.assertEqual('终止', globals()['xfktext']['extend']['customerPrjStatusName'])
            self.assertEqual('小秘挞定' + time.strftime("%Y-%m-%d"),
                             globals()['xfktext']['extend']['followList'][0]['content'])
            self.assertEqual('挞定', globals()['xfktext']['extend']['followList'][1]['content'])
            """修改签约单"""
            # self.FlowPath.TheNewDeal()
            self.XmRequest.DealTicketList()
            self.XfkRequest.ProjectExpect()
            self.XfkRequest.HouseType()
            """修改签约单"""
            test1 = random.randint(100000, 1000000)
            test2 = random.randint(20, 300)
            test3 = random.randint(10000000000, 19999999999)
            self.XmRequest.AlterDealTicket(roomNoStr=dome,
                                           houseTypeId=self.XfkTEXT.get('houseTypeId'),
                                           squareBuilding=test2,   # 面积
                                           roomPriceTotal=float(test1),    # 总价
                                           houseTypeName='公寓',
                                           commissionRate=self.XfkTEXT.get('XFJYJRete'),
                                           commissionRatePrice=self.XfkTEXT.get('XFJYJAmount'),
                                           XFJMoneyRate=self.XfkTEXT.get('XFJXJJRete'),
                                           XFJMoneyRatePrice=self.XfkTEXT.get('XFJXJJAmount'),
                                           proportion=self.XfkTEXT.get('sellerYJRete'),
                                           addAmount=self.XfkTEXT.get('sellerYJAmount'),
                                           LMSMoneyRate=self.XfkTEXT.get('sellerXJJRete'),
                                           LMSMoneyRatePrice=self.XfkTEXT.get('sellerXJJAmount'),
                                           customerMobile=test3,
                                           customerName='客户')
            self.assertEqual(1, self.XmTEXT.get('resultCode'))

        except BaseException as e:
            print("断言错误，错误原因：%s" % e)
            raise RuntimeError(self.XmTEXT.get('xmurl'))

    def test_IdenticalRoomNoStr(self):
        """相同的房号"""
        try:
            """先获取第二个房号、在首位进行修改成第二个房号"""
            self.XmRequest.DealTicketList(value=1)
            dome = self.XmTEXT.get('roomNoStr')
            self.XmRequest.DealTicketList()
            self.XmRequest.DealTicketParticulars()
            self.XfkRequest.ProjectExpect()
            self.XfkRequest.HouseType()
            """修改签约单"""
            test1 = random.randint(100000, 1000000)
            test2 = random.randint(20, 300)
            test3 = random.randint(10000000000, 19999999999)
            self.XmRequest.AlterDealTicket(roomNoStr=dome,
                                           houseTypeId=self.XfkTEXT.get('houseTypeId'),
                                           squareBuilding=test2,   # 面积
                                           roomPriceTotal=float(test1),    # 总价
                                           houseTypeName='公寓',
                                           commissionRate=self.XfkTEXT.get('XFJYJRete'),
                                           commissionRatePrice=self.XfkTEXT.get('XFJYJAmount'),
                                           XFJMoneyRate=self.XfkTEXT.get('XFJXJJRete'),
                                           XFJMoneyRatePrice=self.XfkTEXT.get('XFJXJJAmount'),
                                           proportion=self.XfkTEXT.get('sellerYJRete'),
                                           addAmount=self.XfkTEXT.get('sellerYJAmount'),
                                           LMSMoneyRate=self.XfkTEXT.get('sellerXJJRete'),
                                           LMSMoneyRatePrice=self.XfkTEXT.get('sellerXJJAmount'),
                                           customerMobile=test3,
                                           customerName='客户')
            self.assertEqual('房号不能重复', self.XmTEXT.get('xmcontent'))

        except BaseException as e:
            print("断言错误，错误原因：%s" % e)
            raise RuntimeError(self.XmTEXT.get('xmurl'))


