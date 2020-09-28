"""
使用python自动发送邮件
"""

import smtplib
from email.mime.text import MIMEText
from email.header import Header

# 第一步创建一个smtp对象
smtp = smtplib.SMTP()

# 第二步连接到smtpf服务器
# smtp服务器的地址    # 163邮箱 smtp.163.com   端口25
host = "smtp.qq.com"
port = 465
smtp.ehlo()
smtp.starttls()

smtp.connect(host, port)

# 第三步 登录smtp服务器
user = "153390680@qq.com"
pwd = 'kfubxokhagczcadf'  # 注意点：此处是开启smtp服务的授权码 不是邮箱的登录密码
smtp.login(user, pwd)

# 第四步 准备邮件内容
send_user = "153390680@qq.com"
to_user = "736297001@qq.com"
subject = "测试标题"
contnet = "测试内容"
# 创建一封邮件
msg = MIMEText(contnet, _subtype='plain', _charset='utf8',)
# 添加邮件主题
msg['Subject'] = Header(subject, charset='utf8')
# 添加邮件的发送人
msg['From'] = send_user
# 添加收件人
msg['To'] = to_user


# 第五步发送邮件
smtp.send_message(msg=msg, from_addr=send_user, to_addrs=to_user)
