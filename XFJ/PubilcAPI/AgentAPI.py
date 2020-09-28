from XFJ.PubilcAPI.XfkApi import *
import requests


class AgentApi:
    def __init__(self):
        self.do_request = HandleRequest()
        self.to_request = self.do_request
        self.AgentTEXT = GlobalMap()

        self.Xfk = XfkApi()
        self.XfkRequest = self.Xfk
        self.XfkTEXT = GlobalMap()

    def GetRequest(self, url, data):
        """GET请求"""
        r = self.do_request.to_request(method="get",
                                       url=(ApiAgentUrl + url),
                                       data=data)
        r.raise_for_status()
        globals()['r.text'] = json.loads(r.text)
        self.AgentTEXT.set_map('text', globals()['r.text'])
        self.AgentTEXT.set_map('resultCode', globals()['r.text']['resultCode'])
        self.AgentTEXT.set_map('Agenturl', url)

    def PostRequest(self, url, data):
        """post请求"""
        r = self.do_request.to_request(method="post",
                                       url=(ApiAgentUrl + url),
                                       data=data)
        r.raise_for_status()
        globals()['r.text'] = json.loads(r.text)
        self.AgentTEXT.set_map('XFKtext', globals()['r.text'])
        self.AgentTEXT.set_map('XFKcontent', globals()['r.text']['content'])
        self.AgentTEXT.set_map('resultCode', globals()['r.text']['resultCode'])
        self.AgentTEXT.set_map('Agenturl', url)

    def LoginAgent(self, Uesr=AgentUesr, Pwd=AgentPwd):
        """登陆经纪人"""
        do_request = HandleRequest()
        r = do_request.to_request(method="post",
                                  url=(ApiLoninUrl + "/account.do?command=checkLogin"),
                                  data={"agentTel": Uesr,
                                        "agentLoginPassword": Pwd})
        r.raise_for_status()
        globals()['r.text'] = json.loads(r.text)
        globals()["token"] = globals()['r.text']['Extend']['agentToken']
        globals()["agentName"] = globals()['r.text']['Extend']['agentName']
        self.AgentTEXT.set_map('sellerCityId', globals()['r.text']['Extend']['sellerCityId'])
        self.AgentTEXT.set_map('sellerId', globals()['r.text']['Extend']['sellerId'])
        self.AgentTEXT.set_map('token', globals()['r.text']['Extend']['agentToken'])
        # globals()["token"] = globals()['r.text']['Extend']['agentToken']
        self.AgentTEXT.set_map('projectId', '178')

    def ForRegistrationID(self, type='local', keyword=ProjectName):
        """获取报名ID---新房列表"""
        self.GetRequest(url='/api/mobile/projectService/getProjectAllTypeList/7.2.5.json',
                        data={'cityId': cityId,
                              'tpye': type,
                              'token': globals()['token'],
                              'keyword': keyword})
        if type == 'local':
            a = 0
            globals()['tuanName'] = globals()['r.text']['extend'][a]['projectName']
            while ProjectName != globals()['tuanName']:
                a = a + 1
                # print(globals()['r.text']['extend'][a]['projectName'])
                globals()['tuanName'] = globals()['r.text']['extend'][a]['projectName']
            globals()['tuanId'] = globals()['r.text']['extend'][a]['tuanId']
            self.AgentTEXT.set_map('projectId', globals()['r.text']['extend'][a]['projectId'])
        else:
            globals()['tuanId'] = globals()['r.text']['extend'][0]['tuanId']
        print(self.AgentTEXT.get('projectId'))

    def NewHouseParticulars(self):
        """新房详情"""
        self.GetRequest(url='/api/mobile/projectService/getProjectDetailV6/7.2.0.json',
                        data={'token': globals()['token'],
                              'tuanId': globals()['tuanId']})
        self.AgentTEXT.set_map('extend', globals()['r.text']['extend'])

    def RecommendNew(self, phone=None):
        import time
        """报名新房"""
        phone1 = '1' + str(int(time.time()))
        self.AgentTEXT.set_map('ClientPhone', phone1)
        username = '用户' + phone1[-4:]
        self.AgentTEXT.set_map('ClientNeme', username)
        if phone == None:
            phone = phone1
        self.PostRequest(url=('/api/mobile/agentService/v4/apply/' +
                              globals()['tuanId'] + '/0/' +
                              globals()['token'] + '/7.2.0.json'),
                         data={'phone': phone,
                               'username': username})
        self.AgentTEXT.set_map('Agentcontent', globals()['r.text']['content'])

    def TheSoundOfHappinessOrTheVoiceOfTheCity(self, cityId=cityId):
        """幸福之声：0 /城市之声--默认"""
        self.GetRequest(url='/api/mobile/forumService/getForumThreads/ios/7.2.0.json',
                        data={'token': globals()['token'],
                              'cityId': cityId})
        globals()['threadId'] = globals()['r.text']['extend']['list'][0]['threadId']

    def TheSoundOfHappinessOrTheVoiceOfTheCityParticulars(self):
        """幸福之声/城市之声   详情"""
        self.GetRequest(url='/api/mobile/forumService/getThreadPosts.json',
                        data={'token': globals()['token'],
                              'threadId': globals()['threadId']})

    def WealthStory(self):
        """财富故事"""
        self.GetRequest(url='/api/mobile/newsService/getNewsList.json',
                        data={'token': globals()['token'],
                              'pageNum': '1',
                              'rowsDisplayed': '20'})
        globals()['newsId'] = globals()['r.text']['extend'][0]['newsId']

    def WealthStoryParticulars(self):
        """财富故事详情"""
        self.GetRequest(url='/api/mobile/newsService/getNewsDetail.json',
                        data={'token': globals()['token'],
                              'newsId': globals()['newsId']})

    def AdvertisingBy(self, value=0):
        """广告轮播图"""
        self.GetRequest(url='/api/mobile/newsService/getHomeAdvertisingV5.json',
                        data={'token': globals()['token'],
                              'cityId': cityId})
        globals()['newsId'] = globals()['r.text']['extend'][value]['Id']

    def AdvertisingForDetails(self):
        """广告轮播图详情"""
        self.GetRequest(url='/api/mobile/newsService/getNewsDetailWithoutTitle.json',
                        data={'newsId': globals()['newsId'],
                              'token': globals()['token']})

    def TheHeadlineForDetails(self):
        """头条详情"""
        self.GetRequest(url='/api/mobile/newsService/getNewsDetail.json',
                        data={'token': globals()['token'],
                              'newsId': globals()['pid']})

    def HappinessHeadlines(self, value=0):
        """幸福头条"""
        r = requests.get(url=PushUrl + '/interface.do?command=getPushWebNotificationsIndexV4',
                         params={'token': globals()['token'],
                                 'cityId': cityId,
                                 'pushSystem': 'xfj'})
        r.raise_for_status()
        globals()['r.text'] = json.loads(r.text)
        globals()['pid'] = globals()['r.text']['Extend']['List'][value]['pid']

    def KeywordNewHouse(self, keyword=ProjectName):
        """关键字搜索新房"""
        self.GetRequest(url='/api/mobile/indexV6/search/project/ios/7.2.0',
                        data={'token': globals()['token'],
                              'projectName': keyword})

    def HomeHouseList(self, cityId=cityId):
        """首页显示列表（财富故事/本地新房/全国旅居/海外地产/活动海报）"""
        self.GetRequest(url='/api/mobile/indexV6/getIndexInfoV6_1',
                        data={'token': globals()['token'],
                              'cityId': cityId})

    def TheCityData(self):
        """城市数据"""
        self.GetRequest(url='/api/mobile/projectService/getCityListV3',
                        data=None)

    def Activity(self):
        """活动"""
        r = requests.get(url=ApiAgentUrl + '/activity/sweepstakes/index/' + globals()['token'] + '/165.html',
                         params=None)
        r.raise_for_status()

    def HappySchool(self):
        """幸福学堂"""
        r = requests.get(url=ApiAgentUrl + '/happySchool/sweepstakes/happySchool/' + globals()['token'] + '/168.html',
                         params={'os': 'ios'})
        r.raise_for_status()

    def Client(self, status=None):
        """客户列表"""
        self.GetRequest(url='/api/mobile/agentCustomerService/getRecommendCustomerList',
                        data={'token': globals()['token'],
                              'osType': 'ios',
                              'version': '7.2.0',
                              'status': status})
        globals()['applyId'] = globals()['r.text']['extend']['list'][0]['applyId']
        self.AgentTEXT.set_map('applyId', globals()['r.text']['extend']['list'][0]['applyId'])

    def TheTaskOfIntegral(self):
        """任务积分"""
        self.GetRequest(url='/api/mobile/newsService/getPointsUnreadListV5',
                        data={'token': globals()['token']})

    def PersonalPayments(self):
        """个人收支"""
        r = requests.post(url=PushUrl + '/interface.do?command=getPushNotificationsListV5',
                          data={'alias': AgentUesr,
                                'pushSystem': 'xfj',
                                'token': globals()['token'],
                                'pushUnreadType': 'money',
                                'pageNum': '1',
                                'language': 'CHS',
                                'rowsDisplayed': '20'})
        r.raise_for_status()

    def SystemMessages(self):
        """系统消息"""
        r = requests.get(url=PushUrl + '/interface.do',
                         params={'command': 'getPushNotificationsListV5',
                                 'pushUnreadType': 'shuoshuo',
                                 'alias': AgentUesr,
                                 'token': globals()['token'],
                                 'language': 'CHS',
                                 'pageNum': '1',
                                 'rowsDisplayed': '20'})
        r.raise_for_status()

    def My_Integral(self):
        """我的"""
        self.GetRequest(url='/api/mobile/goldService/getMyGoldV7.json',
                        data={'agentUid': agentUid,
                              'agentToken': globals()['token'],
                              'token': globals()['token']})

    def PostBarComment(self, content):
        """贴吧评论"""
        self.PostRequest(url='/api/mobile/estateResourceService/addErpComment',
                         data={'token': globals()['token'],
                               'estateResourceId': globals()['estateResourceId'],
                               'postContent': content,
                               'language': 'CHS',
                               'postId': ''})

    def PostBarLike(self):
        """贴吧点赞"""
        self.GetRequest(url='/api/mobile/estateResourceService/updateErpLike',
                        data={'token': globals()['token'],
                              'estateResourceId': globals()['estateResourceId']})

    def CityPostBarList(self):
        """城市 贴吧列表"""
        self.GetRequest(url='/api/mobile/estateResourceService/getEstateResourceByCityId',
                        data={'token': globals()['token'],
                              'cityId': cityId,
                              })
        globals()['title'] = globals()['r.text'].json()['title']

    def MyPostBarList(self):
        """城市 贴吧列表"""
        self.GetRequest(url='/api/mobile/estateResourceService/getIndividualEstateResource',
                        data={'token': globals()['token'],
                              'cityId': cityId,
                              })
        globals()['content'] = globals()['r.text']['content']

    def AddPostBar(self, content='', resourceLabels=None, imgs=None):
        """新增帖子"""
        """content：帖子内容
            resourceLabels：帖子标签   交友,晒单,健身,娱乐
            imgs：图片开关"""
        a = 1
        all_imgs = {}
        if imgs is None:
            all_imgs = None
        else:
            imgs1 = imgs + int(1)
            while a != imgs1:
                b = 'f' + str(a)
                files = 'file' + str(a)
                b = open('D:\\PycharmProjects\\XFJ\\Agent_Api\\imgs\\购房版APP-750x1334-0.png', 'rb')
                all_imgs[files] = ('购房版APP-750x1334-0.png', b, 'image/jpeg')
                a = a + 1
        r = requests.post(url=ApiAgentUrl + '/api/mobile/estateResourceService/saveIndividualEstateResourceV2',
                          data={'token': globals()['token'],
                                'phoneType': 'ios',
                                'resourceContent': content,
                                'resourceCity': cityId,
                                'resourceLabels': resourceLabels},
                          files=all_imgs)
        r.raise_for_status()
        globals()['r.text'] = json.loads(r.text)
        self.AgentTEXT.set_map('content', globals()['r.text']['content'])

    def DelPostBar(self):
        """删除帖子"""
        self.MyPostBarList()
        while globals()['r.text']['extend']['list'] != []:
            globals()['resourceId'] = globals()['r.text']['extend']['list'][0]['resourceId']
            self.GetRequest(url='/api/mobile/estateResourceService/deleteIndividualEstateResource',
                            data={'token': globals()['token'],
                                  'resourceId': globals()['resourceId'],
                                  })
            self.MyPostBarList()

    def LookSeller(self, agentTel=AgentUser9):
        """查看所属公司"""
        self.GetRequest(url='/api/mobile/agentService/getApplyLeaveStatus',
                        data={'token': self.AgentTEXT.get('token'),
                              'agentTel': agentTel,
                              'version': 'V1',
                              'language': 'CHS'})
        if globals()['r.text']['resultCode'] == 1:
            self.AgentTEXT.set_map('SellerNo', globals()['r.text']['extend']['aSellerInfoVo']['sellerNo'])

    def GetSeller(self, phone=AgentUser1):
        """查询联盟商"""
        self.GetRequest(url='/api/mobile/agentService/getTeamInfo/V1',
                        data={'token': self.AgentTEXT.get('token'),
                              'phone': phone})
        if globals()['r.text']['resultCode'] == 1:
            self.AgentTEXT.set_map('SellerNo', globals()['r.text']['extend']['sellerNo'])

    def BindingSeller(self, phone):
        """绑定公司"""
        self.PostRequest(url='/api/mobile/agentService/applyJoinASeller',
                         data={'token': self.AgentTEXT.get('token'),
                               'phone': phone})

    def DddTeamInfo(self, phone):
        """添加团队C"""
        self.PostRequest(url='/api/mobile/agentService/addTeamInfo',
                         data={'token': self.AgentTEXT.get('token'),
                               'phone': phone})

    def RelieveSeller(self, phone=AgentUser9):
        """解除绑定公司"""
        self.PostRequest(url='/api/mobile/agentService/applyLeaveASeller.json',
                         data={'phone': phone,
                               'token': self.AgentTEXT.get('token')})

    def updateSellerConfig(self, configKey='1'):
        """更新联盟商加入和退出团队配置"""
        self.PostRequest(url='/api/mobile/agentService/updateSellerJoinAndLeaveVerificationConfig',
                         data={
                             'token': self.AgentTEXT.get('token'),
                             'configKey': configKey
                         })

    def agreeSellerAgentApply(self, joinOrLeave=1):
        """ 同意经纪人申请加入或退出团队"""
        self.PostRequest(url='/api/mobile/agentService/agreeSellerAgentApply',
                         data={
                             'token': globals()['token'],
                             'applyId': self.AgentTEXT.get('applyId'),      # 申请Id
                             'joinOrLeave': joinOrLeave             # 1.申请加入 2.申请退出
                         })

    def refuseSellerAgentApply(self, joinOrLeave=1):
        """ 拒绝经纪人申请加入或退出团队"""
        self.PostRequest(url='/api/mobile/agentService/refuseSellerAgentApply',
                         data={
                             'token': globals()['token'],
                             'applyId': self.AgentTEXT.get('applyId'),      # 申请Id
                             'joinOrLeave': joinOrLeave             # 1.拒绝加入 2.拒绝退出
                         })

    def SellerAgentApplyList(self, processingStatus=1):
        """ 获取经纪人申请加入和退出团队审核列表"""
        self.PostRequest(url='/api/mobile/agentService/getSellerAgentApplyList',
                         data={
                                 'token': globals()['token'],
                                 'pageNumber': 1,
                                 'pageSize': 999,
                                 'processingStatus': processingStatus       # 申请状态 1.待处理验证 2，已处理验证
                             })
        if len(globals()['r.text']['extend']['list']) != 0:
            self.AgentTEXT.set_map('applyId', globals()['r.text']['extend']['list'][0]['applyId'])
        else:
            self.AgentTEXT.set_map('appkyId', '')
        # try:
        #     self.AgentTEXT.set_map('applyId', globals()['r.text']['extend'][0]['applyId'])
        # except BaseException as e:
        #     print("错误，错误原因：%s" % e)
        #     self.AgentTEXT.set_map('appkyId', '')
        #     print(self.AgentTEXT.get('Agenturl'))
        #     # raise RuntimeError(self.AgentTEXT.get('Agenturl'))

    def getSellerJoinAndLeaveVerificationConfig(self, value=0):
        """获取联盟商加入和退出团队配置"""
        self.PostRequest(
            url='/api/mobile/agentService/getSellerJoinAndLeaveVerificationConfig',
            data={
                'token': self.AgentTEXT.get('token')
            })
        self.AgentTEXT.set_map('isCheck', globals()['r.text']['extend']['configDetail'][value]['isCheck'])


if __name__ == '__main__':
    a = AgentApi()


