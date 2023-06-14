import matplotlib.pyplot as plt
import numpy as np


def barChart():
    x = np.arange(4)
    y1 = np.random.randint(20, 50, 4)
    y2 = np.random.randint(10, 60, 4)
    plt.figure(figsize=(6, 4), dpi=120)
    # 通过横坐标的偏移，让两组数据对应的柱子分开
    # width参数控制柱子的粗细，label参数为柱子添加标签
    plt.bar(x - 0.1, y1, width=0.2, label='销售A组')
    plt.bar(x + 0.1, y2, width=0.2, label='销售B组')
    # 定制横轴的刻度
    plt.xticks(x, labels=['Q1', 'Q2', 'Q3', 'Q4'])
    # 定制显示图例
    plt.legend()
    plt.show()


def stackGraph():
    x = np.arange(4)
    y1 = np.random.randint(20, 50, 4)
    y2 = np.random.randint(10, 60, 4)
    labels = ['Q1', 'Q2', 'Q3', 'Q4']
    plt.figure(figsize=(6, 4), dpi=120)
    plt.bar(labels, y1, width=0.4, label='销售A组')
    # 注意：堆叠柱状图的关键是将之前的柱子作为新柱子的底部
    # 可以通过bottom参数指定底部数据，新柱子绘制在底部数据之上
    plt.bar(labels, y2, width=0.4, bottom=y1, label='销售B组')
    plt.legend(loc='lower right')
    plt.show()


def pie():
    data = np.random.randint(100, 500, 7)
    labels = ['苹果', '香蕉', '桃子', '荔枝', '石榴', '山竹', '榴莲']

    plt.figure(figsize=(5, 5), dpi=120)
    plt.pie(
        data,
        # 自动显示百分比
        autopct='%.1f%%',
        # 饼图的半径
        radius=1,
        # 百分比到圆心的距离
        pctdistance=0.8,
        # 颜色（随机生成）
        colors=np.random.rand(7, 3),
        # 分离距离
        # explode=[0.05, 0, 0.1, 0, 0, 0, 0],
        # 阴影效果
        # shadow=True,
        # 字体属性
        textprops=dict(fontsize=8, color='black'),
        # 楔子属性（生成环状饼图的关键）
        wedgeprops=dict(linewidth=1, width=0.35),
        # 标签
        labels=labels
    )
    # 定制图表的标题
    plt.title('水果销售额占比')
    plt.show()


if __name__ == '__main__':
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Songti SC']
    plt.rcParams['axes.unicode_minus'] = False
    #plt.figure(figsize=(8, 4), dpi=120, facecolor='darkgray')
    #plt.subplot(2, 2, 1)

    # barChart()
    # stackGraph()
    pie()
