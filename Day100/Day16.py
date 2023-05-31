from abc import ABCMeta, abstractmethod

prices = {
    'APPLE': 191.88,
    'GOOG': 1186.96,
    'IBM': 149.24,
    'ORCL': 48.44,
    'ACN': 166.89,
    'FB': 208.09,
    'SYMC': 21.29
}

names = ['关羽', '张飞', '赵云', '马超', '黄忠']
courses = ['语文', '数学', '英语']

if __name__ == '__main__':
    prices2 = {key: value for key, value in prices.items() if value > 1000}
    print(prices2)
    #
    # scores = [[None] * len(courses) for _ in range(len(names))]
    # for row, name in enumerate(names):
    #     for col, course in enumerate(courses):
    #         scores[row][col] = float(input(f'请输入{name}的{course}成绩'))
    #         print(scores)
