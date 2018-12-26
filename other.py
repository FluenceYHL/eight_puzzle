# package
import numpy
# self


def make_move(l):
    cnt = 0
    matrix = numpy.full((l + 2, l + 2), -1)
    for i in range(1, l + 1):
        for j in range(1, l + 1):
            matrix[i][j] = cnt
            cnt = cnt + 1
    # print('初始矩阵 : \n', matrix)
    res = numpy.zeros((l ** 2, 4))
    for i in range(l + 2):
        for j in range(l + 2):
            cur = matrix[i][j]
            if(cur != -1):
                res[cur][0] = matrix[i - 1][j]
                res[cur][1] = matrix[i][j + 1]
                res[cur][2] = matrix[i + 1][j]
                res[cur][3] = matrix[i][j - 1]
    return res.astype(numpy.int32)


if __name__ == '__main__':
    print(make_move(3))
