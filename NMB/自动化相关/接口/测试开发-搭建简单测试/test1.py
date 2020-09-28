from flask import Flask, request
from requests import request
import requests
import json
# import args
# 导入模块
app = Flask(__name__)
# 初始化服务器对象


def http_helper(url, method, params):
    params = json.loads(params)

    if method == "get":
        res = requests.get(url, params)
        return res.text

    elif method == "post":
        res = requests.post(url, params)
        return res.text


@app.route('/deal-data')  # 路由

def deal_login():   # 试图函数
    # 转发 获取HTML  传过来的URL  method param 转发给后台接口
    url = request.args['url']   # 获取前端传过来的参数
    method = request.args['method']
    params = request.args['data']   # 字符串
    # python  怎么访问后台接口 requests
    res = http_helper(url, method, params)
    return res
    # return "heheda"

# 预期结果 -- login success


app.run(port=8000)
