# -*- coding: utf-8 -*-
# @Time    : 2019/12/7 9:36
# @Author  : 潘师傅
# @File    : Project_InvoiceManagement_casc.py
"""发票管理"""
from XFJ.PubilcAPI.FlowPath import *


class InvoiceManagement(unittest.TestCase):
    """小秘----项目---发票管理"""
    """
        异地A   1异地A  2异地C  3本地A  4本地C  5普通C
        异地C   2异地C  3本地A  4本地C  5普通C
        本地A   3本地A  4本地C  5普通C
        本地C   4本地C  5普通C
        普通C   5普通C
    """
    def __init__(self, *args, **kwargs):
        super(InvoiceManagement, self).__init__(*args, **kwargs)
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



