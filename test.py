import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import pandas as pd
import seaborn as sns


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
    # print(np.linspace(0, 10, 6))
    # data = pd.DataFrame({'A': [1, 2, 3, 4, 5, 6, 7, 8],
    #                      'B': [12, 12, 13, 14, 15, 16, 17, 0]})
    # s = 'A'
    # print(data[s])
    ma = np.array([[1, 2, 4], [1, 1, 1]])
    print(np.sum(ma))


if __name__ == '__main__':
    main()
