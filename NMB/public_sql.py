# python 对接mysql
"""
# 第一步： 安装pymysql模块
    安装命令：pip install pymysql
# 第二步：导入安装好的模块到文件

# 第三步：连接到mysql数据库
连接的参数：IP地址  端口  登录的账号  密码
# 第四步：创建一个游标
"""

import pymysql
# 连接到mysql数据库，返回一个连接的对象
pymysql.connect(host="192.168.10.17",
                port=3306,
                user="root",
                password="123456")
# 创建一个游标
# cur = con.cursor()


