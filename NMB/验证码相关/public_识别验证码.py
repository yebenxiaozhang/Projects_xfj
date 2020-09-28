"""
准备：
selenium  安装  pip install selenium
chromedriver  驱动安装
去百度找官网找相对应的版本
pillow 模块安装  pip intall pillow

"""

from selenium import webdriver
from PIL import Image
from chaojiying import Chaojiying
"""
自动识别验证码登录的案例
"""
# 打开浏览器，进入登录的页面
driver = webdriver.Chrome()
driver.get("http://www.chaojiying.com/user/login/")
# 浏览器最大化
driver.maximize_window()

# 自动账号  输入密码
driver.find_element_by_name('user').send_keys("pan951105")
driver.find_element_by_name('pass').send_keys("happy15157951")

# 识别验证码思路

# 1、获取验证码
# 对当前网页页面进行截屏处理   保存一个文件 名字为 page.png
driver.save_screenshot('page.png')
# 选中验证码
v_code = driver.find_element_by_xpath('/html/body/div[3]/div/div[3]/div[1]/form/div/img')
loc = v_code.location
# print(loc)   # 打印 x ,y 坐标
# 获取高度跟宽度
size = v_code.size

# 构造验证码图片  上下左右的位置
left = loc.get('x')
top = loc.get('y')
right = loc.get('x') + size.get('width')    # 有屏幕缩放比例的 要乘上
buttom = loc.get('y') + size.get('height')  # 有屏幕缩放比例的 要乘上
# 验证码位置
val = (left, top, right, buttom)

# 打开验证码
page_pic = Image.open('page.png')
# 把验证码的位置传进去
code_pic = page_pic.crop(val)
# 保存验证码
code_pic.save('code.png')


# 2、调用第三方的接口来识别验证码
yz = Chaojiying(username="pan951105", password='happy15157951', soft_id="900450")
with open('code.png', 'rb') as f:
    pic = f.read()
# 通过对象调用post_pic 方法，进行图片识别是一个地点类型数据，其中的一个pic_str就是一个识别的结果
result = yz.post_pic(pic, codetype='1004')
print("识别的结果:", result.get('pic_str'))
res = result.get('pic_str')


# 在页面上输入验证码
driver.find_element_by_name('imgtxt').send_keys(res)
# 点击登录
driver.find_element_by_class_name('login_form_input_submit').click()
