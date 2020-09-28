# -*- coding: utf-8 -*-
# @Time    : 2019/12/14 10:40
# @Author  : 潘师傅
# @File    : UploadTheInvoice_casc.py

"""通知开票/上传发票"""

from XFJ.PubilcAPI.FlowPath import *


class TestCase(unittest.TestCase):
    """小秘----通知开票/上传发票"""
    def __init__(self, *args, **kwargs):
        super(TestCase, self).__init__(*args, **kwargs)
        self.do_request = XmApi()
        self.XmRequest = self.do_request
        self.XmTEXT = GlobalMap()
        self.AgentRequest = AgentApi()
        self.ToAgentRequest = self.AgentRequest
        self.AgentTEXT = GlobalMap()
        self.Xfk_request = XfkApi()
        self.XfkRequest = self.Xfk_request
        self.XfkTEXT = GlobalMap()
        self.FlowPath = FlowPath()
        self.FlowPath = self.FlowPath
        self.city = LogIn()
        self.City = self.city
        self.Web = WebTools()
        self.WebTooles = self.Web

    @classmethod
    def setUpClass(cls):
        """登录小秘 只执行一次
        登录经纪人 获取ID"""
        cls.do_request = XmApi()
        cls.XmRequest = cls.do_request
        cls.XmRequest.ApiLogin()
        cls.request = AgentApi()
        cls.AgentRequest = cls.request
        cls.AgentRequest.LoginAgent()
        cls.AgentRequest.ForRegistrationID()
        cls.do_request = XfkApi()
        cls.to_request = cls.do_request
        cls.to_request.LoginXfk()
        cls.FP = FlowPath()
        cls.FlowPath = cls.FP
        cls.FlowPath.CityEstablishMessage()   # 新做数据

    def test_01(self):
        """新数据验证搜索功能"""
        try:
            self.XmRequest.NoticeOfMakeOutAnInvoiceORUploadTheInvoiceList(keyWord=self.AgentTEXT.get('ClientNeme'))
            self.assertEqual([], self.XmTEXT.get('source'))
            self.XmRequest.NoticeOfMakeOutAnInvoiceORUploadTheInvoiceList(keyWord=XmSellerName)
            self.assertNotEqual([], self.XmTEXT.get('source'))
            self.XmRequest.NoticeOfMakeOutAnInvoiceORUploadTheInvoiceList(keyWord='房号')
            self.assertNotEqual([], self.XmTEXT.get('source'))
        except BaseException as e:
            print("断言错误，错误原因：%s" % e)
            raise RuntimeError(self.XmTEXT.get('xmurl'))

    def test_02(self):
        """确认发票类型"""
        try:
            self.XmRequest.NoticeOfMakeOutAnInvoiceORUploadTheInvoiceList()
            self.XmRequest.InvoiceType()
            self.assertEqual('发票类型已确认', self.XmTEXT.get('xmcontent'))
        except BaseException as e:
            print("断言错误，错误原因：%s" % e)
            raise RuntimeError(self.XmTEXT.get('xmurl'))

    def test_03(self):
        """通知开票"""
        try:
            self.XmRequest.NoticeOfMakeOutAnInvoiceORUploadTheInvoiceList()
            self.XmRequest.NoticeOfMakeOutAnInvoice()
            self.assertEqual('通知成功！', self.XmTEXT.get('xmcontent'))
        except BaseException as e:
            print("断言错误，错误原因：%s" % e)
            raise RuntimeError(self.XmTEXT.get('xmurl'))

    def test_04(self):
        """已通知列表验证"""
        try:
            self.XmRequest.NoticeOfMakeOutAnInvoiceORUploadTheInvoiceList(
                keyWord=self.AgentTEXT.get('ClientNeme'), isNotice=1)
            self.assertEqual([], self.XmTEXT.get('source'))
            self.XmRequest.NoticeOfMakeOutAnInvoiceORUploadTheInvoiceList(keyWord=XmSellerName, isNotice=1)
            self.assertNotEqual([], self.XmTEXT.get('source'))
            self.XmRequest.NoticeOfMakeOutAnInvoiceORUploadTheInvoiceList(keyWord='房号', isNotice=1)
            self.assertNotEqual([], self.XmTEXT.get('source'))
        except BaseException as e:
            print("断言错误，错误原因：%s" % e)
            raise RuntimeError(self.XmTEXT.get('xmurl'))

    def test_05(self):
        """待上传进行验证"""
        try:
            self.XmRequest.NoticeOfMakeOutAnInvoiceORUploadTheInvoiceList(
                keyWord=self.AgentTEXT.get('ClientNeme'), invoiceStatus=1)
            self.assertEqual([], self.XmTEXT.get('source'))
            self.XmRequest.NoticeOfMakeOutAnInvoiceORUploadTheInvoiceList(keyWord=XmSellerName, invoiceStatus=1)
            self.assertNotEqual([], self.XmTEXT.get('source'))
            self.XmRequest.NoticeOfMakeOutAnInvoiceORUploadTheInvoiceList(keyWord='房号', invoiceStatus=1)
            self.assertNotEqual([], self.XmTEXT.get('source'))

        except BaseException as e:
            print("断言错误，错误原因：%s" % e)
            raise RuntimeError(self.XmTEXT.get('xmurl'))

    def test_06(self):
        """上传发票"""
        try:
            self.XmRequest.NoticeOfMakeOutAnInvoiceORUploadTheInvoiceList(invoiceStatus=1)
            self.XmRequest.ReceiptAccountInvoice()
            self.XmRequest.uploadingInvoice(sellerInvoiceNo="自动化发票号：" + time.strftime("%y-%m-%d"))
            self.assertEqual('上传成功！', self.XmTEXT.get('xmcontent'))
        except BaseException as e:
            print("断言错误，错误原因：%s" % e)
            raise RuntimeError(self.XmTEXT.get('xmurl'))

    def test_07(self):
        """已上传进行验证"""
        try:
            self.XmRequest.NoticeOfMakeOutAnInvoiceORUploadTheInvoiceList(keyWord=self.AgentTEXT.get('ClientNeme'),
                                                                          invoiceStatus=2)
            self.assertEqual([], self.XmTEXT.get('source'))
            self.XmRequest.NoticeOfMakeOutAnInvoiceORUploadTheInvoiceList(keyWord=XmSellerName,
                                                                          invoiceStatus=2)
            self.assertNotEqual([], self.XmTEXT.get('source'))
            self.XmRequest.NoticeOfMakeOutAnInvoiceORUploadTheInvoiceList(keyWord='房号',
                                                                          invoiceStatus=2)
            self.assertNotEqual([], self.XmTEXT.get('source'))
        except BaseException as e:
            print("断言错误，错误原因：%s" % e)
            raise RuntimeError(self.XmTEXT.get('xmurl'))




