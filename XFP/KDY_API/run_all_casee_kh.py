import unittest
from HTMLTestRunner import HTMLTestRunner
import time
import yagmail
import os
import sys
sys.path.append(r'D:\\PycharmProjects\\XFP\\')
from XFP.Config.Config import *
mima = 'nighqgkwmdkrbgic'
from selenium import webdriver

def send_mail():
    # 连接服务器
    password = PassWord
    mail = yagmail.SMTP("153390680@qq.com", password, "smtp.qq.com", 465)  # 465 端口号
    # 准备正文内容
    theme = '客第壹客户相关接口测试报告'
    content = '''
    测试报告请下载好后查看
    '''

    if ApiXfpUrl == 'http://xfp.xfj100.com':
        to = ['34414822@qq.com', 'chenxiaomumu@163.com', '736297001@qq.com', '23071059@qq.com']
    elif ApiXfpUrl == 'http://xfpapi.ykb100.com':
        # to = ['23071059@qq.com', 'chenxiaomumu@163.com', '736297001@qq.com']
        to = ['736297001@qq.com']
        # to = ['736297001@qq.com', '975118135@qq.com', 'chenxiaomumu@163.com']
    else:
        to = ['736297001@qq.com', '1459792453@qq.com', 'chenxiaomumu@163.com']
    # 45324214@qq.com  23071059@qq.com 34414822@qq.com  "chenxiaomumu@163.com"
    # 发送邮件
    mail.send(to=to,
              # 如果多个收件人的话，写成list就行了，如果只是一个账号，就直接写字符串就行to='chenxiaomumu@163.com'
              subject=theme,  # 主题
              contents=content,  # 内容
              attachments=latest_report,  # 附件
              cc="736297001@qq.com")  # 抄送a


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
    report_dir = './report_kh'
    test_dir = './test_case'

    all_case = unittest.defaultTestLoader.discover(test_dir, pattern='*_kh.py')
    now = time.strftime("%Y-%m-%d~~%H_%M_%S")
    report_name = report_dir + '/' + now + '_' + 'result.html'
    description = '环境：' + ApiXfpUrl + '\n' + '用例执行情况'
    with open(report_name, "wb") as f:
        runner = HTMLTestRunner(stream=f, title='客第壹客户接口相关测试报告', description=description)
        runner.run(all_case)
        f.close()

    # h获取最新测试报告
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("D:\PycharmProjects\XFP\KDY_API" + (report_name)[1:])
    latest_report = latest_report(report_dir)
    # 发送邮件报告
    time.sleep(2)
    dome = driver.find_element_by_class_name('btn-primary').text
    if dome == '通过率 [100.00% ]':
        pass
    else:
        pass
        send_mail()
    driver.quit()
