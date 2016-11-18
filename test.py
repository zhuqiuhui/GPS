import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


def getXY():
    x = 3
    y = 6
    return x, y


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
    pList = [(1, 2, 3), (4, 5, 6), (7, 8, 9)]
    print(pList[-1])
    print("%s records %s " % (len(pList), 9))


if __name__ == '__main__':
    main()
