"""
为什么测试人员必须掌握HTTP协议呢？

1、被测试的对象大部分都是b\s模式的项目
2、大部分接口自动化测试都是通过http(编码)请求实现的
3、通过http响应结果分析出大部分测试结果
3、postman、jmeter、lordrunner全部支持http协议接口测试


什么是HTTP协议

·协议
    约定。计算器与计算机之间通过网络实现通讯
    一些常见的协议：http soap smtp ftp
    了解TCP/IP协议
·http协议 超文本传输协议
    基于了客户端和服务端请求和响应，无状态，应用层的协议


状态码

1XX100-199： 正在请求
200：        正常请求完毕
3XX：        重定向（302） 被存储（304）
4XX：        客户端错误，服务端无法处理请求404
5XX：        服务器请求错误，500


请求头里面的q指的是权重

"""

