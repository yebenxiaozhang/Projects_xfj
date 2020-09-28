# 去掉验证码
# 万能通关验证码
# 验证码识别技术
# 记录cookie

# 先下载谷歌插件EditThisCookie
# 用户栏会多出一个小饼干的东西
# 会员卡

# 先引入
from selenium import webdriver
import time
# 访问谷歌浏览器
driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://www.baidu.com/")
# cookie用字典存储


cookie_1 = {"name": "BAIDUID", "value": "3CA4202A0E73498B681BB85BA585AD16:FG=1"}
cookie_2 = {"name": "BDUSS", "value": "VpkfmVqNDktZnJWVGo2OWpNTXd1aG15SWtXQVk3MUV0alh3bXBEYWdxS3c0eXBkRVFBQUFBJCQAAAAA"
                                      "AAAAAAEAAAD2Wdg4aHJkMTMzMTI5MDA5NzAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
                                      "AAAAAAAAAAAAAAAAAAAAAALBWA12wVgNdR"}
time.sleep(5)
# 导入cookie
driver.add_cookie(cookie_1)
driver.add_cookie(cookie_2)
# 重新访问
driver.get("https://www.baidu.com/")
