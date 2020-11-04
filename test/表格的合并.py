# import xlrd
# import xlsxwriter
#
# source_xls = ["G:/下载/简历/333/幸福家一手业务数据字典.xlsx"]
# target_xls = "G:/下载/简历/333/3.xlsx"
#
# # 读取数据
# data = []
# for i in source_xls:
#     wb = xlrd.open_workbook(i)
#     for sheet in wb.sheets():
#         for rownum in range(sheet.nrows):
#             data.append(sheet.row_values(rownum))
# print(data)
# # 写入数据
# workbook = xlsxwriter.Workbook(target_xls)
# worksheet = workbook.add_worksheet()
# font = workbook.add_format({"font_size": 14})
# for i in range(len(data)):
#     for j in range(len(data[i])):
#         worksheet.write(i, j, data[i][j], font)
# # 关闭文件流
# workbook.close()

# """合并后去重"""
# import pandas as pd
#
# # 读取Excel中Sheet1中的数据
# data = pd.DataFrame(pd.read_excel('G:/下载/简历/333/3.xlsx', 'Sheet1'))
#
# # 查看读取数据内容
# print(data)
#
# # 查看是否有重复行
# re_row = data.duplicated()
# print(re_row)
#
# # 查看去除重复行的数据
# no_re_row = data.drop_duplicates()
# print(no_re_row)
#
# # 查看基于[物品]列去除重复行的数据
# wp = data.drop_duplicates(['业务'])
# print(wp)
#
# # 将去除重复行的数据输出到excel表中
# no_re_row.to_excel("过滤重复行.xlsx")
