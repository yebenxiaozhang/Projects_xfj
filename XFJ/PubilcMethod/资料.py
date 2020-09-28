# 定位为元素的地方，元素看不见的情况下，使得滚动条下拉
# target = d.find_element_by_css_selector('#renovation_chosen')
# d.execute_script('arguments[0].scrollIntoView();', target)

# option value  下拉框选中（通过下标）
# select = Select(d.find_element_by_id('chooseDept'))
# select.select_by_index("3")

# 选中后取值 select  下 option value
# d.execute_script('return $("#seachcity option:selected").text()')

# 接口测试中 要是请求失败 则抛出异常
# r = requests.get(url=url, params=None)
# r.raise_for_status()


# 刷新单前页面
# d.refresh()

# 取第几个元素
# A = '123abc'
# print(A[3])

# a = '22.29元'
# print(a[:-1])
# 22.29

# # 删除非数字(-)的字符串
# import re
# num = re.sub(r'\D', "", phone)
# print "电话号码是 : ", num
# D大写去非数字，小写去数字

# from decimal import Decimal
# a=1
# a=Decimal(a).quantize(Decimal('0.00'))
# print (a)
# #结果1.00

# import os
# os.system(r'路径')
# os.system(r"D:\Python_test\xfj\photo_uploading\2.exe")
# 该路径执行文件为.exe  文件  需要用到autoIT这个软件

# # 点击申请合作
# d.find_element_by_css_selector('#applyCooperBtn').click()
# sleep(0.5)
# d.switch_to.default_content()
# sleep(0.5)
# d.find_element_by_css_selector('#applyContent').send_keys(test + '我的合作测试填写信息')
# sleep(0.5)
# d.find_element_by_link_text('申请').click()
# sleep(0.5)

