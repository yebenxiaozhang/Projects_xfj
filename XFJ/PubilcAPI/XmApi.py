from XFJ.PubilcMethod.HandleRequest import HandleRequest
from XFJ.Config.Conifg import *
from XFJ.PubilcAPI.AgentAPI import *
import requests
import json
import time
import random
import re
# import XFJ.globalvar as
from XFJ.GlobalMap import GlobalMap
from XFJ.PubilcAPI.FlowPath import *

class XmApi:
    def __init__(self):
        self.do_request = HandleRequest()
        self.to_request = self.do_request
        self.XMtext = GlobalMap()

        self.Agent_request = AgentApi()
        self.AgentRequest = self.Agent_request
        self.AgentTEXT = GlobalMap()

        self.XFK_request = XfkApi()
        self.XfkRequest = self.XFK_request
        self.XFKTEXT = GlobalMap()

    #
    # def judge(self):
    #     """判断环境索要读取的元素"""
    #     if ApiXmUrl == 'http://api.xfj100.com':
    #         cityId

    def ApiLogin(self):
        do_request = HandleRequest()
        r = do_request.to_request(method="post",
                                  url=(ApiLoninUrl + "/account.do?command=checkLogin"),
                                  data={"agentTel": XmUser,
                                        "agentLoginPassword": XmPwd})
        r.raise_for_status()
        globals()['r.text'] = json.loads(r.text)
        globals()["token"] = globals()['r.text']['Extend']['agentToken']
        globals()["agentName"] = globals()['r.text']['Extend']['agentName']

    def InquireRegularMembers(self):
        """查询普通会员"""
        self.GetRequest(url="/api/mobile/secretarySellerService/getSellerAgentList.json",
                        data={"agentToken": globals()["token"]})

    def VerbalTrickList(self, label, content):
        """话术列表"""
        self.GetRequest(url="/api/mobile/secretaryService/getMyChatTemplateList",
                        data={"agentToken": globals()["token"],
                              "label": label})
        globals()['a'] = 0
        while globals()['r.text']['extend'][globals()['a']]['createUser'] == -1:
            if globals()['a'] == 16:
                break
            else:
                globals()['a'] = globals()['a'] + 1
        if content is not None:
            assert globals()['r.text']['extend'][globals()['a']]['followTemplate'] == content, \
                print(globals()['r.text']['extend'][globals()['a']]['followTemplate'], content)
            globals()['followTemplateId'] = globals()['r.text']['extend'][globals()['a']]['followTemplateId']
        else:
            pass

    def AddVerbalTrick(self, content, label):
        """新增话术"""
        """label:上班#拓展联盟商#案场跟进#回访联盟商#踩盘#下班#联盟商培训#"""
        self.PostRequest(url="/api/mobile/secretaryService/saveMyChatTemplate",
                         data={"agentToken": globals()['token'],
                               "content": content,
                               "label": label})

    def AlterVerbalTrick(self, label, content):
        """修改话术"""
        self.PostRequest(url="/api/mobile/secretaryService/updateMyChatTemplate",
                         data={"agentToken": globals()['token'],
                               "templateId": globals()['followTemplateId'],
                               "label": label,
                               "content": content})

    def DelVerbalTrick(self):
        """删除话术"""
        self.VerbalTrickList(label=None, content=None)
        while globals()['a'] != 16:
            globals()['followTemplateId'] = globals()['r.text']['extend'][globals()["a"]]['followTemplateId']
            self.PostRequest(url="/api/mobile/secretaryService/delMyChatTemplate",
                             data={"agentToken": globals()['token'],
                                   "templateId": globals()['followTemplateId']})
            assert globals()['r.text']['content'] == "操作成功！"
            self.VerbalTrickList(label=None, content=None)

    def The_receivable_queries(self):
        """回款查询"""
        self.GetRequest(url="/api/mobile/secretarySellerService/getSecretaryMoneyBackList.json",
                        data={"agentToken": globals()['token']})

    def Payment_query(self, keyWord):
        """付款查询"""
        self.GetRequest(url="/api/mobile/secretarySellerService/getSecretaryPaymentList.json",
                        data={"agentToken": globals()['token'],
                              "keyWord": keyWord})  # 关键字
        if keyWord is not None:
            assert globals()['r.text']['extend']['count'] == 0
        else:
            pass

    def Client_list(self, clientType=1, value=0):
        """客户列表"""
        """clientType:1 推荐 2 上门 3 成交"""
        self.GetRequest(url='/api/mobile/secretarySellerService/getMyCustomerList.json',
                        data={'agentToken': globals()['token'],
                              'type': clientType,
                              'day': '7'})
        self.XMtext.set_map('xmcount', globals()['r.text']['extend']['count'])
        self.XMtext.set_map('xmapplyId', globals()['r.text']['extend']['sources'][value]['applyId'])

    def SignedTail(self, keyWord):
        """成交跟踪"""
        self.GetRequest(url='/api/mobile/secretarySellerService/getDealTrackList.json',
                        data={'agentToken': globals()['token'],
                              'keyWord': keyWord})
        try:
            assert globals()['r.text']['resultCode'] == 1
            self.XMtext.set_map('resultCode', globals()['r.text']['resultCode'])
            self.XMtext.set_map('xmcount', globals()['r.text']['extend']['count'])
        except BaseException as e:
            self.XMtext.set_map('xmcontent', globals()['r.text']['content'])

    def ResultsSummary(self, keyWork):
        """业绩报表---业绩汇总"""
        self.GetRequest(url='/api/mobile/secretarySellerService/getSecretaryAchievement.json',
                        data={'agentToken': globals()['token']})
        globals()['a'] = 0
        while keyWork != globals()['r.text']['extend']['list'][globals()['a']]['title']:
            globals()['a'] = globals()['a'] + 1
        self.XMtext.set_map('xmday', globals()['r.text']['extend']['list'][globals()['a']]['day'])
        self.XMtext.set_map('xmmonth', globals()['r.text']['extend']['list'][globals()['a']]['month'])
        self.XMtext.set_map('xmweek', globals()['r.text']['extend']['list'][globals()['a']]['week'])
        self.XMtext.set_map('xmyear', globals()['r.text']['extend']['list'][globals()['a']]['year'])

    def UnionMonthly(self):
        """业绩报表---联盟商月报"""
        self.GetRequest(url='/api/mobile/secretarySellerService/getSellerRanking.json',
                        data={'agentToken': globals()['token']})
        globals()['a'] = 0
        while XmSellerName != globals()['r.text']['extend']['sources'][globals()['a']]['sellerName']:
            globals()['a'] = globals()['a'] + 1
        self.XMtext.set_map('xmapplyCount', globals()['r.text']['extend']['sources'][globals()['a']]['applyCount'])
        self.XMtext.set_map('xmvisitCount', globals()['r.text']['extend']['sources'][globals()['a']]['visitCount'])
        self.XMtext.set_map('xmdealCount', globals()['r.text']['extend']['sources'][globals()['a']]['dealCount'])
        self.XMtext.set_map('xmamount', globals()['r.text']['extend']['sources'][globals()['a']]['amount'])

    def ProjectMonthly(self):
        """业绩报表---项目月报"""
        self.GetRequest(url='/api/mobile/secretarySellerService/getProjectRanking.json?',
                        data={'agentToken': globals()['token']})
        globals()['a'] = 0
        while ProjectName != globals()['r.text']['extend']['sources'][globals()['a']]['projectName']:
            globals()['a'] = globals()['a'] + 1
        self.XMtext.set_map('xmapplyCount', globals()['r.text']['extend']['sources'][globals()['a']]['applyCount'])
        self.XMtext.set_map('xmvisitCount', globals()['r.text']['extend']['sources'][globals()['a']]['visitCount'])
        self.XMtext.set_map('xmdealCount', globals()['r.text']['extend']['sources'][globals()['a']]['dealCount'])
        self.XMtext.set_map('xmamount', globals()['r.text']['extend']['sources'][globals()['a']]['amount'])

    def Post(self, sellerId, projectId, reportType, content, reportImgs):
        """报岗"""
        self.PostRequest(url='/api/mobile/secretarySellerService/secretaryReporting',
                         data={'agentToken': globals()['token'],
                               'sellerId': sellerId,    # 联盟商ID
                               'projectId': projectId,  # 项目ID
                               'reportType': reportType,   # 报岗类型
                               'reportRemark': content,     # 报岗内容
                               'reportImgs': reportImgs,        # 图片
                               'longitude': '113.59503458567298',
                               'latitude': '22.254844543421868',
                               'reportAddress': '吉大海洲路8号',
                               'mobileDeviceType': 'MI 8 SE',
                               'mobileDeviceId': '864368034653440'})
        self.XMtext.set_map('xmcontent', globals()['r.text']['content'])

    def HistoryPost(self):
        """历史报岗"""
        self.GetRequest(url='/api/mobile/secretarySellerService/getMyReportingList.json',
                        data={'agentToken': globals()['token']})
        self.XMtext.set_map('postcontent', globals()['r.text']['extend']['sources'][0]['reportRemark'])
        self.XMtext.set_map('posttype', globals()['r.text']['extend']['sources'][0]['reportType'])

    def PostSeller(self):
        """报岗查看联盟商"""
        self.GetRequest(url='/api/mobile/secretarySellerService/getSellerListNew.json',
                        data={'token': globals()['token'],
                              'keywords': XmSellerName})
        if ApiXmUrl == 'http://192.168.10.123:9090':
            self.XMtext.set_map('xmsellerId', globals()['r.text']['extend']['vo']['D'][0]['sellerId'])
        elif ApiXmUrl == 'http://api.ykb100.com':
            self.XMtext.set_map('xmsellerId', globals()['r.text']['extend']['vo']['T'][0]['sellerId'])
        else:
            self.XMtext.set_map('xmsellerId', globals()['r.text']['extend']['vo']['C'][0]['sellerId'])


    def PostProject(self):
        """报岗查看项目"""
        self.GetRequest(url='/api/mobile/secretarySellerService/getSecretaryProjectList.json',
                        data={'agentToken': globals()['token'],
                              'keyWord': ProjectName})
        if ApiXmUrl == 'http://192.168.10.123:9090':
            self.XMtext.set_map('xmprojectId', globals()['r.text']['extend']['source']['P'][0]['projectId'])
        elif ApiXmUrl == 'http://api.ykb100.com':
            self.XMtext.set_map('xmprojectId', globals()['r.text']['extend']['source']['P'][0]['projectId'])
        else:
            self.XMtext.set_map('xmprojectId', globals()['r.text']['extend']['source']['#'][0]['projectId'])

    def XmHome(self):
        """小秘主页"""
        self.GetRequest(url='/api/mobile/secretarySellerService/getSecretaryHomeData.json',
                        data={'agentToken': globals()['token']})
        self.XMtext.set_map('postcontent', globals()['r.text']['extend']['todayWork'][0]['reportRemark'])
        self.XMtext.set_map('posttype', globals()['r.text']['extend']['todayWork'][0]['reportType'])

    def MB(self, shopName, shopCompany, shopAgentName, shopAgentTel, shopMainName=None, shopMainTel=None,
           shopType=None, shopAgentCount=None, shopYears=None, shopImgs=None, industryType=None, content=None):
        """陌拜"""
        self.PostRequest(url='/api/mobile/secretarySellerService/createMBStore',
                         data={'agentToken': globals()['token'],
                               'shopName': shopName,                # *门店名称
                               'shopCityId': cityId,                # *城市ID
                               'shopAreaId': 697,   # *区域
                               'shopCompany': shopCompany,              # *归属公司
                               'longitude': '113.59503458567298',
                               'latitude': '22.254844543421868',
                               'address': '珠海',
                               'shopAddress': '吉大海洲路8号',
                               'shopAgentName': shopAgentName,      # *店长
                               'shopAgentTel': shopAgentTel,        # *店长电话
                               'shopMainName': shopMainName,        # 关键联系人
                               'shopMainTel': shopMainTel,          # 关键联系人手机号码
                               'shopType': shopType,
                               # 主营方向 （本地新房，二手房，租房，外地新房，其他），分开
                               'shopAgentCount': shopAgentCount,
                               # 员工人数区间】5人以下，6～10人，11～20人，21～50人，51～100人，100人以上
                               'shopYears': shopYears,          # 门店经营时长 <1年 1～3年 3年以上
                               'shopImgs': shopImgs,            # 附件
                               'industryType': industryType,    # 类型 中介、电销、平台、其他
                               'mainArea': content})           # 备注
        self.XMtext.set_map('xmcontenr', globals()['r.text']['content'])

    def MBList(self, keyWord=None, dayWithin=None, shopAgentCount=None):
        """陌拜列表"""
        self.GetRequest(url='/api/mobile/secretarySellerService/getTSellerShopList.json',
                        data={'agentToken': globals()['token'],
                              'keyWord': keyWord,
                              'dayWithin': dayWithin,           # 第几天内：0单天、7：七天内、30：0天内 180：半年内
                              'shopAgentCount': shopAgentCount,
                              'pageNumber': 1,
                              'pageLimit': 999})    # 人数5人以下 6~10人 11~20人 21~50人 50~100人 100人以上

        self.XMtext.set_map('xmsellerShopId', globals()['r.text']['extend']['source'][0]['sellerShopId'])

    def MBParticulars(self):
        """陌拜详情"""
        self.GetRequest(url='/api/mobile/secretarySellerService/getTSellerShopDetails.json',
                        data={'agentToken': globals()['token'],
                              'sellerShopId': globals()['r.text']['extend']['source'][0]['sellerShopId']})
        # self.XMtext.set_map('xmshopName', globals()['r.text']['extend']['source']['shopName'])
        # self.XMtext.set_map('xmindustryType', globals()['r.text']['extend']['source']['industryType'])
        # self.XMtext.set_map('xmshopAgentName', globals()['r.text']['extend']['source']['shopAgentName'])
        # self.XMtext.set_map('xmshopAgentTel', globals()['r.text']['extend']['source']['shopAgentTel'])

    def AlterMB(self, shopName, shopCompany, shopAgentName, shopAgentTel,
                shopMainName=None, shopMainTel=None,
                shopType=None, shopAgentCount=None,
                shopYears=None, shopRemark=None,
                mainArea=None, shopImgs=None, industryType=None):
        """修改陌拜"""
        self.GetRequest(url='/api/mobile/area/getAreaList.json',
                        data={'cityId': cityId,
                              'token': globals()['token']})
        self.PostRequest(url='/api/mobile/secretarySellerService/updateMBStore',
                         data={'agentToken': globals()['token'],
                               'shopName': shopName,  # *门店名称
                               'shopCityId': cityId,  # *城市ID
                               'shopAreaId': globals()['r.text']['extend']['areas'][0]['areaId'],  # *区域
                               'shopCompany': shopCompany,  # *归属公司
                               'longitude': '113.59503458567298',
                               'latitude': '22.254844543421868',
                               'address': '珠海',
                               'shopAddress': '吉大海洲路8号',
                               'shopAgentName': shopAgentName,  # *店长
                               'shopAgentTel': shopAgentTel,  # *店长电话
                               'sellerShopId': self.XMtext.get('xmsellerShopId'),
                               'shopMainName': shopMainName,  # 关键联系人
                               'shopMainTel': shopMainTel,  # 关键联系人手机号码
                               'shopType': shopType,
                               # 主营方向 （本地新房，二手房，租房，外地新房，其他），分开
                               'shopAgentCount': shopAgentCount,
                               # 员工人数区间】5人以下，6～10人，11～20人，21～50人，51～100人，100人以上
                               'shopYears': shopYears,  # 门店经营时长 <1年 1～3年 3年以上
                               'shopRemark': shopRemark,   # 备注
                               'mainArea': mainArea,    # 主营区域
                               'shopImgs': shopImgs,  # 附件
                               'industryType': industryType,  # 类型 中介、电销、平台、其他
                               })

    def SellerPrincipalPhone(self, sellerType, sellerName, sellerFullName, agentId, agentName,
                             mainPerson=None, mainPersonTel=None,
                             sellerShopType=None, sellerAgentCount=None,
                             sellerYears=None, sellerUserIdcards=None,
                             sellerLicensePics=None, showPic=None,
                             sellerBackbook=None, sellerAgreement=None):
        """负责人手机号码（创建联盟商）"""
        try:
            self.GetRequest(url='/api/mobile/area/getAreaList.json',
                            data={'cityId': cityId,
                                  'token': globals()['token']})
            self.PostRequest(url='/api/mobile/secretarySellerService/addSellerV1',
                             data={'agentToken': globals()['token'],
                                   'sellerType': sellerType,  # 联盟商类型
                                   'sellerName': sellerName,  # *联盟商名称
                                   'sellerFullName': sellerFullName,  # *联盟商全称
                                   'agentId': agentId,  # 队长ID（手机号查询）
                                   'areaId': 1,
                                   'agentName': agentName,  # 队长名字
                                   'mainPerson': mainPerson,  # 关键联系人
                                   'mainPersonTel': mainPersonTel,  # 关键联系人手机号码
                                   'longitude': '113.59503458567298',
                                   'latitude': '22.254844543421868',
                                   'sellerAddress': '吉大海洲路8号',
                                   'sellerShopType': sellerShopType,
                                   # 主营方向 （本地新房，二手房，租房，外地新房，其他），分开
                                   'sellerAgentCount': sellerAgentCount,
                                   # 员工人数区间】5人以下，6～10人，11～20人，21～50人，51～100人，100人以上
                                   'sellerYears': sellerYears,  # 门店经营时长 <1年 1～3年 3年以上
                                   'sellerUserIdcards': sellerUserIdcards,  # 负责人身份证照
                                   'sellerLicensePics': sellerLicensePics,  # 营业执照
                                   'showPic': showPic,                  # 门店照片 可以上传多张
                                   'sellerBackbook': sellerBackbook,    # 备案证书
                                   'sellerAgreement': sellerAgreement,  # 联盟商协议
                                   'showPics': showPic,
                                   'sellerShopId': self.XMtext.get('xmsellerShopId'),  # 陌拜ID
                                   'cityId': cityId,
                                   'cityName': cityName,
                                   'areaName': globals()['r.text']['extend']['areas'][0]['areaName'],   # 区域名字
                                   'hasShop': 1,
                                   'pageNumber': 1})
            if ApiXmUrl == 'http://api.xfjb100.com':
                self.XMtext.set_map('sellerId', globals()['r.text']['extend']['sellerId'])
                self.XMtext.set_map('sellerNo', globals()['r.text']['extend']['sellerNo'])
            else:
                assert '请联系管理人', globals()['r.text']['content']

        except BaseException as e:
            print("断言错误，错误原因：%s" % e)
            raise RuntimeError(print(ApiXmUrl))

    def Search_C_USER(self, vlue=0, pageNum=1):
        """查询C类账号"""
        self.GetRequest(url='/api/mobile/secretarySellerService/getSellerAgentList.json',
                        data={'agentToken': globals()['token'],
                              'pageNum': pageNum,
                              'rowsDisplayed': '50'})
        self.XMtext.set_map('xmCPhone', globals()['r.text']['extend']['sources'][vlue]['agentTel'])
        self.XMtext.set_map('xmCAgentName', globals()['r.text']['extend']['sources'][vlue]['agentRealName'])
        self.XMtext.set_map('xmCAgentId', globals()['r.text']['extend']['sources'][vlue]['agentId'])

    def CreationSeller(self):
        """创建联盟商"""
        self.PostRequest(url='/api/mobile/secretarySellerService/addSellerV1',
                         data={''})

    def InvoiceTitleList(self, projectId):
        """发票抬头列表"""
        self.GetRequest(url='/api/mobile/projectAdminService/getInvoiceRises.json',
                        data={'agentToken': globals()['token'],
                              'projectId': projectId})
        self.XMtext.set_map('titleId', globals()['r.text']['extend']['invoiceRises'][0]['titleId'])

    def ADDInvoiceTitle(self, titleName, titleDuty, companyLocation, bankName, accountPhone, bankAccount, projectId):
        """新增发票抬头"""
        self.PostRequest(url='/api/mobile/projectAdminService/adminInvoiceRise',
                         data={'agentToken': globals()['token'],
                               'titleName': titleName,              # 名称
                               'titleDuty': titleDuty,              # 税号
                               'companyLocation': companyLocation,  # 单位地址
                               'bankName': bankName,                # 开户银行
                               'accountPhone': accountPhone,        # 电话号码
                               'bankAccount': bankAccount,           # 银行账号
                               'titleType': 2,
                               'invoicePicList': '[]',
                               'externalId': projectId})

    def InvoiceTitleParticulars(self, projectId):
        """发票详情"""
        self.GetRequest(url='/api/mobile/projectAdminService/getInvoiceRiseDetails.json',
                        data={'agentToken': globals()['token'],
                              'titleId': self.XMtext.get('titleId'),
                              'titleType': 2,
                              'projectId': projectId})
        self.XMtext.set_map('extend', globals()['text']['extend'])

    def AlterInvoiceTitle(self, titleName, titleDuty, companyLocation, bankName, accountPhone, bankAccount, titleId):
        """修改发票抬头"""
        self.PostRequest(url='/api/mobile/projectAdminService/adminInvoiceRise',
                         data={'agentToken': globals()['token'],
                               'titleName': titleName,  # 名称
                               'titleDuty': titleDuty,  # 税号
                               'companyLocation': companyLocation,  # 单位地址
                               'bankName': bankName,  # 开户银行
                               'accountPhone': accountPhone,  # 电话号码
                               'bankAccount': bankAccount,  # 银行账号
                               'titleId': titleId,
                               'titleType': 2,
                               'invoicePicList': '[]'})
        self.XMtext.set_map('xmcontenr', globals()['r.text']['content'])
        self.XMtext.set_map('AltertitleName', f"{titleName}")
        self.XMtext.set_map('AltertitleDuty', f"{titleDuty}")
        self.XMtext.set_map('AltercompanyLocation', f"{companyLocation}")
        self.XMtext.set_map('AlterbankName', f"{bankName}")
        self.XMtext.set_map('AlteraccountPhone', f"{accountPhone}")
        self.XMtext.set_map('AlterbankAccount', f"{bankAccount}")

    def ProjectList(self):
        """项目列表"""
        self.GetRequest(url='/api/mobile/projectAdminService/getManagerProject.json',
                        data={'agentToken': globals()['token']})
        globals()['a'] = 0
        while globals()['r.text']['extend']['managerProject'][globals()['a']]['projectName'] != ProjectName:
            globals()['a'] = globals()['a'] + 1
        self.XMtext.set_map('noConfirmedCount',
                            globals()['r.text']['extend']['managerProject'][globals()['a']]['noConfirmedCount'])
        if self.XMtext.get('noConfirmedCount') == 0:
            self.AgentRequest.LoginAgent()
            self.AgentRequest.ForRegistrationID()
            self.XfkRequest.AttacheList()
            self.AgentRequest.RecommendNew()
            """报名成功后的操作"""
            self.XfkRequest.AttacheList()
            self.XfkRequest.ExamineClientParticulars()
            self.XfkRequest.AttacheOperation(SalesId=self.XfkTEXT.get('xfkSalesId'))
            self.XfkRequest.HousesOperation()
            self.XfkRequest.ProjectExpect()
            self.XfkRequest.HouseType()
            self.XfkRequest.ContractAgo()
            self.XfkRequest.AttacheContract()

    def PrpjectParticulars(self):
        """项目详情"""
        self.ProjectList()
        self.GetRequest(url='/api/mobile/projectAdminService/getManagerProjectDetails.json',
                        data={'agentToken': globals()['token'],
                              'projectId': globals()['r.text']['extend']['managerProject'][globals()['a']]['projectId']})

    def DealTicketList(self, DealTicketType=1, value=0):
        """成交确认列表"""
        self.ProjectList()
        self.GetRequest(url='/api/mobile/projectAdminService/getSignManagementList.json',
                        data={'agentToken': globals()['token'],
                              'projectId': globals()['r.text']['extend']['managerProject'][globals()['a']]['projectId'],
                              'type': DealTicketType})
        globals()['dealId'] = globals()['r.text']['extend']['sources'][value]['dealId']
        self.XMtext.set_map('dealId', globals()['r.text']['extend']['sources'][value]['dealId'])
        self.XMtext.set_map('roomNoStr', globals()['r.text']['extend']['sources'][value]['roomNoStr'])
        self.XMtext.set_map('customerMobile', globals()['r.text']['extend']['sources'][value]['customerMobile'])

    # def DealHome(self, houseTypeName='公寓', control=0):
    #     """户型比例"""
    #     self.GetRequest(url='/api/mobile/projectAdminService/getHouseTypes.json',
    #                     data={'dealId': globals()['dealId']})
    #     globals()['a'] = 0
    #     if ApiXmUrl == 'http://api.xfj100.com':
    #         if control == 0:
    #             houseTypeName = '1~49套'
    #         else:
    #             pass
    #     else:
    #         pass
    #     while houseTypeName != globals()['r.text']['extend'][globals()['a']]['houseTypeName']:
    #         globals()['a'] = globals()['a'] + 1
    #     self.XMtext.set_map('extend', globals()['r.text']['extend'][globals()['a']])

    def DealCancellation(self, checkingRemark=None):
        """作废成交单"""
        self.PostRequest(url='/api/mobile/projectAdminService/dealCancel',
                         data={'agentToken': globals()['token'],
                               'dealId': globals()['dealId'],
                               'checkingRemark': checkingRemark,
                               'checkingDate': time.strftime("%Y-%m-%d")})

    def PerformanceSynchronization(self):
        """业绩同步"""
        self.PostRequest(url='/api/mobile/projectAdminService/automatedPreservationAchievementNew',
                         data={'agentToken': globals()['token'],
                               'dealId': globals()['dealId']})

    def getDealTransactionAmount(self):
        """客户来源"""
        self.GetRequest(url='/api/mobile/projectAdminService/getDealTransactionAmountNew.json',
                        data={'agentToken': globals()['token'],
                              'dealId': globals()['dealId']})
        self.XMtext.set_map('from', globals()['r.text']['extend']['commission']['from'])
        globals()['from'] = globals()['r.text']['extend']['commission']['from']

    def DealTicketParticulars(self):
        self.PerformanceSynchronization()
        """成交确认详情"""
        self.GetRequest(url='/api/mobile/projectAdminService/getDealDetails.json',
                        data={'agentToken': globals()['token'],
                              'dealId': self.XMtext.get('dealId'),
                              'checkingDate': time.strftime("%Y-%m-%d")})
        self.XMtext.set_map('extend', globals()['r.text']['extend'])
        self.XFKTEXT.set_map('applyId', globals()['r.text']['extend']['applyId'])
        # self.XMtext.set_map('sellerType', globals()['r.text']['extend']['sellerType'])
        self.XMtext.set_map('RoomNoStr', globals()['r.text']['extend']['roomNoStr'])
        self.XMtext.set_map('signTime', globals()['r.text']['extend']['signTime'])
        self.XMtext.set_map('houseTypeId', globals()['r.text']['extend']['houseTypeId'])
        self.XMtext.set_map('customerName', globals()['r.text']['extend']['customerName'])
        self.XMtext.set_map('customerMobile', globals()['r.text']['extend']['customerMobile'])
        self.XMtext.set_map('company', globals()['r.text']['extend']['company'])        # 全称
        self.XMtext.set_map('roomPriceTotal', globals()['r.text']['extend']['roomPriceTotal'])

    def AlterDealTicket(self, roomNoStr,        # 房号
                        houseTypeId,            # 户型
                        squareBuilding,         # 面积
                        roomPriceTotal,         # 签约总价
                        commissionRate,         # 比例 佣金
                        commissionRatePrice,        # 应收代理费 佣金
                        XFJMoneyRate,           # 现金奖比例
                        XFJMoneyRatePrice,      # 现金奖加的金额
                        proportion,             # 比例    佣金
                        addAmount,              # 要加的业绩 佣金
                        LMSMoneyRate,           # 现金奖比例
                        LMSMoneyRatePrice,      # 现金奖加的金额
                        houseTypeName,
                        customerName,
                        customerMobile,
                        commissionRemark='应付备注',   # 应付备注
                        remark='专员备注',             # 专员备注
                        dealPic='/uploads/2019/0930/1f62b001-2547-4193-a1e8-1d695790f4c4.png',
                        submitType=0,
                        paymentMethod='一次性付款',
                        signTime=time.strftime("%Y-%m-%d")
                        ):

        """修改成交确认单"""
        self.PostRequest(url='/api/mobile/projectAdminService/updateCustomerDemandTuanDealNew',
                         data={'agentToken': globals()['token'],
                               'dealId': globals()['dealId'],       # 成交单ID
                               'roomNoStr': roomNoStr,     # 房号
                               # 'tuanId': '1508',
                               # 'YJtypeFormula': '2.500%+2,500.00',
                               # 'XFJXJJtypeFormula': '5.000%+5,000.00',
                               # 'LMSYJtypeFormula': '1.500%+1,500.00',
                               # 'LMSXJJtypeFormula': '3.000%+3,000.00',
                               # 'YJtypeTitle': '佣金',
                               # 'XFJXJJtypeTitle': '现金奖',
                               # 'LMSYJtypeTitle': '佣金',
                               # 'LMSXJJtypeTitle': '现金奖',
                               # 'auditStatus': '0',
                               # 'projectName': '潘测试皇爵商业广场',
                               # 'commissionPrice1': round((roomPriceTotal)*(commissionRate)
                               #                           + (commissionRatePrice),2),
                               # 'commissionPrice2': round((roomPriceTotal)*(XFJMoneyRate)
                               #                           + (XFJMoneyRatePrice),2),
                               # 'amount1': round((roomPriceTotal)*(proportion)
                               #                  + (addAmount), 2),
                               # 'amount2': round((roomPriceTotal)*(LMSMoneyRate)
                               #                  + (LMSMoneyRatePrice), 2),


                               'squareBuilding': squareBuilding,       # 面积
                               'roomPriceTotal': roomPriceTotal,       # 签约总价
                               'signTime': signTime,                   # 签约日期
                               'customerName': customerName,           # 客户姓名
                               'customerMobile': customerMobile,       # 客户电话
                               'paymentMethod': paymentMethod,         # 付款方式
                               'commissionRate': commissionRate,       # 比例
                               'houseTypeName': houseTypeName,                  # 户型名称
                               'houseTypeId': self.XFKTEXT.get('houseTypeId'),  # 户型ID
                               'commissionPrice':
                                   round((roomPriceTotal)*(commissionRate) +
                                         (roomPriceTotal)*(XFJMoneyRate) + (XFJMoneyRatePrice) +
                                         (commissionRatePrice),2),
                               # 根据户型得出的应收代理费金额
                               'commissionRatePrice': commissionRatePrice,     # 应收代理费
                               'remark': remark,       # 签约备注
                               'dealPic': dealPic,     # 附件 # 隔开

                               'checkingDate': time.strftime("%Y-%m-%d"),   # 对账日期
                               'submitType': submitType,       # 0 修改 1 修改带提交
                               'relType': 1,             # 标识修改哪个人的业绩
                               'proportion': proportion,       # 比例
                               'addAmount': addAmount,     # 要加的业绩
                               'amount':
                                   round((roomPriceTotal)*(proportion) +
                                         (roomPriceTotal)*(LMSMoneyRate) + (LMSMoneyRatePrice) +
                                         (addAmount), 2),
                               # 计算后的业绩
                               'XFJMoneyRate': XFJMoneyRate,
                               'XFJMoneyRatePrice': XFJMoneyRatePrice,
                               'LMSMoneyRate': LMSMoneyRate,
                               'LMSMoneyRatePrice': LMSMoneyRatePrice,
                               'commissionRemark': commissionRemark      # 应付备注
                               })
        self.XMtext.set_map('resultCode', globals()['r.text']['resultCode'])
        self.XMtext.set_map('xmcontent', globals()['r.text']['content'])

    def DealTicket(self, remark=''):
        """成交确认"""
        self.PostRequest(url='/api/mobile/projectAdminService/submitCustomerDemandTuanDeal',
                         data={'agentToken': globals()['token'],
                               'dealId': self.XMtext.get('dealId'),
                               'remark': remark,
                               'checkingDate': time.strftime("%Y-%m-%d")})
        assert 1, globals()['text']['resultCode']

    def ResultsTheChangeStayList(self, projectId, keyWord=None, value=0, excludeType=None):
        """业绩变更-待申请列表"""
        self.GetRequest(url='/api/mobile/changeService/getPerformanceChangeList.json',
                        data={'agentToken': globals()['token'],
                              'projectId': projectId,
                              'excludeType': excludeType,
                              'keyWord': keyWord,
                              'pageNum': 1,
                              'rowsDisplayed': 999})
        self.XMtext.set_map('sources', globals()['r.text']['extend']['sources'][value])
        globals()['dealId'] = globals()['r.text']['extend']['sources'][value]['dealId']
        self.XMtext.set_map('dealId', globals()['r.text']['extend']['sources'][value]['dealId'])
        self.XMtext.set_map('roomNoStr', globals()['r.text']['extend']['sources'][value]['roomNoStr'])

    def ResultsTheChangeList(self, projectId, value=0, dealId=None):
        """业绩变更--已申请列表"""
        self.GetRequest(url='/api/mobile/changeService/getChangeDeals',
                        data={'agentToken': globals()['token'],
                              'projectId': projectId})

        if globals()['r.text']['extend']['count'] == 0:
            globals()['dealChangeId'] = 0
        else:
            if dealId == None:
                globals()['dealId'] = globals()['r.text']['extend']['sources'][value]['dealId']
                self.XMtext.set_map('dealId', globals()['r.text']['extend']['sources'][value]['dealId'])
                globals()['dealChangeId'] = globals()['r.text']['extend']['sources'][value]['dealChangeId']
                self.XMtext.set_map('dealChangeId',
                                    globals()['r.text']['extend']['sources'][value]['dealChangeId'])
                self.XMtext.set_map('changeStatusStr',
                                    globals()['r.text']['extend']['sources'][value]['changeStatusStr'])
                self.XMtext.set_map('changeTypeStr',
                                    globals()['r.text']['extend']['sources'][value]['changeTypeStr'])
            else:
                dome = 0
                globals()['dealId'] = globals()['r.text']['extend']['sources'][dome]['dealId']
                while self.XMtext.get('dealId') != globals()['dealId']:
                    dome = dome + 1
                    globals()['dealId'] = globals()['r.text']['extend']['sources'][dome]['dealId']

    def ResultsTheChange(self, type, houseTypeId=None, isSave=1,commissionRate=None,
                         commissionRatePrice=None, commissionSellerRate=None,
                         commissionSellerPrice=None, customerName=None, customerMobile=None, roomNoStr=None,
                         squareBuilding=None, roomPriceTotal=None, sellerFullName=None, changePic=None,
                         remark=None,
                         signTime=None,
                         changeDesc= time.strftime("%Y-%m-%d %H:%M:%S"), paymentMethod='一次性付款'):

        """业绩变更"""
        if type == '挞定' or type == '更名' or type == '更换开票公司':
            commissionPrice = None
            sellerPlay = None
            if type == '挞定':
                globals()['type'] = 'tarting'   # 挞定
            elif type == '更换开票公司':
                globals()['type'] = 'modifySeller'
            else:
                globals()['type'] = 'modifyCustomer'    # 修改业主信息
            commissionPrice = round(roomPriceTotal * self.XFKTEXT.get('XFJYJRete'), 2) + \
                              round(self.XFKTEXT.get('XFJYJAmount'), 2) + \
                              round(roomPriceTotal * self.XFKTEXT.get('XFJXJJRete'), 2) + \
                              round(self.XFKTEXT.get('XFJXJJAmount'), 2)
            sellerPlay = round(self.XFKTEXT.get('sellerYJRete') * roomPriceTotal, 2) + \
                         round(self.XFKTEXT.get('sellerYJAmount'), 2) + \
                         round(self.XFKTEXT.get('sellerXJJRete') * roomPriceTotal, 2) + \
                         round(self.XFKTEXT.get('sellerXJJAmount'), 2)
        elif type == '调价及调佣' or type == '换房':
            commissionPrice = round(roomPriceTotal * self.XFKTEXT.get('XFJYJRete'), 2) + \
                              round(self.XFKTEXT.get('XFJYJAmount'), 2) + \
                              round(roomPriceTotal * self.XFKTEXT.get('XFJXJJRete'), 2) + \
                              round(self.XFKTEXT.get('XFJXJJAmount'), 2)
            sellerPlay = round(self.XFKTEXT.get('sellerYJRete') * roomPriceTotal, 2) + \
                         round(self.XFKTEXT.get('sellerYJAmount'), 2) + \
                         round(self.XFKTEXT.get('sellerXJJRete') * roomPriceTotal, 2) + \
                         round(self.XFKTEXT.get('sellerXJJAmount'), 2)
            self.XMtext.set_map('commissionPrice', commissionPrice)
            self.XMtext.set_map('sellerPlay', sellerPlay)
            if type == '调价及调佣':
                globals()['type'] = 'modifyPrice'   # 挞定
            else:
                globals()['type'] = 'changeHouse'  # 换房
        else:
            print('没有这样的类型')
        requestParame = {'dealId': globals()['dealId'],
                         'houseTypeId': houseTypeId,        # 户型ID
                         'commissionRate': str(commissionRate),  # 代理费比例
                         'commissionRatePrice': str(commissionRatePrice),  # 代理费金额
                         'signTime': signTime,
                         'commissionPrice': str("%.2f" % commissionPrice),    # 代理费总额
                         'sellerRate': str(commissionSellerRate),  # 应付比例
                         'sellerPrice': str(commissionSellerPrice),    # 应付金额
                         'sellerPlay': str("%.2f" % sellerPlay),      # 应付总金额
                         'customerName': customerName,  # 业主姓名
                         'customerMobile': customerMobile,      # 业主电话
                         'roomNoStr': roomNoStr,                # 房号
                         'changePic': changePic,
                         'changeDesc': changeDesc,
                         'squareBuilding': squareBuilding,      # 面积
                         'roomPriceTotal': roomPriceTotal,      # 合同总价
                         'sellerFullName': sellerFullName,      # 联盟商全称
                         'paymentMethod': paymentMethod,
                         'remark': remark}      # 签约单备注
        if type == '更名' or type == '挞定' or type == '更换开票公司':
            requestParame = json.dumps(requestParame).replace("None", "")
            requestParame = json.loads(requestParame)
        else:
            pass
        for key in list(requestParame.keys()):
            if not requestParame.get(key):
                del requestParame[key]
        self.PostRequest(url='/api/mobile/changeService/publicApplyChange',
                         data={'agentToken': globals()['token'],
                               'type': globals()['type'],
                               'isSave': isSave,  # 0草稿 1 提交
                               'requestParame': json.dumps(requestParame, ensure_ascii=False)})
        self.XMtext.set_map('xmcontent', globals()['r.text']['content'])
        self.XMtext.set_map('ResultCode', globals()['r.text']['resultCode'])

    def ResultsTheChangeAudit(self, type, approveStatus=1):
        """业绩变更审核"""
        if type == '调价及调佣':
            globals()['type'] = 'modifyPrice'
        elif type == '换房':
            globals()['type'] = 'changeHouse'
        elif type == '更名':
            globals()['type'] = 'modifyCustomer'
        elif type == '挞定':
            globals()['type'] = 'tarting'
        elif type == '更换开票公司':
            globals()['type'] = 'modifySeller'
        else:
            raise RuntimeError(print('业绩变更没有这样的类型'))
        requestParame = {'dealChangeId': globals()['dealChangeId'],
                         'approveStatus': approveStatus}
        self.PostRequest(url='/api/mobile/changeService/examineChange',
                         data={'agentToken': globals()['token'],
                               'type': globals()['type'],
                               'requestParame': json.dumps(requestParame, ensure_ascii=False)
                               })

    def ResultsTheChangeParticulars(self, dealChangeId=1):
        """业绩变更---详情"""
        if dealChangeId == 1:
            dealChangeId = globals()['dealChangeId']
        else:
            pass
        self.GetRequest(url='/api/mobile/changeService/getModifyPriceDetailsNew.json',
                        data={'agentToken': globals()['token'],
                              'dealId': self.XMtext.get('dealId'),
                              'dealChangeId': dealChangeId})
        self.XMtext.set_map('houseTypeName', globals()['r.text']['extend']['houseTypeName'])
        self.XMtext.set_map('extend', globals()['r.text']['extend'])

    def CashCollectionList(self, cashStatus=None, value=0):
        """现金回款列表"""
        self.GetRequest(url='/api/mobile/projectAdminService/getCashRefundList',
                        data={'agentToken': globals()['token'],
                              'projectId': self.AgentTEXT.get('projectId'),
                              'cashStatus': cashStatus})
        self.XMtext.set_map('dealId', globals()['text']['extend']['sources'][value]['dealId'])
        self.XMtext.set_map('cashStatusStr',
                            globals()['r.text']['extend']['sources'][value]['cashStatusStr'])

    def CashCollectionParticulars(self, value=0):
        """现金回款详情"""
        self.GetRequest(url='/api/mobile/projectAdminService/getCashRefundDetails',
                        data={'agentToken': globals()['token'],
                              'cashId': globals()['text']['extend']['sources'][value]['cashId']})

    def Payee(self, citySiteId=1,businuessType=2):
        """收款方"""
        self.GetRequest(url='/api/mobile/projectAdminService/getCompanyByCitySite.json',
                        data={'dealId': globals()['dealId']})
        globals()['text1'] = globals()['text']
        """收款详情"""
        self.GetRequest(url='/api/mobile/projectAdminService/getCashRefundBankAccount.json',
                        data={'agentToken': globals()['token'],
                              'citySiteId': citySiteId,
                              'businuessType': businuessType}),

    def CashCollectionEntering(self,
                               type='业主',
                               cashPic=img,
                               cashRemark='现金回款' + time.strftime("%Y-%m-%d %H_%M_%S"),
                               isApply=1,   # 默认提交
                               value=1,     # 收款值的判断 1大于
                               citySiteId=citySiteId,    # 1 城市站 2 联盟商 3 开发商
                               isCashRefund=0,      # 0:付款 1收款
                               meanwhile=0,         # 是否同时录入
                               value1=1,            # 付款值的判断  1代表小于等于
                               businuessType=2):    # 1公司账号 2 个人账号
        """现金收款/付款录入"""
        self.getDealTransactionAmount()
        if self.XFKTEXT.get('sellerType') == 'a':
            a = 0
            try:
                while globals()['r.text']['extend']['commission']['achievement'][a]['typeTitle'] != \
                        '佣金' or globals()['r.text']['extend']['commission']['achievement'][a]['sellerType'] != 'A':
                    a = a + 1
                self.XMtext.set_map('LMSYJ',
                                    globals()['r.text']['extend']['commission']['achievement'][a]['amountSum'])
            except:
                print("该成交单详情联盟商佣金不存在")
                self.XMtext.set_map('LMSYJ', 0)
        else:
            a = 0
            try:
                while globals()['r.text']['extend']['commission']['achievement'][a]['typeTitle'] != \
                        '佣金' or globals()['r.text']['extend']['commission']['achievement'][a]['sellerType'] != 'B':
                    a = a + 1
                self.XMtext.set_map('LMSYJ',
                                    globals()['r.text']['extend']['commission']['achievement'][a]['amountSum'])
            except:
                print("该成交单详情联盟商佣金不存在")
                self.XMtext.set_map('LMSYJ', 0)

        """以上是获取联盟商佣金"""
        a = 0
        try:
            while globals()['r.text']['extend']['commission']['achievement'][a]['typeTitle'] != \
                    '佣金' or globals()['r.text']['extend']['commission']['achievement'][a]['sellerType'] != 'X':
                a = a + 1
            self.XMtext.set_map('XFJYJ', globals()['r.text']['extend']['commission']['achievement'][a]['amountSum'])
        except:
            print("该成交单详情幸福家佣金不存在")
            self.XMtext.set_map('XFJYJ', 0)
        """以上是获取幸福家佣金"""

        if isCashRefund == 1:
            """幸福家佣金"""
            cashAmount = random.randint(0, 100000)
            if value == 1:
                while "%.2f" % cashAmount < "%.2f" % float(self.XMtext.get('XFJYJ')):
                    time.sleep(0.2)
                    cashAmount = random.randint(0, 100000)
            elif value == 0:
                cashAmount = self.XMtext.get('XFJYJ')
            else:
                while "%.2f" % cashAmount > "%.2f" % float(self.XMtext.get('XFJYJ')):
                    time.sleep(0.2)
                    cashAmount = random.randint(0, 100000)
            if meanwhile == 1:
                paymentAmount = random.randint(0, 100000)
                if value1 == 1:
                    while "%.2f" % paymentAmount < "%.2f" % float(self.XMtext.get('LMSYJ')):
                        time.sleep(0.2)
                        paymentAmount = random.randint(0, 100000)
                elif value1 == -1:
                    while "%.2f" % paymentAmount > "%.2f" % float(self.XMtext.get('LMSYJ')):
                        time.sleep(0.2)
                        paymentAmount = random.randint(0, 100000)
                else:
                    paymentAmount = self.XMtext.get('LMSYJ')
            else:
                paymentAmount = None
            self.DealTicketParticulars()
            """现金收款录入"""
            if type == '开发商':
                payType = '2'
                payTypeStr = '开发商'
                self.XMtext.set_map('payName', globals()['text']['extend']['developer'])
            else:
                payType = '1'
                payTypeStr = '业主'
                self.XMtext.set_map('payName', globals()['text']['extend']['customerName'])
                # payName = globals()['text']['extend']['customerName']
            payName = self.XMtext.get('payName')    # 付款方
            """获取收款方"""
            globals()['a'] = 0
            self.GetRequest(url='/api/mobile/projectAdminService/getCompanyByCitySite.json',
                            data={'dealId': globals()['dealId'],
                                  'citySiteId': '1',
                                  'bankAccountType': '3'})
            self.XMtext.set_map('companyId', globals()['r.text']['extend']['sources'][0]['companyId'])
            companyId = self.XMtext.get('companyId')
            self.XMtext.set_map('companyName', globals()['r.text']['extend']['sources'][0]['companyName'])
            companyName = self.XMtext.get('companyName')
            # globals()['text1'] = globals()['text']
            """收款详情"""
            self.GetRequest(url='/api/mobile/projectAdminService/getCashRefundBankAccount.json',
                            data={'agentToken': globals()['token'],
                                  'citySiteId': citySiteId,
                                  'businuessType': businuessType}),
            self.XMtext.set_map('accountId', globals()['r.text']['extend']['sources'][0]['accountId'])
            accountId = self.XMtext.get('accountId')
            self.XMtext.set_map('bankName', globals()['r.text']['extend']['sources'][0]['bankName'])
            bankBranchName = self.XMtext.get('bankName')
            self.XMtext.set_map('bankAccount', globals()['r.text']['extend']['sources'][0]['bankAccount'])
            bankAccount = self.XMtext.get('bankAccount')
            self.XMtext.set_map('bankUserName', globals()['r.text']['extend']['sources'][0]['bankUserName'])
            bankUserName = self.XMtext.get('bankUserName')

        elif isCashRefund == 0:
            paymentAmount = random.randint(0, 100000)
            if value1 == 1:
                while "%.2f" % paymentAmount < "%.2f" % float(self.XMtext.get('LMSYJ')):
                    paymentAmount = random.randint(0, 100000)
            elif value1 == -1:
                while "%.2f" % paymentAmount > "%.2f" % float(self.XMtext.get('LMSYJ')):
                    paymentAmount = random.randint(0, 100000)
            else:
                paymentAmount = self.XMtext.get('LMSYJ')
            payType = None,
            payTypeStr = None,
            payName = None,
            companyId = None
            companyName = None
            accountId = None
            bankBranchName = None
            bankAccount = None
            bankUserName = None
            cashAmount = None
        self.PostRequest(url='/api/mobile/projectAdminService/adminCashRefund',
                         data={'agentToken': globals()['token'],
                               'dealId': self.XMtext.get('dealId'),
                               'payType': payType,
                               'payTypeStr': payTypeStr,
                               'payName': payName,
                               'companyId': companyId,
                               'companyName': companyName,
                               'accountId': accountId,
                               'bankBranchName': bankBranchName,
                               'bankAccount': bankAccount,
                               'bankUserName': bankUserName,
                               'cashAmount': cashAmount,
                               'paybackDate': time.strftime("%Y-%m-%d"),
                               'isCashRefund': isCashRefund,
                               'cashPic': cashPic,
                               'cashRemark': cashRemark,
                               'paymentAmount': paymentAmount,
                               'isApply': isApply})

    def InvoiceEntering(self,
                        statementId=None,   # 传则修改
                        InvoiceType=1,  # 类型
                        compare=0,   # 开票总额 0 相同 1 超过 2 小于
                        totalCount=1,   # 套数
                        attachmentUrls=img,
                        remark='开票录入' + time.strftime("%Y-%m-%d %H:%M:%S"),
                        isApply=1):
        """录入开票"""
        """获取发票抬头"""
        self.InvoiceTitleList(projectId=self.AgentTEXT.get('projectId'))
        self.InvoiceTitleParticulars(projectId=self.AgentTEXT.get('projectId'))
        xftSettleInvoiceTitleJson = json.loads(
            json.dumps(json.loads(self.XMtext.get('extend')),
                       indent=4, sort_keys=False, ensure_ascii=False))
        xftSettleInvoiceTitleJson['invoiceType'] = InvoiceType  # 类型
        self.ResultsTheChangeStayList(projectId=self.AgentTEXT.get('projectId'))
        a = 0
        receiptSettleInfos = []
        while totalCount != a:
            self.DealTicketParticulars()
            globals()['xmtext'] = json.loads(json.dumps(json.loads(self.XMtext.get('extend')),
                                                        indent=4, sort_keys=False, ensure_ascii=False))
            list1 = {'dealId': globals()['xmtext']['dealId'],
                     'confirmCommissionPrice': float(globals()['xmtext']['commissionPrice'])}
            if a != 0:
                totalConfirmAmount = "%.2f" % (float(globals()['xmtext']['commissionPrice']) +
                                               float(totalConfirmAmount))
            else:
                totalConfirmAmount = float(globals()['xmtext']['commissionPrice'])
            receiptSettleInfos.append(list1)
            a = a + 1
            self.ResultsTheChangeStayList(projectId=self.AgentTEXT.get('projectId'), value=a)
        # print(receiptSettleInfos)
        # print(totalConfirmAmount)
        Amount = random.randint(0, 1000000)
        if compare == -1:
            while float(totalConfirmAmount) < Amount:
                Amount = random.randint(0, 1000000)
            totalConfirmAmount = Amount
        elif compare == 1:
            while float(totalConfirmAmount) > Amount:
                Amount = random.randint(0, 1000000)
            totalConfirmAmount = Amount
        else:
            pass
        self.GetRequest(url='/api/mobile/projectAdminService/getCompanyByCitySite.json',
                        data={'dealId': globals()['dealId']})
        self.PostRequest(url='/api/mobile/projectAdminService/adminInvoice',
                         data={'agentToken': globals()['token'],
                               'statementId': statementId,
                               'receiptSettleInfos': json.dumps(receiptSettleInfos,
                                                                ensure_ascii=False),    # 结算详情集合dealId
                               'totalCount': totalCount,    # 成交套数
                               'projectId': self.AgentTEXT.get('projectId'),
                               'totalConfirmAmount': totalConfirmAmount,   # 开票总额
                               'companyId': globals()['text']['extend']['sources'][0]['companyId'],
                               'companyName': globals()['text']['extend']['sources'][0]['companyName'],
                               'xftSettleInvoiceTitleJson':
                                   json.dumps(xftSettleInvoiceTitleJson, ensure_ascii=False),
                               'attachmentUrls': attachmentUrls,
                               'remark': remark,
                               'isApply': isApply})

    def PrecollectedList(self, advanceStatus=None, keyWord=None, value=0):
        """预收列表"""
        self.GetRequest(url='/api/mobile/projectAdminService/getAdvanceList',
                        data={'agentToken': globals()['token'],
                              'projectId': self.AgentTEXT.get('projectId'),
                              'advanceStatus': advanceStatus,
                              'keyWord': keyWord})
        if globals()['r.text']['extend']['count'] != 0:
            self.XMtext.set_map('advanceStatusStr',
                                globals()['r.text']['extend']['sources'][value]['advanceStatusStr'])

    def PrecollectedParticulars(self):
        """预收详情"""
        self.GetRequest(url='/api/mobile/projectAdminService/getAdvanceDetails',
                        data={'advanceId': globals()['r.text'],
                              'agentToken': globals()['token']})

    def GetSellerAndXFJMoney(self):
        """获取联盟商及幸福家佣金"""
        self.getDealTransactionAmount()
        if self.XFKTEXT.get('sellerType') == 'a':
            a = 0
            try:
                while globals()['r.text']['extend']['commission']['achievement'][a]['typeTitle'] != \
                        '佣金' or globals()['r.text']['extend']['commission']['achievement'][a]['sellerType'] != 'A':
                    a = a + 1
                self.XMtext.set_map('LMSYJ',
                                    globals()['r.text']['extend']['commission']['achievement'][a]['amountSum'])
            except:
                print("该成交单详情联盟商佣金不存在")
                self.XMtext.set_map('LMSYJ', 0)
        else:
            a = 0
            try:
                while globals()['r.text']['extend']['commission']['achievement'][a]['typeTitle'] != \
                        '佣金' or globals()['r.text']['extend']['commission']['achievement'][a]['sellerType'] != 'B':
                    a = a + 1
                self.XMtext.set_map('LMSYJ',
                                    globals()['r.text']['extend']['commission']['achievement'][a]['amountSum'])
            except:
                print("该成交单详情联盟商佣金不存在")
                self.XMtext.set_map('LMSYJ', 0)

        """以上是获取联盟商佣金"""
        a = 0
        try:
            while globals()['r.text']['extend']['commission']['achievement'][a]['typeTitle'] != \
                    '佣金' or globals()['r.text']['extend']['commission']['achievement'][a]['sellerType'] != 'X':
                a = a + 1
            self.XMtext.set_map('XFJYJ', globals()['r.text']['extend']['commission']['achievement'][a]['amountSum'])
        except:
            print("该成交单详情幸福家佣金不存在")
            self.XMtext.set_map('XFJYJ', 0)
        """以上是获取幸福家佣金"""

    def PrecollectedApply(self,
                          advanceId=None,       # 预收id主键传就是修改 不传
                          advancePic=img,
                          compare=0,        # 预付
                          compare1=0,       # 预收
                          citySiteId=citySiteId,
                          businuessType=2,
                          meanwhile=0,  # 是否同时录入
                          advanceRemark='预收预付' + time.strftime("%Y-%m-%d %H_%M_%S"),
                          isApply=1,
                          isAdvanceCollect=0):
        """预收|预付申请"""
        self.GetSellerAndXFJMoney()
        Amount = random.randint(0, 1000000)         # y预付
        dome = random.randint(0, 1000000)       # 预收

        if isAdvanceCollect == 1:    # 是否预收
            # 预收---------
            if compare1 == -1:
                while float(self.XMtext.get('XJFYJ')) > dome:
                    dome = random.randint(0, 1000000)
                    time.sleep(0.2)
                advanceTotalAmount = dome
            elif compare1 == 1:
                while float(self.XMtext.get('XJFYJ')) > dome:
                    dome = random.randint(0, 1000000)
                advanceTotalAmount = dome
            else:
                advanceTotalAmount = float(self.XMtext.get('XFJYJ'))
            if meanwhile == 1:
                #  预付----
                if compare == -1:
                    while float(self.XMtext.get('LMSYJ')) < Amount:
                        time.sleep(0.2)
                        Amount = random.randint(0, 1000000)
                    advancePayAmount = Amount
                elif compare == 1:
                    while float(self.XMtext.get('LMSYJ')) > Amount:
                        Amount = random.randint(0, 1000000)
                    advancePayAmount = Amount
                else:
                    advancePayAmount = float(self.XMtext.get('LMSYJ'))
            else:
                advancePayAmount = None
        else:
            if compare == -1:
                while float(self.XMtext.get('LMSYJ')) < Amount:
                    time.sleep(0.2)
                    Amount = random.randint(0, 1000000)
                advancePayAmount = Amount
            elif compare == 1:
                while float(self.XMtext.get('LMSYJ')) > Amount:
                    Amount = random.randint(0, 1000000)
                advancePayAmount = Amount
            else:
                advancePayAmount = float(self.XMtext.get('LMSYJ'))
        self.Payee(citySiteId, businuessType)
        if isAdvanceCollect == 0:
            payName=None,
            companyId=None
            companyName=None
            accountId=None
            bankBranchName=None
            bankAccount=None
            bankUserName=None
            advanceTotalAmount=None
            advanceDate=None
        else:
            payName = globals()['text1']['extend']['sources'][0]['companyName'],  # 收款方
            companyId = globals()['text1']['extend']['sources'][0]['companyId'],  # 结算公司
            companyName = globals()['text']['extend']['sources'][0]['bankName'],  # 公司名称
            accountId =  globals()['text']['extend']['sources'][0]['accountId'],
            # 结算银行账号ID
            bankBranchName = globals()['text']['extend']['sources'][0]['bankBranchName'],
            # 银行名称
            bankAccount = globals()['text']['extend']['sources'][0]['bankAccount'],
            # 银行账号
            bankUserName = globals()['text']['extend']['sources'][0]['bankUserName'],
            # 账户名
            advanceTotalAmount = advanceTotalAmount,  # 预收金额
            advanceDate = time.strftime("%Y-%m-%d"),  # 回款日期

        self.PostRequest(url='/api/mobile/projectAdminService/adminDealAdvance',
                         data={'agentToken': globals()['token'],
                               'advanceId': advanceId,
                               'dealId': self.XMtext.get('dealId'),
                               'payName': payName,  # 收款方
                               'companyId': companyId,  # 结算公司
                               'companyName': companyName,  # 公司名称
                               'accountId': accountId,      # 结算银行账号ID
                               'bankBranchName': bankBranchName,        # 银行名称
                               'bankAccount': bankAccount,          # 银行账号
                               'bankUserName': bankUserName,        # 账户名
                               'advanceTotalAmount': advanceTotalAmount,  # 预收金额
                               'advanceDate': advanceDate,          # 回款日期
                               'advancePayAmount': advancePayAmount,    # 付款金额
                               'advancePic': advancePic,        # 附件
                               'advanceRemark': advanceRemark,  # 备注
                               'isApply': isApply,      # 0：草稿 1：提交 默认草稿
                               'isAdvanceCollect': isAdvanceCollect})       # 是否预收 0：不是 1：是 默认不是

    def NoticeOfMakeOutAnInvoiceORUploadTheInvoiceList(self, invoiceStatus=0, isNotice=0, keyWord=None, value=0):
        """开票通知及上传发票列表
        invoiceStatus: 0 开票通知 1 上传发票
        isNotice： 0待通知  1 已通知
        keyWord： 关键字搜索"""
        self.GetRequest(url='/api/mobile/secretarySellerService/getPaymentRequest.json',
                        data={'agentToken': globals()['token'],
                              'invoiceStatus': invoiceStatus,
                              'isNotice': isNotice,
                              'keyWord': keyWord})
        self.XMtext.set_map('source', globals()['r.text']['extend']['source'])
        if keyWord == None:
            globals()['requestId'] = globals()['r.text']['extend']['source'][value]['requestId']
            self.XMtext.set_map('requestId', globals()['r.text']['extend']['source'][value]['requestId'])

    def InvoiceType(self, inoviceType=1):
        """确认发票类型
        inoviceType: 1 增值税普通发票  2增值税专用发票 3收据"""
        self.PostRequest(url='/api/mobile/secretarySellerService/updateInoviceType',
                         data={"agentToken": globals()['token'],
                               'requestId': globals()['requestId'],
                               'inoviceType': inoviceType})

    def NoticeOfMakeOutAnInvoice(self):
        """通知开票"""
        self.PostRequest(url='/api/mobile/secretarySellerService/noticeSellerInvoice',
                         data={'agentToken': globals()['token'],
                               'requestId': globals()['requestId']})

    def ReceiptAccountInvoice(self, keyWord=0):
        """收款账户---开票"""
        self.GetRequest(url='/api/mobile/secretarySellerService/getReceivablesAccountList.json',
                        data={'agentToken': globals()['token'],
                              'keyWord': keyWord,
                              'sellerId': self.AgentTEXT.get('sellerId')})

        #########要是为空自动添加一条------尚未写入

    def uploadingInvoice(self, sellerInvoiceNo, uploadType=1, imgs=img, value=0, taxRate='0.06'):
        """上传发票"""
        invoicePicList = {"fileSize": 9467, "width": 190, "height": 171, "attachmentUrl": imgs}
        self.PostRequest(url='/api/mobile/secretarySellerService/uploadInvoice',
                         data={'agentToken': globals()['token'],
                               'uploadType': uploadType,
                               'invoicePicList': "[" + json.dumps(invoicePicList, ensure_ascii=False) + "]",
                               'receiveBank': globals()['r.text']['extend']['source'][value]['bankBranchName'],
                               'sellerInvoiceNo': sellerInvoiceNo,
                               'invoiceDate': time.strftime("%Y-%m-%d"),
                               'receiveAccount': globals()['r.text']['extend']['source'][value]['bankAccount'],
                               'receiveName': globals()['r.text']['extend']['source'][value]['bankUserName'],
                               'requestId': self.XMtext.get('requestId'),
                               'taxRate': taxRate})

    def ForPerformance(self, dealId):
        """补业绩"""
        self.PostRequest(url='/api/mobile/projectAdminService/repairPerformance',
                         data={'agentToken': globals()['token'],
                               'dealId': dealId})

    def FillingWater(self, dealId):
        """补流水"""
        self.PostRequest(url='/api/mobile/projectAdminService/repairFlowing',
                         data={'agentToken': globals()['token'],
                               'dealId': dealId})

    def GetRequest(self, url, data):
        """GET请求"""
        r = self.do_request.to_request(method="get",
                                       url=(ApiXmUrl + url),
                                       data=data)
        r.raise_for_status()
        globals()['r.text'] = json.loads(r.text)
        globals()['text'] = globals()['r.text']
        self.XMtext.set_map('xmtext', globals()['r.text'])
        self.XMtext.set_map('xmurl', f"接口路径为:{url}")
        import time
        time.sleep(1)

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

    def PostRequest(self, url, data):
        """post请求"""
        r = self.do_request.to_request(method="post",
                                       url=(ApiXmUrl + url),
                                       data=data)
        r.raise_for_status()
        globals()['r.text'] = json.loads(r.text)
        self.XMtext.set_map('xmtext', globals()['r.text'])
        self.XMtext.set_map('xmcontent', globals()['r.text']['content'])
        self.XMtext.set_map('xmurl', f"接口路径为:{url}")
        self.XMtext.set_map('resultCode', globals()['r.text']['resultCode'])
        # assert globals()['r.text']['resultCode'], 1
        import time
        time.sleep(1)


if __name__ == '__main__':
    a = XmApi()
