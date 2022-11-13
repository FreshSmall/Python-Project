# -*-  coding: utf-8 -*-
import os, sys
import jieba, codecs, math
import jieba.posseg as pseg

names = {}  # 姓名字典
relationship = {}  # 关系字典
lineNames = []  # 每段内任务关系


def init_relation():
    jieba.load_userdict("dict.txt")  # 加载字典
    with codecs.open("busan.txt", "r", "utf-8") as f:
        for line in f.readlines():
            poss = pseg.cut(line)  # 分词并返回该词的词性
            lineNames.append([])  # 为新读入的每一段添加人物名称列表
            for w in poss:
                if w.flag != "nr" or len(w.word) < 2:
                    continue  # 当分词长度小于2时并且词性不为nr说明不是人名
                lineNames[-1].append(w.word)  # 为当前段的环境加一个人物

                if names.get(w.word) is None:
                    names[w.word] = 0
                    relationship[w.word] = {}
                names[w.word] += 1

    for name, times in names.items():
        print(name, times)


def build_relation():
    for line in lineNames:  # 对于每一段
        for name1 in line:
            for name2 in line:  # 每段中任意两个人
                if name1 == name2:
                    continue
                if relationship[name1].get(name2) is None:
                    relationship[name1][name2] = 1
                else:
                    relationship[name1][name2] = relationship[name1][name2] + 1


def make_relation():
    with codecs.open("busan_node.txt", "w", "utf-8") as f:
        f.write("Id Label Weight \r\n")
        for name, times in names.items():
            f.write(name + " " + name + " " + str(times) + "\r\n")

    with codecs.open("busan_edge.txt", "w", "utf-8") as f:
        f.write("Source Target Weight \r\n")
        for name, edges in relationship.items():
            for v, w in edges.items():
                if w > 3:
                    f.write(name + "" + v + "" + str(w) + "\r\n")


if __name__ == '__main__':
    init_relation()
    build_relation()
    make_relation()
