# -*- coding: utf-8 -*-
# @Time    : 2020/9/5 10:22
# @Author  : 潘师傅
# @File    : xfp_web_api.py
# -*- coding: utf-8 -*-
from PubilcAPI.appApi import *
import random
import math

class webApi:

    def __init__(self):
        self.XfpRequest = appApi()
        self.app_api = self.XfpRequest
        self.appText = GlobalMap()
        self.webText = GlobalMap()

    def PostRequest(self, url, data, saasCode=XfpsaasCode, saasCodeSys=None, page=None):
        """post请求"""
        if saasCodeSys is None:
            saasCodeSys = saasCode

        if page is None:
            page = {}

        if saasCodeSys == 1:
            data1 = {
                     "saasCode": saasCode}
        elif saasCodeSys == 0:
            data1 = {"page": page,
                     "saasCode": saasCode,
                     "saasCodeSys": None}
        else:
            data1 = {"page": page,
                     "saasCode": saasCode,
                     "saasCodeSys": saasCodeSys}
        self.XfpRequest.Merge(data1, data)
        r = requests.post(url=(ApiXfpUrl + url),
                          data=(json.dumps(data,
                                           ensure_ascii=False).encode("UTF-8")),
                          headers={
                              'Content-Type': 'application/json',
                              'Authorization': 'Bearer' + ' ' + self.appText.get("user_token")
                          },
                          files=None)
        r.raise_for_status()
        self.webText.set_map('URL', ApiXfpUrl + url)
        globals()['xfp_web_Text'] = globals()['r.text'] = json.loads(r.text)
        self.webText.set_map('ApiXfpUrl', url)
        time.sleep(0.2)
        # if globals()['r.text']['code'] != 200:
        #     raise RuntimeError(self.webText.get('ApiXfpUrl'))

        if r.elapsed.total_seconds() > 5:
            print('接口请求过慢')
            print(self.webText.get('URL'))
        if r.elapsed.total_seconds() > 10:
            print('接口请求过慢大于10秒')
            print(self.webText.get('URL'))

    def Audit_management(self, suspend=False, suspendLevel=1, clueStop=False, clueStopLevel=1,
                         customerStop=False, customerStopLevel=1, customerVisit=False,
                         customerVisitLevel=1, customerDeal=False, customerDealLevel=1,
                         firstCallDaySwitch=True, firstCallDayWealth=10, notFirstCallDayWealth=5,
                         wealthDetailSwitch=False):
        """审核管理"""
        try:
            configValue = {
                    "clueCustomerConfig":
                        {
                            "sclxTimeOut": 1,
                            "nightLastClueTimeMinutes": 23,
                            "morningFirstClueTimeHours": 9,
                            "sclxSwitch": True,
                            "clueFollowTimeHours": 48,
                            "clueFollowOutTimeHours": 1,
                            "clueFollowSwitch": True,
                            "customerFollowTimeHours": 168,
                            "customerFollowOutTimeHours": 1,
                            "customerFollowSwitch": True,
                            "postponeFollowTimeDay": 90,
                            "postponeFollowOutTimeHours": 1,
                            "postponeFollowSwitch": True,
                            "visitOutTimeHours": 1,
                            "visitOutTimeSwitch": True
                        },
                    "auditConfig":
                        {
                            "suspendFollowSwitch": suspend,             # 暂缓跟进开关
                            "suspendFollowLevel": suspendLevel,         # 审核等级
                            "clueStopFollowSwitch": clueStop,           # 线索无效终止开关
                            "clueStopFollowLevel": clueStopLevel,
                            "customerStopFollowSwitch": customerStop,   # 客户终止开关
                            "customerStopFollowLevel": customerStopLevel,
                            "customerVisitSwitch": customerVisit,       # 客户带看计划
                            "customerVisitLevel": customerVisitLevel,
                            "customerDealSwitch": customerDeal,         # 客户成交审核
                            "customerDealLevel": customerDealLevel,
                            "wealthDetailSwitch": wealthDetailSwitch,   # 财务总监审核
                            "wealthDetailLevel": 0
                        },
                    "wealthDetailConfig": {
                            "addConsultantWealth": 30000,
                            "addConsultantWealthSwitch": True,
                            "consultantGetClueMaxWealth": -30000,
                            "consultantGetClueMaxWealthSwitch": True,
                            "platformAddClueWealth": 300,
                            "platformAddClueWealthSwitch": True,
                            "notPlatformAddClueWealth": 0,
                            "notPlatformAddClueWealthSwitch": False,
                            "firstCallSwitch": True,
                            "firstCallDaySwitch": firstCallDaySwitch,           # 首电开关
                            "firstCallDayWealth": firstCallDayWealth,           # 首电及时奖励
                            "notFirstCallDayWealth": notFirstCallDayWealth,     # 首电超时奖励
                            "firstCallMonthSwitch": True,
                            "firstCallMonthInvalid": 20,
                            "firstCallMonthPercentage": 98,
                            "notFirstCallMonthPercentage": 95,
                            "firstCallMonthWealth": 600,
                            "notFirstCallMonthWealth": 600,
                            "followSwitch": True,
                            "followDaySwitch": True,
                            "followDayWealth": 15,
                            "notFollowDayWealth": 10,
                            "followMonthSwitch": True,
                            "followMonthInvalid": 60,
                            "followMonthPercentage": 98,
                            "notFollowMonthPercentage": 95,
                            "followMonthWealth": 600,
                            "notFollowMonthWealth": 600,
                            "visitSwitch": True,
                            "visitSwitchWealth": 50,
                            "notVisitSwitchWealth": 20,
                            "dealSwitch": True,
                            "dealWealth": 5000,
                            "dealPercentageWealth": 10,
                            "dealWealthSwitch": True,
                            "dealPercentageWealthSwitch": False
                        },
                    "authCodeConfig": {             # 授权码相关
                        "authCodeSwitch": False,
                        "authCodeOutTime": 30,      # 授权码时效
                        "authCodeOutTimeLength": 6,     # 授权码长度
                        "authCodeLoginOutTime": 30
                }

                }
            self.PostRequest(url='/api/b/systeminfo/updateSysConfig',
                             data={
                                'saasCodeSys': XfpsaasCode,
                                'key': 'saas_sys_config',
                                'configValue': json.dumps(configValue)
                            }
                             )

        except BaseException as e:
            print("没有找到配置管理%s" % e)
    #
    # def audit_List(self, keyWord=None, auditStatue=0, auditLevel=1):
    #     """审核列表"""
    #     self.PostRequest(url='/api/b/audit/auditList',
    #                      data={
    #                         'keyWord': keyWord,
    #                         'auditLevel': auditLevel,       # 1是经理 2是总监
    #                         'auditStatue': auditStatue      # 状态 0是待审核 1 同意 2 是拒绝
    #                      })
    #     self.webText.set_map('total', globals()['r.text']['data']['total'])
    #     if globals()['r.text']['data']['total'] != 0:
    #         self.webText.set_map('applyReason', globals()['r.text']['data']['records'][0]['applyReason'])
    #         self.webText.set_map('auditId', globals()['r.text']['data']['records'][0]['auditId'])
    #         self.webText.set_map('auditType', globals()['r.text']['data']['records'][0]['auditType'])
    #         self.webText.set_map('auditLevel', globals()['r.text']['data']['records'][0]['auditLevel'])
    #         self.webText.set_map('parentAuditId', globals()['r.text']['data']['records'][0]['parentAuditId'])
    #         self.webText.set_map('clueId', globals()['r.text']['data']['records'][0]['clueId'])
    #         self.webText.set_map('customerId', globals()['r.text']['data']['records'][0]['customerId'])
    #
    # def auditApply(self, vlue=1, auditRemark=None, isAudit=True, customerId='', endTime=''):
    #     """审核"""
    #     if vlue == 2:
    #         parentAuditId = self.appText.get('parentAuditId')
    #     else:
    #         parentAuditId = ''
    #     self.PostRequest(url='/api/b/audit/auditApply',
    #                      data={
    #                          'clueId': self.appText.get('clueId'),
    #                          'auditId': self.webText.get('auditId'),
    #                          'customerId': customerId,
    #                          'applyReason': self.webText.get('applyReason'),
    #                          'consultantId': self.appText.get('consultantId'),
    #                          'auditLevel': self.webText.get('auditLevel'),
    #                          'auditType': self.webText.get('auditType'),
    #                          'isAudit': isAudit,
    #                          'parentAuditId': parentAuditId,
    #                          'endTime': endTime,
    #                          'auditRemark': auditRemark,
    #                      })

    def add_label(self, labelName, labelId, pid, saasCode=XfpsaasCode):
        """新增标签"""
        self.PostRequest(url='/api/b/systembase/saveLabel',
                         data={
                             'labelId': labelId,
                             'pid': pid,                # 添加大标签 这个填0
                             'labelName': labelName
                         },
                         saasCode=saasCode)

    def get_all_label(self, labelNo='', labelName=None):
        """查询所有的标签"""
        self.PostRequest(url='/api/b/systembase/label/list',
                         data={
                             'labelNo': labelNo
                         })
        vlue = 0
        if labelNo is not None:
            vlue = 0
            while labelNo != globals()['r.text']['data'][vlue]['labelNo']:
                vlue = vlue + 1
            if labelName is not None:
                dome = 0
                try:
                    dome1 = globals()['r.text']['data'][vlue]['children'][dome]['labelName']
                except:
                    self.add_label()
                    while labelName != globals()['r.text']['data'][vlue]['children'][dome]['labelName']:
                        dome = dome + 1
        self.webText.set_map('labelId', globals()['r.text']['data'][vlue]['labelId'])

    def house_list(self, keyWord='', vlue=0):
        """楼盘列表"""
        self.PostRequest(url='/api/b/house/list',
                         data={
                             'keyWord': keyWord
                         })
        self.webText.set_map('total', globals()['r.text']['data']['total'])
        if globals()['r.text']['data']['total'] != 0:
            self.webText.set_map('houseId', globals()['r.text']['data']['records'][vlue]['houseId'])

    def add_house_data(self, data, isHaveAttachment=False, attachmentIds=''):
        """添加楼盘信息"""
        self.PostRequest(url='/api/b/house/addOrUpdateHouseInfo',
                         data={
                                "attachmentIds": attachmentIds,     # 附件ID
                                "houseId": self.webText.get('houseId'),     # 楼盘ID
                                "houseInfo": data,
                                "houseInfoType": self.appText.get('XXFL'),   # 标签ID
                                "isDelete": 0,
                                "isHaveAttachment": isHaveAttachment,
                            })

    def add_house(self, houseName):
        """添加新房"""
        self.generate_random_gps(base_log=120.7, base_lat=30, radius=1000000)
        self.PostRequest(url='/api/b/house/save',
                         data={
                                "areaId": self.appText.get('PPQY'),
                                "cityId": self.appText.get('city'),
                                "houseName": houseName,
                                'localeCoordinates': self.webText.get('localeCoordinates'),
                                'localeName': '经纬度转地址'+ time.strftime("%Y-%m-%d %H:%M:%S")
                            })

    def add_house_business_information(self,
                                       reportingRules='这个是报备规则',
                                       residentInfo='0313+11111111111',
                                       reward='这个是佣金+现金奖',
                                       settlementConditions='这个是结算条件'):
        """添加楼盘商务信息"""
        self.PostRequest(url='/api/b/house/addOrUpdateHouseBusiness',
                         data={
                                "agencyId": self.appText.get('DLGS'),
                                # "endTime": "",
                                "houseId": self.webText.get('houseId'),
                                # "infoId": None,
                                # "isDelete": "",
                                # "keyWord": "",
                                "reportingRules": reportingRules,
                                "residentInfo": residentInfo,
                                "reward": reward,
                                # "saasCode": "000029",
                                "settlementConditions": settlementConditions,
                                # "startTime": ""
                            })

    def getHouseBusinessList(self):
        """商务详情"""
        self.PostRequest(url='/api/b/house/getHouseBusinessList',
                         data={
                             'houseId': self.appText.get('houseId')
                         })
        dome = 0
        dome1 = 1
        while globals()['r.text']['data']['records'][0]['residentInfo'][dome:dome1] != '+':
            dome = dome1
            dome1 = dome1 + 1
        self.appText.set_map('BBGZ', globals()['r.text']['data']['records'][0]['reportingRules'])
        self.appText.set_map('JDRXM', globals()['r.text']['data']['records'][0]['residentInfo'][0:dome])
        self.appText.set_map('JDRDH', globals()['r.text']['data']['records'][0]['residentInfo'][dome1:])
        self.appText.set_map('YJXJJ', globals()['r.text']['data']['records'][0]['reward'])
        self.appText.set_map('JSTJ', globals()['r.text']['data']['records'][0]['settlementConditions'])

    def add_house_questions(self, answer='这个是答案', title='这个是问题'):
        """添加楼盘问答"""
        self.PostRequest(url='/api/b/house/addOrUpdateHouseQuestion',
                         data={
                             'houseIds': self.webText.get('houseId'),
                             # 'consultantId': self.appText.get('consultantId'),
                             'questionTypeNo': self.appText.get('labelNo'),
                             'title': title,
                             'attachmentIds': '',
                             'answer': answer
                         })

    def wealth_management(self):
        """财富值设置"""
        configValue = {
            "clueCustomerConfig": {
                "sclxTimeOut": 30,
                "nightLastClueTimeMinutes": 21,
                "morningFirstClueTimeHours": 9,
                "sclxSwitch": True,
                "clueFollowTimeHours": 48,
                "clueFollowOutTimeHours": 6,
                "clueFollowSwitch": True,
                "customerFollowTimeHours": 168,
                "customerFollowOutTimeHours": 6,
                "customerFollowSwitch": True,
                "postponeFollowTimeDay": 90,
                "postponeFollowOutTimeHours": 6,
                "postponeFollowSwitch": True,
                "visitOutTimeHours": 24,
                "visitOutTimeSwitch": True
            },
            "auditConfig": {
                "suspendFollowSwitch": False,
                "suspendFollowLevel": 1,
                "clueStopFollowSwitch": False,
                "clueStopFollowLevel": 1,
                "customerStopFollowSwitch": False,
                "customerStopFollowLevel": 1,
                "customerVisitSwitch": True,
                "customerVisitLevel": 1,
                "customerDealSwitch": False,
                "customerDealLevel": 1
            },
            "wealthDetailConfig": {
                "addConsultantWealth": 30000,
                "addConsultantWealthSwitch": True,  # 新增咨询师财富值
                "consultantGetClueMaxWealth": -30000,
                "consultantGetClueMaxWealthSwitch": True,  # 咨询师低于多少无法获取线索
                "platformAddClueWealth": 300,
                "platformAddClueWealthSwitch": True,  # 平台线索上户 消耗值
                "notPlatformAddClueWealth": 0,
                "notPlatformAddClueWealthSwitch": False,
                "firstCallSwitch": True,
                "firstCallDaySwitch": True,
                "firstCallDayWealth": 5,  # 及时首电
                "notFirstCallDayWealth": 5,  # 超市首电
                "firstCallMonthSwitch": True,
                "firstCallMonthInvalid": 20,  # 小于无效
                "firstCallMonthPercentage": 98,  # 超过百分比
                "notFirstCallMonthPercentage": 95,  # 低于百分比
                "firstCallMonthWealth": 600,  #
                "notFirstCallMonthWealth": 600,
                "followSwitch": True,
                "followDaySwitch": True,
                "followDayWealth": 5,  # 跟进及时
                "notFollowDayWealth": 5,  # 跟进超市
                "followMonthSwitch": True,
                "followMonthInvalid": 60,
                "followMonthPercentage": 98,
                "notFollowMonthPercentage": 95,
                "followMonthWealth": 600,
                "notFollowMonthWealth": 600,
                "visitSwitch": True,
                "visitSwitchWealth": 50,  # 完成带看
                "notVisitSwitchWealth": 50,  # 超时带看
                "dealSwitch": True,
                "dealWealth": 5000,  # 成交
                "dealPercentageWealth": 10,
                "dealWealthSwitch": True,
                "dealPercentageWealthSwitch": False,
                "radioValue": 1
            }
        }
        self.PostRequest(url='/api/b/systeminfo/updateSysConfig',
                         data={
                             'key': 'saas_sys_config',
                             'saasCodeSys': XfpsaasCode,
                             'saasCode': XfpsaasCode,
                             'configValue': json.dumps(configValue)
                         })

    def CluePhoneLog(self):
        """线索通话记录"""
        self.PostRequest(url='/api/b/clue/phoneLog/list',
                         data={'clueId': self.appText.get('clueId')})
        self.webText.set_map('total', len(globals()['r.text']['data']['records']))
        if self.webText.get('total') != 0:
            self.webText.set_map('isFlagCallStr', globals()['r.text']['data']['records'][0]['isFlagCallStr'])   # 是否主叫
            self.webText.set_map('consultantName', globals()['r.text']['data']['records'][0]['consultantName'])

    def TodayClue(self):
        """待首电"""
        self.PostRequest(url='/api/b/consultant/getStatisticalConsultantTaskList',
                         data={
                             'consultantId': self.appText.get('consultantId'),
                             'DateTime': time.strftime("%Y-%m-%d"),
                             'isFirst': 0
                         })
        self.webText.set_map('total', len(globals()['r.text']['data']))
        if self.webText.get('total') != 0:
            self.webText.set_map('r.text', globals()['r.text'])

    def clue_list(self, myClue='Y', rderNo=None, vlue=0, consultantId=None, sourceId=None,
                  followStatus=None):
        """线索列表"""
        self.PostRequest(url='/api/b/clue/list',
                         data={
                             'myClue': myClue,
                             'isWork': True,
                             'orderNo': rderNo,
                             'consultantId': consultantId,
                             'followStatus': followStatus,   # 3 无效释放 2 有效转化 1 跟进中 0 未指派
                             'sourceId': sourceId,
                             'startTime': self.appText.get('start_date'),
                             'endTime': self.appText.get('end_date'),
                         })
        if globals()['r.text']['data']['total'] != 0:
            vlue = vlue + 1
            self.appText.set_map('clueId',
                                 globals()['r.text']['data']['records'][len(globals()['r.text']['data']['records']) - vlue]['clueId'])
            self.appText.set_map('cluePhone',
                                 globals()['r.text']['data']['records'][len(globals()['r.text']['data']['records']) - vlue]['cluePhone'])
            self.appText.set_map('orderNo',
                                 globals()['r.text']['data']['records'][
                                     len(globals()['r.text']['data']['records']) - vlue]['orderNo'])
        else:
            pass
        self.webText.set_map('total', globals()['r.text']['data']['total'])

    def consultant_list(self, vlue=0):
        """咨询师列表"""
        self.PostRequest(url='/api/b/consultant/list',
                         data={
                             'deviceNo': ''
                         })
        self.webText.set_map('total', len(globals()['r.text']['data']['records']))
        if len(globals()['r.text']['data']['records']) != 0:
            self.webText.set_map('consultantId', globals()['r.text']['data']['records'][vlue]['consultantId'])

    def add_clue_admin(self, clueNickName, cluePhone=None):
        """总部添加线索"""
        if cluePhone is None:
            cluePhone = '1' + str(int(time.time()))

        data = {
                "clueAddtype": 2,
                "clueIdList": [

                ],
                "clueNickName": clueNickName,
                "cluePhone": cluePhone,
                "remark": "总站添加线索",
                "saasCodeSys": XfpsaasCode,
                "sourceId": self.appText.get('XSLY_admin'),
                'saasCode': 'admin'
                            }
        r = requests.post(url=(ApiXfpUrl + '/api/b/clue/distribution'),
                          data=(json.dumps(data,
                                           ensure_ascii=False).encode("UTF-8")),
                          headers={
                              'Content-Type': 'application/json',
                              'Authorization': 'Bearer' + ' ' + self.appText.get("user_token")
                          },
                          files=None)
        r.raise_for_status()
        globals()['r.text'] = json.loads(r.text)
        self.webText.set_map('code', globals()['r.text']['code'])
        self.webText.set_map('cluePhone', cluePhone)

    def addGoldDetailInfo(self):
        """幸福币充值"""
        data = {
            "saasCodeSys": XfpsaasCode,
            "goldValue": "50000",
            "goldType": 1,
            "type": "add",
            # "saasName":"小鸡炖蘑菇",
            "saasCode": "admin"
        }
        r = requests.post(url=(ApiXfpUrl + '/api/b/goldDetail/addGoldDetailInfo'),
                          data=(json.dumps(data,
                                           ensure_ascii=False).encode("UTF-8")),
                          headers={
                              'Content-Type': 'application/json',
                              'Authorization': 'Bearer' + ' ' + self.appText.get("user_token")
                          },
                          files=None)
        r.raise_for_status()

    def generate_random_gps(self, base_log=None, base_lat=None, radius=None):
        """随机经纬度"""
        radius_in_degrees = radius / 111300
        u = float(random.uniform(0.0, 1.0))
        v = float(random.uniform(0.0, 1.0))
        w = radius_in_degrees * math.sqrt(u)
        t = 2 * math.pi * v
        x = w * math.cos(t)
        y = w * math.sin(t)
        longitude = y + base_log
        latitude = x + base_lat
        # 这里是想保留6位小数点
        loga = '%.6f' % longitude
        lata = '%.6f' % latitude
        self.webText.set_map('localeCoordinates', loga + ',' + lata)
        return loga, lata

    def consultant_allocition(self, isAppoint=1):
        """咨询师是否分配线索"""
        self.PostRequest(url='/api/b/consultant/save',
                         data={
                             'consultantId': self.appText.get('consultantId'),
                             'isAppoint': isAppoint
                         })

    def clue_await_allocition(self, keyWord=None):
        """线索待分配"""
        self.PostRequest(url='/api/b/clue/subWaitAllocatedClueList',
                         data={
                             'keyWord': keyWord

                         })
        self.webText.set_map('total', globals()['r.text']['data']['total'])
        if self.webText.get('total') != 0:
            self.webText.set_map('createdTime', globals()['r.text']['data']['records'][0]['createdTime'])
            self.webText.set_map('receptionTime', globals()['r.text']['data']['records'][0]['receptionTime'])
            self.webText.set_map('clueId', globals()['r.text']['data']['records'][0]['clueId'])

    def clue_appoint(self):
        """线索指派"""
        self.PostRequest(url='/api/b/clue/appoint',
                         data={
                                "title": "线索指派",
                                "show": "zhipai",
                                "clueId": self.webText.get('clueId'),
                                "isWork": True,
                                # "sourceId": null,
                                # "remark": null,
                                "clueIdList": [
                                    self.webText.get('clueId')
                                ],
                                "consultantId": self.appText.get('consultantId'),
                                "page": {

                                },
                                "saasCode": XfpsaasCode
                            })

    def get_group(self):
        """获取团队ID"""
        self.PostRequest(url='/api/b/systeminfo/part/departments',
                         data={
                         })
        if len(globals()['r.text']['data']) != 0:
            self.webText.set_map('departmentId', globals()['r.text']['data'][0]['departmentId'])

    def deal_list(self, transType=None, transApplyStatus=1, transTime=None):
        """成交列表"""
        if transTime == '认购':
            startTime = 'startTransBuyDate'
            endTime = 'endTransBuyDate'
        elif transTime == '网签':
            startTime = 'startTransContractDate'
            endTime = 'endTransContractDate'
        else:
            startTime = 'startCreatedTime'
            endTime = 'endCreatedTime'
        self.PostRequest(url='/api/b/trans/list',
                         data={
                             'belongConsultantId': self.appText.get('consultantId'),
                             "app": False,
                             f"{endTime}": self.appText.get('end_date') + ' 23:59:59',
                             f"{startTime}": self.appText.get('start_date') + ' 00:00:00',
                             'transProgressStatus': transType,  # 成交项    1 认购 2 网签
                             'transApplyStatus': transApplyStatus,  # 审核状态  1 审核通过
                             # "app": False,
                             # "belongConsultantId": self.appText.get('consultantId'),
                             # "transApplyStatus": "1",
                             # "startTransBuyDate": "2021-01-01 00:00:00",
                             # "endTransBuyDate": "2021-01-31 23:59:59"
                         })
        self.webText.set_map('web_total', globals()['r.text']['data']['total'])
        if self.webText.get('web_total') != 0:
            self.appText.set_map('clueId', globals()['r.text']['data']['records'][0]['clueId'])
            self.appText.set_map('transId', globals()['r.text']['data']['records'][0]['transId'])
            self.appText.set_map('customerId', globals()['r.text']['data']['records'][0]['customerId'])
            self.appText.set_map('CJDH', globals()['r.text']['data']['records'][0]['transOrderNo'])

    def visit_list(self):
        """带看列表"""
        self.PostRequest(url='/api/b/visit/list',
                         data={
                             'belongConsultantId': self.appText.get('consultantId'),
                             'endTime': self.appText.get('end_date') + ' 23:59:59',
                             'startTime': self.appText.get('start_date') + ' 00:00:00',
                             'visitStatus': 3
                         })
        self.appText.set_map('web_total', globals()['r.text']['data']['total'])

    def visit_deal_statistics(self):
        """带看成交统计"""
        self.PostRequest(url='/api/b/report/getVisitAndTransactionReport',
                         data={
                             'departmentId': self.webText.get('departmentId'),
                             'startTime': self.appText.get('start_date'),
                             'endTime': self.appText.get('end_date'),
                         })
        if len(globals()['r.text']['data']) != 0:
            vlue = 0
            while globals()['r.text']['data'][vlue]['consultantName'] != '咨询师01':
                vlue = vlue + 1
                if len(globals()['r.text']['data']) == vlue:
                    break
            dome = json.loads(json.dumps(globals()['r.text']['data'][vlue]))
            self.webText.set_map('web_newClueCount', dome['newClueCount'])     # 上户批数
            self.webText.set_map('web_resultsWealth', dome['resultsWealth'])   # 发放财富值

            """带看成交率   业绩  带看次数    邀约带看率"""
            self.webText.set_map('web_transactionRatio', dome['transactionRatio'])
            self.webText.set_map('web_transactionResults', dome['transactionResults'])
            self.webText.set_map('web_visitCount', dome['visitCount'])
            self.webText.set_map('web_visitOnTimeCount', dome['visitOnTimeCount'])
            self.webText.set_map('web_visitRatio', dome['visitRatio'])
            """认购套数     网签套数        业绩"""
            self.webText.set_map('web_transactionCount', dome['transactionCount'])
            self.webText.set_map('web_subscribeConvertSigning', dome['subscribeConvertSigning'])
            self.webText.set_map('web_transactionResults', dome['transactionResults'])

    def work_statistics(self):
        """咨询师工作统计"""
        self.PostRequest(url='/api/b/consultant/getConsultantWorkReport',
                         data={
                             'departmentId': self.webText.get('departmentId'),
                             'startTime': self.appText.get('start_date'),
                             'endTime': self.appText.get('end_date'),
                         })
        if len(globals()['r.text']['data']) != 0:
            vlue = 0
            while globals()['r.text']['data'][vlue]['consultantName'] != '咨询师01':
                vlue = vlue + 1
                if len(globals()['r.text']['data']) == vlue:
                    break
            dome = json.loads(json.dumps(globals()['r.text']['data'][vlue]))
            self.webText.set_map('web_newClueCount', dome['newClueCount'])     # 上户批数
            self.webText.set_map('web_firstCallCount', dome['firstCallCount'])     # 及时首电
            self.webText.set_map('web_firstCallOutCount', dome['firstCallOutCount'])     # 首电超时
            self.webText.set_map('web_firstCallRatio', dome['firstCallRatio'])     # 首电及时率
            self.webText.set_map('web_followCount', dome['followCount'])     # 跟进次数
            self.webText.set_map('web_followInTimeCount', dome['followInTimeCount'])     # 及时跟进次数
            self.webText.set_map('web_followOutTimeCount', dome['followOutTimeCount'])     # 超时跟进次数
            self.webText.set_map('web_followRatio', dome['followRatio'])     # 跟进及时率
            self.webText.set_map('web_callCount', dome['callCount'])     # 通话次数
            self.webText.set_map('web_seaClaimClueCount', dome['seaClaimClueCount'])     # 公海领取
            self.webText.set_map('web_seaClueCount', dome['seaClueCount'])     # 释放公海批次

    def statistics_wealth(self):
        """财富值统计"""
        self.PostRequest(url='/api/b/wealth/getWealthDetailReportList',
                         data={
                             'departmentId': self.webText.get('departmentId'),
                             'startTime': self.appText.get('start_date'),
                             'endTime': self.appText.get('end_date'),
                         })
        if len(globals()['r.text']['data']) != 0:
            vlue = 0
            while globals()['r.text']['data'][vlue]['consultantName'] != '咨询师01':
                vlue = vlue + 1
                if len(globals()['r.text']['data']) == vlue:
                    break
            dome = json.loads(json.dumps(globals()['r.text']['data'][vlue]))
            self.webText.set_map('web_clueCount', dome['clueCount'])     # 兑换线索数
            self.webText.set_map('web_wealthClueSum', dome['wealthClueSum'])     # 兑换线索消耗财富总数
            self.webText.set_map('web_wealthConsume', dome['wealthConsume'])     # 消耗财富值总数
            self.webText.set_map('web_wealthObtainSum', dome['wealthObtainSum'])     # 新增财富值总数
            self.webText.set_map('web_wealthPerformanceSum', dome['wealthPerformanceSum'])     # 财富业绩
            self.webText.set_map('web_wealthSum', dome['wealthSum'])     # 合计增减
            self.webText.set_map('web_wealthSysDeduct', dome['wealthSysDeduct'])     # 系统扣除
            self.webText.set_map('web_wealthSysSum', dome['wealthSysSum'])     # 系统奖励
            self.webText.set_map('web_clueApplyCount', dome['clueApplyCount'])     # 系统奖励

    def getWealthApplyList(self, keyWord=None):
        """财富值申诉列表"""
        self.PostRequest(url='/api/b/wealthApply/getWealthApplyList',
                         data={
                            'keyWord': keyWord
                         })
        self.appText.set_map('applyId', globals()['r.text']['data']['records'][0]['applyId'])

    def wealthApply(self):
        """申诉审核"""
        self.PostRequest(url='/api/b/wealthApply/apply',
                         data={
                             "type": "yes",
                             'applyId': self.appText.get('applyId'),
                             'applyIds': [self.appText.get('applyId')],
                             'wealthId': self.appText.get('wealthId'),
                             'auditRemark': None,
                             'auditStatus': 1,
                             'applyStatus': 2,

                         })

    def phoneLogList(self):
        """通话记录"""
        self.PostRequest(url='/api/b/customer/getPhoneLogList',
                         data={
                             'consultantId': self.appText.get('consultantId'),
                             'startTime': self.appText.get('start_date'),
                             'endTime': self.appText.get('end_date'),
                         })
        self.appText.set_map('web_total', globals()['r.text']['data']['total'])

    def clue_detail(self):
        """留点记录"""
        self.PostRequest(url='/api/b/clue/detail',
                         data={
                             'clueId': self.appText.get('clueId')
                         })
        if len(globals()['r.text']['data']['clueFollowList']) != 0:
            self.appText.set_map('remark', globals()['r.text']['data']['remark'])

    def auditList(self, auditLevel=1, phoneNum=None):
        """成交审核列表"""
        self.PostRequest(url='/api/b/auditApply/auditList',
                         data={
                             'auditLevel': auditLevel,
                             'auditStatue': 0,
                             'phoneNum': phoneNum,
                         })
        if len(globals()['r.text']['data']['records']) != 0:
            self.appText.set_map('auditId', globals()['r.text']['data']['records'][0]['auditId'])
        self.appText.set_map('web_total', globals()['r.text']['data']['total'])

    def audit(self, auditStatue=1, auditRemark=None):
        """成交审核"""
        if auditStatue == 1:
            auditRemark = None
        self.PostRequest(url='/api/b/auditApply/audit',
                         data={
                             'auditId': self.appText.get('auditId'),
                             'auditRemark': auditRemark,
                             'auditStatue': auditStatue,
                         })

    def finance_deal_auditList(self, keyWord=None, dealStatus=1):
        """成交-财务审核列表"""
        self.PostRequest(url='/api/b/trans/deal/auditList',
                         data={
                             'keyWord': keyWord,
                             'dealStatus': dealStatus

                         })
        if len(globals()['r.text']['data']['records']) != 0:
            self.appText.set_map('dealId', globals()['r.text']['data']['records'][0]['dealId'])
        self.appText.set_map('web_total', globals()['r.text']['data']['total'])

    def finance_deal_audit(self, auditStatue=1, dealAmount=None, remark=None):
        """财务审核"""
        if dealAmount is None:
            dealAmount = self.appText.get('transYeji')
        if auditStatue == 1:
            remark = None
        elif auditStatue==2:
            dealAmount = ''
        self.PostRequest(url='/api/b/trans/deal/audit',
                         data={
                             'auditStatue': auditStatue,
                             'dealAmount': dealAmount,
                             'dealId': self.appText.get('dealId'),
                             'remark': remark
                         })

    def detail(self):
        """成交详情"""
        self.PostRequest(url='/api/b/trans/detail/' + str(self.appText.get('transId')),
                         data={

                         })
        self.appText.set_map('transYeji', globals()['r.text']['data']['transYeji'])
        self.appText.set_map('visitDealId', globals()['r.text']['data']['transVisitDeal']['visitDealId'])
        self.appText.set_map('dealPhone', globals()['r.text']['data']['transReservedTellphone'])

        self.appText.set_map('BBGZ', globals()['r.text']['data']['transVisitDeal']['reportingRules'])
        self.appText.set_map('JDRXM', globals()['r.text']['data']['transVisitDeal']['receptionName'])
        self.appText.set_map('JDRDH', globals()['r.text']['data']['transVisitDeal']['receptionPhone'])
        self.appText.set_map('YJXJJ', globals()['r.text']['data']['transVisitDeal']['reward'])
        self.appText.set_map('JSTJ', globals()['r.text']['data']['transVisitDeal']['settlementConditions'])
        self.appText.set_map('visitProjectId',
                             globals()['r.text']['data']['transVisitDeal']['visitProjectId'])

    def goldApply_addGoldApply(self):
        """线索索赔申请"""
        self.PostRequest(url='/api/b/goldApply/addGoldApply',
                         data={
                             'orderNo': self.appText.get('orderNo'),
                             'clueId': self.appText.get('clueId'),
                             # 'sourceId': self.appText.get('XSLY_admin'),
                             'applyId': None,
                             'applyLabelId': self.appText.get('DHWK'),
                             'applyStatus': None,
                             'auditRemark': '1'

                         })
        self.appText.set_map('data', globals()['r.text']['data'])

    def getGoldApplyList(self):
        """待处理索赔"""
        self.PostRequest(url='/api/b/goldApply/getGoldApplyList',
                         data={
                             'keyWord': self.appText.get('cluePhone')
                         })
        if len(globals()['r.text']['data']['records']) != 0:
            self.appText.set_map('applyId', globals()['r.text']['data']['records'][0]['applyId'])

    def auditGoldApply(self, applyStatus=True, remark=''):
        """审核索赔"""
        if applyStatus == True:
            remark =''
        self.PostRequest(url='/api/b/goldApply/auditGoldApply',
                         data={
                             'applyId': self.appText.get('applyId'),
                             'applyIds': [self.appText.get('applyId')],
                             'applyStatus': applyStatus,
                             'remark': remark
                         })

    def DeptUserListPage(self, deviceNo=None, deviceName=None):
        """设备列表"""
        self.PostRequest(url='/api/b/device/getDeptUserListPage',
                         data={
                             'deviceNo': deviceNo,
                             'deviceName': deviceName
                         })
        self.appText.set_map('web_total', globals()['r.text']['data']['total'])
        if self.appText.get('web_total') != 0:
            self.appText.set_map('deviceNo', globals()['r.text']['data']['records'][0]['deviceNo'])
            self.appText.set_map('deviceName', globals()['r.text']['data']['records'][0]['deviceName'])
            self.appText.set_map('deviceRemark', globals()['r.text']['data']['records'][0]['deviceRemark'])
            if len(globals()['r.text']['data']['records'][0]['deviceBindingList']) != 0:
                userId = []
                a = 0
                while a != len(globals()['r.text']['data']['records'][0]['deviceBindingList']):
                    userId = userId + \
                             [globals()['r.text']['data']['records'][0]['deviceBindingList'][a]['userId']]
                    a = a + 1
                self.appText.set_map('userId', userId)
            else:
                self.appText.set_map('userId', None)

    def addDeviceInfo(self,
                      isUpdate=False,
                      deviceName='设备名称',
                      deviceNo='设备编号',
                      deviceRemark=None):
        """添加设备"""
        self.PostRequest(url='/api/b/device/addOrUpdateDeviceInfo',
                         data={
                             'disabled': isUpdate,
                             'deviceName': deviceName,
                             'deviceNo': deviceNo,
                             'deviceRemark': deviceRemark,
                             'deviceType': 1,
                             'isUpdate': isUpdate,
                             'type': 1
                         })
        self.appText.set_map('data', globals()['r.text']['data'])

    def DelDeviceInfo(self):
        """删除设备"""
        self.PostRequest(url='/api/b/device/delDeviceInfo',
                         data={
                            "type": 1,
                            "userIds": self.appText.get('userId'),
                            "userIdsStr": self.appText.get('userId'),
                            "deviceNo": self.appText.get('deviceNo'),
                            "deviceType": "1",
                            "deviceName": self.appText.get('deviceName'),
                            "deviceRemark": self.appText.get('deviceRemark'),
                         })

    def DeviceBinding(self, userId=None):
        """设备绑定"""
        if userId is None:
            userId = [self.appText.get('userId')]
        self.PostRequest(url='/api/b/device/addDeviceBinding',
                         data={
                                "type": 2,
                                "userIds": userId,
                                "userIdsStr": userId,
                                "deviceNo": self.appText.get('deviceNo'),
                                "deviceType": "1",
                                "deviceName": self.appText.get('deviceName'),
                                "deviceRemark": self.appText.get('deviceRemark'),

                            })

    def UserIdList(self, keyWord=None):
        """用户列表"""
        self.PostRequest(url='/api/b/consultant/list',
                         data={
                              'keyWord': keyWord
                         })
        if len(globals()['r.text']['data']['records']) != 0:
            self.appText.set_map('userId', globals()['r.text']['data']['records'][0]['userId'])

    def configList(self, keyWord=None):
        """配置列表"""
        self.PostRequest(url='/api/b/config/list',
                         data={
                             "configKey": None,
                             "configKeyName": None,
                             "configValue": None,
                             "keyWord": keyWord,
                         })
        if len(globals()['r.text']['data']['records']) == 1:
            self.appText.set_map('configKey', globals()['r.text']['data']['records'][0]['configKey'])
            self.appText.set_map('configKeyName', globals()['r.text']['data']['records'][0]['configKeyName'])
            self.appText.set_map('configid', globals()['r.text']['data']['records'][0]['id'])

    def configSave(self, configValue=0):
        """配置管理"""
        self.PostRequest(url='/api/b/config/save',
                         data={
                             "configKey": self.appText.get('configKey'),
                             "configKeyName": self.appText.get('configKeyName'),
                             "configValue": configValue,
                             "id": self.appText.get('configid'),
                             "isDeleted": 0,
                         })

    def ConsultantAuthList(self):
        """待实名认证-列表"""
        self.PostRequest(url='/api/b/consultantAuth/getConsultantAuthList',
                         data={

                         },
                         saasCode='admin')

    def GoldDetailCountList(self, endTime=None, startTime=None):
        """储值单位统计"""
        self.PostRequest(url='/api/b/goldDetail/getGoldDetailCountList',
                         data={
                             'endTime': endTime,
                             'startTime': startTime,
                         }, saasCode='admin', saasCodeSys=XfpsaasCode,
                         page={
                            'size': '100',
                            'current': '1'
                        })

        if len(globals()['r.text']['data']['records']) != 0:
            dome = 0
            while str(globals()['r.text']['data']['records'][dome]['saasCode']) != XfpsaasCode:
                dome = dome + 1
                if dome == len(globals()['r.text']['data']['records']):
                    break
            if globals()['r.text']['data']['records'][dome]['saasCode'] == XfpsaasCode:
                self.appText.set_map('goldClueCount',
                                     globals()['r.text']['data']['records'][dome]['goldClueCount'])

    def clue_adminList(self, endTime=None, startTime=None, isInvalid=None, saasCodeSys=XfpsaasCode,
                       keyWord=None):
        """总部-线索列表"""
        self.PostRequest(url='/api/b/clue/adminList',
                         data={
                             'endTime': endTime,
                             'isDistribution': None,
                             'keyWord': keyWord,
                             'startTime': startTime,
                             'isInvalid': isInvalid       # 1 有效 2 无效
                         }, saasCode='admin', saasCodeSys=saasCodeSys)
        self.appText.set_map('web_total', globals()['r.text']['data']['total'])

    def admin_report_clue(self):
        """线索消耗及消耗统计"""
        self.PostRequest(url='/api/b/report/clue',
                         data={
                             "statisticsDate": self.appText.get('start_date'),
                             'typeCode': 'admin'
                         },
                         saasCode='admin')
        """新增"""
        self.appText.set_map('monthNewNum',
                             globals()['r.text']['data']['clueReportVos']
                             [len(globals()['r.text']['data']['clueReportVos']) - 1]['monthNewNum'])
        """有效"""
        self.appText.set_map('monthValidNum',
                             globals()['r.text']['data']['clueReportVos']
                             [len(globals()['r.text']['data']['clueReportVos']) - 1]['monthValidNum'])

    def ConsultantCountList(self):
        """工作台-关键指标--队长"""
        self.PostRequest(url='/api/b/consultant/getConsultantCountList',
                         data={
                             'departmentId': self.appText.get('departmentId'),
                             'startTime': self.appText.get('start_date'),
                             'endTime': self.appText.get('end_date')
                         })
        if len(globals()['r.text']['data']) != 0:
            vlue = 0
            while globals()['r.text']['data'][vlue]['consultantName'] != '咨询师01':
                vlue = vlue + 1
                if len(globals()['r.text']['data']) == vlue:
                    break
            dome = json.loads(json.dumps(globals()['r.text']['data'][vlue]))
            self.appText.set_map('web_newClueCount', dome['newClueCount'])       # 上户批数
            self.appText.set_map('web_seaClueCounth', dome['seaClueCount'])      # 释放公海批数
            self.appText.set_map('web_firstCallRatio', dome['firstCallRatio'])   # 首电及时率
            self.appText.set_map('web_followRatio', dome['followRatio'])         # 跟进及时率
            self.appText.set_map('web_visitCount', dome['visitCount'])           # 带看总数
            self.appText.set_map('web_visitRatio', dome['visitRatio'])           # 上户邀约率
            self.appText.set_map('web_dealCount', dome['dealCount'])             # 成交总数
            self.appText.set_map('web_dealRatio', dome['dealRatio'])             # 带看成交率
            self.appText.set_map('web_transactionSum', dome['transactionSum'])   # 成交业绩

    def TransactionSettlementStatistical(self):
        """结算列表---底部统计"""
        self.PostRequest(url='/api/b/transactionSettlement/getTransactionSettlementStatistical',
                         data={
                             'startTime': self.appText.get('start_date'),
                             'endTime': self.appText.get('end_date')
                         })
        self.appText.set_map('amountToBeCollected', globals()['r.text']['data']['amountToBeCollected'])  # 待回款金额
        self.appText.set_map('debtCollectionSchedule', globals()['r.text']['data']['debtCollectionSchedule'])  # 回款进度
        self.appText.set_map('hkCount', globals()['r.text']['data']['hkCount'])     # 回款套数
        self.appText.set_map('paidCommission', globals()['r.text']['data']['paidCommission'])
        self.appText.set_map('paidWealth', globals()['r.text']['data']['paidWealth'])
        self.appText.set_map('printedInvoiceAmount', globals()['r.text']['data']['printedInvoiceAmount'])
        self.appText.set_map('receivableAmount', globals()['r.text']['data']['receivableAmount'])   # 回款金额
        self.appText.set_map('rgCount', globals()['r.text']['data']['rgCount'])     # 认购套数
        self.appText.set_map('verificationResults',
                             globals()['r.text']['data']['verificationResults'])  # 核定业绩
        self.appText.set_map('wcCount', globals()['r.text']['data']['wcCount'])     #
        self.appText.set_map('wqCount', globals()['r.text']['data']['wqCount'])     # 网签套数

    def TransactionSettlementList(self):
        """结算列表-"""
        self.PostRequest(url='/api/b/transactionSettlement/getTransactionSettlementList',
                         data={
                             'startTime': self.appText.get('start_date'),
                             'endTime': self.appText.get('end_date')
                         })
        if len(globals()['r.text']['data']['records']) != 0:
            self.appText.set_map('transOrderNo', globals()['r.text']['data']['records'][0]['transOrderNo'])
            self.appText.set_map('transId', globals()['r.text']['data']['records'][0]['transId'])
            self.appText.set_map('transYeji', globals()['r.text']['data']['records'][0]['transYeji'])
            self.appText.set_map('CJDH', globals()['r.text']['data']['records'][0]['transOrderNo'])

    def TransactionSettlementStatisticalInfo(self):
        """结算详情"""
        self.PostRequest(url='/api/b/transactionSettlement/getTransactionSettlementStatisticalInfo',
                         data={
                             'transId': self.appText.get('transId')
                         })
        self.appText.set_map('amountToBeCollected',
                             globals()['r.text']['data']['amountToBeCollected'])  # 待收金额
        self.appText.set_map('debtCollectionSchedule',
                             globals()['r.text']['data']['debtCollectionSchedule'])  # 回款进度
        self.appText.set_map('paidCommission',
                             globals()['r.text']['data']['paidCommission'])     # 发放佣金
        self.appText.set_map('receivableAmount',
                             globals()['r.text']['data']['receivableAmount'])     # 回款金额
        self.appText.set_map('paidWealth', globals()['r.text']['data']['paidWealth'])     # 财富值
        self.appText.set_map('printedInvoiceAmount',
                             globals()['r.text']['data']['printedInvoiceAmount'])     # 已开票金额

    def TransReturnList(self, returnType=1):
        """回款 | 开票 记录"""
        self.PostRequest(url='/api/b/transactionSettlement/getTransReturnList',
                         data={
                             'transId': self.appText.get('transId'),
                             'returnType': returnType  # 1回款 2开票
                         }, page={
                                'size': '100',
                                'current': '1'
                            })
        if len(globals()['r.text']['data']['records']) != 0:
            self.appText.set_map('web_total', len(globals()['r.text']['data']['records']))
            self.appText.set_map('returnMoney', globals()['r.text']['data']['records'][0]['returnMoney'])
            a = 0
            vlue = 0
            while a != self.appText.get('web_total'):
                vlue = vlue + int(globals()['r.text']['data']['records'][a]['returnMoney'])
                a = a + 1
            self.appText.set_map('vlue', vlue)
        else:
            self.appText.set_map('vlue', 0)

    def WealthDetailList(self):
        """授予财富值记录"""
        self.PostRequest(url='/api/b/transactionSettlement/getWealthDetailList',
                         data={
                             'transId': self.appText.get('transId'),
                             'wealthType': self.appText.get('CJFF'),
                             'wealthTypeRelId': self.appText.get('transId')
                         }, page={
                                'size': '100',
                                'current': '1'
                            })
        if len(globals()['r.text']['data']['records']) != 0:
            self.appText.set_map('web_total', len(globals()['r.text']['data']['records']))
            self.appText.set_map('wealthValue', globals()['r.text']['data']['records'][0]['wealthValue'])
            a = 0
            vlue = 0
            while a != self.appText.get('web_total'):
                vlue = vlue + int(globals()['r.text']['data']['records'][a]['wealthValue'])
                a = a + 1
            self.appText.set_map('vlue', vlue)
        else:
            self.appText.set_map('wealthValue', 0)

    def addOrUpdateReceivableRecords(self, attachmentIds=1798, returnType=1,
                                     returnRemark='备注' + time.strftime("%Y-%m-%d %H:%M:%S")):
        """添加回款 | 开票记录 记录"""
        returnMoney = random.randint(20, 10000)
        self.appText.set_map('returnMoney', returnMoney)
        self.PostRequest(url='/api/b/transactionSettlement/addOrUpdateReceivableRecords',
                         data={
                             'returnNo': '1' + str(int(time.time())),
                             'returnMoney': returnMoney,
                             'returnRemark': returnRemark,
                             'returnType': returnType,  # 1回款 2开票
                             'transId': self.appText.get('transId'),
                             'attachmentIds': attachmentIds
                         })
        self.appText.set_map('returnMoney', returnMoney)

    def awardedWealthDetail(self):
        """授予财富值"""
        wealthValue = random.randint(20, 100)
        self.PostRequest(url='/api/b/transactionSettlement/awardedWealthDetail',
                         data={
                             'consultantId': self.appText.get('consultantId'),
                             'wealthTypeRelId': self.appText.get('transId'),
                             'wealthType': self.appText.get('CJFF'),
                             'wealthRemark': time.strftime("%Y-%m-%d %H:%M:%S") + ' 授予财富值',
                             'wealthValue': wealthValue
                         })
        self.appText.set_map('wealthValue', wealthValue)

    def TransReturnStatistical(self, returnType=1):
        """查询回款 开票总和与进度 """
        self.PostRequest(url='/api/b/transactionSettlement/getTransReturnStatistical',
                         data={
                             'returnType': returnType,  # 1 回款 2 开票
                             'transId': self.appText.get('transId')
                         })
        self.appText.set_map('forReceivable', globals()['r.text']['data']['forReceivable'])  # 待开票 | 待回款
        self.appText.set_map('percentage', globals()['r.text']['data']['percentage'])       # 进度
        self.appText.set_map('returnMoney', globals()['r.text']['data']['returnMoney'])     # 总额

    def paymentRequest(self):
        """新建发佣申请"""
        paymentAmount = random.randint(2, 20)
        self.PostRequest(url='/api/b/payment/request',
                         data={
                             'paymentDetailFormList': [{
                                 'consultantId': self.appText.get('consultantId'),
                                 'paymentAmount': paymentAmount,
                             }],
                             'paymentTypeId': self.appText.get('YJLX'),
                             'transId': self.appText.get('transId'),
                         }, saasCodeSys=1)
        self.appText.set_map('paymentAmount', paymentAmount)

    def paymentRegister(self):
        """付款登记"""
        self.PostRequest(url='/api/b/payment/register',
                         data={
                                "payeeBank": "烟台市华润银行",
                                "payeeBankAccount": "4437897883729183387",
                                "payeeLegalName": "苏先生",
                                "payeeName": "烟台幸福云灵活用工邮箱公司",
                                "paymentAmount": self.appText.get('paymentAmount'),
                                "paymentBank": "烟台市华润银行",
                                "paymentBankAccount": "4437897883729183387",
                                "paymentId": None,
                                "paymentName": "烟台幸福云灵活用工邮箱公司",
                                "paymentNo": "凭证号" + time.strftime("%Y-%m-%d %H:%M:%S"),
                                "paymentRemark": time.strftime("%Y-%m-%d %H:%M:%S") + "付款登记",
                                "requestId": self.appText.get('requestId'),
                            })

    def requestList(self, paymentStatus=0, keyWord=None):
        """付款登记列表"""
        self.PostRequest(url='/api/b/payment/request/list',
                         data={
                             'keyWord': keyWord,
                             'paymentStatus': paymentStatus,
                         })
        if len(globals()['r.text']['data']['records']) != 0:
            self.appText.set_map('requestId', globals()['r.text']['data']['records'][0]['requestId'])

    def requestAudit(self):
        """付款审核"""
        self.PostRequest(url='/api/b/payment/request/audit',
                         data={
                             'auditIdList': [self.appText.get('requestId')],
                             'auditStatue': 1,
                             'auditRemark': None    # 审核备注

                         }, saasCode='admin', saasCodeSys=1)

    def paymentList(self):
        """结算详情--佣金订单"""
        self.PostRequest(url='/api/b/payment/info/list',
                         data={
                             'transId': self.appText.get('transId'),
                             'advanceStatus': [1, 2, 3, 4]
                         }, page={
                                'size': '100',
                                'current': '1'
                            })
        if len(globals()['r.text']['data']['records']) != 0:
            dome = len(globals()['r.text']['data']['records'])
            self.appText.set_map('paymentAmount', globals()['r.text']['data']['records'][0]['paymentAmount'])
            a = 0
            vlue = 0
            while a != dome:
                vlue = vlue + int(globals()['r.text']['data']['records'][a]['paymentAmount'])
                a = a + 1
            self.appText.set_map('vlue', vlue)

    def consultantWealthChange(self, Type=1):
        """授予财富值"""
        if Type == 1:
            Type = 'add'
            consultantWealth = random.randint(10, 100)
        else:
            Type = 'del'
            consultantWealth = random.randint(-100, -10)
        self.PostRequest(url='/api/b/wealth/consultantWealthChange',
                         data={
                             'type': Type,
                             'consultantWealth': consultantWealth,
                             'consultantId': self.appText.get('consultantId'),
                             'wealthRemark': time.strftime("%Y-%m-%d %H:%M:%S")
                         })
        self.appText.set_map('vlue', consultantWealth)

    def getWealthAuditList(self, keyWord=None, auditStatus=0):
        """财务总监审核列表"""
        self.PostRequest(url='/api/b/wealthAudit/getWealthAuditList',
                         data={
                             'keyWord': keyWord,
                             'auditStatus': auditStatus,
                         })
        if len(globals()['r.text']['data']['records']) != 0:
            self.appText.set_map('auditId', globals()['r.text']['data']['records'][0]['auditId'])
        self.appText.set_map('total', len(globals()['r.text']['data']['records']))

    def wealthAudit(self, auditType=True):
        if auditType == True:
            auditRemark = None
        else:
            auditRemark = time.strftime("%Y-%m-%d %H:%M:%S")
        """授予财富值审核"""
        self.PostRequest(url='/api/b/wealthAudit/wealthAudit',
                         data={
                            'auditId': self.appText.get('auditId'),
                            'auditType': auditType,
                            'auditRemark': auditRemark,
                         })

    def repayTaskList(self, keyWord=None, repayStatusList=1, repayType=1):
        """待回访"""
        self.PostRequest(url='/api/b/repayTask/list',
                         data={
                             'keyWord': keyWord,
                             'repayStatusList': [repayStatusList],      # 1 待回访
                             'repayType': repayType             # 1 带看 2 成交

                         },
                         saasCode='admin', saasCodeSys=0,
                         page={
                            "current": 1,
                            "size": 999,
                            "total": 0
                         })
        self.appText.set_map('total', len(globals()['r.text']['data']['records']))
        if self.appText.get('total') != 0:
            self.appText.set_map('taskId', globals()['r.text']['data']['records'][0]['taskId'])

    def repayTask(self):
        """回访"""
        repayMode = random.randint(1, 2)
        repayLevel = random.randint(1, 4)
        self.PostRequest(url='/api/b/repayTask/repay',
                         data={
                             'repayContent': time.strftime("%Y-%m-%d %H:%M:%S") + '回访',
                             'repayLevel': repayLevel,   # 1 非常满意    2 满意    3 不满意   4 非常不满意
                             'repayMode': repayMode,    # 1 电话回访 2 短信回访
                             'taskId': self.appText.get('taskId'),
                         }, saasCode='admin', saasCodeSys=1)

    def repayTaskCancel(self):
        """取消回访"""
        self.PostRequest(url='/api/b/repayTask/cancel',
                         data={
                             'cancelLabel': self.appText.get('QXHF'),
                             'taskId': self.appText.get('taskId')
                         }, saasCode='admin', saasCodeSys=1)


if __name__ == '__main__':
    a = webApi()





