# 300
# 500万 ---住  房买个房 ---全款
# 200万  ---付个首付  --买个车
# 少于200万  ---买个车 + 旅游  ---放假一个月
# money = 300
# city = "珠海"
# # 判断
# if money >= 500 and city == "珠海":
#     print('很开心，买一个房，付个全款')
# elif money >= 200 or city == "深圳":
#     print('买个房付个首付，顺便买个车')
# else:
#     print("买个车，旅游，给自己放假一个月")
#
#
# # 遍历  从头到尾我都访问了一下
# # 所有的电影 8部
movies = ["爱情公寓", "复仇者联盟", "钢铁侠", "惊奇队长", "黑豹", "蜘蛛侠", "奇异博士"]
# for item in movies:
#     # 访问每一个元素后都会执行的语句
#     print("item: " , item)
#     if item == "蜘蛛侠":
#         print("==========就你了，其他的，我不想看了==========")
#         break  # 退出循环
#
#
# # range()       # 列表 --- 整数
# # range(6)      # 默认是从0开始的，默认的步长是1，n来代表终点 包含了起点值 不包含终点
# # range(6)      # [0,1,2,3,4,5]
# # range(2,10)   # [2,3,4,5,6,7,8,9]
# # range(2, 10, 3)   # [2,5,8]
#
for index in range(len(movies)):
    print("下标", index)
    print("对应值", movies[index])
#
# print("---------------------------------")
# ductA = {"key": "value",
#          "hello": "heihei"}
# for item in ductA:
#     print(item)
#
# print("---------------------------------")
# for item in ductA.values():
#     print(item)
#
# print("---------------------------------")
# for key, value in ductA.items():
#     print(key, value)
# tianxiejihe = 'hehe'
# tst1 = 'hheh'
# foo =  [tianxiejihe,tst1]
# from random import choice
# print(choice(foo))
# foo = ['hehe','1','2']
# from random import choice
#
# print(choice(foo))
#
# from selenium import webdriver
#
# driver = webdriver.chrome()
# driver.get('http://www.baidu.com')
# driver.maximize_window()
# from selenium import webdriver


from selenium import webdriver
from time import sleep
from selenium.webdriver import ActionChains
d = webdriver.Chrome()
# d.minimize_window()
# d.maximize_window()
d.get('http://news.to128.com/shouye/')
d.maximize_window()