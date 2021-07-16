from pyecharts.faker import Faker
from pyecharts.charts import Bar3D
from pyecharts import options as opts
import random

data = [(i, j, random.randint(110, 120)) for i in range(18) for j in range(10)]
# 创建数据，数据是一个列表，每一项都是一个三个元素组成的列表/元祖


# 【x坐标，y坐标，z坐标】

bar3d = Bar3D()
bar3d.add(

   "",

   data,

   # xaxis3d_opts=opts.Axis3DOpts(Faker.clock,type_="category"),
	xaxis3d_opts=opts.Axis3DOpts(type_ = 'value',name = '次数'),
    yaxis3d_opts=opts.Axis3DOpts(type_ = 'value',name = '厚度'),
    zaxis3d_opts=opts.Axis3DOpts(type_="value"),                  #数值
   )
bar3d.set_global_opts(
   visualmap_opts=opts.VisualMapOpts(max_=240),
   title_opts=opts.TitleOpts(title="3D演示"),
)
bar3d.render()