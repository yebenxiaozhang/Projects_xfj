from XFP.Config.Config import *
from XFP.PubilcMethod.WebTools import *


class LogIn:
    """幸福派后台登录"""
    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"}
        self.Web = WebTools()
        self.WebTooles = self.Web

    def LogIn(self,method, driver):
        if method == "xfp":
            try:
                driver.get(xfp_url)
                driver.find_element_by_name('username').send_keys(XfpUser)
                driver.find_element_by_name('password').send_keys(XfpPwd)
                driver.find_element_by_class_name('logo_sub').click()
            except BaseException as e:
                print("错误，错误原因：%s" % e)

        elif method == "City":
            """变成双引号"""
            # data = json.dumps(data)
            try:
                pass
            except BaseException as e:
                print("post请求错误，错误原因：%s" % e)
        else:
            print("请检查大小写")
            print(f"暂不支持{method}方法")


if __name__ == '__main__':
    a = LogIn()

