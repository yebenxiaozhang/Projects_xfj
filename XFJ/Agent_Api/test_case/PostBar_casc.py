"""贴吧的逻辑
不能为空
当不添加照片的时候  内容限制不能少于10个字
当添加了照片之后  内容不能为空
内容长度限制为255"""
# 第一步 导入unittest模块
from XFJ.PubilcAPI.AgentAPI import *
import unittest
import time
# 第二步 编写测试用例
"""
1、发布新帖：内容、图片、便签都为空 是否发布成功
2、发布新帖：内容、图片、便签选择一个  是否发布成功
3、发布新帖：内容、图片、便签选择两个  是否发布成功
4、发布新帖：内容、图片、便签选择三个  是否发布成功
5、发布新帖：内容、图片、标签选择四个  是否发布成功
6、发布新帖：内容为空、图片为一张 是否发布成功
7、发布新帖：内容为空、图片为6张  是否发布成功
8、发布新帖：内容为空、图片为7张 是否发布成功
9、发布新帖：内容长度过短  是否发布成功
10、发布新帖：内容过长     是否发布成功
11、发布新帖：内容正常     是否发布成功
12、发布新帖：内容为空     是否发布成功
13、发布新帖：图片为空     是否发布成功
14、发布新帖：便签为空     是否发布成功
15、发布成功后，在个人帖子中是否可以找到
16、发布成功后，在城市帖子中是否可以找到
17、发布成功后，自己能否给自己点赞 在我的及在城市贴吧中查看
18、发布成功后，自己能否给自己评论 在我的及在城市贴吧中查看
23、别人是否可以进行点赞
24、别人是否可以进行评论
25、别人评论后 是否支持回复
26、别人点赞 能否查看到
27、发布新帖：积分是否叠加
28、发布失败的帖子，积分是否有叠加
29、删除帖子后 是否还能查看
30、删除帖子后 积分是否有变化
31、删除帖子后 重新发布帖子 积分是否有叠加
32、重复发布帖 是否有限制
33、多次点赞是否成功

"""


