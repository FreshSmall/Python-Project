from pyecharts.charts import Bar
from pyecharts import options
from pyecharts.globals import ThemeType
from pyecharts.charts import Map


def bar():
    # 创建柱状图对象并设置初始参数（宽度、高度、主题）
    bar = Bar(init_opts=options.InitOpts(
        width='600px',
        height='450px',
        theme=ThemeType.CHALK
    ))
    # 设置横轴数据
    bar.add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
    # 设置纵轴数据（第一组）
    bar.add_yaxis(
        "商家A",
        [25, 20, 36, 10, 75, 90],
    )
    # 设置纵轴数据（第二组）
    bar.add_yaxis(
        "商家B",
        [15, 12, 30, 20, 45, 60]
    )
    # 设置纵轴数据（第三组）
    bar.add_yaxis(
        "商家C",
        [12, 32, 40, 52, 35, 26]
    )
    # 添加全局配置参数
    bar.set_global_opts(
        # 横轴相关的参数
        xaxis_opts=options.AxisOpts(
            axislabel_opts=options.LabelOpts(
                color='white'
            )
        ),
        # 纵轴相关的参数（标签、最小值、最大值、间隔）
        yaxis_opts=options.AxisOpts(
            axislabel_opts=options.LabelOpts(
                color='white'
            ),
            min_=0,
            max_=100,
            interval=10
        ),
        # 标题相关的参数（内容、链接、位置、文本样式）
        title_opts=options.TitleOpts(
            title='2021年销售数据展示',
            title_link='http://www.qfedu.com',
            pos_left='2%',
            title_textstyle_opts=options.TextStyleOpts(
                color='white',
                font_size=16,
                font_family='SimHei',
                font_weight='bold'
            )
        ),
        # 工具箱相关的参数
        toolbox_opts=options.ToolboxOpts(
            orient='vertical',
            pos_left='right'
        )
    )
    # 在Jupyter Notebook中渲染图表
    bar.render('index.html')


def map():
    data = [
        ('广东', 594), ('浙江', 438), ('四川', 316), ('北京', 269), ('山东', 248),
        ('江苏', 234), ('湖南', 196), ('福建', 166), ('河南', 153), ('辽宁', 152),
        ('上海', 138), ('河北', 86), ('安徽', 79), ('湖北', 75), ('黑龙江', 70),
        ('陕西', 63), ('吉林', 59), ('江西', 56), ('重庆', 46), ('贵州', 39),
        ('山西', 37), ('云南', 33), ('广西', 24), ('天津', 22), ('新疆', 21),
        ('海南', 18), ('内蒙古', 14), ('台湾', 11), ('甘肃', 7), ('广西壮族自治区', 4),
        ('香港', 4), ('青海', 3), ('新疆维吾尔自治区', 3), ('内蒙古自治区', 3), ('宁夏', 1)
    ]
    map_chart = Map()
    map_chart.add('', data, 'china', is_roam=False)
    map_chart.render('indexMap.html')


if __name__ == '__main__':
    map()
