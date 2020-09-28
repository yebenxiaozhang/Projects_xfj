# coding: utf-8

from appium import webdriver
desired_caps = {"platformName": "Android",
                "deviceName": "127.0.0.1:52001",
                "platformVersion": "5.1.1",
                "appPackage": "com.xfj.boss",
                "appActivity": "com.uzmap.pkg.EntranceActivity"}

# driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", desired_caps)

# 链接appium server 2、告诉他 我要去那个平台启动那个app
webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)

# "unicodeKeyboard": True,
# # "resetKeyboard": True

# 代码 === appium server === 模拟器
# 2、模拟器在线
# 3、appium启动状态
