# -*- coding: utf-8 -*-
# @Time    : 2020/3/9 11:54
# @Author  : 潘师傅
# @File    : XfpApi.py
import requests
import json
from XFP.GlobalMap import GlobalMap
from XFP.Config.Conifg import *
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

    def PostRequest(self, url, data, header=None, Status=1, files=None):
        """post请求"""
        if header is not None:
            r = requests.post(url=(ApiXfpUrl + url),
                              data=json.dumps(data, ensure_ascii=False),
                              headers={
                                  'Content-Type': 'application/json'

                              })
        else:
            data1 = {"page": {
                'size': '50',
                'current': '1'
            },
                "saasCode": XfpsaasCode,
                "saasCodeSys": XfpsaasCode}
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
        time.sleep(0.2)
        if Status == 1:
            try:
                assert "成功", globals()['r.text']['masg']
            except BaseException as e:
                print("断言错误，错误原因：%s" % e)
                raise RuntimeError(self.appText.get('URL'))

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

    def Login(self, userName=XfpUser, password=XfpPwd):
        """登录"""
        self.PostRequest(url='/api/auth/login',
                         data={"userName": userName,
                               'saasCode': XfpsaasCode,
                               # 'deviceId': deviceId,
                               "password": password},
                         header=1)
        if self.appText.get('msg') == '成功':
            self.appText.set_map('user_token', globals()['XfpText']['data']['token'])

            self.appText.set_map('userId', globals()['XfpText']['data']['userDetail']['id'])
        else:
            self.appText.set_map('data', globals()['XfpText']['data'])

    def GetUserData(self):
        """获取咨询师信息"""
        self.PostRequest(url='/api/a/consultant/info',
                         data={'deviceId': deviceId})
        if self.appText.get('msg') != '禁止访问':
            self.appText.set_map('consultantId', globals()['r.text']['data']['consultantId'])
            self.appText.set_map('consultantName', globals()['r.text']['data']['consultantName'])
            self.appText.set_map('consultantLabels', globals()['r.text']['data']['consultantLabels'])

    def GetUserAgenda(self, endTime, taskType=None, keyWord=None):
        """获取用户待办"""
        self.PostRequest(url='/api/a/clue/task/list',
                         data={
                             'consultantId': self.appText.get('consultantId'),
                             "deviceId": deviceId,
                             "taskType": taskType,  # 0 超时1 线索 2 联系 3带看
                             "isCompleted": 0,
                             "isStop": 0,
                             "endTime": endTime,
                             "overtime": 0,
                             'keyWord': keyWord
                         })
        self.appText.set_map('pages', globals()['r.text']['data']['pages'])

    def CluePhoneLog(self):
        """线索通话记录"""
        self.PostRequest(url='/api/a/clue/phonelog/list',
                         data={'clueId': self.appText.get('Clue')})

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
                             'userLabelType': userLabelType,
                         })
        if globals()['r.text']['data']['total'] != 0:
            self.appText.set_map('labelData', globals()['r.text']['data']['records'][value]['userLabelValue'])

        self.appText.set_map('total', globals()['r.text']['data']['total'])

    def AddUserLabel(self, userLabelValue='线索标签', userLabelType='线索标签'):
        """新增标签"""
        self.PostRequest(url='/api/label/addOrUpdateUserLabel',
                         data={
                             'userLabelValue': userLabelValue,
                             'userLabelType': userLabelType,
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

    def GetTodayDo(self):
        """今日待办"""
        self.PostRequest(url='/api/a/clue/task/list',
                         data={"consultantId": self.appText.get('consultantId'),
                               # "clueId": self.appText.get('clueId'),
                               "isCompleted": 0,
                               "isStop": 0})
        # assert '线索跟进', globals()['r.text']['data']['records'][0]['taskTitle']
        self.appText.set_map('endTimeStr', globals()['r.text']['data']['records'][0]['endTimeStr'])

    def ClaimClue(self):
        """认领线索"""
        self.PostRequest(url='/api/a/clue/claim',
                         data={'clueId': self.appText.get('clueId')})

    def ClueFollowList(self, value=0, followType=None):
        """查询线索跟进列表"""
        self.PostRequest(url='/api/a/clue/follow/list',
                         data={'clueId': self.appText.get('clueId'),
                               'followType': followType})

        # if globals()['r.text']['data']['total'] != 0:
        self.appText.set_map('followContent',
                             globals()['r.text']['data']['records'][value]['followContent'])
        self.appText.set_map('followId', globals()['r.text']['data']['records'][value]['followId'])
        self.appText.set_map('taskId', globals()['r.text']['data']['records'][value]['taskId'])

    def ClueList(self, keyWord=''):
        """查询线索列表"""
        self.PostRequest(url='/api/a/clue/task/list',
                         data={"keyWord": keyWord,
                               "isCompleted": 0,
                               "isStop": 0,
                               "overtime": 0})

    def ClueFollowSave(self, taskEndTime, followType='线索', followContent='python-线索/客户跟进，本次沟通记录',
                       taskRemark='python-线索/客户跟进，下次沟通记录'):
        """线索/客户跟进录入"""
        if followType == '线索':
            followType = '1'
            taskType = '1'
            self.appText.set_map('customerId', 'null')
        else:
            followType = '3'
            taskType = '2'
        self.PostRequest(url='/api/a/clue/saveFollow',
                         data={
                             'clueId': self.appText.get('clueId'),
                             'followContent': followContent,
                             'customerId': self.appText.get('customerId'),
                             'followType': followType,
                             'taskType': taskType,
                             'taskRemark': taskRemark,
                             'taskId': self.appText.get('taskId'),
                             'followId': self.appText.get('followId'),
                             'endTime': taskEndTime,
                             'taskEndTime': taskEndTime
                         })

    def TodayClue(self, keyWord):
        """今日线索"""
        self.PostRequest(url='/api/a/clue/list',
                         data={'keyWord': keyWord})
        self.appText.set_map('Total', globals()['r.text']['data']['total'])
        if self.appText.get('Total') != 0:
            self.appText.set_map('isFirst', globals()['r.text']['data']['records'][0]['isFirst'])

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

    def ClueInfo(self, ):
        """线索详情"""
        self.PostRequest(url='/api/a/clue/info',
                         data={'clueId': self.appText.get('clueId')})
        self.appText.set_map('cluePhone', globals()['r.text']['data']['cluePhone'])

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
                             'sourceId': sourceId})  # 来源
        if globals()['r.text']['msg'] == '成功':
            self.appText.set_map('clueId', globals()['r.text']['data']['clueId'])
            self.appText.set_map('cluePhone', cluePhone)

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

    def ClueTaskSave(self):
        """线索待办录入"""
        self.PostRequest(url='/api/a/clue/task/save',
                         data={})

    def ClientFollowList(self, value=0, followType=None):
        """客户跟进记录"""
        self.PostRequest(url='/api/a/customer/follow/list',
                         data={'clueId': self.appText.get('clueId'),
                               'followType': followType,
                               'customerId': self.appText.get('customerId')
                               })
        self.appText.set_map('followContent',
                             globals()['r.text']['data']['records'][value]['followContent'])
        self.appText.set_map('followId', globals()['r.text']['data']['records'][value]['followId'])
        self.appText.set_map('taskId', globals()['r.text']['data']['records'][value]['taskId'])

    def ClientFolloow(self):
        """客户跟进"""
        self.PostRequest(url='/api/a/customer/follow/save',
                         data={'clueId': self.appText.get('clueId')})

    def ClientTask(self, taskTypeStr='带看行程'):
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
                if globals()['r.text']['data'][vlue]['taskTypeStr'] == taskTypeStr:
                    break
                vlue = vlue + 1
                if vlue == len(globals()['r.text']['data']):
                    vlue = 0
                    break
            self.appText.set_map('taskTypeStr', globals()['r.text']['data'][vlue]['taskTypeStr'])
            self.appText.set_map('taskRemark', globals()['r.text']['data'][vlue]['taskRemark'])
            self.appText.set_map('visitId', globals()['r.text']['data'][vlue]['visitId'])
            self.appText.set_map('taskId', globals()['r.text']['data'][vlue]['taskId'])

    def ClientVisitAdd(self, projectAId, appointmentTime=time.strftime("%Y-%m-%d ") + '22:00:00',
                       projectBId=None, projectCId=None):
        """新增带看计划"""
        self.PostRequest(url='/api/a/customer/visit/add',
                         data={
                             'clueId': self.appText.get('clueId'),
                             'customerId': self.appText.get('customerId'),
                             'seeingPeople': self.appText.get('consultantId'),  # 带看人
                             'appointmentTime': appointmentTime,
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
                             'appointmentTime': time.strftime("%Y-%m-%d ") + '22:00:00',
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

    def VisitFlow1(self, beforeTakingA='python-客户情况', beforeTakingB='python-核心诉求',
                   beforeTakingC='python-核心坑性', beforeTakingD='python-应对方案'):
        """带看前反馈 | 报备核实 | 约见签到"""
        self.PostRequest(url='/api/a/customer/visit/feedback/addOrUpd',
                         data={
                             'beforeTakingA': beforeTakingA,
                             'beforeTakingB': beforeTakingB,
                             'beforeTakingC': beforeTakingC,
                             'beforeTakingD': beforeTakingD,
                             'visitId': self.appText.get('visitId'),
                             'clueId': self.appText.get('clueId')
                         })

        self.PostRequest(url='/api/a/customer/visit/feedback/reportVerification',
                         data={
                             'visitId': self.appText.get('visitId'),
                             'clueId': self.appText.get('clueId'),
                             'reportVerification': 1
                         })

        self.PostRequest(url='/api/a/customer/visit/signIn',
                         data={
                             'saasLocale': {
                                 "localeCoordinates": "113.58856964111328,22.2489070892334",
                                 "localeName": "广东省珠海市香洲区吉大街道九洲大道东1104号"
                             },
                             'visitId': self.appText.get('visitId'),
                             'consultantId': self.appText.get('consultantId')
                         })

    def visit_info(self):
        """带看行程详情"""
        self.PostRequest(url='/api/a/customer/visit/info',
                         data={
                             'taskId': self.appText.get('taskId')
                         })
        self.appText.set_map('visitId', globals()['r.text']['data']['saasClueVisit']['visitId'])

    def OverVisit(self):
        """提前结束带看"""
        self.PostRequest(url='/api/a/customer/visit/over',
                         data={
                             'visitId': self.appText.get('visitId'),
                             'taskId': self.appText.get('taskId'),
                             'clueId': self.appText.get('clueId')
                         })

    def DelVisit(self):
        """删除带看"""
        self.PostRequest(url='/api/a/customer/visit/del',
                         data={
                             'clueId': self.appText.get('clueId'),
                             'visitId': self.appText.get('visitId'),
                             'taskId': self.appText.get('taskId')
                         })

    def ClientTaskPause(self, contactPurpose='python-申请暂停跟进'):
        """申请暂停跟进"""
        self.PostRequest(url='/api/a/customer/task/pause',
                         data={
                             'clueId': self.appText.get('clueId'),
                             'labelId': self.appText.get('labelId'),
                             'endTime': time.strftime("%Y-%m-%d ") + '22:00:00',
                             'customerId': self.appText.get('customerId'),
                             'consultantId': self.appText.get('consultantId'),
                             'labelName': self.appText.get('labelName'),
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

    def ExileSea(self, labelId, remark='python-线索释放公海'):
        """流放公海"""
        self.PostRequest(url='/api/a/clue/exileSea',
                         data={'clueId': self.appText.get('clueId'),
                               'remark': remark,
                               'labelName': self.appText.get('labelName'),
                               'labelId': labelId})

    def client_exile_sea(self, labelId, remark='python-客户释放公海'):
        """客户流放公海"""
        self.PostRequest(url='/api/a/customer/task/delete',
                         data={
                             'customerId': self.appText.get('customerId'),
                             'clueId': self.appText.get('clueId'),
                             'labelId': labelId,
                             'consultantId': self.appText.get('consultantId'),
                             'saasClueFollow': {
                                 'customerId': self.appText.get('customerId'),
                                 'followContent': remark,
                                 'clueId': self.appText.get('clueId')
                             }
                         })

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
                keyWord=None):
        """公海列表"""
        self.PostRequest(url='/api/a/clue/sea/getSeaClueList',
                         data={'keyWord': keyWord,
                               'seaType': seaType,
                               'sourceId': sourceId})
        self.appText.set_map('total', globals()['r.text']['data']['total'])
        if globals()['r.text']['data']['total'] != 0:
            self.appText.set_map('clueNickName', globals()['r.text']['data']['records'][0]['clueNickName'])
            self.appText.set_map('cluePhone', globals()['r.text']['data']['records'][0]['cluePhone'])
            self.appText.set_map('clueId', globals()['r.text']['data']['records'][0]['clueId'])

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

    def my_clue_list(self, vlue=0):
        """我的线索"""
        self.PostRequest(url='/api/a/clue/MyClueList',
                         data={
                             'myClue': 'Y',
                             'consultantId': self.appText.get('consultantId'),
                             'isWork': True,
                         })

        if globals()['r.text']['data']['total'] != 0:
            vlue = vlue + 1
            self.appText.set_map('clueId',
                                 globals()['r.text']['data']['records'][len(globals()['r.text']['data']['records']) - vlue]['clueId'])
            self.appText.set_map('cluePhone',
                                 globals()['r.text']['data']['records'][len(globals()['r.text']['data']['records']) - vlue]['cluePhone'])
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
        if globals()['r.text']['data']['current'] != 0:
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

    def GetLabelList(self, labelNo, labelName=None):
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
                         data={'labelNo': labelNo})
        if len(globals()['r.text']['data']) != 0:
            try:
                if labelName is not None:
                    a = 0
                    while labelName != globals()['r.text']['data'][0]['children'][a]['labelName']:
                        a = a + 1
                        if a == len((globals()['r.text']['data'][0]['children'])):  # 看看有多少个标签
                            break
                    self.appText.set_map('labelId', globals()['r.text']['data'][0]['children'][a]['labelId'])
                    self.appText.set_map('labelName', globals()['r.text']['data'][0]['children'][a]['labelName'])
                    self.appText.set_map('labelNo', globals()['r.text']['data'][0]['children'][a]['labelNo'])
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
        self.PostRequest(url='/api/tool/getAreaHouse',
                         data={})
        self.appText.set_map('total', len(globals()['r.text']['data']))
        if len(globals()['r.text']['data']) != 0:
            self.appText.set_map('houseId', globals()['r.text']['data'][value]['value'])

    def ClientEntering(self, callName=None, sex=1, GFYX=0, ZJZZ=0, GFMD=0, WYSX=0,
                       GFZZ=0, SFST=0, KHXQ=0, PPQY=0,
                       PPLP=1, projectBId=0, projectCId=0, loanSituation='', paymentRatio='',
                       paymentBudget='', apartmentLayout=''):
        """录入需求"""
        self.GetLabelList(labelNo='KHYXDJ')  # 查询购房意向loanSituation
        intentionLevelLableId = globals()['r.text']['data'][0]['children'][GFYX]['labelId']
        self.GetLabelList(labelNo='ZJZZ')  # 查询资金资质
        capitalQualificationLableId = globals()['r.text']['data'][0]['children'][ZJZZ]['labelId']
        self.GetLabelList(labelNo='GFMD')  # 查询购房目的
        purchasePurposeLableIds = globals()['r.text']['data'][0]['children'][GFMD]['labelId']
        self.GetLabelList(labelNo='WYSX')  # 查询物业属性
        propertyAttributeLableIds = globals()['r.text']['data'][0]['children'][WYSX]['labelId']
        self.GetLabelList(labelNo='GFZZ')  # 查询购房资质
        purchaseQualificationLableIds = globals()['r.text']['data'][0]['children'][GFZZ]['labelId']
        self.GetLabelList(labelNo='SFSTF')  # 查询是否首套
        theFirstLableIds = globals()['r.text']['data'][0]['children'][SFST]['labelId']
        self.GetMatchingArea()  # 查询匹配区域
        if PPQY != '':
            areaId = globals()['r.text']['data']['data'][0]['val'][0]['children'][0]['value']
        else:
            areaId = 0
        self.GetMatchingAreaHouse()  # 匹配楼盘
        if PPLP != '':
            projectAId = globals()['r.text']['data'][0]['value']
            projectBId = globals()['r.text']['data'][1]['value']
            projectCId = globals()['r.text']['data'][2]['value']
        else:
            projectAId = 0
        self.GetLabelList(labelNo='QTKHXQ')  # 查询客户需求
        customerDemandLableIds = globals()['r.text']['data'][0]['children'][KHXQ]['labelId']
        self.PostRequest(url='/api/a/customer/form/add',
                         data={
                             'clueId': self.appText.get('clueId'),
                             'intentionLevelLableId': intentionLevelLableId,  # *购房意向
                             'capitalQualificationLableId': capitalQualificationLableId,  # *资金资质
                             'areaId': areaId,  # *区域匹配
                             'projectAId': projectAId,  # *匹配楼盘A
                             'phoneNum': self.appText.get('cluePhone'),

                             'clueNickName': callName,  # 称呼
                             'sex': sex,  # 性别 0女 1 男
                             'projectBId': projectBId,  # *匹配楼盘B
                             'projectCId': projectCId,  # *匹配楼盘C
                             'purchasePurposeLableIds': purchasePurposeLableIds,  # 购房目的，
                             'propertyAttributeLableIds': propertyAttributeLableIds,  # 物业属性，
                             'purchaseQualificationLableIds': purchaseQualificationLableIds,  # 购房资质
                             'theFirstLableIds': theFirstLableIds,  # 是否首套
                             'loanSituation': loanSituation,  # 贷款情况

                             'paymentRatio': paymentRatio,  # 首付比例
                             'paymentBudget': paymentBudget,  # 首付预算
                             'apartmentLayout': apartmentLayout,  # 户型面积
                             'customerDemandLableIds': customerDemandLableIds  # 客户需求
                         })

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
            self.appText.set_map('clueId', globals()['r.text']['data']['records'][vlue]['clueId'])
            self.appText.set_map('taskCount', globals()['r.text']['data']['records'][vlue]['taskCount'])

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

    def TransactionSave(self, transFloorage=25, Status=0,
                        transHouseBuilding='2', transHouseUnit='1-1',
                        transOwnerName='潘师傅', transRemark='python-签约', transReservedTellphone='17600000000',
                        transTotalPrice='998888.56',
                        transYeji='88.88',
                        attachmentIds='12'):
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
                               'transType': self.appText.get('labelId'),  # 成交项
                               'transYeji': transYeji,  # 业绩
                               'attachmentIds': attachmentIds})  # 附件
        self.appText.set_map('data', globals()['r.text']['data'])

    def TransactionList(self):
        """成交列表"""
        self.PostRequest(url='/api/a/transaction/list',
                         data={})
        self.appText.set_map('total', globals()['r.text']['data']['total'])
        if self.appText.get('total') != 0:
            self.appText.set_map('transStatus', globals()['r.text']['data']['records'][0]['transStatus'])

    def TransactionInfo(self):
        """成交详情"""
        self.PostRequest(url='/api/a/transaction/info',
                         data={'transId': self.appText.get('transId')})

    def AllBuildingUpdate(self, keyWord=None):
        """全部楼盘"""
        self.PostRequest(url='/api/a/house/getHouseList',
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

    def CustomerStatisticalInfo(self):
        """服务统计"""
        self.PostRequest(url='/api/a/customer/getCustomerStatisticalInfo',
                         data={
                             'consultantId': self.appText.get('consultantId')
                         })

    def ClientStatistics(self):
        """客户统计"""
        self.PostRequest(url='/api/a/customer/getCustomerStatistical',
                         data={
                             'consultantId': self.appText.get('consultantId')
                         })

    def audit_List(self):
        """跟进申请"""
        self.PostRequest(url='/api/a/audit/auditList',
                         data={
                             'consultantId': self.appText.get('consultantId')
                         })
        self.appText.set_map('total', globals()['r.text']['data']['total'])
        if self.appText.get('total') != 0:
            self.appText.set_map('auditStatueStr', globals()['r.text']['data']['records'][0]['auditStatueStr'])
            self.appText.set_map('auditStatue', globals()['r.text']['data']['records'][0]['auditStatue'])
            self.appText.set_map('auditRemark', globals()['r.text']['data']['records'][0]['auditRemark'])

    def Task_Visit_List(self, appointmentTime):
        """我的带看"""
        self.PostRequest(url='/api/a/consultant/getTaskVisitList',
                         data={
                             'consultantId': self.appText.get('consultantId'),
                             'startTime': time.strftime("%Y-%m-%d"),
                             'endTime': time.strftime("%Y-%m-%d")
                         })
        self.appText.set_map('total', globals()['r.text']['data']['total'])
        if self.appText.get('total') != 0:
            a = 0
            while globals()['r.text']['data']['records'][a]['appointmentTime'] != appointmentTime:
                a = a + 1
                if a == self.appText.get('total'):
                    break
            self.appText.set_map('auditRemark', globals()['r.text']['data']['records'][a]['auditRemark'])
            self.appText.set_map('visiteStatusStr', globals()['r.text']['data']['records'][a]['visiteStatusStr'])
            self.appText.set_map('visiteStatus', globals()['r.text']['data']['records'][a]['visiteStatus'])

    def my_Wealth(self):
        """我的财富值"""
        self.get_current_month_start_and_end(date=time.strftime("%Y-%m-%d"))
        self.PostRequest(url='/api/a/wealth/getWealthDetailCount',
                         data={
                             'consultantId': self.appText.get('consultantId'),
                             'startTime': self.appText.get('start_date'),
                             'endTime': self.appText.get('end_date'),
                             'consultantIds': [self.appText.get('consultantId')]
                         })
        self.appText.set_map('monthWealth', globals()['r.text']['data']['monthWealth'])     # 当前财富值
        self.appText.set_map('monthConsumeWealth', globals()['r.text']['data']['monthConsumeWealth'])  # 本月扣除
        self.appText.set_map('monthGetWealth', globals()['r.text']['data']['monthGetWealth'])   # 本月获得

    def getWealthDetailList(self):
        """财富值明细"""
        self.PostRequest(url='/api/b/wealth/getWealthDetailList',
                         data={
                             'consultantId': self.appText.get('consultantId'),
                             'startTime': self.appText.get('start_date'),
                             'endTime': self.appText.get('end_date'),
                             'consultantIds': [self.appText.get('consultantId')]
                         })
        self.appText.set_map('wealthValue', globals()['r.text']['data']['records'][0]['wealthValue'])
        self.appText.set_map('typeStr', globals()['r.text']['data']['records'][0]['typeStr'])
        self.appText.set_map('wealthId', globals()['r.text']['data']['records'][0]['wealthId'])

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


if __name__ == '__main__':
    a = appApi()
