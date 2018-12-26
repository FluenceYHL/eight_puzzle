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


class idaStar():
    def transform(self, blank, nex):
        self.src[blank], self.src[nex] = self.src[nex], self.src[blank]

    def solve(self, blank, deep, pre, h=evaluate):
        t = h(self.src, self.des)
        # 记录最小的“至少要走的步数"
        if(self.step > t): 
            self.step = t
        # 如果已走的步数　+ 至少要走的步数　> limit 或者已找到解
        if(deep + t > self.limit or self.found is True):
            return
        if(t == 0):
            self.found = True
            return
        for nex in self.move[blank]:
            if(nex == -1 or nex == pre):
                continue
            # 如果找到了, 就会返回; 找不到就会被下一次的替代
            self.res[deep] = nex
            self.transform(blank, nex)
            self.solve(nex, deep + 1, blank)
            if(self.found):
                return
            self.transform(blank, nex)

    def fit(self, src, des, h=evaluate):
        # 判断状态是否非法
        if(len(Counter(src)) != len(src) or Counter(src) != Counter(des)):
            raise "起始状态　or 目标状态非法"
        # 利用逆序数的性质判断是否有解
        L = int(math.sqrt(len(src)))
        print('\n从\n', numpy.array(src).reshape(L, L), '\n到　\n',
              numpy.array(des).reshape(L, L))
        if((inversion(src) & 1) != (inversion(des) & 1)):
            print('无解')
            return None
        self.move = other.make_move(L)
        # 注意是深拷贝
        self.src, self.des = src.copy(), des.copy()
        self.found = False
        # 设置初始阈值
        self.limit = h(src, des)
        # 记录路径交换的点
        self.res = [-2] * 1022
        while(self.found is False):
            self.step = 1e8
            self.solve(src.index(-1), 0, -219, h)
            self.limit += self.step  # 小优化, 每次多走几步

        print('路径如下 : ')
        self.res = [it for it in self.res if(it != -2)]
        blank = src.index(-1)
        for it in self.res:
            src[blank], src[it] = src[it], src[blank]
            blank = it
            print(numpy.array(src).reshape(L, L))
        print('search success  ', len(self.res), ' 步')


if __name__ == '__main__':
    solve = idaStar()

    src = [2, 8, 3, 1, 6, 4, 7, -1, 5]
    des = [1, 2, 3, 8, -1, 4, 7, 6, 5]
    solve.fit(src, des)

    src = [1, 2, 3, 4, 5, 6, 7, 8, -1]
    des = [2, 1, 3, 4, 5, 6, 7, 8, -1]
    solve.fit(src, des)

    src = [1, 2, 3, 4, 6, 7, 8, -1, 5, 10, 11, 12, 9, 13, 14, 15]
    des = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, -1]
    solve.fit(src, des)
