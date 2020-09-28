# -*- coding: utf-8 -*-
# @Time    : 2019/11/15 14:36
# @Author  : 潘师傅
# @File    : FlowPath.py
"""幸福家主要流程"""
from XFJ.GlobalMap import GlobalMap
from XFJ.PubilcAPI.XmApi import *
from XFJ.PubilcAPI.AgentAPI import *
from XFJ.PubilcAPI.XfkApi import *
from XFJ.PubilcMethod.HandleRequest import *
from XFJ.PubilcMethod.LogIn import *
from XFJ.PubilcMethod.WebTools import *
# from XFJ.PubilcAPI.XfpApi import *
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait

import json


class FlowPath:
    """小秘----成交确认"""
    def __init__(self, *args, **kwargs):
        super(FlowPath, self).__init__(*args, **kwargs)
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
        self.NRTEXT = GlobalMap()
        self.city = LogIn()
        self.City = self.city
        self.Web = WebTools()
        self.WebTooles = self.Web

    @classmethod
    def setUpClass(cls):
        """登录小秘、幸福客 只执行一次"""
        cls.do_request = XmApi()
        cls.to_request = cls.do_request
        cls.to_request.ApiLogin()
        cls.do_request = XfkApi()
        cls.to_request = cls.do_request
        cls.to_request.LoginXfk()

    def TheNewDeal(self, user=AgentUesr):
        """新成交"""
        self.AgentRequest.LoginAgent(Uesr=user)
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
        try:
            self.XfkRequest.AttacheContract()
            assert self.XfkTEXT.get('resultCode'), 1
        except:
            self.XfkRequest.AttacheContract()
            assert self.XfkTEXT.get('resultCode'), 1
            pass

    def DealTicket(self):
        """成交确认"""
        self.XmRequest.DealTicketList()
        self.XmRequest.DealTicketParticulars()
        self.XmRequest.DealTicket()
        # self.XmRequest.DealTicketList(DealTicketType=2)
        # self.XmRequest.DealTicketParticulars()

    def ResultsTheChange(self, user=AgentUesr, signTime=0,TypeValue='调价及调佣', repetition=0, isSave=1, remark=None):
        # repetition  换房时  是否重复
        # audit 是否需要审核---城市中开票
        # repetition 房号是否重复
        # isSave 草稿
        # compare 比较
        self.TheNewDeal(user)
        self.DealTicket()
        if ApiXmUrl == 'http://api.xfj100.com':
            demo = self.XmRequest.RandomText(textArr=['50~100套', '两房', '三房', '复式', '别墅'])
        else:
            demo = self.XmRequest.RandomText(textArr=['一房', '两房', '复式', '写字楼', '三房'])
        demo1 = self.XmRequest.RandomText(textArr=['分期付款', '不限定', '按揭贷款'])
        # print(x, y)
        roomPriceTotal = random.randint(200000, 10000000)  # 成交总价
        squareBuilding = random.randint(20, 200)  # 面积
        customerMobile = '1' + (str(time.time()))[:10]
        if repetition == 1:
            self.XmRequest.ResultsTheChangeStayList(projectId=self.AgentTEXT.get('projectId'), value=1)
            globals()['roomNoStr'] = self.XmTEXT.get('roomNoStr')
            self.XmRequest.DealTicketParticulars()
            self.XmRequest.ResultsTheChangeStayList(projectId=self.AgentTEXT.get('projectId'))
        else:
            self.XmRequest.DealTicketParticulars()
            self.XmRequest.ResultsTheChangeStayList(
                projectId=self.AgentTEXT.get('projectId'), keyWord=self.XmTEXT.get('RoomNoStr'))
        self.XmRequest.ResultsTheChangeParticulars(dealChangeId=0)
        # globals()['xmtext'] = json.loads(json.dumps(json.loads(self.XmTEXT.get('xmtext')),
        #                                             indent=4, sort_keys=False, ensure_ascii=False))

        if TypeValue == '挞定':
            pass
        elif TypeValue == '更名' or TypeValue == '更换开票公司':
            if TypeValue == '更换开票公司':
                self.XmTEXT.set_map('company', '更换' + time.strftime("%Y-%m-%d"))
            else:
                self.XmTEXT.set_map('customerName', '更名')
                self.XmTEXT.set_map('customerMobile', customerMobile)

        elif TypeValue == '换房' or TypeValue == '调价及调佣':
            if repetition == 1:
                pass
            else:
                if TypeValue == '调价及调佣':
                    pass
                else:
                    self.XmTEXT.set_map('roomNoStr', f'{TypeValue}-' + (self.XmTEXT.get('roomNoStr'))[2:])
                self.XfkRequest.HouseType(houseTypeName=demo)

        if TypeValue == '换房':
            if signTime == 0:
                signTime = self.XmTEXT.get('signTime')
        if repetition == 1:
            self.XmTEXT.set_map('roomNoStr', globals()['roomNoStr'])
        self.XmRequest.ResultsTheChange(
            type=f'{TypeValue}', houseTypeId=self.XmTEXT.get('houseTypeId'),
            commissionRate=self.XmTEXT.get('XFJYJRete'),
            commissionRatePrice=self.XmTEXT.get('XFJYJAmount'),
            commissionSellerRate=self.XmTEXT.get('sellerYJRete'),
            commissionSellerPrice=self.XmTEXT.get('sellerYJAmount'),
            roomPriceTotal=roomPriceTotal,
            changePic=img,
            roomNoStr=self.XmTEXT.get('roomNoStr'),
            signTime=signTime,
            customerName=self.XmTEXT.get('customerName'),
            customerMobile=self.XmTEXT.get('customerMobile'),
            squareBuilding=squareBuilding,
            paymentMethod=demo1,
            changeDesc=f'{TypeValue}' + time.strftime("%Y-%m-%d %H:%M:%S"),
            isSave=isSave,
            sellerFullName=self.XmTEXT.get('company'),
            remark=remark)
        if repetition == 1:
            assert self.XmTEXT.get('xmcontent'), '房号不能重复'
        else:
            if self.XmTEXT.get('xmcontent') == '应付佣金超过了应收代理费':
                pass
            else:
                assert 1, self.XmTEXT.get('ResultCode')

        """审核前后的对比"""
        if TypeValue == '更名':
            self.XmRequest.ResultsTheChangeList(projectId=self.AgentTEXT.get('projectId'))
            globals()['xmtext'] = json.loads(json.dumps(json.loads(self.XmTEXT.get('xmtext')),
                                                        indent=4, sort_keys=False, ensure_ascii=False))
            assert self.XmTEXT.get('changeStatusStr'), '已通过'
            assert self.XmTEXT.get('changeTypeStr'), '更名'
        elif TypeValue == '更换开票公司' or TypeValue == '挞定':
            self.XmRequest.ResultsTheChangeList(projectId=self.AgentTEXT.get('projectId'))
            self.XmRequest.ResultsTheChangeParticulars()
            globals()['xmtext'] = json.loads(json.dumps(json.loads(self.XmTEXT.get('xmtext')),
                                                        indent=4, sort_keys=False, ensure_ascii=False))
            if TypeValue == '更换开票公司':
                assert ('更换' + time.strftime("%Y-%m-%d")), globals()['xmtext']['extend']['companyNew']
            self.XmRequest.ResultsTheChangeList(projectId=self.AgentTEXT.get('projectId'))
            self.XmRequest.ResultsTheChangeAudit(type=f"{TypeValue}")
            self.XmRequest.ResultsTheChangeList(projectId=self.AgentTEXT.get('projectId'))
            globals()['xmtext'] = json.loads(json.dumps(json.loads(self.XmTEXT.get('xmtext')),
                                                        indent=4, sort_keys=False, ensure_ascii=False))
            assert self.XmTEXT.get('changeStatusStr'), '已通过'
            assert self.XmTEXT.get('changeTypeStr'), f'{TypeValue}'
            if TypeValue == '更换开票公司':
                self.XmRequest.ResultsTheChangeParticulars()
                globals()['xmtext'] = json.loads(json.dumps(json.loads(self.XmTEXT.get('xmtext')),
                                                            indent=4, sort_keys=False, ensure_ascii=False))
                assert ('更换' + time.strftime("%Y-%m-%d")), globals()['xmtext']['extend']['company']
            if TypeValue == '挞定':
                self.XfkRequest.ExamineClientParticulars()
                globals()['xfktext'] = json.loads(json.dumps(json.loads(self.XmTEXT.get('XFKtext')),
                                                             indent=4, sort_keys=False, ensure_ascii=False))
                assert '终止', globals()['xfktext']['extend']['customerPrjStatusName']
                assert '变更挞定', globals()['xfktext']['extend']['followList'][0]['content']
                assert '挞定', globals()['xfktext']['extend']['followList'][1]['content']
                """作废后查看客户详情"""
                self.XfkRequest.ExamineClientParticulars()
                globals()['xfktext'] = json.loads(json.dumps(json.loads(self.XmTEXT.get('XFKtext')),
                                                             indent=4, sort_keys=False, ensure_ascii=False))
                assert '终止', globals()['xfktext']['extend']['customerPrjStatusName']
                assert '变更挞定', globals()['xfktext']['extend']['followList'][0]['content']
                assert '小秘', globals()['xfktext']['extend']['followList'][0]['createUserName']
        else:
            if repetition == 1:
                pass
            else:
                a = 1
                while a != 3:
                    time.sleep(2)
                    # if audit == 0:
                    """差值是否小于5000"""
                    if a == 1 and (TypeValue == '调价及调佣' or TypeValue == '换房'):
                        self.XmRequest.ResultsTheChangeList(projectId=self.AgentTEXT.get('projectId'))
                        if self.XmTEXT.get('changeStatusStr') == '已通过':
                            a = 2
                        else:
                            a = 1
                    self.XmRequest.ResultsTheChangeList(projectId=self.AgentTEXT.get('projectId'),
                                                        dealId=self.XmTEXT.get('dealId'))
                    self.XmRequest.ResultsTheChangeParticulars()
                    globals()['xmtext'] = json.loads(json.dumps(json.loads(self.XmTEXT.get('xmtext')),
                                                                indent=4, sort_keys=False, ensure_ascii=False))
                    """户型ID、户型名字、签约总价、应收比例、额外比例、应收总额"""
                    if a == 1:
                        b = 'New'
                    else:
                        b = ''
                    """对比的数据有：户型ID、代理费总额、签约总价"""
                    assert "%.2f" % self.XmTEXT.get('commissionPrice'), \
                        "%.2f" % (globals()['xmtext']['extend']['commissionPrice' + b])
                    assert float(roomPriceTotal), float(globals()['xmtext']['extend']['roomPriceTotal' + b])
                    if a == 1:
                        """审核"""
                        time.sleep(5)
                        self.XmRequest.ResultsTheChangeAudit(type=f'{TypeValue}')
                    else:
                        pass
                    a = a + 1

    def CityEstablishMessage(self):
        """新成交--城市发票申请"""
        self.TheNewDeal()
        self.DealTicket()
        self.WebTooles.Openbrowser()
        self.city.LogIn(method='City', d=self.WebTooles.driver)
        """收款管理---新建发票申请"""
        self.WebTooles.Click(type='link_text', value='收款模块')
        self.WebTooles.Click(type='link_text', value='新建发票申请')
        self.WebTooles.Click(type='id', value='s2id_projectSelect')
        time.sleep(2)
        self.WebTooles.Input(type='id', value='s2id_autogen4_search', inputvalue=ProjectName)
        self.WebTooles.Click(type='xpath', value='//*[@id="select2-results-4"]/li/ul/li')
        self.WebTooles.Click(type='id', value='s2id_companySelect')  # 结算公司
        self.WebTooles.Click(type='xpath', value='//*[@id="select2-results-3"]/li[1]')
        self.WebTooles.Click(type='id', value='settleTitleSelect')     # 发票抬头
        self.WebTooles.Click(type='xpath', value='//*[@id="invoiceTitleFieldset"]/div[5]/div/ul/li[1]')
        self.WebTooles.Input(type='id', value='invoiceRemark',
                             inputvalue='新建发票申请' + time.strftime("%Y-%m-%d"))  # 其他要求
        self.WebTooles.Click(type='class', value='btn-next')        # 下一步
        self.WebTooles.Click(type='id', value='selroom')
        self.WebTooles.Input(type='id', value='keyWord', inputvalue=self.XfkTEXT.get('RoomNoStr'))
        self.WebTooles.Click(type='id', value='searchSeller')
        time.sleep(0.5)
        self.WebTooles.Click(type='class', value='checker')
        self.WebTooles.Click(type='id', value='btnconfirm')     # 确定
        self.WebTooles.Click(type='id', value='confirmRatioBtn')    # 弹框确定
        # 需要进行调整
        self.WebTooles.Click(type='link_text', value='调整')
        time.sleep(0.5)
        self.WebTooles.driver.find_element_by_id('currentInvoiceAmount').clear()
        self.WebTooles.Input(type='id', value='currentInvoiceAmount',
                             inputvalue=str(self.XfkTEXT.get('sellerMoney')))
        self.WebTooles.driver.find_element_by_id('currentHandleAmount').clear()
        self.WebTooles.Input(type='id', value='currentHandleAmount',
                             inputvalue=str(self.XfkTEXT.get('sellerMoney')))
        time.sleep(0.5)
        self.WebTooles.Click(type='id', value='adoptIsPassDealChangeAudit')

        self.WebTooles.Click(type='class', value='btn-next')        # 下一步
        self.WebTooles.Click(type='id', value='submitBtn')          # 提交
        SQDH = self.WebTooles.driver.find_element_by_id('popStatementNoSpan').text
        self.WebTooles.Click(type='id', value='addNewRequisitionBtn')       # 确定

        self.WebTooles.Click(type='link_text', value='发票申请确认')     # 进入确认
        self.WebTooles.Input(type='id', value='keyWord', inputvalue=SQDH)       # 输入审核单号
        self.WebTooles.Click(type='link_text', value='查询')
        time.sleep(0.2)
        self.WebTooles.Click(type='link_text', value='查看')
        self.WebTooles.Current_handel()     # 切换到新的窗口
        ##############################################################
        # 要是没有计提公式的  需要添加-----该操作尚未写入
        self.WebTooles.Input(type='id', value='auditRemark',
                             inputvalue='发票申请审核确认' + time.strftime("%Y-%m-%d"))
        time.sleep(0.2)
        self.WebTooles.Click(type='id', value='addButton')
        time.sleep(3)
        self.WebTooles.driver.quit()
        self.WebTooles.Openbrowser()
        self.city.LogIn(method='City', d=self.WebTooles.driver)
        self.WebTooles.Click(type='link_text', value='收款模块')
        if CityUrl == 'http://city.xfj100.com':
            self.WebTooles.Click(type='link_text', value='开票登记')
        elif CityUrl == 'http://city.ykb100.com':
            self.WebTooles.Click(type='link_text', value='发票登记')
        else:
            self.WebTooles.Click(type='link_text', value='开票登记')
        self.WebTooles.Click(type='id', value='s2id_projectSelect')
        self.WebTooles.Input(type='id', value='s2id_autogen1_search', inputvalue=ProjectName)
        self.WebTooles.Click(type='xpath', value='//*[@id="select2-results-1"]/li/ul')
        dome = self.WebTooles.driver.find_element_by_xpath('//*[@id="dealTable"]/tbody/tr[1]/td[1]').text
        if dome == SQDH:
            pass
        else:
            print('申请单号错误')
        self.WebTooles.driver.find_element_by_xpath('//*[@id="dealTable"]/tbody/tr[1]/td[9]/a[1]').click()
        # self.WebTooles.Click(type='link_text', value='开票登记')
        KPJE = (self.WebTooles.driver.find_element_by_id(
            'step3TotalInvoiceAmount').text).replace(',', '')
        text1 = self.WebTooles.driver.find_element_by_id('step3TotalInvoiceAmount').text
        self.WebTooles.Click('id', value='invoiceTime')
        self.WebTooles.NewIframe('#_my97DP > iframe')
        self.WebTooles.Click(type='id', value='dpTodayInput')
        self.WebTooles.QuitIframe()
        self.WebTooles.Input(type='id', value='cityInvoiceNo',
                             inputvalue=time.strftime("%y%m%d"))
        time.sleep(2)
        self.WebTooles.Click(type='id', value='addButton')      # 保存
        self.WebTooles.Click(type='id', value='button-0')       # 确定

        self.WebTooles.Click(type='link_text', value='收款登记')
        self.WebTooles.Click(type='id', value='s2id_projectSelect')     # 项目
        self.WebTooles.Input(type='id', value='s2id_autogen1_search', inputvalue=ProjectName)
        self.WebTooles.Click(type='xpath', value='//*[@id="select2-results-1"]/li/ul')

        self.WebTooles.Click(type='id', value='paymentNameSelect')      # 付款方户名
        self.WebTooles.Click(type='xpath', value='//*[@id="span6"]/div[1]/div/ul/li[1]')

        self.WebTooles.Click(type='id', value='payeeNameSelect')        # 收款方户名
        self.WebTooles.Click(type='xpath', value='//*[@id="span7"]/div[1]/div/ul/li[1]')

        self.WebTooles.Input(type='id', value='amount', inputvalue=KPJE)    # 输入开票金额
        self.WebTooles.Input(type='xpath', value='//*[@id="remark"]',
                             inputvalue='收款登记' + time.strftime("%y-%m-%d"))  # 备注
        time.sleep(3)
        self.WebTooles.Click(type='id', value='submitReceiptButton')        # 确认提交
        self.WebTooles.Click(type='id', value='submitReceiptButton')        # 确认提交
        time.sleep(1)

        self.WebTooles.Click(type='link_text', value='收款核销')
        self.WebTooles.Click('id', value='receivedTime')  # 收款日期
        self.WebTooles.NewIframe('#_my97DP > iframe')
        self.WebTooles.Click(type='id', value='dpTodayInput')
        self.WebTooles.QuitIframe()
        self.WebTooles.Click('xpath', value='//*[@id="pageForm"]/a')
        # self.WebTooles.driver.find_elements_by_class_name('btn-primary')[0].click()
        dome4 = 1
        dome3 = self.WebTooles.driver.find_element_by_xpath(
            '//*[@id="dealtableReceived"]/tbody/tr[' + str(dome4) + ']/td[8]').text
        try:
            while dome3 != text1:
                dome4 = dome4 + 1
                time.sleep(0.5)
                dome3 = self.WebTooles.driver.find_element_by_xpath(
                    '//*[@id="dealtableReceived"]/tbody/tr[' + str(dome4) + ']/td[8]').text
            self.WebTooles.driver.find_element_by_xpath(
                '//*[@id="dealtableReceived"]/tbody/tr[' + str(dome4) + ']/td[8]').click()
        except Exception as e:
            print(e)
            self.WebTooles.driver.find_element_by_xpath(
                '//*[@id="dealtableReceived"]/tbody/tr[' + str('1') + ']/td[8]').click()
        time.sleep(2)
        dome2 = 1
        dome1 = self.WebTooles.driver.find_element_by_xpath(
            '//*[@id="dealtableStatement"]/tbody/tr[' + str(dome2) + ']/td[7]').text
        while dome1 != text1:
            dome2 = dome2 + 1
            time.sleep(0.5)
            dome1 = self.WebTooles.driver.find_element_by_xpath(
                '//*[@id="dealtableStatement"]/tbody/tr[' + str(dome2) + ']/td[7]').text
        self.WebTooles.driver.find_element_by_xpath(
            '//*[@id="dealtableStatement"]/tbody/tr[' + str(dome2) + ']/td[1]/input').click()
        self.WebTooles.Click(type='link_text', value='下一步')
        self.WebTooles.Click(type='link_text', value='确认核销')
        time.sleep(0.3)
        self.WebTooles.Click(type='id', value='button-0')       # 确定
        time.sleep(2)
        HXDH = self.WebTooles.driver.find_element_by_xpath('//*[@id="writeOffTable"]/tbody/tr/td[2]').text
        """付款模块"""
        self.WebTooles.Click(type='link_text', value='付款模块')
        self.WebTooles.Click(type='link_text', value='付款通知管理')
        # """创建付款申请"""
        self.WebTooles.Click(type='link_text', value='收起')
        self.WebTooles.driver.find_elements_by_class_name('btn-success')[0].click()
        self.WebTooles.Current_handel()
        self.WebTooles.Click(type='id', value='s2id_projectSelect')     # 项目
        self.WebTooles.Input(type='id', value='s2id_autogen1_search', inputvalue=ProjectName)
        self.WebTooles.driver.find_elements_by_class_name('select2-results-dept-0')[0].click()
        self.WebTooles.Click(type='id', value='select2-chosen-2')
        self.WebTooles.Input(type='id', value='s2id_autogen2_search', inputvalue=HXDH)  # 直接填写回销单
        self.WebTooles.Click(type='id', value='select2-results-2')
        self.WebTooles.Click(type='id', value='uniform-confirmSelectAllTh')  # 全选
        time.sleep(2)
        self.WebTooles.Click(type='class_name', value='btn-next')
        time.sleep(1)
        self.WebTooles.Click(type='id', value='saveBtn')
        # 关闭浏览器 重新打开
        self.WebTooles.driver.quit()
        self.WebTooles.Openbrowser()
        self.city.LogIn(method='City', d=self.WebTooles.driver)
        self.WebTooles.Click(type='link_text', value='付款模块')
        self.WebTooles.Click(type='link_text', value='付款通知管理')
        self.WebTooles.driver.refresh()
        self.WebTooles.Input(type='id', value='keyWord', inputvalue=self.AgentTEXT.get('ClientNeme'))
        self.WebTooles.Click(type='xpath', value='//*[@id="pageForm"]/a')
        self.WebTooles.WebDriverWait(type='id', value='dealTable_length')
        self.WebTooles.driver.find_element_by_id('dealTable_length').click()
        self.WebTooles.driver.find_element_by_class_name('mini-btn').click()
        try:
            self.WebTooles.Click(type='id', value='uniform-confirmSelectAllTh')
        except BaseException as e:
            print("断言错误，错误原因：%s" % e)
            self.WebTooles.driver.find_element_by_id('dealTable_length').click()
            self.WebTooles.Click(type='id', value='uniform-confirmSelectAllTh')  # 全选
        self.WebTooles.Click(type='class', value='icon-upload')
        self.WebTooles.Click(type='id', value='button-0')
        self.WebTooles.driver.refresh()
        self.WebTooles.Click(type='link_text', value='付款通知审核')
        self.WebTooles.Input(type='id', value='keyWord', inputvalue=self.AgentTEXT.get('ClientNeme'))
        self.WebTooles.Click(type='xpath', value='//*[@id="pageForm"]/a')
        self.WebTooles.Click(type='id', value='uniform-confirmSelectAllTh')  # 全选
        self.WebTooles.driver.find_elements_by_link_text('审核通过')[0].click()
        # self.WebTooles.Click(type='id', value='uniform-invoiceCheck')   # 是否上传发票  默认上传
        self.WebTooles.driver.find_elements_by_link_text('审核通过')[2].click()
        time.sleep(2)
        self.WebTooles.Click(type='id', value='button-0')  # 确定
        time.sleep(0.5)
        self.WebTooles.driver.quit()

    def TheReceivableReview(self, tpyeName='收款付款'):
        """现金收款 | 付款审核"""
        if tpyeName == '收款付款':
            dome = '现金回款确认'
            self.XmRequest.CashCollectionList()
        else:
            dome = '预收款确认'
            self.XmRequest.PrecollectedList()
        if self.XmTEXT.get('cashStatusStr') == '财务确认中' or self.XmTEXT.get('advanceStatusStr') == '财务确认中':
            self.WebTooles.Openbrowser()
            self.city.LogIn(method='City', d=self.WebTooles.driver)
            self.WebTooles.Click(type='link_text', value='收款模块')
            self.WebTooles.Click(type='link_text', value=dome)
            self.WebTooles.Click(type='link_text', value='收起')
            self.WebTooles.Input(type='id', value='keyWord', inputvalue=self.XfkTEXT.get('RoomNoStr'))
            self.WebTooles.Click(type='id', value='closeSelect')
            self.WebTooles.Click(type='link_text', value='查看')
            # self.WebTooles.Click(type='xpath', value='//*[@id="dealTable"]/tbody/tr/td[16]/a')
            self.WebTooles.Click(type='id', value='adoptIsPassDealChangeAudit')
            self.WebTooles.Click(type='id', value='button-0')
            if tpyeName == '收款付款':
                self.XmRequest.CashCollectionList()
            else:
                self.XmRequest.PrecollectedList()
            if self.XmTEXT.get('cashStatusStr') == '已通过':
                pass
            self.WebTooles.driver.quit()
        elif self.XmTEXT.get('cashStatusStr') == '已通过' or self.XmTEXT.get('advanceStatusStr') == '已通过':
            pass
        else:
            self.WebTooles.Openbrowser()
            self.city.LogIn(method='City', d=self.WebTooles.driver)
            self.WebTooles.Click(type='link_text', value='预付和变更审核')
            self.WebTooles.Click(type='xpath', value='//*[@id="collapse5"]/li[1]/a/span')
            self.WebTooles.Click(type='xpath', value='//*[@id="s2id_approveType"]/a')
            if tpyeName == '收款付款':
                dome1 = '现金付款'
            else:
                dome1 = '预收预付'
            self.WebTooles.Input(type='id', value='s2id_autogen2_search', inputvalue=dome1)
            self.WebTooles.Click(type='id', value='select2-results-2')
            self.WebTooles.Input(type='id', value='keyWord', inputvalue=self.XfkTEXT.get('RoomNoStr'))
            self.WebTooles.Click(type='link_text', value='查询')
            time.sleep(0.5)
            text = self.WebTooles.driver.find_element_by_id('dealTable_info').text
            if text == '显示第 0 至 0 项结果，共 0 项':
                self.WebTooles.Click(type='link_text', value='财务确认')
                self.WebTooles.Click(type='id', value='s2id_approveType')
                self.WebTooles.Input(type='id', value='s2id_autogen2_search', inputvalue=dome1)
                self.WebTooles.Click(type='xpath', value='//*[@id="select2-results-2"]')
                self.WebTooles.Input(type='id', value='keyWord', inputvalue=self.XfkTEXT.get('RoomNoStr'))
                self.WebTooles.Click(type='link_text', value='查询')
                text = self.WebTooles.driver.find_element_by_id('dealTable_info').text
                if text == '显示第 0 至 0 项结果，共 0 项':
                    pass
                else:
                    self.WebTooles.Click(type='link_text', value='查看')
                    self.WebTooles.Click(type='link_text', value='通过')
                    self.WebTooles.Click(type='id', value='button-0')
                    time.sleep(1)
                    self.WebTooles.driver.quit()
                    self.TheReceivableReview(tpyeName=f"{tpyeName}")
            else:
                self.WebTooles.Click(type='link_text', value='查看')
                self.WebTooles.Click(type='id', value='adoptIsPassDealChangeAudit2')
                self.WebTooles.Click(type='id', value='button-0')
                time.sleep(1)
                self.WebTooles.driver.quit()
                self.TheReceivableReview(tpyeName=f"{tpyeName}")


if __name__ == '__main__':
    a = FlowPath()
