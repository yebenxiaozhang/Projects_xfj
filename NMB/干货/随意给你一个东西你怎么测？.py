"""
面试官的考察点：
    你能不能测试，没有需求文档或者需求文档不完整的东西
    能不能把测试用例设计方法应用到实际工作中去
    你的测试思维是否完整
    随口问问，看你的应变能力
"""

"""
例：电梯

·1、那么首先，你要反问一下面试官，需求是什么样的电梯，
是普通电梯、观光电梯还是其他
·2、如果回答是没有，那么你接下来的思路是：没有需求文档，
但是我了解电梯的基本业务，以此为依据从下面这几个方面进行分析
    
··功能测试（单个功能、逻辑业务/功能交互）、界面测试、易用性测试
兼容性测试、安全性测试、性能测试


功能测试---单个功能
1、电梯楼层按键是否正常
2、开关键是否正常
3、障碍物时，感应系统是否有效
4、应急按钮是否正常
5、屏幕显示是否正常
6、电梯楼层按键是否支持取消
7、电梯屏幕上下键是否正常    
8、同时关注屏幕显示、对应楼层、运行是否正常
9、呼叫、紧急呼叫

功能业务层面：
当前电梯停止、上行、下行状态，你上行、下行
1、电梯停止状态、电梯在一楼，有人按了10楼、18楼、上升到6楼的时候，
电梯外有人按上、下、电梯会不会停
2、电梯上行状态，上升到了8楼、有人按16楼，接着按2楼
3、电梯下行状态，22楼，16楼，23楼，
4、电梯满员，有人按上下，电梯是否会停
5、还未满员，某一楼层进入2人，继续3人、后满员是否报警
6、2部电梯，2楼、6楼 有人在1楼按  是否2 楼往下
7、多部电梯条件下~~~~

·电梯设备与功能设备间的接口对接
电梯与报警/呼叫系统、摄像头、通风扇、电灯、空调对接;停电情况下是否有的备用电池


界面测试
电梯外观、按钮的图标设计、长宽高、粘贴在电梯内部的提示说明（承重，报警装置说明）

易用性测试
1、按键高度、顺序
2、电梯是否有扶手、针对残疾人的扶手设计
3、防滑设计（地毯）、按键盲文设计
4、是否有语音提示
5、是否有摄像头、通风扇、电灯、空调

兼容性：
电梯的整体与其他设备的兼容性、与大楼楼层间的兼容、海底隧道
不同类型电梯电压、其他相关设备的兼容

安全测试：
1、防坠落、是否信号干扰
2、是否通风
3、暴力破坏电梯/超载，是否自动感应报警
4、是否耐热、不传热
5、关门障碍物是否有感应
6、突然断电，是否启用备用电池？  ---报警处理

压力测试

1、负载单人、多人、 且电梯平均等待时间可接受
2、满员情况长时间（一般7*24）
3、不断增加人数导致电梯故障 报警
4、超出极限负载测试，是否出现坠落故障

"""

"""
英雄联盟皮肤


UI：特效动作（回城、死亡）
    特效技能
    皮肤自带话术
    头像
    
功能：列队（1、选人等待队列 2、进入游戏的等待队列）
      进入游戏（游戏的流畅性是否收到印象、游戏画质是否收到影响、皮肤画质是否受到影响）
      使用皮肤的人数 1、排位  一种皮肤只能出现一次
                     2、匹配  10种不同皮肤，是否受到影响
                              多个同样皮肤，是否受到影响
                     3、娱乐模式  10种不同皮肤，是否受到影响
                                  多个同样皮肤，是否受到影响
      技能   特殊技能是否影响皮肤
      无视体积碰撞
      限时皮肤   卡时间节点
                 重复购买

竞技的公平：出招的姿势
            出招的弹道
            皮肤对于人物模型的大小，由装备引起的特性变化，皮肤是否显示
          
交互（皮肤展示的地方）： 在商城展示
                         角色选择
                         战利品
                         

性能 ··电脑的配置： 低配，显示是否收到影响
                    高配，显示是否收到影响
                    低特效，显示是否收到影响
                    特效全开，显示是否收到影响

可玩性（易用性）：开放性测试

兼容性： 电脑（笔记本、台式机）
         系统（WIN10、WIN7）
            
"""

"""
如何測式一个紙杯? ( 炎似于鉛篭、椅子、申梯、雨傘等!)

      。功能性:是否能装水，能装多少水
      。兼容性:是否能泡茶、珈俳，装酒精等液体，是否能在不同的温度下使用
      。界面性:杯子外双logo、字体、花紋能否湿示正常，是否会掉色
      。易用性:杯子能否正常手持、放在稟面会不会傾斜
      。安全性:杯子材貭是否安全，杯子是否対人体有害
      。圧カ測式: 从不同高度仍下来，用手挌圧杯子

"""

"""
给你一个购物车模块，你会如何设计测试用例?

      首先设计购物车的正常业务流程的用例，主要采用场景法来分析
      
      正常业务流程:
      将商品加入购物车- ->确认购买一>生成订单一 -> 查看订单详情，显示商品信息;
      且购物车商品被清空
      
      其他流程:

      将商品加入购物车、刪除购物车的商品一->查看购物车该商品是否被刪除

      将商品加入购物车、增加/减少商品数量一->查看购物车该商品是否增加/刪除

      购物车商品默认全选/部分勾选/不勾选一->点击购买一>生成订单显示全部商品/生成订单显示部分商品/提示未添加商品
      
      其他自己拓展。

"""

"""
优惠券怎么测

优惠券 

  客户端  
        ---➢领券可以领多张？
        ---➢可以叠加使用吗？
        ---➢过期了还能使用吗？
                    ---➢修改服务器的时间
                    ---➢修改数据库券的时间
        ---➢其他类型/店铺可以使用吗？
        ---➢券的数量
        ---➢下单页面，支付页的付款金额要正确
        ---➢使用优惠后，包邮？
         
  
  
  服务端
        ---➢金额（满50-10、满100-20）  
  
        ---➢创建规则
                    --➢购物券（生鲜、服装、电子产品、全场通用）
                    --➢店铺券（指定店铺，店铺的所有的商品都可以使用）
  
  查看优惠券
        ---➢分类显示我的优惠券
                ➢未使用
                ➢已使用
                ➢已过期
        ---➢排序
        ---➢点击优惠券会不会跳转到使用场景(需求)

  支付完成之后
        ---➢退款      优惠券不退 但是钱得退
        ---➢订单详情  使用优惠券下单，但是不支付，再去取消订单，优惠券没了        



"""

