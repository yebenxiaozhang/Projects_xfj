import random
import pyecharts.options as opts
from pyecharts.charts import Bar3D

hours = ["厚度1","厚度2","厚度3","厚度4","厚度5","厚度6","厚度7","厚度8","厚度9","平均厚度"]
days = ["1", "2", "3", "4", "5", "6", "7"]

data = [(i, j, random.randint(0, 12)) for i in range(6) for j in range(24)]
data = [[d[1], d[0], d[2]] for d in data]


c=(
    Bar3D(init_opts=opts.InitOpts(width="900px", height="600px"))
    .add(
        series_name="",
        data=data,
        xaxis3d_opts=opts.Axis3DOpts(type_="category", data=hours),
        yaxis3d_opts=opts.Axis3DOpts(type_="category", data=days),
        zaxis3d_opts=opts.Axis3DOpts(type_="value"),
    )
    .set_global_opts(
        title_opts=opts.TitleOpts("标准3D柱状图"),
        visualmap_opts=opts.VisualMapOpts(
            max_=20,
            range_color=[
                "#313695",
                "#4575b4",
                "#74add1",
                "#abd9e9",
                "#e0f3f8",
                "#ffffbf",
                "#fee090",
                "#fdae61",
                "#f46d43",
                "#d73027",
                "#a50026",
            ],
        )
    )
    .render("标准3D柱状图.html")
)
c.render_notebook()
