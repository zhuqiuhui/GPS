import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


def getXY():
    x = 3
    y = 6
    return x, y


def writeFile(path, content):
    fileObj = open(path, 'a+')
    fileObj.write(content)
    fileObj.close()


def getClusNum(compList):
    """
       get number cluster
       Args:
            compList: such as [(1, 0, 1), (2, 1, 0)...]
       Returns:
            total cluster number of column 2
            total cluster number of column 3
    """
    sum1 = 0
    sum2 = 0
    index = 1
    pre = compList[0]
    if pre[1] == 1:
        sum1 = 1
    if pre[2] == 1:
        sum2 = 1
    lenCompList = len(compList)
    while index < lenCompList:
        cur = compList[index]
        if pre[1] == 0 and cur[1] == 1:
            sum1 += 1
        if pre[2] == 0 and cur[2] == 1:
            sum2 += 1
        index += 1
        pre = cur
    return sum1, sum2


def main():
    # mu = 0  # mean
    # sigma = 1  # standard deviation
    # x = np.arange(-5, 5, 0.1)
    # y = stats.norm.pdf(x, 0, 1)
    # print(y)
    # plt.plot(x, y)
    # plt.title('Normal: $\mu$=%.1f, $\sigma^2$=%.1f' % (mu, sigma))
    # plt.xlabel('x')
    # plt.ylabel('Probability density', fontsize=15)
    # plt.show()

    # print(type(np.random.normal(0, 1, 10)))
    # a = np.array([1, 2, 3, 4])
    # print(a)
    # alist = []
    # alist.append(6)
    # alist.append(7)
    # alist.append(8)
    # alist.append(9)
    # print(type(np.array(alist)))

    # x = np.random.normal(0, 1, 1000)
    # test_stat = stats.kstest(x, 'norm')
    # print(type(test_stat))
    # print(test_stat)
    # print(test_stat.pvalue)

    # arr = np.array([34, 54, 23, 23, 34, 44, 60])
    # arr = np.argsort(arr)
    # print(arr)
    # x, y = getXY()
    # print(x)
    # # print(y)
    # listp = np.array([1, 2, 3, 4])
    # print(len(listp))
    # print(type(listp))
    # for i in listp:
    #     print(i)
    # pList = [1, 2, 3, 4, 5]
    # pList.pop(len(pList)-1)
    # pList.pop(0)
    # print(pList)
    # pList = [(1, 2, 3), (4, 5, 6), (7, 8, 9)]
    # # print(pList[-1])
    # # print("%s records %s " % (len(pList), 9))
    # writeFile('write.txt', "str(pList)" + "\n")
    # writeFile('write.txt', str(pList))
    # lineCuple = (1, 2, 2)
    # lineCuple = lineCuple + (3)
    # print(lineCuple)
    # x = [[1, 2, 3], [4, 5, 6]]
    # y = [(7, 8, 9), [33, 23,22]]
    # x = [[1, 2, 3]]
    # y = [[7, 8, 9]]
    # for i, j in zip(x, y):
    # 	print(i)
    # 	print(j)
    # lineList = [(13187, 40.2894833333333, 116.212283333333, 0),
    #             (13188, 40.2896166666667, 116.21215, 0),
    #             (13189, 40.2898333333333, 116.212183333333, 0),
    #             (13190, 40.28995, 116.21225, 0)]
    # for item in lineList:
    #     print(item[0:3])
    # dist1 = np.array([35.77614704, 23.8507647, 20.60117184, 27.35237362, 51.03,
    #                   48.38809363, 21.50955565, 14.74592028, 17.2563313, 41.08,
    #                   14.7657882, 20.49371959, 11.36716191, 26.34382325, 13.56,
    #                   19.54089429, 13.26133225, 14.14017804])
    # dist2 = np.random.normal(0, 1, 100)
    # dist3 = np.array([1, 2, 22, 23, 24, 22, 18, 45, 56, 66])
    # dist4 = np.array([36, 24, 21, 27, 51,
    #                   48, 22, 15, 17, 41,
    #                   15, 20, 11, 26, 14,
    #                   20, 13, 14])
    # dist5 = np.array((12, 12, 12, 12, 13, 11, 13, 11,9,15))
    # print(stats.kstest(dist1, 'norm'))
    # print(stats.kstest(dist2, 'norm'))
    # print(stats.kstest(dist3, 'norm'))
    # print(stats.kstest(dist4, 'norm'))
    # print(stats.kstest(dist5, 'norm'))
    # al = [(1, 0, 1),
    #       (2, 1, 0),
    #       (3, 1, 1),
    #       (4, 1, 1),
    #       (5, 1, 0),
    #       (6, 0, 0),
    #       (7, 1, 1),
    #       (8, 1, 1),
    #       (9, 1, 1),
    #       (10, 0, 1),
    #       (11, 0, 0),
    #       (12, 1, 1),
    #       (13, 0, 0),
    #       (14, 1, 0)]
    # spCorNum = 0
    # f = 0
    # for item in al:
    #     if item[2] == 1:
    #         if item[1] == 1 and f == 0:
    #             # find
    #             spCorNum += 1
    #             f = 1
    #     else:
    #         f = 0
    # print(spCorNum)
    # sum1, sum2 = getClusNum(al)
    # print(sum1)
    # print(sum2)
    # temp = []
    # temp.append(1)
    # temp.append(2)
    # temp.append(3)
    # sett = []
    # sett.append(temp)
    # sett.append(temp)
    # print(sett)
    # temp1 = [(732708, 'none'), (732709, 'non-walk-point'),
    #          (732710, 'walk-point'), (732711, 'walk-point')]
    # for label in temp1[0:3]:
    #     te = (label[0], 'test')
    #     temp1[1] = te
    # print(temp1)
    p = []
    p.append((2,))
    p.append((4,))
    print(p)


if __name__ == '__main__':
    main()
