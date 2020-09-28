# -*- coding: utf-8 -*-
# @Time    : 2019/11/4 9:34
# @Author  : 潘师傅
# @File    : Project_InvoiceTitle_casc.py

import unittest
from XFJ.PubilcAPI.XmApi import *
from XFJ.PubilcAPI.AgentAPI import *
import json
import time


class InvoiceTitleTestCace(unittest.TestCase):
    """小秘----项目---发票抬头"""
    def __init__(self, *args, **kwargs):
        super(InvoiceTitleTestCace, self).__init__(*args, **kwargs)
        self.do_request = XmApi()
        self.XmRequest = self.do_request
        self.XmTEXT = GlobalMap()
        self.AgentRequest = AgentApi()
        self.ToAgentRequest = self.AgentRequest
        self.AgentTEXT = GlobalMap()

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

    @classmethod
    def tearDownClass(cls):
        """所用用例执行之后的操作"""
        pass

    def test_ADDInvoiceTitle(self):
        """新增发票抬头"""
        try:
            self.XmRequest.ADDInvoiceTitle(titleName='测试发票抬头', titleDuty='税号',
                                           companyLocation=None, bankName=None, accountPhone=None,
                                           bankAccount=None, projectId=self.AgentTEXT.get('projectId'))
            self.assertEqual('操作成功', self.XmTEXT.get('xmcontent'))
            self.XmRequest.InvoiceTitleList(projectId=self.AgentTEXT.get('projectId'))
            self.XmRequest.InvoiceTitleParticulars(projectId=self.AgentTEXT.get('projectId'))
            globals()['r.text'] = json.loads(self.XmTEXT.get('xmtext'))
            self.assertEqual(self.XmTEXT.get('projectId'), str(globals()['r.text']['extend']['projectId']))
            self.assertEqual('测试发票抬头', globals()['r.text']['extend']['titleName'])
            self.assertEqual('税号', globals()['r.text']['extend']['titleDuty'])
        except BaseException as e:
            print("错误，错误原因：%s" % e)
            raise RuntimeError(self.XmTEXT.get('xmurl'))

    def test_AlterInvoiceTitle(self):
        """修改发票抬头"""
        try:
            self.XmRequest.InvoiceTitleList(projectId=self.AgentTEXT.get('projectId'))
            self.XmRequest.AlterInvoiceTitle(
                titleName=time.strftime("%Y-%m-%d") + '测试发票抬头',       # *名称
                titleDuty='SH' + str(PhoneFront),                           # *税号
                companyLocation='广东省珠海市香洲区海洲路8号九昌大厦',      # 单位地址
                bankName='中国建设银行珠海市九昌大厦分店',                  # 开户银行
                accountPhone='0597-63765499',                               # 电话号码
                bankAccount=145454644445555551,                             # 银行账号
                titleId=self.XmTEXT.get('titleId'))
            self.assertEqual('操作成功', self.XmTEXT.get('xmcontent'))
            self.XmRequest.InvoiceTitleList(projectId=self.AgentTEXT.get('projectId'))
            self.XmRequest.InvoiceTitleParticulars(projectId=self.AgentTEXT.get('projectId'))
            globals()['r.text'] = json.loads(self.XmTEXT.get('xmtext'))
            self.assertEqual(self.XmTEXT.get('projectId'), str(globals()['r.text']['extend']['projectId']))
            self.assertEqual(self.XmTEXT.get('AltertitleName'), globals()['r.text']['extend']['titleName'])
            self.assertEqual(self.XmTEXT.get('AltertitleDuty'), globals()['r.text']['extend']['titleDuty'])
            self.assertEqual(self.XmTEXT.get('AltercompanyLocation'),
                             globals()['r.text']['extend']['companyLocation'])
            self.assertEqual(self.XmTEXT.get('AlterbankName'), globals()['r.text']['extend']['bankName'])
            self.assertEqual(self.XmTEXT.get('AlteraccountPhone'), globals()['r.text']['extend']['accountPhone'])
            self.assertEqual(self.XmTEXT.get('AlterbankAccount'), globals()['r.text']['extend']['bankAccount'])

        except BaseException as e:
            print("错误，错误原因：%s" % e)
            raise RuntimeError(self.XmTEXT.get('xmurl'))



