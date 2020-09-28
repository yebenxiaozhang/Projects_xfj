# 编写一个程序
# 1、能在当前目录下查找文件名包含制定字符串的文件;
# 2、并打印出绝对路径

# OS：opreate system
# OS模块是python标准库钟的一个用于访问操作系统功能的模块
# 使用OS模块中提供的接口，可以实现跨平台访问

# 通常操作：
# 1、获取平台信息
# 2、对目录的操作
# 3、判断操作

import os
print(os.sep)             # 主要用于系统路径的分隔符

print(os.name)            # 指示你正常使用的工作平台 WINDOWS  是NT

print(os.getenv("Path"))  # 获取环境变量

print(os.getcwd())        # 获取当前路径
print("------------------------------")
# 示例1
dirs = "D:\\android-sdk-windows"
# os.listdir()    # 返回指示目录下的所有的文件和目录名
files = os.listdir(dirs)
print(files)


# 判断文件或者目录是否存在。存在则返回为True  否则为False
if os.path.exists(dirs):
    # fullpath = dirs + "//" + files[0]
    # 连接目录与文件名
    fullpath = os.path.join(dirs, files[1])
    print(fullpath)
    if os.path.isfile(fullpath):
        print("我是一个文件")
    else:
        print("我不是一个文件")

print("------------------------------")

# 示例2
my_dirs = "D:\\android-sdk-windows\\test\\office"
# 判断是否有该目录，要是没有 则创建
if not os.path.exists(my_dirs):
    os.makedirs(my_dirs)

print("------------------------------")

# 示例3
if os.path.exists("D:\\android-sdk-windows\\test"):
    os.rmdir("D:\\android-sdk-windows\\test\\office")
    # os.removedirs("D:\\android-sdk-windows\\test")

print("------------------------------")

'''
编写一个程序
    1、能在当前目录下查找文件名包含制定字符串的文件;
    2、并打印出绝对路径
'''
sub_str = "os"
current_path = os.getcwd()
files = os.listdir(current_path)
for item in files:
    print(item)
    if os.path.isfile(os.path.join(current_path, item)):
        # 看看文件名是否包含指定的字符串
        # 然后指定的输出

        # 字符串的查找
        if item.find(sub_str) != -1:
            print(os.path.join(current_path, item))
            pass


# 增删改查
# os.mkdir()      # 创建一个目录，值创建一个目录文件
# os.rmdir()      # 删除一个空目录，若目录中有文件则无法删除
# os.makedirs(dirname)     # 可以生产多层递归目录，如果目录全部存在，则创建失败
# os.removedirs(dirname)   # 可以删除多层递归的空目录  若目录中有文件则无法删除
# os.chdir()               # 改变当前目录，到指定目录中
# os.rename()              # 重命令目录或者文件名。重命名后的文件名已存在，则重命名失败

# 判断
# os.path.exists(path=)   # 判断文件或者目录是否存在。存在则返回为True  否则为False
# os.path.isfile(path=)   # 判断是否为文件。是文件则返回为True  否则为False
# os.path.isdir(path=)    # 判断是否问目录 是目录则返回为True  否则为False

# os.path.basename(path=)   # 返回文件名
# os.path.dirname(path=)    # 返回文件路径
# os.path.getsize(name)     # 获取文件大小 如果那么是目录放回OL
# os.path.abspath(name)     # 获取绝对路径
# os.path.join(path=,name)  # 连接目录与文件名
