# -*- coding: utf-8 -*-
# @Time    : 2020/3/9 11:54
# @Author  : 潘师傅
# @File    : XfpApi.py
import requests
import json
from GlobalMap import GlobalMap
from Config.Config import *
import unittest
import time
import random
import datetime
import calendar


class appApi:

    def __init__(self):
        self.appText = GlobalMap()

    def RandomText(self, textArr):
        """指定字符串随机取值"""
        # ['你好啊','阿米里！','扣你七娃','你好','hello']
        length = len(textArr)
        if length < 1:
            return ''
        if length == 1:
            return str(textArr[0])
        randomNumber = random.randint(0, length - 1)
        return str(textArr[randomNumber])

    def Merge(self, dict1, dict2):
        return (dict2.update(dict1))

    def PostRequest(self, url, data, header=None, Status=1, files=None, saasCode=XfpsaasCode):
        """post请求"""
        if header is not None:
            r = requests.post(url=(ApiXfpUrl + url),
                              data=json.dumps(data, ensure_ascii=False),
                              headers={
                                  'Content-Type': 'application/json'

                              })
        else:
            data1 = {"page": {
                'size': '100',
                'current': '1'
            },
                "saasCode": saasCode,
                "saasCodeSys": saasCode
            }
            self.Merge(data1, data)
            time.sleep(0.2)
            r = requests.post(url=(ApiXfpUrl + url),
                              data=(json.dumps(data,
                                               ensure_ascii=False).encode("UTF-8")),
                              headers={
                                  'Content-Type': 'application/json',
                                  'Authorization': 'Bearer' + ' ' + self.appText.get("user_token")
                              },
                              files=files)
        r.raise_for_status()
        self.appText.set_map('URL', ApiXfpUrl + url)
        globals()['XfpText'] = globals()['r.text'] = json.loads(r.text)
        self.appText.set_map('XfpText', globals()['r.text'])
        self.appText.set_map('ApiXfpUrl', url)
        self.appText.set_map('msg', globals()['XfpText']['msg'])
        self.appText.set_map('code', globals()['XfpText']['code'])
        self.appText.set_map('data', globals()['XfpText']['data'])
        time.sleep(0.2)
        if Status == 1:
            try:
                assert "成功", globals()['r.text']['msg']
            except BaseException as e:
                print("断言错误，错误原因：%s" % e)
                raise RuntimeError(self.appText.get('URL'))
        if globals()['r.text']['code'] == 500:
            raise RuntimeError(self.appText.get('ApiXfpUrl'))

        if r.elapsed.total_seconds() > 5:
            print('接口请求过慢')
            print(self.appText.get('ApiXfpUrl'))
        if r.elapsed.total_seconds() > 10:
            print('接口请求过慢大于10秒')
            print(self.appText.get('ApiXfpUrl'))

    def Sign(self, userName, password='123456789'):
        """注册"""
        self.PostRequest(url='/api/auth/sign',
                         data={"userName": userName,
                               'saasCode': XfpsaasCode,
                               "password": password
                               },
                         header=1
                         )
        self.appText.set_map('msg', globals()['XfpText']['msg'])

    def Login(self, userName=XfpUser, password=XfpPwd, saasCode=XfpsaasCode, authCode=None, device=None):
        """登录"""
        if device is None:
            device = deviceId
        if authCode is None:
            self.PostRequest(url='/api/auth/login',
                             data={"userName": userName,
                                   'saasCode': saasCode,
                                   'deviceId': device,
                                   # 'deviceId': deviceId,
                                   "password": password},
                             header=1)
        else:
            self.PostRequest(url='/api/auth/login',
                             data={"userName": userName,
                                   'saasCode': saasCode,
                                   'authCode': authCode,
                                   "password": password},
                             header=1)

        if self.appText.get('msg') == '成功':
            if (globals()['XfpText']['data']['userDetail']) is not 'None':
                if authCode is None:
                    self.appText.set_map('user_token', globals()['XfpText']['data']['token'])

                else:
                    self.appText.set_map('user_token', globals()['XfpText']['data']['token'])
                try:
                    self.appText.set_map('resultStr', globals()['r.text']['data']['resultStr'])
                except:
                    pass

            else:
                self.appText.set_map('userId', globals()['XfpText']['data']['userDetail']['id'])

        else:
            self.appText.set_map('data', globals()['XfpText']['data'])

    def GetUserData(self, device=None):
        """获取咨询师信息"""
        if device is None:
            device = deviceId
        self.PostRequest(url='/api/a/consultant/info',
                         data={'deviceId': device})
        if self.appText.get('code') == 200:
            self.appText.set_map('consultantId', globals()['r.text']['data']['consultantId'])
            self.appText.set_map('consultantName', globals()['r.text']['data']['consultantName'])
            self.appText.set_map('consultantLabels', globals()['r.text']['data']['consultantLabels'])
            self.appText.set_map('userId', globals()['r.text']['data']['userId'])
        # else:
        #     pass

    def GetUserAgenda(self, keyWord=None, visitNo=True, tesk=1):
        """获取用户待办"""
        self.PostRequest(url='/api/a/consultant/getConsultantWorkSchedule',
                         data={
                             'consultantId': self.appText.get('consultantId'),
                             "deviceId": deviceId,
                             # "taskType": taskType,  # 0 超时1 线索 2 联系 3带看
                             "isCompleted": 0,
                             # 'clueId': clueId,
                             'consultantIds': [self.appText.get('consultantId')],
                             'day': 7,
                             "isStop": 0,
                             "endTime": time.strftime("%Y-%m-%d"),
                             'isWorkSchedule': True,
                             "overtime": None,
                             'keyWord': keyWord,
                             'visitNo': visitNo
                         })
        self.appText.set_map('dome', globals()['r.text']['data'][0])
        dome = json.loads(self.appText.get('dome'))
        self.appText.set_map('total', len(dome[time.strftime("%Y-%m-%d")]['taskVos']))
        if self.appText.get('total') != 0:
            dome1 = 0
            while int(dome[time.strftime("%Y-%m-%d")]['taskVos'][dome1]['taskTypeAlias']) != tesk:
                dome1 = dome1 + 1
                if dome1 == self.appText.get('total'):
                    break
            if dome1 == self.appText.get('total'):
                dome1 = dome1 - 1
            self.appText.set_map('endTime', dome[time.strftime("%Y-%m-%d")]['taskVos'][dome1]['endTime'])
            self.appText.set_map('clueId', dome[time.strftime("%Y-%m-%d")]['taskVos'][dome1]['clueId'])
            self.appText.set_map('taskType', dome[time.strftime("%Y-%m-%d")]['taskVos'][dome1]['taskType'])
            self.appText.set_map('customerId',
                                 dome[time.strftime("%Y-%m-%d")]['taskVos'][dome1]['customerId'])

    def CluePhoneLog(self, clueId=None):
        if clueId is None:
            clueId = self.appText.get('clueId')
        """线索通话记录"""
        self.PostRequest(url='/api/a/clue/phonelog/list',
                         data={'clueId': clueId})
        self.appText.set_map('total', len(globals()['r.text']['data']['records']))
        if self.appText.get('total') != 0:
            self.appText.set_map('isFlagCallStr', globals()['r.text']['data']['records'][0]['isFlagCallStr'])   # 是否主叫
            self.appText.set_map('consultantName', globals()['r.text']['data']['records'][0]['consultantName'])
            self.appText.set_map('isFirst', globals()['r.text']['data']['records'][0]['isFirst'])

    def ConsultantUpdate(self, consultantName='潘师傅(测试)'):
        """修改咨询师名称"""
        self.PostRequest(url='/api/a/consultant/update',
                         data={'consultantId': self.appText.get('consultantId'),
                               'consultantName': consultantName,
                               'userId': self.appText.get('userId'),
                               'consultantPhone': XfpUser,
                               'deviceId': deviceId,
                               'isDeleted': 0,
                               'consultantSex': 1,
                               'consultantService': '1111',
                               'consultantLabels': '专注,细致,高分服务,政策解读达人'})

    def GetUserEmploymentObjective(self):
        """获取咨询师工作目标"""
        self.PostRequest(url='/api/a/consultant/goal/info',
                         data={'consultantId': self.appText.get('consultantId')})

    def GetUserLabelList(self, userLabelType='线索标签', value=0):
        """获取标签"""
        self.PostRequest(url='/api/label/getUserLabelList',
                         data={
                             'userLabelType': userLabelType
                         })
        if globals()['r.text']['data']['total'] != 0:
            self.appText.set_map('labelData', globals()['r.text']['data']['records'][value]['userLabelValue'])

        self.appText.set_map('total', globals()['r.text']['data']['total'])

    def AddUserLabel(self, userLabelValue='线索标签', userLabelType='线索标签'):
        """新增标签"""
        self.PostRequest(url='/api/label/addOrUpdateUserLabel',
                         data={
                             'userLabelValue': userLabelValue,
                             'userLabelType': userLabelType
                         })

    def UpdateUserLabel(self, userLabelValue=None, userLabelType='线索标签'):
        """修改标签"""
        self.PostRequest(url='/api/label/addOrUpdateUserLabel',
                         data={
                             'userLabelId': self.appText.get('userLabelId'),
                             'userLabelValue': userLabelValue,
                             'userLabelType': userLabelType,
                         })

    def DelUserLabel(self):
        """删除标签"""
        self.PostRequest(url='/api/label/delUserLabel',
                         data={
                             'userLabelId': self.appText.get('userLabelId')
                         })

    def ClueTask(self):
        """线索待办"""
        self.PostRequest(url='/api/a/clue/task/list',
                         data={"consultantId": self.appText.get('consultantId'),
                               "clueId": self.appText.get('clueId'),
                               "isCompleted": 0,
                               "isStop": 0})
        # assert '线索跟进', globals()['r.text']['data']['records'][0]['taskTitle']
        self.appText.set_map('total', len(globals()['r.text']['data']['records']))
        if len(globals()['r.text']['data']['records']) != 0:
            self.appText.set_map('endTime', globals()['r.text']['data']['records'][0]['endTime'])
            self.appText.set_map('taskRemark', globals()['r.text']['data']['records'][0]['taskRemark'])

    def ClaimClue(self):
        """认领线索"""
        self.PostRequest(url='/api/a/clue/claim',
                         data={'clueId': self.appText.get('clueId')})

    def ClueFollowList(self, value=0, followType=None):
        """查询线索跟进列表"""
        self.PostRequest(url='/api/a/clue/follow/list',
                         data={'clueId': self.appText.get('clueId'),
                               'followType': followType
                               })
        if len(globals()['r.text']['data']['records']) != 0:
            self.appText.set_map('total', len(globals()['r.text']['data']['records']))
            self.appText.set_map('followContent',
                                 globals()['r.text']['data']['records'][value]['followContent'])
            self.appText.set_map('followId', globals()['r.text']['data']['records'][value]['followId'])
            self.appText.set_map('taskId', globals()['r.text']['data']['records'][value]['taskId'])
        else:
            print('线索跟进列表为空？')
            self.appText.set_map('followId', None)
            self.appText.set_map('taskId', None)

    def ClueList(self, keyWord=''):
        """查询线索列表"""
        self.PostRequest(url='/api/a/clue/task/list',
                         data={"keyWord": keyWord,
                               "isCompleted": 0,
                               "isStop": 0,
                               "overtime": 0})

    def ClueFollowSave(self, taskEndTime, followType='线索',
                       followContent='python-线索/客户跟进，本次沟通记录',
                       taskRemark='python-线索/客户跟进，下次沟通记录'):
        """线索/客户跟进录入"""
        if followType == '线索':
            followType = 1
            taskType = '1'
            self.appText.set_map('customerId', 'null')
            taskId = 'taskId'
        else:
            followType = '3'
            taskType = '2'
            taskId = 'taskOldId'
        self.PostRequest(url='/api/a/clue/saveFollow',
                         data={
                             'clueId': self.appText.get('clueId'),
                             'attachmentIds': None,
                             'followContent': followContent,
                             'customerId': self.appText.get('customerId'),
                             'followType': followType,
                             'taskType': taskType,
                             'taskRemark': taskRemark,
                             'taskId': self.appText.get('taskId'),
                             'followId': self.appText.get('followId'),
                             'endTime': taskEndTime,
                             'taskOldId': self.appText.get('taskId'),
                             'taskEndTime': taskEndTime
                         })

    def TodayClue(self, isFirst=0):
        """今日线索"""
        self.PostRequest(url='/api/a/consultant/firstCallList',
                         data={
                               'consultantId': self.appText.get('consultantId'),
                               'isFirst': isFirst})
        self.appText.set_map('Total', len(globals()['r.text']['data']['records']))
        if self.appText.get('Total') != 0:
            self.appText.set_map('records', globals()['r.text']['data']['records'])

    def ResetPassword(self, userId):
        """重设密码"""
        self.PostRequest(url='/api/b/systemrole/resetPassword',
                         data={'userId': userId})

    def ClueContinue(self, taskEndTime):
        """创建线索计划"""
        self.PostRequest(url='/api/a/clue/continue',
                         data={
                             # 'followContent': followContent,    # 内容
                             "consultantId": self.appText.get('consultantId'),
                             "consultantPhone": XfpUser,
                             "deviceId": deviceId,
                             "clueId": self.appText.get('clueId'),
                             "customerPhone": self.appText.get('cluePhone'),
                             "isCompleted": 0,
                             "isStop": 0,
                             "taskEndTime": taskEndTime})

    def ClueInfo(self):
        """线索详情"""
        self.PostRequest(url='/api/a/clue/info',
                         data={'clueId': self.appText.get('clueId')})
        if (globals()['r.text']['data']['cluePhone'])[3:4] == '*':
            self.appText.set_map('cluePhone', '1' + str(int(time.time())))
        else:
            self.appText.set_map('cluePhone', globals()['r.text']['data']['cluePhone'])
        self.appText.set_map('sourceId', globals()['r.text']['data']['sourceId'])
        self.appText.set_map('receptionTime', globals()['r.text']['data']['receptionTime'])
        self.appText.set_map('createdTime', globals()['r.text']['data']['createdTime'])
        self.appText.set_map('isFirst', globals()['r.text']['data']['isFirst'])
        self.appText.set_map('orderNo',globals()['r.text']['data']['orderNo'])

    def ClueSave(self, Status=1,  # 1新增 其他修改
                 cluePhone=None,
                 clueNickName='潘师傅',
                 sourceId=1,
                 clueAddtypeText='表单',  # 表单，来电，IM客服
                 keyWords='',     # 标签
                 remark=''
                 ):
        self.appText.set_map('cluePhone', cluePhone)
        if cluePhone != None:
            pass
        else:
            cluePhone = '1' + str(int(time.time()))
        """新增/修改线索"""
        if Status == 1:
            clueId = ' '
        else:
            clueId = self.appText.get('clueId')
        self.PostRequest(url='/api/a/clue/save',
                         data={
                             'clueId': clueId,
                             'cluePhone': cluePhone,  # 联系方式
                             'clueNickName': clueNickName,  # 称呼
                             # 'clueName': clueNickName,
                             'clueAddtypeText': clueAddtypeText,
                             'keyWords': keyWords,
                             "remark": remark,
                             'sourceId': sourceId
                         })  # 来源
        if globals()['r.text']['msg'] == '成功':
            self.appText.set_map('clueId', globals()['r.text']['data']['clueId'])
            self.appText.set_map('cluePhone', cluePhone)
            self.appText.set_map('createdTime', globals()['r.text']['data']['createdTime'])
            self.appText.set_map('orderNo', globals()['r.text']['data']['orderNo'])

    def ClientSave(self, GFYX, ZJZZ, areaId, phoneNum=None,
                   sex='1', clueNickName='潘师傅', XSLY=None, LYBQ='表单',  # 表单，来电，IM客服
                   projectAId=None, projectBId=None,
                   projectCId=None, GFMD=None, WYSX=None, GFZZ=None, SFST=None,
                   DKQK=None, SFYS=None, SFBL=None, MJ=None, KHXQ=None,
                   remark='python-直接录入客户' + time.strftime("%Y-%m-%d")):
        if phoneNum is None:
            phoneNum = '1' + str(int(time.time()))
        """直接录入客户"""
        self.PostRequest(url='/api/a/customer/save',
                         data={
                             'customerDemandForm': {
                                 'phoneNum': phoneNum,  # 电话号码
                                 'sex': sex,  # 性别
                                 'clueNickName': clueNickName,  # 称呼
                                 'sourceId': XSLY,  # 线索来源
                                 'clueAddtypeText': LYBQ,  # 来源标签

                                 'intentionLevelLableId': GFYX,  # 购房意向
                                 'capitalQualificationLableId': ZJZZ,  # 资金资质
                                 'areaId': areaId,  # 区域
                                 'projectAId': projectAId,  # 项目一
                                 'projectBId': projectBId,  # 项目二
                                 'projectCId': projectCId,  # 项目三

                                 'purchasePurposeLableIds': GFMD,
                                 # 购房目的
                                 'propertyAttributeLableIds': WYSX,
                                 # 物业属性
                                 'purchaseQualificationLableIds': GFZZ,
                                 # 购房资质

                                 'theFirstLableIds': SFST,  # 是否首套
                                 'loanSituation': DKQK,  # 贷款情况
                                 'paymentBudget': SFYS,  # 首付预算
                                 'paymentRatio': SFBL,  # 首付比例
                                 'apartmentLayout': MJ,  # 面积
                                 'customerDemandLableIds': KHXQ,  # 客户需求
                                 'remark': remark,  # 备注
                             },
                             'saasClueForm': {
                                 'cluePhone': phoneNum,  # 电话号码
                                 'sex': sex,  # 性别
                                 'clueNickName': clueNickName,  # 称呼
                                 'sourceId': XSLY,  # 线索来源
                                 'clueAddtypeText': LYBQ,  # 来源标签

                                 'intentionLevelLableId': GFYX,  # 购房意向
                                 'capitalQualificationLableId': ZJZZ,  # 资金资质
                                 'areaId': areaId,  # 区域
                                 'projectAId': projectAId,  # 项目一
                                 'projectBId': projectBId,  # 项目二
                                 'projectCId': projectCId,  # 项目三

                                 'purchasePurposeLableIds': GFMD,
                                 # 购房目的
                                 'propertyAttributeLableIds': WYSX,
                                 # 物业属性
                                 'purchaseQualificationLableIds': GFZZ,
                                 # 购房资质

                                 'theFirstLableIds': SFST,  # 是否首套
                                 'loanSituation': DKQK,  # 贷款情况
                                 'paymentBudget': SFYS,  # 首付预算
                                 'paymentRatio': SFBL,  # 首付比例
                                 'apartmentLayout': MJ,  # 面积
                                 'customerDemandLableIds': KHXQ,  # 客户需求
                                 'remark': remark,  # 备注
                             }

                         })
        self.appText.set_map('cluePhone', phoneNum)
        self.appText.set_map('clueId', globals()['r.text']['data']['clueId'])
        self.appText.set_map('customerId', globals()['r.text']['data']['customerId'])

    def ClientFollowList(self, value=0, followType=None):
        """客户跟进记录"""
        self.PostRequest(url='/api/a/customer/follow/list',
                         data={'clueId': self.appText.get('clueId'),
                               'followType': followType,
                               'customerId': self.appText.get('customerId')
                               })
        if len(globals()['r.text']['data']['records']) != 0:
            self.appText.set_map('total', len(globals()['r.text']['data']['records']))
            self.appText.set_map('followContent',
                                 globals()['r.text']['data']['records'][value]['followContent'])
            self.appText.set_map('followId', globals()['r.text']['data']['records'][value]['followId'])
            self.appText.set_map('taskId', globals()['r.text']['data']['records'][value]['taskId'])

    def ClientFolloow(self):
        """客户跟进"""
        self.PostRequest(url='/api/a/customer/follow/save',
                         data={'clueId': self.appText.get('clueId')})

    def ClientTask(self, taskType='3'):
        """客户待办提醒"""
        self.PostRequest(url='/api/a/customer/task/list',
                         data={
                             'clueId': self.appText.get('clueId'),
                             'customerId': self.appText.get('customerId')
                         })
        self.appText.set_map('total', len(globals()['r.text']['data']))
        if len(globals()['r.text']['data']) != 0:
            vlue = 0
            while vlue != self.appText.get('total'):
                # print(vlue)
                if self.appText.get('total') != vlue:
                    if globals()['r.text']['data'][vlue]['taskType'] == str(taskType):
                        break
                    vlue = vlue + 1
            if vlue == self.appText.get('total'):
                vlue = vlue - 1
            self.appText.set_map('taskType', globals()['r.text']['data'][vlue]['taskType'])
            self.appText.set_map('taskRemark', globals()['r.text']['data'][vlue]['taskRemark'])
            self.appText.set_map('visitId', globals()['r.text']['data'][vlue]['visitId'])
            self.appText.set_map('taskId', globals()['r.text']['data'][vlue]['taskId'])
            self.appText.set_map('endTime', globals()['r.text']['data'][vlue]['endTime'])

    def ClientVisitAdd(self, projectAId, appointConsultant, seeingConsultant,
                       appointmentTime=time.strftime("%Y-%m-%d %H:%M:%S"),
                       projectBId=None, projectCId=None, beforeTakingA='这个是客户情况',
                       beforeTakingB='这个是核心诉求', beforeTakingC='这个是核心抗性',
                       beforeTakingD='这个是应对方案', visitRemark='这个是带看备注'):
        """新增带看计划"""
        self.PostRequest(url='/api/a/visit/save',
                         data={
                             'clueId': self.appText.get('clueId'),
                             'appointConsultant': appointConsultant,    # 邀约咨询师
                             'customerId': self.appText.get('customerId'),  # 客户ID
                             'seeingConsultant': seeingConsultant,  # 带看人
                             # 'consultantId': self.appText.get('consultantId'),
                             'appointmentTime': appointmentTime,
                             'visitMode': self.appText.get('CXFS'),
                             'projectAId': projectAId,
                             'projectBId': projectBId,
                             'projectCId': projectCId,
                             'beforeTakingA': beforeTakingA,    # 客户情况
                             'beforeTakingB': beforeTakingB,    # 核心诉求
                             'beforeTakingC': beforeTakingC,    # 核心抗性
                             'beforeTakingD': beforeTakingD,    # 应对方案
                             'visitRemark': visitRemark,        # 带看备注
                             "appointmentPlaceLocale": {
                                 "localeCoordinates": "113.587585,22.251877",
                                 "localeName": "广东省珠海市香洲区吉大街道园林花园(园林路)",
                                 # "lon": 113.587585,
                                 # "lat": 22.251877
                             }
                         })
        self.appText.set_map('data', globals()['r.text']['data'])

    def UpdateVisitAdd(self, projectAId, projectBId=None, projectCId=None):
        """修改带看计划"""
        self.PostRequest(url='/api/a/customer/visit/update',
                         data={
                             'clueId': self.appText.get('clueId'),
                             'isTask': True,
                             'visitId': self.appText.get('visitId'),
                             'taskId': self.appText.get('taskId'),
                             'customerId': self.appText.get('customerId'),
                             'seeingPeople': self.appText.get('consultantId'),  # 带看人
                             'appointmentTime': time.strftime("%Y-%m-%d %H:%M:%S"),
                             'projectAId': projectAId,
                             'projectBId': projectBId,
                             'projectCId': projectCId,
                             "saasLocale": {
                                 "localeCoordinates": "113.587585,22.251877",
                                 "localeName": "广东省珠海市香洲区吉大街道园林花园(园林路)",
                                 "lon": 113.587585,
                                 "lat": 22.251877
                             }
                         })

    def VisitFlow1(self, agencyId, attachmentIds='1031', is_QA=2,questionTypeNo=None,
                   houseId=None, receptionName=None, receptionPhone=None,
                   answer=None, title=None, visitSummary='带看总结'):
        # self.GetMatchingAreaHouse()  # 匹配楼盘
        """完成带看"""
        if is_QA == 1:
            visitQaList = [{
                                 'answer': answer,                      # 答案
                                 'houseIds': houseId,
                                 # 'id': houseId,                             # 楼盘ID
                                 'questionTypeNo': questionTypeNo,          # 问答分类
                                 'title': title                         # 标题
                             }]
        else:
            visitQaList = []

        self.PostRequest(url='/api/a/visit/complete',
                         data={
                             'visitProjectList': [
                                 {
                                     'agencyId': agencyId,              # 对接平台
                                     'attachmentIds': attachmentIds,    # 报备附件
                                     'houseId': self.appText.get('houseId'),                # 楼盘ID
                                     'receptionName': receptionName,    # 对接人姓名
                                     'receptionPhone': receptionPhone   # 对接人电话
                                 }
                             ],
                             # 'customerId': self.appText.get('customerId'),
                             'visitId': self.appText.get('visitId'),
                             # 'clueId': self.appText.get('clueId'),
                             'visitSummary': visitSummary,              # 带看总结
                             'isComplete': 1,
                             'visitQaList': visitQaList
                         })

    def visit_info(self):
        """带看行程详情"""
        self.PostRequest(url='/api/a/customer/visit/info',
                         data={
                             'taskId': self.appText.get('taskId')
                         })
        self.appText.set_map('visitId', globals()['r.text']['data']['saasClueVisit']['visitId'])

    def visit_cancel(self, cancelRemark=time.strftime("%Y-%m-%d %H:%M:%S") + ' 取消带看'):
        """取消带看"""
        self.PostRequest(url='/api/a/visit/cancel',
                         data={
                             'visitId': self.appText.get('visitId'),
                             'cancelRemark': cancelRemark
                         })

    def ClientTaskPause(self, contactPurpose='python-申请暂停跟进',
                        endTime=time.strftime("%Y-%m-%d %H:%M:%S")):
        """申请暂停跟进"""
        self.PostRequest(url='/api/a/customer/task/pause',
                         data={
                             'clueId': self.appText.get('clueId'),
                             'labelId': self.appText.get('ZHGJ'),
                             'endTime': endTime,
                             'customerId': self.appText.get('customerId'),
                             'consultantId': self.appText.get('consultantId'),
                             # 'labelName': self.appText.get('labelName'),
                             'contactPurpose': contactPurpose,
                             'saasClueFollow': {
                                 'clueId': self.appText.get('clueId'),
                                 'customerId': self.appText.get('customerId'),
                                 'followLabelId': self.appText.get('labelId')
                             }
                         })
        self.appText.set_map('data', globals()['r.text']['data'])

    def HistoryFollow(self):
        """查看历史跟进"""
        self.PostRequest(url='/api/a/customer/getCustomerFollowHistoryList',
                         data={
                             'clueId': self.appText.get('clueId')
                         })

    def ExileSea(self, remark='python-线索释放公海'):
        """流放公海"""
        self.PostRequest(url='/api/a/clue/exileSea',
                         data={'clueId': self.appText.get('clueId'),
                               'remark': remark,
                               # 'labelName': self.appText.get('labelName'),
                               'labelId': self.appText.get('ZZGJ')})
        self.appText.set_map('data', globals()['r.text']['data'])

    def client_exile_sea(self, remark='python-客户释放公海'):
        """客户流放公海"""
        self.PostRequest(url='/api/a/customer/task/delete',
                         data={
                             'customerId': self.appText.get('customerId'),
                             'clueId': self.appText.get('clueId'),
                             # 'labelId': self.appText.get('ZZGJ'),
                             'consultantId': self.appText.get('consultantId'),
                             'saasClueFollow': {
                                 'customerId': self.appText.get('customerId'),
                                 'followContent': remark,
                                 'followLabelId': self.appText.get('ZZGJ'),
                                 'clueId': self.appText.get('clueId')
                             }
                         })
        self.appText.set_map('data', globals()['r.text']['data'])

    def LookHistoryFollow(self, value=0):
        """查看历史跟进"""
        self.PostRequest(url='/api/a/customer/getCustomerFollowHistoryList',
                         data={
                             'clueId': self.appText.get('clueId')
                         })
        self.appText.set_map('followContent', globals()['r.text']['data']['records'][value]['followContent'])

    def SeaList(self,
                seaType=None,  # 1表示线索 2 表示客户
                sourceId=None,  # 取流放公海的原因
                isTrans=0,
                keyWord=None):
        """公海列表"""
        self.PostRequest(url='/api/a/clue/sea/getSeaClueList',
                         data={'keyWord': keyWord,
                               'seaType': seaType,
                               'isTrans': isTrans,
                               'sourceId': sourceId})
        self.appText.set_map('total', globals()['r.text']['data']['total'])
        if globals()['r.text']['data']['total'] != 0:
            self.appText.set_map('clueNickName', globals()['r.text']['data']['records'][0]['clueNickName'])
            self.appText.set_map('clueId', globals()['r.text']['data']['records'][0]['clueId'])
            self.appText.set_map('isTrans', globals()['r.text']['data']['records'][0]['isTrans'])
            self.appText.set_map('labelName', globals()['r.text']['data']['records'][0]['labelName'])

    def clue_Assigned(self):
        """领取线索"""
        self.PostRequest(url='/api/a/clue/sea/clueAssigned',
                         data={
                             'consultantId': self.appText.get('consultantId'),
                             'clueId': self.appText.get('clueId'),
                             'isWorks': 0,
                             'isClaim': True,
                             'list': [
                                 {
                                     'consultantId': self.appText.get('consultantId'),
                                     'clueId': self.appText.get('clueId')
                                 }
                             ]
                         })

    def my_clue_list(self, vlue=0, myClue='Y', keyWord=None):
        """我的线索"""
        self.PostRequest(url='/api/a/clue/MyClueList',
                         data={
                             'myClue': myClue,
                             'consultantId': self.appText.get('consultantId'),
                             'isWork': True,
                             'keyWord': keyWord,
                         })

        if globals()['r.text']['data']['total'] != 0:
            vlue = vlue + 1
            self.appText.set_map('clueId',
                                 globals()['r.text']['data']['records'][len(globals()['r.text']['data']['records']) - vlue]['clueId'])
            self.appText.set_map('orderNo',
                                 globals()['r.text']['data']['records'][
                                     len(globals()['r.text']['data']['records']) - vlue]['orderNo'])
        else:
            pass
        self.appText.set_map('total', globals()['r.text']['data']['total'])

    def ConsultantList(self):
        """咨询师列表"""
        self.PostRequest(url='/api/a/consultant/list',
                         data={
                             'consultantId': self.appText.get('consultantId'),
                             'isShow': 0
                         })
        if len(globals()['r.text']['data']['records']) != 0:
            x = 0
            dome = globals()['r.text']['data']['records'][x]['consultantPhone']
            if dome != XfpUser1:
                while dome != XfpUser1:
                    x = x + 1
                    self.appText.set_map('consultantId2', globals()['r.text']['data']['records'][x]['consultantId'])
                    dome = globals()['r.text']['data']['records'][x]['consultantPhone']
                    if x > globals()['r.text']['data']['total']:
                        break
            else:
                self.appText.set_map('consultantId2', globals()['r.text']['data']['records'][x]['consultantId'])

    def ClueChange(self):
        """线索转移"""
        self.PostRequest(url='/api/a/clue/appoint',
                         data={
                             'clueIdList': [self.appText.get('clueId')],
                             'consultantId': self.appText.get('consultantId2'),
                         })

    def client_change(self):
        """客户转移"""
        self.PostRequest(url='/api/a/customer/transfer',
                         data={
                             'consultantId': self.appText.get('consultantId2'),
                             'customerId': self.appText.get('customerId'),
                             'clueId': self.appText.get('clueId')
                         })

    def GetLabelList(self, labelNo, labelName=None, saasCode=XfpsaasCode):
        """查询标签"""
        """
        线索标签        XSBQ             购房目的          GFND
        客户标签        KHBQ             物业属性          WYSX
        咨询师标签      ZXSBQ            购房资质          GFZZ
        线索来源        KHLY             是否首套房        SFSTF
        客户意向等级    KHYXDJ           其他客户需求      QTKHXQ
        资金资质        ZJZZ             咨询师个性标签    ZXSGXBQ

        """
        self.PostRequest(url='/api/tool/getLabelList/parameter',
                         data={'labelNo': labelNo},
                         saasCode=saasCode)
        if len(globals()['r.text']['data']) != 0:
            try:
                if labelName is not None:
                    a = 0
                    while labelName != globals()['r.text']['data'][0]['children'][a]['labelName']:
                        a = a + 1
                        if a == len((globals()['r.text']['data'][0]['children'])):  # 看看有多少个标签
                            a = a - 1
                            break
                    self.appText.set_map('labelId', globals()['r.text']['data'][0]['children'][a]['labelId'])
                    self.appText.set_map('labelName', globals()['r.text']['data'][0]['children'][a]['labelName'])
                    self.appText.set_map('labelNo', globals()['r.text']['data'][0]['children'][a]['labelNo'])
                    self.appText.set_map('remark', globals()['r.text']['data'][0]['children'][a]['remark'])
                else:
                    dome = random.randint(0, len(globals()['r.text']['data'][0]['children']) - 1)
                    self.appText.set_map('labelId', globals()['r.text']['data'][0]['children'][dome]['labelId'])
            except:
                self.appText.set_map('labelId', None)
                self.appText.set_map('labelName', None)
            self.appText.set_map('LabelId', globals()['r.text']['data'][0]['labelId'])
        else:
            self.appText.set_map('labelId', None)
            self.appText.set_map('labelName', None)

    def GetMatchingArea(self, text=None):
        """匹配区域"""
        self.PostRequest(url='/api/tool/getMatchingAreaList',
                         data={})

        if text is not None:
            a = 0
            while text != globals()['r.text']['data']['data'][0]['val'][0]['children'][a]['value']:
                a = a + 1
            self.appText.set_map('PPQY', globals()['r.text']['data']['data'][0]['val'][0]['children'][a]['value'])
        else:
            self.appText.set_map('PPQY', globals()['r.text']['data']['data'][0]['val'][0]['children'][0]['value'])
        self.appText.set_map('city', globals()['r.text']['data']['data'][0]['val'][0]['value'])

    def GetMatchingAreaHouse(self, value=0):
        """匹配楼盘"""
        self.PostRequest(url='/api/b/house/list',
                         data={})
        self.appText.set_map('total', len(globals()['r.text']['data']))
        if len(globals()['r.text']['data']['records']) != 0:
            self.appText.set_map('houseId', globals()['r.text']['data']['records'][value]['houseId'])
            self.appText.set_map('projectAId', globals()['r.text']['data']['records'][value]['houseId'])
            self.appText.set_map('projectBId', globals()['r.text']['data']['records'][1]['houseId'])
            self.appText.set_map('projectCId', globals()['r.text']['data']['records'][2]['houseId'])

    def ClientEntering(self, callName=None, sex=1, projectBId=0, projectCId=0,
                       loanSituation='', paymentRatio='',
                       paymentBudget='', apartmentLayout=''):
        """录入需求"""
        self.PostRequest(url='/api/a/customer/save',
                         data={
                             'consultantId': self.appText.get('consultantId'),
                             'customerDemandForm': {
                                 'clueId': self.appText.get('clueId'),
                                 'intentionLevelLableId': self.appText.get('KHYXDJ'),  # *购房意向
                                 'capitalQualificationLableId': self.appText.get('ZJZZ'),  # *资金资质
                                 'areaId': self.appText.get('PPQY'),  # *区域匹配
                                 'projectAId': self.appText.get('projectAId'),  # *匹配楼盘A
                                 'phoneNum': self.appText.get('cluePhone'),
                                 'cluePhone': self.appText.get('cluePhone'),
                                 'clueNickName': callName,  # 称呼
                                 'sex': sex,  # 性别 0女 1 男
                                 'projectBId': projectBId,  # *匹配楼盘B
                                 'projectCId': projectCId,  # *匹配楼盘C
                                 'purchasePurposeLableIds': self.appText.get('GFMD'),  # 购房目的，
                                 'propertyAttributeLableIds': self.appText.get('WYSX'),  # 物业属性，
                                 'purchaseQualificationLableIds': self.appText.get('GFZZ'),  # 购房资质
                                 'theFirstLableIds': self.appText.get('SFSTF'),  # 是否首套
                                 'loanSituation': loanSituation,  # 贷款情况
                                 'paymentRatio': paymentRatio,  # 首付比例
                                 'sourceId': self.appText.get('sourceId'),
                                 'paymentBudget': paymentBudget,  # 首付预算
                                 'apartmentLayout': apartmentLayout,  # 户型面积
                                 'customerDemandLableIds': self.appText.get('QTKHXQ')  # 客户需求
                             },
                             'saasClueForm': {
                                 'clueId': self.appText.get('clueId'),
                                 'intentionLevelLableId': self.appText.get('KHYXDJ'),  # *购房意向
                                 'capitalQualificationLableId': self.appText.get('ZJZZ'),  # *资金资质
                                 'areaId': self.appText.get('PPQY'),  # *区域匹配
                                 'projectAId': self.appText.get('projectAId'),  # *匹配楼盘A
                                 'phoneNum': self.appText.get('cluePhone'),
                                 'cluePhone': self.appText.get('cluePhone'),
                                 'clueNickName': callName,  # 称呼
                                 'sourceId': self.appText.get('sourceId'),
                                 'saasCode': XfpsaasCode,
                                 'sex': sex,  # 性别 0女 1 男
                                 'projectBId': projectBId,  # *匹配楼盘B
                                 'projectCId': projectCId,  # *匹配楼盘C
                                 'purchasePurposeLableIds': self.appText.get('GFMD'),  # 购房目的，
                                 'propertyAttributeLableIds': self.appText.get('WYSX'),  # 物业属性，
                                 'purchaseQualificationLableIds': self.appText.get('GFZZ'),  # 购房资质
                                 'theFirstLableIds': self.appText.get('SFSTF'),  # 是否首套
                                 'loanSituation': loanSituation,  # 贷款情况
                                 'paymentRatio': paymentRatio,  # 首付比例
                                 'paymentBudget': paymentBudget,  # 首付预算
                                 'apartmentLayout': apartmentLayout,  # 户型面积
                                 'customerDemandLableIds': self.appText.get('QTKHXQ')  # 客户需求
                             }
                         })

        self.appText.set_map('data', globals()['r.text']['data'])

    def ClientFormInfo(self):
        """客户需求详情"""
        self.PostRequest(url='/api/a/customer/form/info',
                         data={'clueId': self.appText.get('clueId')})

    def ClientList(self, customerLevel=None, customerMoney=None, lastFollowDay=None, vlue=0):
        """客户列表"""
        self.PostRequest(url='/api/a/customer/list',
                         data={
                             # 'lastFollowTime': lastFollowTime,  # 最近根进时间
                             'consultantId': self.appText.get('consultantId'),
                             # 'consultantPhone': XfpUser,
                             # 'deviceId': deviceId,
                             # 'projectId': None,
                             "taskStartTime": "",  # 开始时间
                             "taskEndTime": "",  # 结束时间
                             'customerLevel': customerLevel,  # 客户资质
                             'customerMoney': customerMoney,  # 客户资金
                             'lastFollowDay': lastFollowDay,  # 最近根进时间,int 类型
                             "customerAreaId": None,
                         })
        self.appText.set_map('total', globals()['r.text']['data']['total'])
        if globals()['r.text']['data']['total'] != 0:
            self.appText.set_map('customerId', globals()['r.text']['data']['records'][vlue]['customerId'])
            self.appText.set_map('clueId', globals()['r.text']['data']['records'][vlue]['clueId'])
            self.appText.set_map('taskCount', globals()['r.text']['data']['records'][vlue]['taskCount'])
            self.appText.set_map('orderNo', globals()['r.text']['data']['records'][vlue]['orderNo'])

    def ClientCallLog(self):
        """客户通话记录"""
        self.PostRequest(url='/api/a/customer/phone/list',
                         data={'clueId': self.appText.get('clueId')})

    def ClientAddThePlan(self):
        """客户添加计划"""
        self.PostRequest(url='/api/a/customer/plan/save',
                         data={})

    def SaveClientData(self):
        """保存客户信息"""
        self.PostRequest(url='/api/a/customer/save',
                         data={'clueId': self.appText.get('clueId')})

    def UploadFiles(self):
        """上传"""
        all_imgs = {}
        b = open('D:\\PycharmProjects\\XFJ\\Agent_Api\\imgs\\购房版APP-750x1334-0.png', 'rb')
        all_imgs['f1'] = ('购房版APP-750x1334-0.png', b, 'image/jpeg')
        requests.post(url=(ApiXfpUrl + '/api/b/systembase/uploadFiles'),
                      files=all_imgs)

    def add_deal_former(self, transFloorage=25, Status=0,
                        transHouseBuilding='2', transHouseUnit='1-1',
                        transOwnerName='潘师傅', transRemark='python-签约', transReservedTellphone='17600000000',
                        transTotalPrice='998888.56',isDeleted=None,
                        attachmentIds='12'):

        transYeji = random.randint(30000, 100000)
        """成交录入"""
        if Status == 0:
            transId = 0
        else:
            transId = self.appText.get('transId')
        self.PostRequest(url='/api/a/transaction/save',
                         data={'consultantId': self.appText.get('consultantId'),  # 咨询师ID
                               'transId': transId,  # 成交ID
                               'customerId': self.appText.get('customerId'),  # 客户ID
                               'clueId': self.appText.get('clueId'),  # 线索ID
                               'houseId': self.appText.get('houseId'),  # 楼盘ID
                               'transContractDate': time.strftime("%Y-%m-%d"),  # 成交日期
                               'transFloorage': transFloorage,  # 建筑面积
                               'transHouseBuilding': transHouseBuilding,  # 楼栋
                               'transHouseUnit': transHouseUnit,  # 房号
                               'transOwnerName': transOwnerName,  # 业主姓名
                               'transRemark': transRemark,  # 备注
                               'transReservedTellphone': transReservedTellphone,  # 电话
                               'transTotalPrice': transTotalPrice,  # 成交总价
                               'transType': self.appText.get('CJX'),  # 成交项
                               'transYeji': transYeji,  # 业绩
                               'isDeleted': isDeleted,  # 是否删除
                               'attachmentIds': attachmentIds})  # 附件
        self.appText.set_map('data', globals()['r.text']['data'])

    def add_deal(self, transFloorage=25, Status=0,
                        transHouseBuilding='2', transHouseUnit='1-1',
                        transOwnerName=None, transRemark='python-签约', transReservedTellphone=None,
                        transTotalPrice='998888.56',isDeleted=None,
                        transYeji=None,
                        attachmentIds='13'):
        if transYeji is None:
            transYeji = random.randint(20000, 100000)
        transTotalPrice = random.randint(200000, 20000000)
        """成交录入"""
        if Status == 0:
            transId = None
            visitDealId = None
        else:
            transId = self.appText.get('transId')
            visitDealId = self.appText.get('visitDealId')
        if transReservedTellphone is None:
            transReservedTellphone = '1' + str(int(time.time()))
        if transOwnerName is None:
            transOwnerName = self.RandomText(textArr=surname)
        self.PostRequest(url='/api/a/trans/save',
                         data={'consultantId': self.appText.get('consultantId'),  # 咨询师ID
                               'transId': transId,  # 成交ID
                               'customerId': self.appText.get('customerId'),  # 客户ID
                               'clueId': self.appText.get('clueId'),  # 线索ID
                               'houseId': self.appText.get('houseId'),  # 楼盘ID
                               'transContractDate': time.strftime("%Y-%m-%d"),  # 成交日期
                               'transFloorage': transFloorage,  # 建筑面积
                               'transHouseBuilding': transHouseBuilding,  # 楼栋
                               'transHouseUnit': transHouseUnit,  # 房号
                               'transOwnerName': transOwnerName,  # 业主姓名
                               'transRemark': transRemark,  # 备注
                               'transReservedTellphone': transReservedTellphone,  # 电话
                               'transTotalPrice': transTotalPrice,  # 成交总价
                               'transType': self.appText.get('CJX'),  # 成交项
                               'transYeji': transYeji,  # 业绩
                               # 'isDeleted': isDeleted,  # 是否删除
                               'attachmentIds': attachmentIds,
                               'applyRemark': '成交审核备注信息',
                               'transVisitDealForm': {
                                   'agencyId': self.appText.get('DLGS'),      # 代理公司
                                   'appointConsultant': self.appText.get('consultantId'),    # 邀请咨询师
                                   'attachmentIds': attachmentIds,            # 带看报备附件
                                   'receptionName': self.appText.get('JDRXM'),            # 接待人姓名
                                   'receptionPhone': self.appText.get('JDRDH'),          # 接待人电话
                                   'reportingRules': self.appText.get('BBGZ'),          # 报备规则
                                   'reward': self.appText.get('YJXJJ'),                          # 佣金现金奖
                                   'seeingConsultant': self.appText.get('consultantId'),      # 带看咨询师
                                   'settlementConditions': self.appText.get('JSTJ'),      # 结算条件
                                   'visitDealId': visitDealId,            # 成交带看报备ID
                                   'visitProjectId': self.appText.get('visitProjectId')       # 关联带看报备ID
                               }
                               })  # 附件
        self.appText.set_map('data', globals()['r.text']['data'])
        self.appText.set_map('transYeji', transYeji)
        self.appText.set_map('dealPhone', transReservedTellphone)

    def visitProject_list(self):
        """带看报备列表"""
        self.PostRequest(url='/api/a/visit/visitProject/list',
                         data={
                             "customerId": self.appText.get('customerId'),
                             "houseId": self.appText.get('houseId'),
                             "visitStatus": 1
                         })
        self.appText.set_map('web_total', len(globals()['r.text']['data']))
        if len(globals()['r.text']['data']) != 0:
            self.appText.set_map('visitProjectId', globals()['r.text']['data'][0]['visitProjectId'])
            dome = 0
            dome1 = 1
            if globals()['r.text']['data'][0]['houseBusinessInfo'] != None:
                while globals()['r.text']['data'][0]['houseBusinessInfo']['residentInfo'][dome:dome1] != '+':
                    dome = dome1
                    dome1 = dome1 + 1
                self.appText.set_map('DLGS', globals()['r.text']['data'][0]['houseBusinessInfo']['agencyId'])
                self.appText.set_map('BBGZ', globals()['r.text']['data'][0]['houseBusinessInfo']['reportingRules'])
                self.appText.set_map('JDRXM', globals()['r.text']['data'][0]['houseBusinessInfo']
                                              ['residentInfo'][0:dome])
                self.appText.set_map('JDRDH', globals()['r.text']['data'][0]['houseBusinessInfo']
                                              ['residentInfo'][dome1:])
                self.appText.set_map('YJXJJ', globals()['r.text']['data'][0]['houseBusinessInfo']['reward'])
                self.appText.set_map('JSTJ', globals()['r.text']['data'][0]
                ['houseBusinessInfo']['settlementConditions'])

    def deal_List(self, transStatus=None, ApplyStatus=None, keyWord=None, transProgressStatus=None):
        """成交列表"""
        self.PostRequest(url='/api/a/trans/list',
                         data={
                             'consultantId': self.appText.get('consultantId'),
                             'transApplyStatus': ApplyStatus,
                             'transProgressStatus': transProgressStatus,        # 成交项 1 认购 2 网签
                             'keyWord': keyWord
                         })
        self.appText.set_map('total', globals()['r.text']['data']['total'])
        if self.appText.get('total') != 0:
            if transStatus is not None:
                dome = 0
                while globals()['r.text']['data']['records'][dome] == transStatus:
                    dome = dome + 1
                    if dome == globals()['r.text']['data']['total']:
                        print('成交列表没有已确认的成交')
                        raise RuntimeError(self.appText.get('ApiXfpUrl'))
            else:
                dome = 0
            self.appText.set_map('transStatus', globals()['r.text']['data']['records'][dome]['transApplyStatus'])
            self.appText.set_map('clueId', globals()['r.text']['data']['records'][dome]['clueId'])

            self.appText.set_map('transId', globals()['r.text']['data']['records'][dome]['transId'])
            self.appText.set_map('customerId', globals()['r.text']['data']['records'][dome]['customerId'])
            self.appText.set_map('transOrderNo', globals()['r.text']['data']['records'][dome]['transOrderNo'])

    def deal_Info(self):
        """成交详情"""
        self.PostRequest(url='/api/a/transaction/info',
                         data={'transId': self.appText.get('transId')})

    def AllBuildingUpdate(self, keyWord=None):
        """全部楼盘"""
        self.PostRequest(url='/api/a/house/list',
                         data={
                             'keyWord': keyWord
                         })
        self.appText.set_map('total', globals()['r.text']['data']['total'])
        self.appText.set_map('records', globals()['r.text']['data']['records'])

    def BusinessInformation(self, keyWord=None):
        """商务信息"""
        self.PostRequest(url='/api/a/house/getHouseBusinessList',
                         data={
                             'keyWord': keyWord
                         })
        self.appText.set_map('total', globals()['r.text']['data']['total'])
        if self.appText.get('total') != 0:
            self.appText.set_map('houseName', globals()['r.text']['data']['records'][0]['houseName'])

    def Information(self, keyWord=None):
        """资料信息"""
        self.PostRequest(url='/api/a/house/getHouseInfoList',
                         data={
                             'keyWord': keyWord
                         })
        self.appText.set_map('total', globals()['r.text']['data']['total'])
        if self.appText.get('total') != 0:
            self.appText.set_map('houseName', globals()['r.text']['data']['records'][0]['houseName'])

    def HouseQA(self, keyWord=None):
        """楼盘QA"""
        self.PostRequest(url='/api/a/house/getHouseQuestionList',
                         data={
                             'keyWord': keyWord
                         })
        self.appText.set_map('total', globals()['r.text']['data']['total'])
        if self.appText.get('total') != 0:
            self.appText.set_map('houseName', globals()['r.text']['data']['records'][0]['houseName'])
            self.appText.set_map('title', globals()['r.text']['data']['records'][0]['title'])

    # def CustomerStatisticalInfo(self):
    #     """服务统计"""
    #     self.PostRequest(url='/api/a/customer/getCustomerStatisticalInfo',
    #                      data={
    #                          'consultantId': self.appText.get('consultantId')
    #                      })
    #
    # def ClientStatistics(self):
    #     """客户统计"""
    #     self.PostRequest(url='/api/a/customer/getCustomerStatistical',
    #                      data={
    #                          'consultantId': self.appText.get('consultantId')
    #                      })

    def follow_apply(self, vlue=0, keyWord=None):
        """跟进申请"""
        self.PostRequest(url='/api/a/audit/auditList',
                         data={
                             'consultantId': self.appText.get('consultantId'),
                             'keyWord': keyWord,
                         })
        self.appText.set_map('total', globals()['r.text']['data']['total'])
        if self.appText.get('total') != 0:
            self.appText.set_map('auditStatueStr', globals()['r.text']['data']['records'][vlue]['auditStatueStr'])
            self.appText.set_map('auditStatueApp', globals()['r.text']['data']['records'][vlue]['applyStatus'])
            self.appText.set_map('auditRemark', globals()['r.text']['data']['records'][vlue]['auditRemark'])
            self.appText.set_map('clueId', globals()['r.text']['data']['records'][vlue]['clueId'])

    def Task_Visit_List(self, appointmentTime=None,
                        startTime=time.strftime("%Y-%m-%d") + ' 00:00:00',
                        endTime=time.strftime("%Y-%m-%d") + ' 23:59:59',
                        visiteStatus=None):
        """我的带看"""
        self.PostRequest(url='/api/a/visit/list',
                         data={
                             'consultantIds': [self.appText.get('consultantId')],
                             'startTime': startTime,
                             'endTime': endTime,
                             'appVisitStatus': visiteStatus,
                         })
        self.appText.set_map('total', globals()['r.text']['data']['total'])
        if self.appText.get('total') != 0:
            a = 0
            if appointmentTime is not None:
                while globals()['r.text']['data']['records'][a]['appointmentTime'] != appointmentTime[:-3]:
                    a = a + 1
                    if a == self.appText.get('total'):
                        break
                try:
                    self.appText.set_map('auditRemark',
                                         globals()['r.text']['data']['records'][a]['auditRemark'])
                except:
                    self.appText.set_map('auditRemark',
                                         None)
                self.appText.set_map('visitAuditStatus',
                                     globals()['r.text']['data']['records'][a]['visitAuditStatus'])
                self.appText.set_map('visitAuditStatusName',
                                     globals()['r.text']['data']['records'][a]['visitAuditStatusName'])
                self.appText.set_map('visitStatus',
                                     globals()['r.text']['data']['records'][a]['visitStatus'])
                self.appText.set_map('visitStatusName',
                                     globals()['r.text']['data']['records'][a]['visitStatusName'])

    def my_Wealth(self):
        """我的财富值"""
        self.PostRequest(url='/api/a/wealth/getWealthDetailCount',
                         data={
                             'consultantId': self.appText.get('consultantId'),
                             'startTime': self.appText.get('start_date'),
                             'endTime': self.appText.get('end_date'),
                             'consultantIds': [self.appText.get('consultantId')]
                         })
        self.appText.set_map('monthWealth', globals()['r.text']['data']['monthWealth'])     # 当前财富值
        self.appText.set_map('monthConsumeWealth',
                             globals()['r.text']['data']['monthConsumeWealth'])  # 本月扣除
        self.appText.set_map('monthGetWealth', globals()['r.text']['data']['monthGetWealth'])   # 本月获得
        self.appText.set_map('lastMonthWealthDifference',
                             globals()['r.text']['data']['lastMonthWealthDifference'])   # 本月增减
        self.appText.set_map('monthGetClueConsumeWealth',
                             globals()['r.text']['data']['monthGetClueConsumeWealth'])   # 线索消耗
        self.appText.set_map('monthGetClueCount',
                             globals()['r.text']['data']['monthGetClueCount'])   # 兑换线索总数
        self.appText.set_map('monthNotClueWealth',
                             globals()['r.text']['data']['monthNotClueWealth'])     # 系统扣除

    def getWealthDetailList(self, startTime, endTime, orderNo=None, wealthType=None):
        """财富值明细"""
        self.PostRequest(url='/api/b/wealth/getWealthDetailList',
                         data={
                             'consultantId': self.appText.get('consultantId'),
                             'startTime': startTime,
                             'endTime': endTime,
                             'wealthType': wealthType,      # 类型
                             'orderNo': orderNo,
                             'consultantIds': [self.appText.get('consultantId')]
                         })
        self.appText.set_map('web_total', globals()['r.text']['data']['total'])
        if len(globals()['r.text']['data']['records']) != 0:
            self.appText.set_map('total', len(globals()['r.text']['data']['records']))
            self.appText.set_map('records', globals()['r.text']['data']['records'])
            self.appText.set_map('vlue1', int(globals()['r.text']['data']['records'][0]['wealthValue']))
            a = 0
            vlue = 0
            while a != self.appText.get('total'):
                vlue = vlue + int(globals()['r.text']['data']['records'][a]['wealthValue'])
                a = a + 1
            self.appText.set_map('vlue', vlue)
            self.appText.set_map('wealthValue', globals()['r.text']['data']['records'][0]['wealthValue'])
            self.appText.set_map('typeStr', globals()['r.text']['data']['records'][0]['typeStr'])
            self.appText.set_map('wealthId', globals()['r.text']['data']['records'][0]['wealthId'])
        else:
            self.appText.set_map('vlue', 0)

    def get_current_month_start_and_end(self, date):
        """
        年份 date(2017-09-08格式)
        :param date:
        :return:本月第一天日期和本月最后一天日期
        """
        if date.count('-') != 2:
            raise ValueError('- is error')
        year, month = str(date).split('-')[0], str(date).split('-')[1]
        end = calendar.monthrange(int(year), int(month))[1]
        start_date = '%s-%s-01' % (year, month)
        end_date = '%s-%s-%s' % (year, month, end)
        self.appText.set_map('start_date', start_date)
        self.appText.set_map('end_date', end_date)

    def phone_log(self, callee_num, call_time, is_own_call=1, is_me=1, talk_time=None, wait_time=None):
        """录音上传"""
        if is_me == 1:
            user = XfpUser
        else:
            user = XfpUser1
        r = requests.post(url=ApiXfpUrl1 + '/api/agent/phone_log',
                          data={
                              'login_phone': user,
                              'device_no': deviceId,
                              'is_own_call': is_own_call,   # 1呼出 0呼入
                              'callee_num': callee_num,
                              'saas_code': XfpsaasCode,
                              'call_time': call_time,       # 拨打|接听时间
                              'file_name': None,
                              'talk_time': talk_time,       # 通话时长
                              'wait_time': wait_time        # 等待时长
                          },
                          verify=False)
        r.raise_for_status()

    def getConsultantCount(self):
        """本月概况"""
        self.PostRequest(url='/api/a/consultant/getConsultantCount',
                         data={
                             'consultantId': self.appText.get('consultantId')
                         })
        self.appText.set_map('firstCallRatio', globals()['r.text']['data']['firstCallRatio'])   # 首电
        self.appText.set_map('followRatio', globals()['r.text']['data']['followRatio'])         # 跟进
        self.appText.set_map('visitRatio', globals()['r.text']['data']['visitRatio'])           # 上户
        self.appText.set_map('dealRatio', globals()['r.text']['data']['dealRatio'])             # 带看
        self.appText.set_map('newClueCount', globals()['r.text']['data']['newClueCount'])       # 上户总数
        self.appText.set_map('visitCount', globals()['r.text']['data']['visitCount'])           # 带看总数
        self.appText.set_map('dealCount', globals()['r.text']['data']['dealCount'])             # 成交总数
        self.appText.set_map('seaClueCount', globals()['r.text']['data']['seaClueCount'])       # 释放公海总数

    def time_add(self, second):
        if int(self.appText.get('createdTime')[-2:]) + second > 60:
            x = int(self.appText.get('createdTime')[-2:]) + second - 60
            y = int(self.appText.get('createdTime')[-5:-3]) + 1
            if int(self.appText.get('createdTime')[-5:-3]) + 1 > 60:
                y = int(self.appText.get('createdTime')[-5:-3]) + 1 - 60
                if int(self.appText.get('createdTime')[-8:-6]) + 1 > 24:
                    print('小时数超过24没写')
                    raise RuntimeError(self.appText.get('ApiXfpUrl'))
                else:
                    print('小时数未超过24没写')
                    raise RuntimeError(self.appText.get('ApiXfpUrl'))
            else:
                y = int(self.appText.get('createdTime')[-5:-3]) + 1
        else:
            x = int(self.appText.get('createdTime')[-2:]) + second

        self.appText.set_map('time_add', self.appText.get('createdTime')[:-5] + str(y) + ':' + str(x))

    def time_difference(self):
        """时间差"""
        from datetime import datetime, date
        dome = time.strftime("%Y-%m-%d %H:%M:%S")
        time_1_struct = datetime.strptime(self.appText.get('endTime'), "%Y-%m-%d %H:%M:%S")
        time_2_struct = datetime.strptime(dome, "%Y-%m-%d %H:%M:%S")
        if time_1_struct > time_2_struct:
            if dome[:10] == self.appText.get('endTime'):
                self.appText.set_map('vlue', (time_1_struct - time_2_struct).seconds/60/60)
            else:
                total_seconds = (time_1_struct - time_2_struct).total_seconds()
                self.appText.set_map('vlue', -(total_seconds)/60/60)
        elif time_1_struct < time_2_struct:
            if dome[:10] == self.appText.get('endTime'):
                self.appText.set_map('vlue', (time_2_struct - time_1_struct).seconds/60/60)
            else:
                total_seconds = (time_2_struct - time_1_struct).total_seconds()
                self.appText.set_map('vlue', (total_seconds)/60/60)

    def hone_wealth(self):
        """首页财富值"""
        today = datetime.date.today()
        oneday = datetime.timedelta(days=1)
        yesterday = today - oneday
        self.PostRequest(url='/api/a/consultant/getWealthDetailCount',
                         data={
                                "consultantId": self.appText.get('consultantId'),
                                "consultantIds": [
                                    self.appText.get('consultantId')
                                ],
                                "startTime": str(yesterday),
                                "endTime": time.strftime("%Y-%m-%d")
                            })
        self.appText.set_map('lastMonthWealth', globals()['r.text']['data']['lastMonthWealth'])
        self.appText.set_map('lastMonthWealthDifference',
                             globals()['r.text']['data']['lastMonthWealthDifference'])
        self.appText.set_map('monthWealth', globals()['r.text']['data']['monthWealth'])

    def client_info(self):
        """post请求"""
        self.PostRequest(url='/api/a/customer/info',
                         data={
                             'clueId': self.appText.get('clueId'),
                             'customerId': self.appText.get('customerId')
                         })
        if len(globals()['r.text']['data']) != 0:
            self.appText.set_map('cluePhone',
                                 globals()['r.text']['data']['saasClue']['cluePhone'])
            self.appText.set_map('orderNo',
                                 globals()['r.text']['data']['saasClue']['orderNo'])

    def ping_admin(self):
        """测试网站是否正常"""
        r = requests.get(url=ApiXfpUrl1)
        r.raise_for_status()

    def addWealthApply(self):
        """财富值申诉"""
        self.PostRequest(url='/api/b/wealthApply/addWealthApply',
                         data={
                                "applyContent": "python财富值申诉",
                                "wealthId": self.appText.get('wealthId'),
                                "clueId": self.appText.get('clueId'),
                                "orderNo": self.appText.get('orderNo'),

                            })

    def transProgress(self):
        """成交进度"""
        self.PostRequest(url='/api/a/trans/progress',
                         data={
                             'id': self.appText.get('transId')
                         })
        if len(globals()['r.text']['data']['nodes']) != 0:
            self.appText.set_map('directorAuditDesc', globals()['r.text']['data']['nodes'][0]['nodeLists'][0]['directorAuditDesc'])     # 总监
            self.appText.set_map('financialAuditDesc', globals()['r.text']['data']['nodes'][0]['nodeLists'][0]['financialAuditDesc'])   # 财务
            self.appText.set_map('managerAuditDesc', globals()['r.text']['data']['nodes'][0]['nodeLists'][0]['managerAuditDesc'])       # 经理

    def agoTime(self, days=60):
        """几天前的数据"""
        # import time
        import datetime

        # 先获得时间数组格式的日期
        threeDayAgo = (datetime.datetime.now() - datetime.timedelta(days=days))
        # 转换为时间戳
        timeStamp = int(time.mktime(threeDayAgo.timetuple()))
        # 转换为其他字符串格式
        otherStyleTime = threeDayAgo.strftime("%Y-%m-%d")
        self.appText.set_map('start_date', otherStyleTime)
        # print(time.strftime('%Y-%m-%d', LocalTime))

    def deal_statistics(self):
        """我的成交统计 60天的数据"""
        self.PostRequest(url='/api/a/trans/getMyDealAmountTotal',
                         data={

                         })
        self.appText.set_map('dealCount',
                             globals()['r.text']['data']['my60DealAmountTotal']['dealCount'])
        self.appText.set_map('totalAmount',
                             globals()['r.text']['data']['my60DealAmountTotal']['totalAmount'])

    def generateAuthCode(self):
        """获取授权码"""
        self.PostRequest(url='/api/tool/generateAuthCode',
                         data={
                             'consultantId': self.appText.get('consultantId')
                         })
        self.appText.set_map('code', globals()['r.text']['data']['code'])

    def ConsultantAuth(self,
                       consultantRealName='真实姓名',
                       consultantIdCard='身份证号码',
                       consultantIdCardImg1=None,
                       consultantIdCardImg2=None):
        """申请认证审核"""
        self.PostRequest(url='/api/a/consultantAuth/addConsultantAuthInfo',
                         data={
                             'consultantId': self.appText.get('consultantId'),
                             'consultantIdCard': consultantIdCard,
                             'consultantIdCardImg1': consultantIdCardImg1,
                             'consultantIdCardImg2': consultantIdCardImg2,
                             'consultantRealName': consultantRealName,
                         })

    def getConsultantAuthInfo(self):
        """个人认证详情"""
        self.PostRequest(url='/api/a/consultantAuth/getConsultantAuthInfo',
                         data={
                             'consultantId': self.appText.get('consultantId')

                         })

    def updateConsultantOnline(self, isOnline=1):
        """咨询师在线/离线"""
        self.PostRequest(url='/api/a/consultant/updateConsultantOnline',
                         data={
                             'isOnline': isOnline,      # 1在线  0 离线
                             'consultantId': self.appText.get('consultantId')
                         })

    def time_(self):
        """时间"""
        # 获取今天（现在时间）
        days = random.randint(1, 7)
        today = datetime.datetime.today()
        # 昨天
        yesterday = today - datetime.timedelta(days=days)
        # 明天
        tomorrow = today + datetime.timedelta(days=days)
        self.appText.set_map('yesterday', yesterday.strftime("%Y-%m-%d %H:%M:%S"))
        self.appText.set_map('tomorrow', tomorrow.strftime("%Y-%m-%d %H:%M:%S"))


if __name__ == '__main__':
    a = appApi()









