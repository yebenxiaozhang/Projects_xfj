from XFJ.Config.Conifg import *
from XFJ.PubilcMethod.WebTools import *

class LogIn:
    """幸福家后台登录"""
    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"}
        self.Web = WebTools()
        self.WebTooles = self.Web

    def LogIn(self, method, d):
        if method == "Xfm":
            try:
                if XfmUrl == 'http://192.168.10.188:9092':
                    d.get('http://192.168.10.188:9092')
                elif XfmUrl == 'http://xfm.ykb100.com':
                    d.get('http://xfm.ykb100.com')
                elif XfmUrl == 'http://xfm.xfj100.com':
                    d.get('http://xfm.xfj100.com')
                d.find_element_by_css_selector('#agentUser').send_keys(XfmBossUser)
                d.find_element_by_css_selector('#agentPwd').send_keys(XfmBossPwd)
                d.find_elements_by_class_name('m-t-l')[0].click()

            except BaseException as e:
                print("错误，错误原因：%s" % e)

        elif method == "City":
            """变成双引号"""
            # data = json.dumps(data)
            try:
                d.get(CityUrl)
                d.find_element_by_css_selector('#j_username').send_keys(CityUser)
                d.find_element_by_css_selector('#j_password').send_keys(CityPwd)
                d.find_elements_by_class_name('btn-primary')[0].click()
                time.sleep(2)
                dome = d.find_elements_by_class_name('dropdown-toggle')[0].text
                while dome != '总站管理员':
                    d.find_element_by_link_text('总站管理员').click()
                    time.sleep(0.5)
                    dome = d.find_elements_by_class_name('dropdown-toggle')[0].text
            except BaseException as e:
                print("post请求错误，错误原因：%s" % e)

        elif method == 'admin':
            # data = json.dumps(data)
            try:
                d.get(AdminUrl)
                d.find_element_by_css_selector('#j_username').send_keys(AdminUser)
                d.find_element_by_css_selector('#j_password').send_keys(AdminPwd)
                d.find_elements_by_class_name('btn-primary')[0].click()
                time.sleep(2)
                d.find_element_by_css_selector('#showCityName').click()
                time.sleep(2)
                d.find_element_by_link_text(CityName).click()
                time.sleep(2)
                dome = d.find_element_by_css_selector('#showCityName').text
                while dome != '幸福家股份':
                    d.find_element_by_css_selector('#showCityName').click()
                    time.sleep(0.5)
                    d.find_element_by_link_text(CityName).click()
                    time.sleep(2)
                    dome = d.find_element_by_css_selector('#showCityName').text
            except BaseException as e:
                print("post请求错误，错误原因：%s" % e)
        else:
            print("请检查大小写")
            print(f"暂不支持{method}方法")


if __name__ == '__main__':
    a = LogIn()