class PostBarTestCase(unittest.TestCase):
    """幸福家经纪人---贴吧"""

    def __init__(self, *args, **kwargs):
        super(PostBarTestCase, self).__init__(*args, **kwargs)
        self.Agent = AgentApi()
        self.AgentRequest = self.Agent
        self.AgentTEXT = GlobalMap()

    @classmethod
    def setUpClass(cls):
        """登陆经纪人"""
        cls.Agent = AgentApi()
        cls.AgentRequest = cls.Agent
        cls.AgentRequest.LoginAgent()

    # 测试用例方法必须用test开头
    def setUp(self):
        """警告处理"""
        # warnings.simplefilter("ignore", ResourceWarning)

    def tearDown(self):
        """每个测试用例结束的时候 都把个人帖子删除"""
        self.AgentRequest.DelPostBar()

    def test_postbar_all_is_null(self):
        """1、发布新帖：内容、图片、便签都为空 是否发布成功"""
        try:
            self.AgentRequest.AddPostBar(resourceLabels='')
            self.assertEqual('发布内容能不低于10字', self.AgentTEXT.get('content'))
        except BaseException as e:
            print("错误，错误原因：%s" % e)
            raise RuntimeError(self.AgentTEXT.get('Agenturl'))

    def test_postbar_Labeled_one(self):
        """2、发布新帖：内容、图片、便签选择一个  是否发布成功"""
        try:
            self.AgentRequest.AddPostBar(resourceLabels='交友')
            self.assertEqual('发布内容能不低于10字', self.AgentTEXT.get('content'))
        except BaseException as e:
            print("错误，错误原因：%s" % e)
            raise RuntimeError(self.AgentTEXT.get('Agenturl'))

    def test_postbar_Labeled_two(self):
        """3、发布新帖：内容、图片、便签选择两个  是否发布成功"""
        try:
            self.AgentRequest.AddPostBar(resourceLabels='交友,晒单')
            self.assertEqual('发布内容能不低于10字', self.AgentTEXT.get('content'))
        except BaseException as e:
            print("错误，错误原因：%s" % e)
            raise RuntimeError(self.AgentTEXT.get('Agenturl'))

    def test_postbar_Labeled_three(self):
        """4、发布新帖：内容为空、图片为空、便签选择3个  是否发布成功"""
        try:
            self.AgentRequest.AddPostBar(resourceLabels='交友,晒单,健身')
            self.assertEqual('发布内容能不低于10字', self.AgentTEXT.get('content'))
        except BaseException as e:
            print("错误，错误原因：%s" % e)
            raise RuntimeError(self.AgentTEXT.get('Agenturl'))

    def test_postbar_Labeled_four(self):
        """5、发布新帖：内容为空、图片为空、便签选择4个  是否发布成功"""
        try:
            self.AgentRequest.AddPostBar(resourceLabels='交友,晒单,健身,娱乐')
            self.assertEqual('发布内容能不低于10字', self.AgentTEXT.get('content'))
        except BaseException as e:
            print("错误，错误原因：%s" % e)
            raise RuntimeError(self.AgentTEXT.get('Agenturl'))

    def test_postbar_imgs_one_(self):
        """6、发布新帖：内容为空、图片为一张 是否发布成功"""
        try:
            self.AgentRequest.AddPostBar(content='这是一个帖子', imgs=1, resourceLabels='')
        except BaseException as e:
            print("错误，错误原因：%s" % e)
            raise RuntimeError(self.AgentTEXT.get('Agenturl'))

    def test_postbar_imgs_six(self):
        """7、发布新帖：内容为空、图片为6张 是否发布成功"""
        try:
            self.AgentRequest.AddPostBar(content='这是一个帖子', imgs=6, resourceLabels='')
        except BaseException as e:
            print("错误，错误原因：%s" % e)
            raise RuntimeError(self.AgentTEXT.get('Agenturl'))

    def test_postbar_imgs_seven(self):
        """8、发布新帖：内容为空、图片为7张 是否发布成功"""
        try:
            self.AgentRequest.AddPostBar(imgs=7)
        except BaseException as e:
            print("错误，错误原因：%s" % e)
            raise RuntimeError(self.AgentTEXT.get('Agenturl'))

    def test_postbar_content_short(self):
        """9、发布新帖：内容长度过短  是否发布成功"""
        try:
            self.AgentRequest.AddPostBar(content='幸福家测试')
        except BaseException as e:
            print("错误，错误原因：%s" % e)
            raise RuntimeError(self.AgentTEXT.get('Agenturl'))

    def test_postbar_content_long(self):
        """10、发布新帖：内容过长     是否发布成功"""
        try:
            self.AgentRequest.AddPostBar(content=ContentLong)
        except BaseException as e:
            print("错误，错误原因：%s" % e)
            raise RuntimeError(self.AgentTEXT.get('Agenturl'))

    def test_postbar_content_true(self):
        """11、发布新帖：内容正常     是否发布成功"""
        try:
            self.AgentRequest.AddPostBar(content='幸福家测试' + time.strftime("%Y-%m-%d~~%H_%M_%S"),
                                         resourceLabels='交友', imgs=1)
        except BaseException as e:
            print("错误，错误原因：%s" % e)
            raise RuntimeError(self.AgentTEXT.get('Agenturl'))

    def test_postbar_content_null(self):
        """12、发布新帖：内容为空     是否发布成功"""
        try:
            self.AgentRequest.AddPostBar(resourceLabels='交友', imgs=1)
        except BaseException as e:
            print("错误，错误原因：%s" % e)
            raise RuntimeError(self.AgentTEXT.get('Agenturl'))

    def test_postbar_imgs_null(self):
        """13、发布新帖：图片为空     是否发布成功"""
        try:
            self.AgentRequest.AddPostBar(content='幸福家测试' +
                                                 time.strftime("%Y-%m-%d~~%H_%M_%S"), resourceLabels='交友')
        except BaseException as e:
            print("错误，错误原因：%s" % e)
            raise RuntimeError(self.AgentTEXT.get('Agenturl'))

    def test_postbar_resourceLabels_null(self):
        """14、发布新帖：便签为空     是否发布成功"""
        try:
            self.AgentRequest.AddPostBar(content='幸福家测试' +
                                                 time.strftime("%Y-%m-%d~~%H_%M_%S"), imgs=1)
        except BaseException as e:
            print("错误，错误原因：%s" % e)
            raise RuntimeError(self.AgentTEXT.get('Agenturl'))

    def test_Release_success_is_my(self):
        """15、发布成功后，在个人帖子中是否可以找到"""
        try:
            self.AgentRequest.AddPostBar(content='幸福家测试' + time.strftime("%Y-%m-%d"),
                                         resourceLabels='交友', imgs=1)
            self.AgentRequest.MyPostBarList()
            globals()['agenttext'] = json.loads(json.dumps(json.loads(self.AgentTEXT.get('text')),
                                                           indent=4, sort_keys=False, ensure_ascii=False))
            self.assertEqual('幸福家测试' + time.strftime("%Y-%m-%d"),
                             globals()['agenttext']['extend']['list'][0]['resourceContent'])
        except BaseException as e:
            print("错误，错误原因：%s" % e)
            raise RuntimeError(self.AgentTEXT.get('Agenturl'))

    def test_Release_success_is_city(self):
        """16、发布成功后，在城市帖子中是否可以找到"""

    def test_Release_success_Like(self):
        """17、发布成功后，自己能否给自己点赞 在我的及在城市贴吧中查看"""

    def test_Release_success_comment(self):
        """18、发布成功后，自己能否给自己评论  在我的及在城市贴吧中查看"""


    def test_Thumb_up_others(self):
        """23、别人是否可以进行点赞"""


    def test_Others_comment(self):
        """24、别人是否可以进行评论"""


    def tset_Comment_back(self):
        """别人评论后 是否支持回复"""

    def test_Others_thumb_up_visible(self):
        """别人点赞 能否查看到"""

    def test_add_postbar(self):
        """新增帖子后查看任务积分"""

    def test_repetition_add_postbar(self):
        """重复新增帖子"""


