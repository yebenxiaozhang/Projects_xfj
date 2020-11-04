import requests
import json
from XFJ.GlobalMap import GlobalMap


class HandleRequest:
    def __init__(self):
        self.headers = {'Content-Type': 'application/json'}
        # self.headers = {"User-Agent": "0.0.0 rv:73 (iPhone; iOS 12.2; zh_CN)",
        #                 "Connection": "close",
        #                 "Accept-Encoding": 'gzip'}
        self.TEXT = GlobalMap()

    def to_request(self, method, url, data):
        if method == "get":
            try:
                r = requests.get(url=url, params=data, headers=self.headers)
                # response = json.loads(r.text)
                response = json.dumps(json.loads(r.text), indent=4, sort_keys=False, ensure_ascii=False)
                # print("get请求结果为：\n %s" % response)
            except BaseException as e:
                print("get请求错误，错误原因：%s" % e)
        elif method == "post":
            """变成双引号"""
            # data = json.dumps(data)
            try:
                r = requests.post(url=url, data=data, headers=self.headers)
                # response = json.loads(r.text)
                response = json.dumps(json.loads(r.text), indent=4, sort_keys=False, ensure_ascii=False)
                # print("post请求结果为：\n %s" % response)
            except BaseException as e:
                print("post请求错误，错误原因：%s" % e)
        else:
            r = None
            print(f"暂不支持{method}方法")
        # self.TEXT.set_map('text', response)
        return r


if __name__ == '__main__':
    a = HandleRequest()

