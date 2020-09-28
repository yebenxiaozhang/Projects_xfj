"""
python发送带附件的邮件

"""

import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.header import Header


# 创建smtp对象，连接并登录
smtp = smtplib.SMTP()
host = "smtp.163.com"
port = 25
# 连接
smtp.connect(host, port)
# 登录
user = "a546245426@163.com"
pwd = "python3"
smtp.login(user, pwd)


#  准备邮件内容，创建邮件
with open('report.html', 'rb') as f:
    content = f.read()
subject = "柠檬班测试报告"
send_user = "a546245426@163.com"
to_user = "596481198@qq.com"

# 创建一封可以添加附件的邮件
msg_enclosure = MIMEMultipart()


# 创建附件
enclosure = MIMEApplication(content)
enclosure.add_header('content-disposition', 'attachment', filename='report.html')

# 邮件的文本内容
msg = MIMEText('测试报告')

msg_enclosure.attach(msg)
msg_enclosure.attach(enclosure)

msg_enclosure['Subject'] = Header(subject, 'utf8')
msg_enclosure['From'] = send_user
msg_enclosure['To'] = to_user

# 发送邮件
smtp.send_message(msg, send_user, to_user)
