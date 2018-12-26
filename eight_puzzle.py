# package
import math
import numpy
import queue
import random
from collections import Counter
from functools import reduce
# self
import other


# 根据逆序数判断是否有解, 证明详见 https://blog.csdn.net/hnust_xiehonghao/article/details/7951173
def inversion(sequence):
    return reduce(sum, [sum(sequence[i] != -1 and sequence[j] != -1 and sequence[i] < sequence[j] for i in range(len(sequence)) for j in range(i))])


# h 函数, 估计离　des 还有多远
def evaluate(now, des):
    return sum(l != r for l, r in zip(now, des)) - 1 + (now.index(-1) == des.index(-1))


# 每个拓展的节点要包含的信息
class element():
    # now 当前八数码状态, deep 已走过的深度, score 评估函数得分, father 父亲节垫
    def __init__(self, now, deep, score, father):
        self.now = now
        self.deep = deep
        self.score = score
        self.father = father
        self.id = ''.join([str(it) for it in now])  # 形成该状态的唯一标识符, 用于　Close 表判重

    # 定义优先级队列的比较函数
    def __lt__(self, rhs):
        return self.score < rhs.score

    # 将　i, j 的八数码状态交换, 主要是为了移动空格
    def transform(self, i, j):
        self.now[i], self.now[j] = self.now[j], self.now[i]


# 只能解决二维　N * N 的八数码问题;　有时间试试　N * N * N 三维乃至于多维
# 而且 8 个数字不能有重复, 以免非法的八数码
def solve(src, des, move, g=lambda x: x, h=evaluate):
    # 判断状态是否非法
    if(len(Counter(src)) != len(src) or Counter(src) != Counter(des)):
        raise "起始状态　or 目标状态非法"
    # 利用逆序数的性质判断是否有解
    if((inversion(src) & 1) != (inversion(des) & 1)):
        return None
    # 如果起点和目标一样, 直接返回起点信息即可
    begin = element(src, 0, h(src, des), None)
    if(src == des):
        return begin
    openList = queue.PriorityQueue()  # 优先级队列这里还可以继续优化
    openList.put(begin)
    closedLost = {begin.id: 1}  # 利用字典和状态的唯一标识　id 来维护　Close 表
    while(not openList.empty()):
        cur = openList.get()    # Open 表中得分最低的
        blank = cur.now.index(-1)  # 找到空格
        for direct in move[blank]:  # 向多个方向拓展
            if(direct == -1):
                continue
            cur.transform(direct, blank)  # 空格移动, 产生新状态
            expansion = element(list(cur.now), cur.deep + 1,
                                g(cur.deep) + h(cur.now, des), cur)
            cur.transform(direct, blank)
            if(expansion.now == des):  # 已搜索到解
                return expansion
            if(expansion.id not in closedLost.keys()):  # 未在　Close 表中
                openList.put(expansion)
                closedLost[expansion.id] = 1
    return None


def fit(src, des):
    L = int(math.sqrt(len(src)))
    move = other.make_move(L)
    res = solve(src, des, move)
    print('\n\n从　', src, '\n到　', des)
    if(res != None):
        print('\nsearch success ', res.deep, ' 步 : \n')
        printlist = []
        while(res != None):
            printlist.append(res.now)
            res = res.father
        printlist = reversed(printlist)
        for it in printlist:
            print(numpy.array(it).reshape(L, L), '\n')
    else:
        print('\nsearch fail 无解')


if __name__ == '__main__':
    src = [2, 8, 3, 1, 6, 4, 7, -1, 5]
    des = [1, 2, 3, 8, -1, 4, 7, 6, 5]
    fit(src, des)

    src = [1, 2, 3, 4, 5, 6, 7, 8, -1]
    des = [2, 1, 3, 4, 5, 6, 7, 8, -1]
    fit(src, des)

    src = [1, 2, 3, 4, 6, 7, 8, -1, 5, 10, 11, 12, 9, 13, 14, 15]
    des = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, -1]
    fit(src, des)

    # src = [5, 16, 2, -1, 4, 10, 1, 6, 14, 9, 24, 11, 7,
    #        17, 3, 23, 19, 18, 12, 8, 20, 21, 15, 22, 13]
    # des = [5, 1, 2, 3, 4, 10, 6, 7, -1, 9, 24, 11, 12,
    #        8, 18, 23, 19, 15, 13, 14, 20, 21, 22, 16, 17]
    # fit(src, des)

    # ex = list(range(-1, 25))
    # ex.remove(0)
    # one = element(ex, 0, 0, 0)
    # print(one.now)
    # move = other.make_move(5)
    # for i in range(100):
    #     blank = one.now.index(-1)
    #     print(blank)
    #     nex = move[blank][random.randint(0, 3)]
    #     if(blank == -1):
    #         continue
    #     one.transform(blank, nex)
    #     print(one.now)
