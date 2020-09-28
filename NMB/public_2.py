# 数据类型：字符串
str1 = "可爱多"
# 数字类型： 整形：100 、 浮点型
num = 10
num_2 = 100.05

# 布尔值 True False
a = True
b = False

# 列表 = 字典
cc = None

# 请列出你在王者荣耀当中你最熟悉的五个英雄
# 表达一组数据 - list
hero_list = ["亚瑟", "鲁班七号", "狄仁杰", "武则天", "孙尚香"]
# 有序列表
# 读取数据 -变量名[下标] -从0开始
print(hero_list[0])
# 给列表添加数据   -列表变量名append(英雄名字)  -追加到末尾
hero_list.append("芈月")
print(hero_list)

# 修改列表当中，某一个位置的值
# 先找到这个位置，然后再更换数据
hero_list[1] = "芈月"
hero_list[5] = "鲁班七号"
print("修改之后的英雄榜:", hero_list)

# 获取列表的长度   -len(列表变量名)
print(len(hero_list))

# 获取列表的最后一个元素
print(hero_list[-1])
print(hero_list[len(hero_list)-1])

# str_hero = "亚瑟、鲁班七号、狄仁杰、武则天、孙尚香"

# 字典  key = value  键值对
# 键名 = 字符串
# 键值 = 各种数据类型
# 无序 - 键名唯一
yase_dict = {"name": "亚瑟",
             "type": "战士",
             "技能": "大宝剑",
             "玩家心得": "XXXXX",
             "年龄": "3",
             }

# 取值 - 根据键名来取值 - 字典的变量名[键名]
print(yase_dict['type'])
print(yase_dict['技能'])

# 给一个字典添加键值对 - 字典的变量名[键名]=键值  键名是不存在与字典中
yase_dict['装备'] = "XXXX"
print(yase_dict)

# 加皮肤
yase_dict["skin"] = ["皮肤1", "皮肤2", "皮肤3"]
print(yase_dict)

# 修改值
yase_dict["玩家心得"] = "好好玩!"
print(yase_dict)

# 获取字典的长度   -len(字典变量名)
print(len(yase_dict))
hero_list_new = [
    {"name": "亚瑟",
     "type": "战士"},
    {"name": "鲁班七号",
     "type": "射手"},
    {"name": "狄仁杰",
     "type": "射手"},
    yase_dict
]

# 修改新英雄亚瑟的type的值
# print(hero_list_new[0]["type"] = "辅助")
print(hero_list_new)
# 删除字典中的一个键值对
yase_dict.pop("name")
print(yase_dict)

