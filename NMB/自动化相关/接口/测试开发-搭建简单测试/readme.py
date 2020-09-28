"""
预期结果  !== 实际结果

服务器返回了接口的数据
测试人员设计一个服务器的接口
登录接口 定义了一个网址  返回数据

http --> pip install requests
Excel --> pip install openpyxl
server --> pip install flask/django

"""
from flask import Flask
# 导入模块

# 初始化服务器对象

app = Flask(__name__)


@app.route('/login')  # 路由

def deal_login():
    # 试图函数
    print("dadad")
    print("hhh")
    return "login success"

# 预期结果 -- login success
# 如何开发，架构
# 页面 --> Html
# 后端开发  -->中间人（工具）
# 接口
# flutter,vue,react,-->HTML,css,js


app.run()

# 运行服务器
