import func


def checkTime(fileName):
    """
    check if there is a GPS point's time before cur GPS point's time,
    fileName's records such as:
              39.975541,116.330842,2008/09/01 00:15:00,none
          39.975354,116.330829,2008/09/01 00:15:02,none
          39.975427,116.330881,2008/09/01 00:15:04,none
          ......
          index of time : 2
        Args:
            fileName: the path of checked file
        """
    file = open(fileName)
    lineNum = 1
    pre = file.readline()
    pre = pre.strip('\n')
    while 1:
        lineNum += 1
        cur = file.readline()
        cur = cur.strip('\n')
        if not cur:
            break
        preArr = pre.split(',')
        curArr = cur.split(',')
        preTimeStr = preArr[2]
        curTimeStr = curArr[2]
        f = func.compareTime1(preTimeStr, curTimeStr)
        if f == 1:
            excep = '第 ' + str(lineNum) + ' 发生异常！'
            print(excep)
        pre = cur
    print('文件 ' + fileName + ' 处理结束！')


if __name__ == '__main__':
    path = '../../data/integration_process/integration_'
    for i in range(32):
        filePath = path + str(i + 1) + '.txt'
        checkTime(filePath)
