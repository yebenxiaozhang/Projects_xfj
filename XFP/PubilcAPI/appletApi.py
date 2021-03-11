# -*- coding: utf-8 -*-
# @Time    : 2020/3/9 11:54
# @Author  : 潘师傅
# @File    : XfpApi.py
import requests
import json
from GlobalMap import GlobalMap
from Config.Config import *
import unittest
import time
import random
import datetime
import calendar


class appletApi:

    def __init__(self):
        self.appletText = GlobalMap()

    def RandomText(self, textArr):
        """指定字符串随机取值"""
        # ['你好啊','阿米里！','扣你七娃','你好','hello']
        length = len(textArr)
        if length < 1:
            return ''
        if length == 1:
            return str(textArr[0])
        randomNumber = random.randint(0, length - 1)
        return str(textArr[randomNumber])

    def Merge(self, dict1, dict2):
        return (dict2.update(dict1))

    def PostRequest(self, url, data, header=None, Status=1, files=None, saasCode=XfpsaasCode):
        """post请求"""
        if header is not None:
            r = requests.post(url=(ApiXfpUrl + url),
                              data=json.dumps(data, ensure_ascii=False),
                              headers={
                                  'Content-Type': 'application/json'

                              })
        else:
            data1 = {"page": {
                'size': '100',
                'current': '1'
            },
                "saasCode": saasCode,
                "saasCodeSys": saasCode
            }
            self.Merge(data1, data)
            time.sleep(0.2)
            r = requests.post(url=(ApiXfpUrl + url),
                              data=(json.dumps(data,
                                               ensure_ascii=False).encode("UTF-8")),
                              headers={
                                  'Content-Type': 'application/json',
                                  'Authorization': 'Bearer' + ' ' + self.appletText.get("user_token")
                              },
                              files=files)
        r.raise_for_status()
        self.appletText.set_map('URL', ApiXfpUrl + url)
        globals()['XfpText'] = globals()['r.text'] = json.loads(r.text)
        self.appletText.set_map('XfpText', globals()['r.text'])
        self.appletText.set_map('ApiXfpUrl', url)
        self.appletText.set_map('msg', globals()['XfpText']['msg'])
        self.appletText.set_map('code', globals()['XfpText']['code'])
        self.appletText.set_map('data', globals()['XfpText']['data'])
        time.sleep(0.2)
        if Status == 1:
            try:
                assert "成功", globals()['r.text']['msg']
            except BaseException as e:
                print("断言错误，错误原因：%s" % e)
                raise RuntimeError(self.appletText.get('URL'))
        if globals()['r.text']['code'] == 500:
            raise RuntimeError(self.appletText.get('ApiXfpUrl'))

        if r.elapsed.total_seconds() > 5:
            print('接口请求过慢')
            print(self.appletText.get('ApiXfpUrl'))
        if r.elapsed.total_seconds() > 10:
            print('接口请求过慢大于10秒')
            print(self.appletText.get('ApiXfpUrl'))

    def sendCodeWeiXin(self, userName='19859080323'):
        """获取验证码"""
        self.PostRequest(url='/api/auth/sendCodeWeiXin',
                         data={
                             'senderSource': '微信小程序',
                             'senderDevice': 'ces',
                             'userName': userName
                         })

    def Login(self, userName=XfpUser, code='12345678'):
        """登录"""
        self.PostRequest(url='/api/auth/loginByCodeWeiXin',
                         data={
                             "senderSource": "微信小程序",
                             # "senderDevice": "ces",
                             "userName": userName,
                             "code": code})
        if self.appletText.get('msg') == '成功':
            if (globals()['XfpText']['data']['userDetail']) is not 'None':
                self.appletText.set_map('user_token', globals()['XfpText']['data']['token'])

    def LogIn(self, userName=XfpUser, password=XfpPwd, saasCode=XfpsaasCode, authCode=None, device=None):
        """登录"""
        if device is None:
            device = deviceId
        if authCode is None:
            self.PostRequest(url='/api/auth/login',
                             data={"userName": userName,
                                   'saasCode': saasCode,
                                   'deviceId': device,
                                   # 'deviceId': deviceId,
                                   "password": password},
                             header=1)
        else:
            self.PostRequest(url='/api/auth/login',
                             data={"userName": userName,
                                   'saasCode': saasCode,
                                   'authCode': authCode,
                                   "password": password},
                             header=1)

        if self.appletText.get('msg') == '成功':
            if (globals()['XfpText']['data']['userDetail']) is not 'None':
                if authCode is None:
                    self.appletText.set_map('user_token', globals()['XfpText']['data']['token'])

                else:
                    self.appletText.set_map('user_token', globals()['XfpText']['data']['token'])
                try:
                    self.appletText.set_map('resultStr', globals()['r.text']['data']['resultStr'])
                except:
                    pass

            else:
                self.appletText.set_map('userId', globals()['XfpText']['data']['userDetail']['id'])

        else:
            self.appletText.set_map('data', globals()['XfpText']['data'])


if __name__ == '__main__':
    a = appletApi()


