import unittest
from HTMLTestRunner import HTMLTestRunner
import time
import yagmail
import os
import sys
sys.path.append(r'D:\\PycharmProjects\\')
from XFJ.Agent_Api.Config import *


def send_mail():
    # 连接服务器
    password = "llqxelyhzutrbiaa"
    mail = yagmail.SMTP("153390680@qq.com", password, "smtp.qq.com", 465)  # 465 端口号
    # 准备正文内容
    theme = '幸福客接口测试报告'
    content = '''
    测试报告请下载好后查看
    '''
    if xfj_url == 'http://api.xfj100.com/api/mobile':
        to = ['45324214@qq.com', '23071059@qq.com', '34414822@qq.com', 'chenxiaomumu@163.com', '736297001@qq.com']
    elif xfj_url == 'http://api.ykb100.com/api/mobile':
        to = ['736297001@qq.com']
    else:
        to = ['736297001@qq.com', '1421510096@qq.com']
    # 45324214@qq.com  23071059@qq.com 34414822@qq.com  "chenxiaomumu@163.com"
    # 发送邮件
    mail.send(to=to,
              # 如果多个收件人的话，写成list就行了，如果只是一个账号，就直接写字符串就行to='chenxiaomumu@163.com'
              subject=theme,  # 主题
              contents=content,  # 内容
              attachments=latest_report,  # 附件
              cc="736297001@qq.com")  # 抄送


def latest_report(report_dir):
    lists = os.listdir(report_dir)
    print(lists)
    # 按时间顺序对该目录文件夹下面的文件进行排序
    lists.sort(key=lambda fn: os.path.getatime(report_dir + "\\" + fn))
    print("The latest report is:" + lists[-1])
    file = os.path.join(report_dir, lists[-1])
    print(file)
    return file


if __name__ == '__main__':
    report_dir = './report'
    test_dir = './test_case'

    all_case = unittest.defaultTestLoader.discover(test_dir, pattern='*_casc.py')
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    report_name = report_dir + '/' + now + '_' + 'result.html'
    description = '环境：' + xfj_url + '\n' + '用例执行情况'
    with open(report_name, "wb") as f:
        runner = HTMLTestRunner(stream=f, title='幸福客接口测试报告', description=description)
        runner.run(all_case)
        f.close()

    # h获取最新测试报告
    latest_report = latest_report(report_dir)
    # 发送邮件报告
    # send_mail()
