# 第一步 导入unittest模块
from XFJ.PubilcAPI.FlowPath import *
import unittest
# 第二步 编写测试用例

# login()


class MyTestCase(unittest.TestCase):
    """我的测试用例类"""

    def __init__(self, *args, **kwargs):
        super(MyTestCase, self).__init__(*args, **kwargs)
        self.Xfk_request = XfkApi()
        self.XfkRequest = self.Xfk_request
        self.XfkTEXT = GlobalMap()
    # 测试用例方法必须用test开头

    @classmethod
    def setUpClass(cls):
        """登录幸福客"""
        cls.do_request = XfkApi()
        cls.to_request = cls.do_request
        cls.to_request.LoginXfk()

    def test_101_alter_agent_name(self):
        """修改经纪人昵称前后对比"""
        self.XfkRequest.alterName(agentname='幸福家测试1')
        self.XfkRequest.LoginXfk()
        self.assertEqual('幸福家测试1', self.XfkTEXT.get('agentName'))

    def test_102_alter_agent_name_null(self):
        """经纪人昵称为空"""
        self.XfkRequest.alterName(agentname=None)
        self.XfkRequest.LoginXfk()
        self.assertNotEqual(None, self.XfkTEXT.get('agentName'))

    def test_103_alter_agent_name_long(self):
        """经纪人昵称过长"""
        self.XfkRequest.alterName(agentname=ContentLong)
        self.assertEqual('昵称过长', self.XfkTEXT.get('Content'))

    def test_104_alter_agent_name_expression(self):
        """经纪人昵称为表情"""
        self.XfkRequest.alterName(agentname='♥')
        self.assertEqual('修改成功', self.XfkTEXT.get('Content'))

    def test_201_follow_template(self):
        """获取跟进模板、要是有跟进模板则删除"""
        self.XfkRequest.getTemplate()
        while self.XfkTEXT.get('extend') != []:
            self.XfkRequest.delTemplate(TemplateIds=self.XfkTEXT.get('followTemplateId'))
            self.XfkRequest.getTemplate()

    def test_202_follow_template_add(self):
        """新增模版"""
        self.XfkRequest.Template(countent='模板内容')
        self.assertEqual(self.XfkTEXT.get('content'), '新增模版成功')
        self.XfkRequest.getTemplate()
        self.assertEqual(self.XfkTEXT.get('followTemplate'), '模板内容')

    def test_203_follow_template_alter(self):
        """修改模版"""
        self.XfkRequest.getTemplate()
        self.XfkRequest.Template(countent='呵呵啊1', countentId=self.XfkTEXT.get('followTemplateId'))
        self.assertEqual(self.XfkTEXT.get('content'), '修改模版成功')
        self.XfkRequest.getTemplate()
        self.assertEqual(self.XfkTEXT.get('followTemplate'), '呵呵啊1')

    def test_204_follow_template_long(self):
        """模板长度的限制"""
        self.XfkRequest.getTemplate()
        self.XfkRequest.Template(countent=ContentLong, countentId=self.XfkTEXT.get('followTemplateId'))
        self.assertEqual(self.XfkTEXT.get('content'), '模版内容过长')
        self.XfkRequest.getTemplate()
        self.XfkRequest.Template(countent='123466', countentId=self.XfkTEXT.get('followTemplateId'))
        self.assertEqual(self.XfkTEXT.get('content'), '修改模版成功')

    def test_205_follow_template_expression(self):
        """修改模版为表情"""
        self.XfkRequest.getTemplate()
        self.XfkRequest.Template(countent='♥', countentId=self.XfkTEXT.get('followTemplateId'))
        self.assertNotEqual(self.XfkTEXT.get('Content'), '修改模版成功')

    def test_206_follow_template_centent_uell(self):
        """修改模版为空"""
        self.XfkRequest.getTemplate()
        self.XfkRequest.Template(countent=None, countentId=self.XfkTEXT.get('followTemplateId'))
        self.assertEqual(self.XfkTEXT.get('content'), '模版内容不能为空')

    def test_207_follow_template_dal(self):
        """删除所有的模版"""
        self.test_201_follow_template()

    def test_208_look_all_follow_template(self):
        """在所有的跟进模板中查看"""
        self.test_202_follow_template_add()
        self.XfkRequest.Template(countent='模板内容')
        self.assertEqual(self.XfkTEXT.get('content'), '新增模版成功')
        self.XfkRequest.getAllTemplate()
        self.assertEqual(self.XfkTEXT.get('followTemplate'), '模板内容')
        self.test_207_follow_template_dal()

    def test_301_alter_pwd_oldpwd_is_erroe(self):
        """旧密码不正确"""
        self.XfkRequest.alterPwd(new='123456', old='123456789')
        self.assertEqual(self.XfkTEXT.get('Content'), '旧密码不正确')

    def test_302_alter_pwd_newpwd_is_null(self):
        """新密码为空"""
        self.XfkRequest.alterPwd(new=None, old='123456789')
        self.assertEqual(self.XfkTEXT.get('Content'), '新旧密码不能为空')

    def test_303_alter_pwd_all_null(self):
        """新旧密码都为空"""
        self.XfkRequest.alterPwd(new=None, old=None)
        self.assertEqual(self.XfkTEXT.get('Content'), '新旧密码不能为空')

    def test_304_alter_pwd_oldpwd_is_null(self):
        """旧密码为空"""
        self.XfkRequest.alterPwd(new='123456', old=None)
        self.assertEqual(self.XfkTEXT.get('Content'), '新旧密码不能为空')

    def test_305_alter_pwd_new_is_long(self):
        """密码长度超过限制"""
        self.XfkRequest.alterPwd(new='123456123456123456123456123456123456123456123456', old='123456')
        if self.XfkTEXT.get('Content') == '修改登录密码成功':
            self.XfkRequest.LoginXfk(pwd='123456123456123456123456123456123456123456123456')
            self.XfkRequest.alterPwd(new='123456', old='123456123456123456123456123456123456123456123456')
            self.assertEqual('修改登录密码成功', self.XfkTEXT.get('Content'))
            self.XfkRequest.LoginXfk()
        else:
            self.assertEqual('密码长度超过限制', self.XfkTEXT.get('Content'))

    def test_306_alter_pwd_newpwd_is_short(self):
        """密码过短"""
        self.XfkRequest.alterPwd(new='123', old='123456')
        if self.XfkTEXT.get('Content') == '修改登录密码成功':
            self.XfkRequest.LoginXfk(pwd='123')
            self.XfkRequest.alterPwd(new='123456', old='123')
            self.assertEqual('修改登录密码成功', self.XfkTEXT.get('Content'))
            self.XfkRequest.LoginXfk()
        else:
            self.assertEqual('密码长度超过限制', self.XfkTEXT.get('Content'))

    def test_307_alter_pwd_new_is_expression(self):
        """密码不能为表情"""
        self.XfkRequest.alterPwd(new='♥', old='123456')
        if self.XfkTEXT.get('Content') == '修改登录密码成功':
            self.XfkRequest.LoginXfk(pwd='♥')
            self.XfkRequest.alterPwd(new='123456', old='♥')
            self.assertEqual('修改登录密码成功', self.XfkTEXT.get('Content'))
            self.XfkRequest.LoginXfk()
        else:
            self.assertEqual('密码长度超过限制', self.XfkTEXT.get('Content'))

    def test_getBindingWx(self):
        """获取绑定微信页面"""
        self.XfkRequest.bindingWx()
        self.assertEqual('获取成功', self.XfkTEXT.get('content'))

