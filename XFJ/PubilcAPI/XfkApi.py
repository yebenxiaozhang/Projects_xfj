from XFJ.PubilcMethod.HandleRequest import HandleRequest
from XFJ.Config.Conifg import *
import json
import random
from XFJ.GlobalMap import GlobalMap


class XfkApi:
    def __init__(self):
        self.do_request = HandleRequest()
        self.to_request = self.do_request
        self.XfkTEXT = GlobalMap()

    def GetRequest(self, url, data):
        """GET请求"""
        r = self.do_request.to_request(method="get",
                                       url=(ApiAgentUrl + url),
                                       data=data)
        r.raise_for_status()
        globals()['r.text'] = json.loads(r.text)
        assert globals()['r.text']['resultCode'] == 1
        self.XfkTEXT.set_map('XFKtext', globals()['r.text'])

    def PostRequest(self, url, data):
        """post请求"""
        r = self.do_request.to_request(method="post",
                                       url=(ApiAgentUrl + url),
                                       data=data)
        r.raise_for_status()
        globals()['r.text'] = json.loads(r.text)
        self.XfkTEXT.set_map('XFKtext', globals()['r.text'])
        self.XfkTEXT.set_map('XFKcontent', globals()['r.text']['content'])

    def LoginXfk(self, user=XfkUser, pwd=XfkPwd):
        do_request = HandleRequest()
        r = do_request.to_request(method="post",
                                  url=(ApiLoninUrl + "/account.do?command=checkLogin"),
                                  data={"agentTel": user,
                                        "agentLoginPassword": pwd})
        r.raise_for_status()
        globals()['r.text'] = json.loads(r.text)
        self.XfkTEXT.set_map('Content', globals()['r.text']['Content'])
        if self.XfkTEXT.get('Content') == '登录成功':
            globals()["token"] = globals()['r.text']['Extend']['agentToken']
            self.XfkTEXT.set_map('agentName', globals()['r.text']['Extend']['agentName'])
            globals()["agentUid"] = globals()['r.text']['Extend']['agentUid']

    def alterName(self, agentname):
        """修改昵称"""
        do_request = HandleRequest()
        r = do_request.to_request(method='post',
                                  url=ApiLoninUrl + '/account.do?command=updateAgentInfoAll',
                                  data={'agentToken': globals()['token'],
                                        'agentUid': globals()['agentUid'],
                                        'agentName': agentname,
                                        'token': globals()['token']})
        r.raise_for_status()
        globals()['r.text'] = json.loads(r.text)
        self.XfkTEXT.set_map('Content', globals()['r.text']['Content'])

    def Template(self, countent, countentId=None):
        """新增/修改模板"""
        self.PostRequest(url='/api/mobile/followTemplateService/addOrUpdateFollowTemplate.json',
                         data= {'token': globals()['token'],
                                'followTemplateId': countentId,
                                'followTemplate': countent})
        self.XfkTEXT.set_map('content', globals()['r.text']['content'])

    def getTemplate(self, value=0):
        """获取跟进模板"""
        self.GetRequest(url='/api/mobile/followTemplateService/getMySelfFollowTemplate.json',
                        data={'token': globals()['token']})
        self.XfkTEXT.set_map('extend', globals()['r.text']['extend'])
        if self.XfkTEXT.get('extend') != []:
            self.XfkTEXT.set_map('followTemplate', globals()['r.text']['extend'][value]['followTemplate'])
            self.XfkTEXT.set_map('followTemplateId', globals()['r.text']['extend'][value]['followTemplateId'])

    def getAllTemplate(self):
        """获取所有跟进模板+系统模板"""
        self.GetRequest(url='/api/mobile/followTemplateService/getMySelfAndPublicFollowTemplate.json',
                        data={
                             'token': globals()['token'],
                             'followTemplateType': '2'
                         })
        if globals()['r.text']['extend']['mySelfFollowTemplateList'] != []:
            self.XfkTEXT.set_map('followTemplate',
                                 globals()['r.text']['extend']['mySelfFollowTemplateList'][0]['followTemplate'])
            self.XfkTEXT.set_map('followTemplateId',
                                 globals()['r.text']['extend']['mySelfFollowTemplateList'][0]['followTemplateId'])

    def delTemplate(self, TemplateIds):
        """删除跟进模板"""
        self.PostRequest(url='/api/mobile/followTemplateService/deleteFollowTemplate.json',
                         data={
                             'token': globals()['token'],
                             'followTemplateIds': TemplateIds
                         })

    def alterPwd(self, new, old):
        """修改密码"""
        do_request = HandleRequest()
        r = do_request.to_request(method='post',
                                  url=ApiLoninUrl + '/password.do?command=updateAgentLoginPassword',
                                  data={'newPassword': new,
                                        'oldPassword': old,
                                        'agentUid': globals()['agentUid'],
                                        'token': globals()['token'],
                                        'agentToken': globals()['token']})
        r.raise_for_status()
        globals()['r.text'] = json.loads(r.text)
        self.XfkTEXT.set_map('Content', globals()['r.text']['Content'])

    def bindingWx(self):
        """获取绑定微信页面"""
        self.GetRequest(url='/api/mobile/agentService/getBindingAllWxList',
                        data={'agentToken': globals()['token']})
        self.XfkTEXT.set_map('content', globals()['r.text']['content'])

    def AttacheList(self, StartTime='', EndTime='', Page=1, Level=None, Status=None, Days=None, vlue=0):
        """专员列表"""
        self.GetRequest(url="/api/mobile/projectCommissionerService/getCustomerList/v2",
                        data={'token': globals()["token"],
                              'startTime': StartTime,  # 开始时间
                              'endTime': EndTime,  # 结束时间
                              'rowsDisplayed': '20',
                              'pageNum': Page,
                              'level': Level,  # 等级： a、b、c
                              'status': Status,  # 状态:  1：待处理 2：未上门 3：已上门 4：已签约 5：已结佣 6：终止
                              'days': Days,  # 时间筛选
                              'projectId': ''})
        globals()['projectName'] = globals()['r.text']['extend']['list'][0]['projectName']
        globals()['applyId'] = globals()['r.text']['extend']['list'][0]['applyId']
        self.XfkTEXT.set_map('applyId', globals()['r.text']['extend']['list'][0]['applyId'])
        self.XfkTEXT.set_map('xfkcustomerTel', globals()['r.text']['extend']['list'][vlue]['customerTel'])
        self.XfkTEXT.set_map('XFKTotal', globals()['r.text']['extend']['total'])

    def HousesList(self, StartTime='', EndTime='', Page=1, Level=None, Status=None, Days=None):
        """专员列表"""
        self.GetRequest(url="/api/mobile/salesService/getCustomerList/v2",
                        data={'token': globals()["token"],
                              'startTime': StartTime,  # 开始时间
                              'endTime': EndTime,  # 结束时间
                              'rowsDisplayed': '20',
                              'pageNum': Page,
                              'level': Level,  # 等级： a、b、c
                              'status': Status,  # 状态:  1：待处理 2：未上门 3：已上门 4：已签约 5：已结佣 6：终止
                              'days': Days,  # 时间筛选
                              'projectId': ''})
        globals()['projectName'] = globals()['r.text']['extend']['list'][0]['projectName']
        globals()['applyId'] = globals()['r.text']['extend']['list'][0]['applyId']
        self.XfkTEXT.set_map('applyId', globals()['r.text']['extend']['list'][0]['applyId'])
        self.XfkTEXT.set_map('xfkcustomerTel', globals()['r.text']['extend']['list'][0]['customerTel'])
        self.XfkTEXT.set_map('XFKTotal', globals()['r.text']['extend']['total'])

    def ForRegistrationID(self):
        """获取报名ID"""
        self.GetRequest(url='/api/mobile/projectService/getProjectAllTypeList/7.1.2.json',
                        data={'cityId': cityId,
                              'tpye': 'local',
                              'token': globals()['token']})
        a = 0
        globals()['tuanName'] = globals()['r.text']['extend'][a]['projectName']
        while ProjectName != globals()['tuanName']:
            a = a + 1
            globals()['tuanName'] = globals()['r.text']['extend'][a]['projectName']
        globals()['tuanId'] = globals()['r.text']['extend'][a]['tuanId']

    def RecommendNew(self):
        """报名新房"""
        import time
        phone = '1' + str(int(time.time()))
        username = '用户' + phone[-4:]
        self.PostRequest(url=('/api/mobile/agentService/v4/apply/' +
                              globals()['tuanId'] + '/0/' +
                              globals()['token'] + '/7.2.0.json'),
                         data={'phone': phone,
                               'username': username})

    def ExamineClientParticulars(self):
        """客户详情"""
        self.GetRequest(url='/api/mobile/projectCommissionerService/getCustomerDetail.json',
                        data={'token': globals()['token'],
                              'applyId': self.XfkTEXT.get('applyId')})
        a = 0
        while globals()['r.text']['extend']['salesList'][a]['salesName'] != XfkSalesName:
            a = a + 1
        self.XfkTEXT.set_map('xfkSalesId', globals()['r.text']['extend']['salesList'][a]['salesId'])
        globals()['salesId'] = globals()['r.text']['extend']['salesList'][a]['salesId']
        self.XfkTEXT.set_map('sellerCityId', globals()['r.text']['extend']['sellerCityId'])
        self.XfkTEXT.set_map('sellerCityName', globals()['r.text']['extend']['sellerCityName'])
        self.XfkTEXT.set_map('content', globals()['r.text']['extend']['followList'][0]['content'])
        globals()['sellerCityId'] = globals()['r.text']['extend']['sellerCityId']
        self.XfkTEXT.set_map('sellerType', globals()['r.text']['extend']['sellerType'])

    def AttacheOperation(self, content='测试数据', FollowConclusion=1, Level='a', SalesId=None, TureOrFalse=1):
        """验客跟进/报备分配"""
        self.PostRequest(url='/api/mobile/projectCommissionerService/submitCustomerOperating/v2',
                         data={'token': globals()['token'],
                               'applyId': globals()['applyId'],
                               'customerFollow': content,
                               'followConclusion': FollowConclusion,  # 1:持续跟进 0：无效终止
                               'level': Level,  # 等级： a、b、c
                               'salesId': SalesId,  # 售楼员ID
                               'propertyDeveloperRecordStatus': TureOrFalse})
        self.XfkTEXT.set_map('content', globals()['r.text']['content'])

    def HousesOperation(self, content='测试数据', FollowConclusion=1, Level='a', FollowType=2):
        """电话跟进/上门跟进"""
        self.PostRequest(url='/api/mobile/salesService/submitCustomerOperating/v2',
                         data={'token': globals()['token'],
                               'applyId': globals()['applyId'],
                               'customerFollow': content,
                               'followConclusion': FollowConclusion,  # 1:持续跟进 0：无效终止
                               'level': Level,  # 等级： a、b、c
                               'followType': FollowType  # 1：电话跟进 2：上门跟进
                               })

    def ProjectExpect(self, value=0):
        """查询项目的期数"""
        self.GetRequest(url='/api/mobile/commonBussinuess/searchTuansByApplyId',
                        data={
                            'token': globals()['token'],
                            'applyId': self.XfkTEXT.get('applyId')
                        })
        self.XfkTEXT.set_map('tuanId', globals()['r.text']['extend'][value]['tuanId'])

    def HouseType(self, houseTypeName='公寓'):
        """选择户型"""
        self.ExamineClientParticulars()
        self.GetRequest(url='/api/mobile/commonBussinuess/searchTuanHouseTypeCommissionTypesByTuanId',
                        data={
                            'token': globals()['token'],
                            'tuanId': self.XfkTEXT.get('tuanId')
                        })
        globals()['a'] = 0
        if ApiXmUrl == 'http://api.xfj100.com':
            houseTypeName = '1~49套'
        else:
            pass

        try:
            while globals()['r.text']['extend'][globals()['a']]['houseTypeName'] != houseTypeName:
                globals()['a'] = globals()['a'] + 1
        except:
            globals()['a'] = 0
            print(f"找不到户型为{houseTypeName}, 现默认为第一个户型")
        self.XfkTEXT.set_map('houseTypeId', globals()['r.text']['extend'][globals()['a']]['houseTypeId'])
        self.XfkTEXT.set_map('houseTypeName', globals()['r.text']['extend'][globals()['a']]['houseTypeName'])
        globals()['houseTypes'] = globals()['r.text']['extend'][globals()['a']]['commissionTypeVOList']
        """房间类型、房间名称、签约百分比、签约百分比之后的金额"""
        if self.XfkTEXT.get('sellerType') == 'a':
            a = 0
            try:
                while globals()['houseTypes'][a]['typeTitle'] != '佣金' or \
                        globals()['houseTypes'][a]['sellerType'] != 'A':
                    a = a + 1
                self.XfkTEXT.set_map('sellerYJRete', globals()['houseTypes'][a]['rate'])
                self.XfkTEXT.set_map('sellerYJAmount', globals()['houseTypes'][a]['amount'])
            except:
                print("该户型可能不存在佣金比例，默认都为O")
                self.XfkTEXT.set_map('sellerYJRete', 0)
                self.XfkTEXT.set_map('sellerYJAmount', 0)

            a = 0
            try:
                while globals()['houseTypes'][a]['typeTitle'] != '现金奖' or \
                        globals()['houseTypes'][a]['sellerType'] != 'A':
                    a = a + 1
                self.XfkTEXT.set_map('sellerXJJRete', globals()['houseTypes'][a]['rate'])
                self.XfkTEXT.set_map('sellerXJJAmount', globals()['houseTypes'][a]['amount'])
            except:
                print("该户型可能不存在现金奖，默认都为O")
                self.XfkTEXT.set_map('sellerXJJRete', 0)
                self.XfkTEXT.set_map('sellerXJJAmount', 0)
        else:
            a = 0
            try:
                while globals()['houseTypes'][a]['typeTitle'] != '佣金' or \
                        globals()['houseTypes'][a]['sellerType'] != 'B':
                    a = a + 1
                self.XfkTEXT.set_map('sellerYJRete', globals()['houseTypes'][a]['rate'])
                self.XfkTEXT.set_map('sellerYJAmount', globals()['houseTypes'][a]['amount'])
            except:
                print("该户型可能不存在佣金，默认都为O")
                self.XfkTEXT.set_map('sellerYJRete', 0)
                self.XfkTEXT.set_map('sellerYJAmount', 0)

            a = 0
            try:
                while globals()['houseTypes'][a]['typeTitle'] != '现金奖' or \
                        globals()['houseTypes'][a]['sellerType'] != 'B':
                    a = a + 1
                self.XfkTEXT.set_map('sellerXJJRete', globals()['houseTypes'][a]['rate'])
                self.XfkTEXT.set_map('sellerXJJAmount', globals()['houseTypes'][a]['amount'])
            except:
                print("该户型可能不存在现金奖，默认都为O")
                self.XfkTEXT.set_map('sellerXJJRete', 0)
                self.XfkTEXT.set_map('sellerXJJAmount', 0)

        a = 0
        try:
            while globals()['houseTypes'][a]['typeTitle'] != '佣金' or \
                    globals()['houseTypes'][a]['sellerType'] != 'X':
                a = a + 1
            self.XfkTEXT.set_map('XFJYJRete', globals()['houseTypes'][a]['rate'])
            self.XfkTEXT.set_map('XFJYJAmount', globals()['houseTypes'][a]['amount'])
        except:
            print("该户型可能不存在佣金，默认都为O")
            self.XfkTEXT.set_map('XFJYJRete', 0)
            self.XfkTEXT.set_map('XFJYJAmount', 0)

        a = 0
        try:
            while globals()['houseTypes'][a]['typeTitle'] != '现金奖' or \
                    globals()['houseTypes'][a]['sellerType'] != 'X':
                a = a + 1
            self.XfkTEXT.set_map('XFJXJJRete', globals()['houseTypes'][a]['rate'])
            self.XfkTEXT.set_map('XFJXJJAmount', globals()['houseTypes'][a]['amount'])
        except:
            print("该户型可能不存在现金奖，默认都为O")
            self.XfkTEXT.set_map('XFJXJJRete', 0)
            self.XfkTEXT.set_map('XFJXJJAmount', 0)

    def ContractAgo(self):
        """签约前"""
        self.GetRequest(url='/api/mobile/deal/getDealInformation/v3',
                        data={'token': globals()['token'],
                              'applyId': globals()['applyId']})
        self.XfkTEXT.set_map('dealNo', globals()['r.text']['extend']['deal']['dealNo'])
        self.XfkTEXT.set_map('xflbId', globals()['r.text']['extend']['deal']['xflbId'])
        self.XfkTEXT.set_map('estateName', globals()['r.text']['extend']['deal']['estateName'])

        self.XfkTEXT.set_map('signTime', globals()['r.text']['extend']['deal']['signTimeStr'])
        self.XfkTEXT.set_map('customerName', globals()['r.text']['extend']['deal']['customerName'])
        self.XfkTEXT.set_map('customerMobile', globals()['r.text']['extend']['deal']['customerMobile'])

    def AttacheContract(self):
        """签约"""
        dome = random.randint(200000, 1000000)
        self.XfkTEXT.set_map('commissionPrice', "%.2f" % (round(dome * self.XfkTEXT.get('XFJYJRete'), 2) +
                             round(self.XfkTEXT.get('XFJYJAmount'), 2) +
                             round(dome * float(self.XfkTEXT.get('XFJXJJRete')), 2) +
                             round(self.XfkTEXT.get('XFJXJJAmount'), 2)))
        self.XfkTEXT.set_map('sellerMoney', "%.2f" % (round(self.XfkTEXT.get('sellerYJRete') * dome, 2) +
                             self.XfkTEXT.get('sellerYJAmount')))
        self.XfkTEXT.set_map('RoomNoStr', '房号' + globals()['applyId'])
        self.XfkTEXT.set_map('dealNo', self.XfkTEXT.get('dealNo'))
        self.PostRequest(url='/api/mobile/deal/addOrUpdateDeal',
                         data={'xflbId': self.XfkTEXT.get('xflbId'),
                               'token': globals()['token'],
                               'squareBuilding': '25',
                               'signTime': self.XfkTEXT.get('signTime'),
                               'roomPriceTotal': dome,
                               'roomNoStr': '房号' + globals()['applyId'],
                               'remark': 'Python自动化签约',
                               'phoneType': 'ios',
                               'paymentMethod': '一次性付款',
                               'xflbName': '无',
                               'houseTypeName': self.XfkTEXT.get('houseTypeName'),
                               'houseTypeId': self.XfkTEXT.get('houseTypeId'),
                               'estateName': self.XfkTEXT.get('estateName'),
                               'dealPic': img + '#' + img,
                               'dealNo': self.XfkTEXT.get('dealNo'),
                               'customerName': self.XfkTEXT.get('customerName'),
                               'customerMobile': self.XfkTEXT.get('customerMobile'),
                               'commissionRatePrice': 0,
                               'commissionRate': 0,
                               'commissionPrice': self.XfkTEXT.get('commissionPrice'),
                               'channelType': '0',
                               # 'proportion': self.XfkTEXT.get('sellerYJRete'),
                               # 'addAmount': self.XfkTEXT.get('sellerYJAmount'),
                               # 'amount':
                               #     round(dome*self.XfkTEXT.get('sellerYJRete') +
                               #           self.XfkTEXT.get('sellerYJAmount') +
                               #           dome*self.XfkTEXT.get('sellerXJJRete') +
                               #           self.XfkTEXT.get('sellerXJJAmount'), 2),
                               'applyId': globals()['applyId']})

    def NewsList(self):
        """消息列表"""
        r = self.do_request.to_request(method="post",
                                       url=ApiNewsUrl,
                                       data={'alias': XfkUser,
                                             'pushSystem': 'xfk',
                                             'token': globals()['token'],
                                             'pageNum': 1,
                                             'rowsDisplayed': '20'})
        r.raise_for_status()
        globals()['r.text'] = json.loads(r.text)
        if ApiAgentUrl == 'http://api.ykb100.com':
            self.XfkTEXT.set_map('push_title', globals()['r.text']['Extend']['List'][0]['pushTitle'])
        else:
            self.XfkTEXT.set_map('push_title', globals()['r.text']['extend']['List'][0]['pushTitle'])

    def TimeoutClient(self):
        """获取超时列表"""
        self.GetRequest(url='/api/mobile/agentService/getMyOutApply/2.4.5.json',
                        data={'token': globals()['token'],
                              'pageNum': '1',
                              'rowsDisplayed': '20'})

    # 随机取值
    def RandomString(self, required):
        from random import choice
        self.XfkTEXT.set_map('Random', choice(required))


if __name__ == '__main__':
    a = XfkApi()


