# -*- coding: utf-8 -*-
# @Time    : 2020/9/5 10:22
# @Author  : 潘师傅
# @File    : xfp_web_api.py
# -*- coding: utf-8 -*-

from XFP.PubilcAPI.appApi import *
import random
import math

class webApi:

    def __init__(self):
        self.XfpRequest = appApi()
        self.app_api = self.XfpRequest
        self.appText = GlobalMap()
        self.webText = GlobalMap()

    def PostRequest(self, url, data, saasCode=XfpsaasCode):
        """post请求"""
        data1 = {"page": {},
                 "saasCode": saasCode,
                 "saasCodeSys": saasCode}
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
        if globals()['r.text']['code'] != 200:
            raise RuntimeError(self.webText.get('ApiXfpUrl'))

        if r.elapsed.total_seconds() > 5:
            print('接口请求过慢')
            print(self.webText.get('URL'))
        if r.elapsed.total_seconds() > 10:
            print('接口请求过慢大于10秒')
            raise RuntimeError(self.webText.get('URL'))


    def Audit_management(self, suspend=False, suspendLevel=1, clueStop=False, clueStopLevel=1,
                         customerStop=False, customerStopLevel=1, customerVisit=False,
                         customerVisitLevel=1, customerDeal=False, customerDealLevel=1):
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
                            "customerDealLevel": customerDealLevel
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
                            "firstCallDaySwitch": True,
                            "firstCallDayWealth": 10,
                            "notFirstCallDayWealth": 5,
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

    def audit_List(self, keyWord=None, auditStatue=0, auditLevel=1):
        """审核列表"""
        self.PostRequest(url='/api/b/audit/auditList',
                         data={
                            'keyWord': keyWord,
                            'auditLevel': auditLevel,       # 1是经理 2是总监
                            'auditStatue': auditStatue      # 状态 0是待审核 1 同意 2 是拒绝
                         })
        self.webText.set_map('total', globals()['r.text']['data']['total'])
        if globals()['r.text']['data']['total'] != 0:
            self.webText.set_map('applyReason', globals()['r.text']['data']['records'][0]['applyReason'])
            self.webText.set_map('auditId', globals()['r.text']['data']['records'][0]['auditId'])
            self.webText.set_map('auditType', globals()['r.text']['data']['records'][0]['auditType'])
            self.webText.set_map('auditLevel', globals()['r.text']['data']['records'][0]['auditLevel'])
            self.webText.set_map('parentAuditId', globals()['r.text']['data']['records'][0]['parentAuditId'])
            self.webText.set_map('clueId', globals()['r.text']['data']['records'][0]['clueId'])
            self.webText.set_map('customerId', globals()['r.text']['data']['records'][0]['customerId'])

    def auditApply(self, vlue=1, auditRemark=None, isAudit=True, customerId='', endTime=''):
        """审核"""
        if vlue == 2:
            parentAuditId = self.appText.get('parentAuditId')
        else:
            parentAuditId = ''
        self.PostRequest(url='/api/b/audit/auditApply',
                         data={
                             'clueId': self.appText.get('clueId'),
                             'auditId': self.webText.get('auditId'),
                             'customerId': customerId,
                             'applyReason': self.webText.get('applyReason'),
                             'consultantId': self.appText.get('consultantId'),
                             'auditLevel': self.webText.get('auditLevel'),
                             'auditType': self.webText.get('auditType'),
                             'isAudit': isAudit,
                             'parentAuditId': parentAuditId,
                             'endTime': endTime,
                             'auditRemark': auditRemark,
                         })

    def add_label(self, labelName, labelId, pid):
        """新增标签"""
        self.PostRequest(url='/api/b/systembase/saveLabel',
                         data={
                             'labelId': labelId,
                             'pid': pid,                # 添加大标签 这个填0
                             'labelName': labelName
                         })

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

    def clue_list(self, myClue='Y', rderNo=None, vlue=0):
        """线索列表"""
        self.PostRequest(url='/api/b/clue/list',
                         data={
                             'myClue': myClue,
                             'isWork': True,
                             'orderNo': rderNo
                         })
        if globals()['r.text']['data']['total'] != 0:
            vlue = vlue + 1
            self.appText.set_map('clueId',
                                 globals()['r.text']['data']['records'][len(globals()['r.text']['data']['records']) - vlue]['clueId'])
            self.appText.set_map('cluePhone',
                                 globals()['r.text']['data']['records'][len(globals()['r.text']['data']['records']) - vlue]['cluePhone'])
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

    def add_clue_admin(self, clueNickName):
        """总部添加线索"""
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

    def deal_list(self, transType=None):
        """成交列表"""
        self.PostRequest(url='/api/b/transationInfo/list',
                         data={
                             'transStatus': 1,
                             'consultantId': self.appText.get('consultantId'),
                             'endTime': self.appText.get('end_date'),
                             'startTime': self.appText.get('start_date'),
                             'transType': transType
                         })
        self.webText.set_map('web_total', globals()['r.text']['data']['total'])
        if self.webText.get('web_total') != 0:
            self.appText.set_map('clueId', globals()['r.text']['data']['records'][0]['clueId'])
            self.appText.set_map('transId', globals()['r.text']['data']['records'][0]['transId'])
            self.appText.set_map('customerId', globals()['r.text']['data']['records'][0]['customerId'])
            self.appText.set_map('transYeji', globals()['r.text']['data']['records'][0]['transYeji'])

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
            self.webText.set_map('web_newClueCount', dome['newClueCount'])     # 通话次数
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

if __name__ == '__main__':
    a = webApi()

