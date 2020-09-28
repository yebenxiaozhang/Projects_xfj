import requests

# # url = "http://127.0.0.1:5000/login"
# url = "https://www.baidu.com"
# # requests发送get请求
# # 添加请求头
# hea = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"}
# res = requests.get(url=url,headers = hea)
# print(res)
# # 获取请求返回内容
# # print(res.text)
#
# # 返回的结果以指定的一种编码格式
# print(res.content.decode("utf-8"))


# requests发送post请求

url = "http://127.0.0.1:5000/login"
data = {"user": "python01", "pwd": "lemonban"}
res = requests.post(url=url,data=data)
print(res)
print(res.text)
print(res.json())