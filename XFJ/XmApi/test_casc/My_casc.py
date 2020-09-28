"""幸福小秘---我的"""
# 第一步 导入unittest模块
from XFJ.PubilcAPI.XmApi import *
import requests
import unittest
from XFJ.GlobalMap import GlobalMap
# 第二步 编写测试用例
"""
1、回款查询
2、付款查询
3、带关键字 付款查询
4、添加话术、是否可以在列表中显示
5、添加话术、内容为空是否有相应的提示
6、添加话术、内容过长是否有相应的提示
7、修改话术、不同类型下进行修改并且列表是否可见
8、删除所有话术、保留原有的话术

"""


class MyTestCase(unittest.TestCase):
    """小秘——我的"""

    def __init__(self, *args, **kwargs):
        super(MyTestCase, self).__init__(*args, **kwargs)
        self.do_request = XmApi()
        self.to_request = self.do_request
        self.XmTEXT = GlobalMap()

    def setUp(self):
        # 每条用例开始前
        """登录"""
        self.to_request.ApiLogin()

    def tearDown(self):
        # 每条用例结束后
        """9、删除所有话术"""
        self.to_request.DelVerbalTrick()

    def test_The_receivable_queries(self):
        """回款查询"""
        self.to_request.The_receivable_queries()

    def test_Payment_query_keyword_is_None(self):
        """付款查询"""
        self.to_request.Payment_query(keyWord=None)

    def test_Payment_query_keyword(self):
        """付款查询带关键字"""
        self.to_request.Payment_query(keyWord="AAA")

    def test_AddVerbalTrick_list_of_visible(self):
        """添加话术、是否可以在列表中显示"""
        self.to_request.AddVerbalTrick(content="这是一条话术", label="上班#")
        self.to_request.VerbalTrickList(label="上班", content='这是一条话术')

    def test_AddVerbalTrick_content_is_null(self):
        """添加话术、内容为空是否有相应的提示"""
        self.to_request.AddVerbalTrick(content=None, label="上班#")
        self.assertEqual('内容不能为空', self.XmTEXT.get('xmcontent'))

    def test_AddVerbalTrick_content_is_long(self):
        """添加话术、内容过长是否有相应的提示"""
        self.to_request.AddVerbalTrick(content=ContentLong, label="上班#")
        self.assertEqual('内容超长', self.XmTEXT.get('xmcontent'))

    def test_AlterVerbalTrick_all_type(self):
        """修改话术、不同类型下进行修改并且列表是否可见"""
        VerbalTrick = ['上班#', '拓展联盟商#', '案场跟进#', '回访联盟商#', '踩盘#', '下班#', '联盟商培训#']
        VerbalTrickType = ['上班', '拓展联盟商', '案场跟进', '回访联盟商', '踩盘', '下班', '联盟商培训']
        self.to_request.AddVerbalTrick(content="这是一条话术", label="上班#")
        for x, y in zip(VerbalTrick, VerbalTrickType):
            self.to_request.VerbalTrickList(label=None, content='这是一条话术')
            self.to_request.AlterVerbalTrick(label=x, content='这是一条话术')
            self.to_request.VerbalTrickList(label=y, content='这是一条话术')

