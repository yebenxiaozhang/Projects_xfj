# 函数


def cup():
    # 实现这个功能的代码
    print("盛水")
    
# 调用函数


cup()
cup()

print("------------------------------------")


# 要使用某一个功能  ---必须提供对应的数据
# 参数  ---内部功能实现的时候，必须要用到的值
def bus_385(bus_card):
    print("刷了公交卡：", bus_card)
    print("我用公交卡坐车，从公司到家！")


bus_385("22334455")
bus_385("22334456")

print("------------------------------------")


# 返回值的表示 ：return 变量  == 调用函数后 主动去接受返回值
def getMoney_from_ATM(card_num, passwd, money=200, bank="中国银行"):
    print("取钱操作！！！")
    if type(passwd) is str and len(passwd) == 6:
        print("密码格式正确")
    else:
        print("密码格式错误，请重来")
        return
    print("卡号： ", card_num, "密码： ", passwd, "取钱金额： ", money)
    print(bank)
    return [card_num, money]


def buy(RMB):
    pass


# # 位置参数
# getMoney_from_ATM("1122335544", "123245", 500)
# # 默认参数 money = 200
# getMoney_from_ATM("1122335544", "123245")
# getMoney_from_ATM("1122335544", "123245", 1000)
# res = getMoney_from_ATM("1122335544", "123245", bank="招商银行")
# print(res)
# print("我去买小龙虾！！！", res[1])

res = getMoney_from_ATM("1122335544", "1213245", bank="招商银行")
print(res)
