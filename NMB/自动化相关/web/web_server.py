#  后台框架：flask

from flask import Flask, request, jsonify

app = Flask(__name__)
#  测试数据
user_info = {"user": 'python01', 'pwd': 'lemonban'}


# 登录
@app.route('/', methods=['get', 'post'])
@app.route('/login', methods=['post', 'get'])
def login():
    data = request.form
    # 判断账号，密码是否正确
    if data.get('user') == None:
        return jsonify({'code': "0", "data": None, "msg": "账号不能为空"})
    elif data.get('pwd') == None:
        return jsonify({'code': "0", "data": None, "msg": "密码不能为空"})
    elif user_info.get('user') == data.get('user') and user_info.get('pwd') == data.get('pwd'):
        return jsonify({'code': "1", "data": None, "msg": "成功"})
    else:
        return jsonify({'code': "0", "data": None, "msg": "密码有误"})


@app.route('/load',methods=['post','get'])
def loan():
    print(request.form)
    return "python-flask"


if __name__ == '__main__':
    app.run(debug=True)

