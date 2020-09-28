"""幸福小秘---报岗"""
# 第一步 导入unittest模块
from XFJ.PubilcAPI.XmApi import *
import requests
import unittest
from XFJ.GlobalMap import GlobalMap
import time
"""
类型：必传 1上班、2下班、3拓展联盟商、4回访联盟商、5联盟商培训、6踩盘、7案场跟进
内容：200字以内
图片：最多4
联盟商：单选
项目：单选
"""


class PostTestCase(unittest.TestCase):
    """小秘——报岗"""

    def __init__(self, *args, **kwargs):
        super(PostTestCase, self).__init__(*args, **kwargs)
        self.do_request = XmApi()
        self.to_request = self.do_request
        self.XmTEXT = GlobalMap()

    @classmethod
    def setUpClass(cls):
        """登录小秘 只执行一次"""
        cls.do_request = XmApi()
        cls.to_request = cls.do_request
        cls.to_request.ApiLogin()

    @classmethod
    def tearDownClass(cls):
        """所用用例执行之后的操作"""
        pass

    def test_PostContentIsNull(self):
        """报岗内容为空"""
        try:
            self.to_request.Post(sellerId=None, projectId=None, reportType=1, content='', reportImgs=None)
            self.assertEqual('报岗成功！', self.XmTEXT.get('xmcontent'))
        except BaseException as e:
            print("断言错误，错误原因：%s" % e)
            raise RuntimeError(self.XmTEXT.get('xmurl'))

    def test_PostContentIsLong(self):
        """报岗内容超长"""
        try:
            self.to_request.Post(sellerId=None, projectId=None, reportType=1, content=ContentLong, reportImgs=None)
            self.assertEqual('内容超长', self.XmTEXT.get('xmcontent'))
        except BaseException as e:
            print("断言错误，错误原因：%s" % e)
            raise RuntimeError(self.XmTEXT.get('xmurl'))

    def test_PostSeller(self):
        """报岗+联盟商"""
        try:
            self.to_request.PostSeller()
            self.to_request.Post(sellerId=self.XmTEXT.get('xmsellerId'), projectId=None,
                                 reportType=1, content=None, reportImgs=None)
            self.assertEqual('报岗成功！', self.XmTEXT.get('xmcontent'))
        except BaseException as e:
            print("断言错误，错误原因：%s" % e)
            raise RuntimeError(self.XmTEXT.get('xmurl'))

    def test_PostProject(self):
        """报岗+项目"""
        try:
            self.to_request.PostProject()
            self.to_request.Post(sellerId=None, projectId=self.XmTEXT.get('xmprojectId'),
                                 reportType=1, content=None, reportImgs=None)
            self.assertEqual('报岗成功！', self.XmTEXT.get('xmcontent'))
        except BaseException as e:
            print("断言错误，错误原因：%s" % e)
            raise RuntimeError(self.XmTEXT.get('xmurl'))

    def test_PostImgsOne(self):
        """图片为1张"""
        try:
            self.to_request.Post(sellerId=None, projectId=None,
                                 reportType=1, content=None,
                                 reportImgs='/uploads/2019/0930/1f62b001-2547-4193-a1e8-1d695790f4c4.png')
            self.assertEqual('报岗成功！', self.XmTEXT.get('xmcontent'))
        except BaseException as e:
            print("断言错误，错误原因：%s" % e)
            raise RuntimeError(self.XmTEXT.get('xmurl'))

    def test_PostImgsFour(self):
        """图片为9张"""
        try:
            self.to_request.Post(sellerId=None, projectId=None,
                                 reportType=1, content=None,
                                 reportImgs='/uploads/2019/0930/1f62b001-2547-4193-a1e8-1d695790f4c4.png,'
                                            '/uploads/2019/0930/1f62b001-2547-4193-a1e8-1d695790f4c4.png,'
                                            '/uploads/2019/0930/1f62b001-2547-4193-a1e8-1d695790f4c4.png,'
                                            '/uploads/2019/0930/1f62b001-2547-4193-a1e8-1d695790f4c4.png,'
                                            '/uploads/2019/0930/1f62b001-2547-4193-a1e8-1d695790f4c4.png,'
                                            '/uploads/2019/0930/1f62b001-2547-4193-a1e8-1d695790f4c4.png,'
                                            '/uploads/2019/0930/1f62b001-2547-4193-a1e8-1d695790f4c4.png,'
                                            '/uploads/2019/0930/1f62b001-2547-4193-a1e8-1d695790f4c4.png,'
                                            '/uploads/2019/0930/1f62b001-2547-4193-a1e8-1d695790f4c4.png')
            self.assertEqual('报岗成功！', self.XmTEXT.get('xmcontent'))
        except BaseException as e:
            print("断言错误，错误原因：%s" % e)
            raise RuntimeError(self.XmTEXT.get('xmurl'))

    def test_PostImgsFive(self):
        """图片为10张"""
        try:
            self.to_request.Post(sellerId=None, projectId=None,
                                 reportType=1, content=None,
                                 reportImgs='/uploads/2019/0930/1f62b001-2547-4193-a1e8-1d695790f4c4.png,'
                                            '/uploads/2019/0930/1f62b001-2547-4193-a1e8-1d695790f4c4.png,'
                                            '/uploads/2019/0930/1f62b001-2547-4193-a1e8-1d695790f4c4.png,'
                                            '/uploads/2019/0930/1f62b001-2547-4193-a1e8-1d695790f4c4.png,'
                                            '/uploads/2019/0930/1f62b001-2547-4193-a1e8-1d695790f4c4.png,'
                                            '/uploads/2019/0930/1f62b001-2547-4193-a1e8-1d695790f4c4.png,'
                                            '/uploads/2019/0930/1f62b001-2547-4193-a1e8-1d695790f4c4.png,'
                                            '/uploads/2019/0930/1f62b001-2547-4193-a1e8-1d695790f4c4.png,'
                                            '/uploads/2019/0930/1f62b001-2547-4193-a1e8-1d695790f4c4.png,'
                                            '/uploads/2019/0930/1f62b001-2547-4193-a1e8-1d695790f4c4.png,')
            self.assertEqual('图片最多不能超过9张', self.XmTEXT.get('xmcontent'))
        except BaseException as e:
            print("断言错误，错误原因：%s" % e)
            raise RuntimeError(self.XmTEXT.get('xmurl'))

    def test_PostCirculationExamine(self):
        """类型 +  内容  循环报岗 并在首页（报岗历史记录）查看"""
        globals()['a'] = 1
        Types = ['上班', '下班', '', '回访联盟商', '联盟商培训', '踩盘', '案场跟进']
        while globals()['a'] != 7:
            try:
                if globals()['a'] == 3:
                    pass
                else:
                    self.to_request.Post(sellerId=None, projectId=None, reportType=globals()['a'],
                                         content='这是一条报岗记录', reportImgs=None)
                    self.assertEqual('报岗成功！', self.XmTEXT.get('xmcontent'))
                    self.to_request.XmHome()
                    time.sleep(0.3)
                    self.assertEqual(self.XmTEXT.get('postcontent'), '这是一条报岗记录')
                    self.assertEqual(self.XmTEXT.get('posttype'), Types[globals()['a']-1])
                    time.sleep(0.4)
                    self.to_request.HistoryPost()
                    self.assertEqual(self.XmTEXT.get('postcontent'), '这是一条报岗记录')
                    self.assertEqual(self.XmTEXT.get('posttype'), Types[globals()['a']-1])
            except BaseException as e:
                print("断言错误，错误原因：%s" % e)
                raise RuntimeError(self.XmTEXT.get('xmurl'))
            globals()['a'] = globals()['a'] + 1
