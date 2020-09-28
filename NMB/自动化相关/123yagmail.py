import yagmail
# 连接服务器
password = "llqxelyhzutrbiaa"
mail = yagmail.SMTP("153390680@qq.com", password, "smtp.qq.com", 465)   # 465 端口号
# 准备正文内容
content = '''
不想伤别离,奈何人世间总是散和聚。
不想叹忧虑,人生无非又是苦乐交替。
'''

# 发送邮件
mail.send(["chenxiaomumu@163.com"],
          "离乱青春、感慨深几许",  # 主题
          content,  # 内容
          "D:\\Python_xfj\\img\\QQ截图20180814143153.png",  # 附件
          "736297001@qq.com",  # 抄送
          "735830934@qq.com")   # 秘密抄送
