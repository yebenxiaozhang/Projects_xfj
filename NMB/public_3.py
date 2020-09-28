# 算术运算符
num_a = 22
num_b = 45
# 加法
print(num_a + num_b)

# 减法
print(num_a - num_b)

# 乘法
print(num_a * num_b)

# 除法
print(num_a / num_b)

# 余数
print(num_a % num_b)

count = 0
# 西瓜 30
count = count + 30
# 冰  50
count = count + 50
# 卫  20
count += 20
print(count)

# 在原来的基础上 减掉50
# count = count - 50
count -= 50
print(count)

# 相等  == 结果：真与假
num_a = 22
num_b = 45

print(num_a == num_b)  # False
print(num_a < num_b)   # True
print(num_a > num_b)   # False
print('-------------')
print(num_a <= num_b)  # True
print(num_a >= num_b)  # False
# 不等于
print(num_a != num_b)  # True

str_a = "hello"
str_b = "work"
print(str_a != str_b)  # True

# or   条件A or 条件B  有一个为真  则为真
# and  条件A and 条件B  有一个为假  则为假
# not  notA A为真则假   A为假则真
print("----------------------------------")
print(num_a == 22 or False)
print(num_a == 22 and False)
print(num_a == 22 and not False)
print(not num_b > 100)

# 成员名  in 集合对象 在集合里则为True 负责为False
a = ["A", "B", "C罗", "D", "E", "F"]
b = {"name": "A",
     "sex": "male",
     "height": 190
     }
print("**************************")
print("C罗" in a)        # True
print("梅西" in a)       # False
print("梅西" not in a)   # True

print('name' not in b.keys())  # False
# ["name", "sex", "height"]
print('190' not in b.values())  # False
# ["A", "male", 190]

