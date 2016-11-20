import time
from math import *
import datetime
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np


def compareTime1(str1, str2):
    """
    Args:
        str1, str2 are the string of time
    Returns:
        0: if time of str1 appears before str2
        1: or not
    """
    t1_struct_time = time.strptime(str1, '%Y/%m/%d %H:%M:%S')
    t2_struct_time = time.strptime(str2, '%Y/%m/%d %H:%M:%S')
    res = 0
    # print(t1_struct_time)
    # print(t2_struct_time)
    # print(t1_struct_time < t2_struct_time)
    if t1_struct_time > t2_struct_time:
        res = 1
    return res


def compareTime2(str1, str2, str3):
    """
    Args:
        str1, str2, str3 are the string of time
    Returns:
        1: if time of str3 is in str1~str2
        0: or not
    """
    f1 = compareTime1(str1, str3)
    f2 = compareTime1(str2, str3)
    res = 0
    if f1 == 0 and f2 == 1:
        res = 1
    return res


def getDistance(latA, lonA, latB, lonB):
    if latA == latB and lonA == lonB:
        return 0
    ra = 6378140  # radius of equator: meter
    rb = 6356755  # radius of polar: meter
    flatten = (ra - rb) / ra  # Partial rate of the earth
    # change angle to radians
    radLatA = radians(latA)
    radLonA = radians(lonA)
    radLatB = radians(latB)
    radLonB = radians(lonB)

    pA = atan(rb / ra * tan(radLatA))
    pB = atan(rb / ra * tan(radLatB))
    x = acos(sin(pA) * sin(pB) + cos(pA) * cos(pB) * cos(radLonA - radLonB))
    c1 = (sin(x) - x) * (sin(pA) + sin(pB))**2 / cos(x / 2)**2
    if sin(x / 2) == 0:
        return getDistance2(latA, lonA, latB, lonB)
    c2 = (sin(x) + x) * (sin(pA) - sin(pB))**2 / sin(x / 2)**2
    dr = flatten / 8 * (c1 - c2)
    distance = ra * (x + dr)
    return distance


def getDistance2(latA, lonA, latB, lonB):
    """
    deal with the case which function getDistance could not handle
    """
    radLatA = radians(latA)
    radLonA = radians(lonA)
    radLatB = radians(latB)
    radLonB = radians(lonB)
    a = radLatA - radLatB
    b = radLonA - radLonB
    s = 2 * asin(sqrt(pow(sin(a / 2), 2) + cos(radLatA) *
                      cos(radLatB) * pow(sin(b / 2), 2)))
    s = s * 6378137
    s = round(s * 10000) / 10000
    return s


def getTimeInterval(timeStr1, timeStr2):
    """
    Args:
        timeStr1 and timeStr2 are the string of time,
        default: timeStr1 is before timeStr2
    Returns:
        the interval of timeStr1 and timeStr2 (type: seconds)
    """
    date1 = time.strptime(timeStr1, "%Y/%m/%d %H:%M:%S")
    date2 = time.strptime(timeStr2, "%Y/%m/%d %H:%M:%S")
    d1 = datetime.datetime(date1[0], date1[1], date1[
                           2], date1[3], date1[4], date1[5])
    d2 = datetime.datetime(date2[0], date2[1], date2[
                           2], date2[3], date2[4], date2[5])
    return (d2 - d1).seconds


def isTrafficCongestion(pointsList, changeAngle, changeRate):
    """
    Args:
        pointsList: list of [point_id, lat, lon]
                content: [(39, 39.8146666666667, 119.476816666667),......]
        changeAngle: three points relative change angle threshold
        changeRate: the number of change angle which is greater than
                    changeAngle divide the length of pointsList
    Returns:
        1: this points set is in traffic congestion
        0: or not
    """
    #  the number of GPS point which change angle is greate than changeAngle
    chSP = 0
    stlen = len(pointsList)
    """
        if pointsList contains only one or two GPS point, we regard this
        condition as non-congestion, because it is possible that user go
        into the area (such as underground shop) which he/she cannot receive
        the signal.
    """
    if stlen == 1 or stlen == 2:
        return 0
    # at least three GPS points, we can calculate the angle change
    for i in range(stlen - 2):
        cur = pointsList[i]
        next = pointsList[i + 1]
        last = pointsList[i + 2]
        tempDegree1 = getDegree(cur[1], cur[2], next[1], next[2])
        tempDegree2 = getDegree(next[1], next[2], last[1], last[2])
        degreeDiff = abs(tempDegree2 - tempDegree1)
        if degreeDiff >= changeAngle:
            chSP += 1
    print("the number of GPS points whose change angle is greater than thd:")
    writeFile('stay_point_set_result.txt',
              'the number of GPS points whose change angle is greater than thd:' +
              str(chSP))
    print(chSP)
    print("total number of Stay point number:")
    writeFile('stay_point_set_result.txt',
              'total number of Stay point number:' + str(stlen))
    print(stlen)
    if chSP / stlen < changeRate:
        return 1
    else:
        return 0


def getDegree(latA, lonA, latB, lonB):
    """
    Args:
        point p1(latA, lonA)
        point p2(latB, lonB)
    Returns:
        bearing between the two GPS points,
        default: the basis of heading direction is north
    """
    radLatA = radians(latA)
    radLonA = radians(lonA)
    radLatB = radians(latB)
    radLonB = radians(lonB)
    dLon = radLonB - radLonA
    y = sin(dLon) * cos(radLatB)
    x = cos(radLatA) * sin(radLatB) - sin(radLatA) * cos(radLatB) * cos(dLon)
    brng = degrees(atan2(y, x))
    brng = (brng + 360) % 360
    return brng


def isNormalDistr(pointsList):
    """
    check if the list of pointsList is consistent with normal distribution,
    we caculate the distance between each two consecutive points.

    Args:
        pointsList: list of [point_id, lat, lon]
                content: [(39, 39.8146666666667, 119.476816666667),......]
    Returns:
        1: this points set is consistent with normal distribution.
        0: or not
    """
    distList = []
    lenList = len(pointsList)
    if lenList == 0 or lenList == 1 or lenList == 2:
        return 0
    index = 0
    while index < lenList - 1:
        cur = pointsList[index]
        next = pointsList[index + 1]
        dist = getDistance(cur[1], cur[2], next[1], next[2])
        distList.append(dist)
    distArray = np.array(distList)
    test_stat = stats.kstest(distArray, 'norm')
    pValue = test_stat.pvalue
    if pValue > 0.05:
        # showNormalDistr(distArray)
        return 1
    else:
        return 0


def showNormalDistr(x, mu, sigma):
    """
        draw figure of normal distribution
    """
    y = stats.norm.pdf(x, 0, 1)
    # print(y)
    plt.plot(x, y)
    plt.title('Normal: $\mu$=%.1f, $\sigma^2$=%.1f' % (mu, sigma))
    plt.xlabel('x')
    plt.ylabel('Probability density', fontsize=15)
    plt.show()


def getMuAndSigma(arrayDist):
    """
        get mathematical expection and standard deviation
        from normal distribution

        Args:
            arrayDist: type: numpy.ndarray
        Returns:
            mu: mathematical expection
            sigma: standard deviation
    """
    mu = arrayDist.mean()
    sigma = arrayDist.std()
    return mu, sigma


def noiseFilter(pointsList, thd):
    """
    noise filter: 3sigma rule, calculate
          (xi - mu)/sigma  >? thd
    Args:
        pointsList: list of [point_id, lat, lon]
                content: [(39, 39.8146666666667, 119.476816666667),......]
        thd: appointed value, such as 2, 2.6, 3 et.
    Returns:

        resPoints: result of stay point list,
                content: [(39, 39.8146666666667, 119.476816666667, 0),......],
                0 represents the GPS point is not deleted
                1 represents the GPS point is deleted
    """
    distList = []
    lenList = len(pointsList)
    if lenList == 0 or lenList == 1 or lenList == 2:
        pass
    index = 0
    while index < lenList - 1:
        cur = pointsList[index]
        next = pointsList[index + 1]
        dist = getDistance(cur[1], cur[2], next[1], next[2])
        distList.append(dist)
        index += 1
    distArray = np.array(distList)
    mu, sigma = getMuAndSigma(distArray)
    #  calculate noise
    j = 0
    # if firstFlag or lastFlag is 1, remove the first or last point from
    # pointslist
    firstFlag = 0
    lastFlag = 0
    resPoints = []
    pre = -9999
    while j < len(distArray):
        isDeleted = 0
        res = abs((distArray[j] - mu) / sigma)
        if res > thd:
            """
            if the outlier is a first or last point of stay
            points, remove them from stay point set to be merged
            with its posterier and pervious segment, or delete it
            from database (in this case, we can set field of is_deleted
            is 1)
            """
            if j == 0:
                firstFlag = 1
            elif j == len(distArray) - 1:
                lastFlag = 1
            else:
                if j - pre != 1:
                    isDeleted = 1
                    pre = j
        resPoints.append((pointsList[j + 1][0],
                          pointsList[j + 1][1],
                          pointsList[j + 1][2],
                          isDeleted))
        j += 1
    if lastFlag == 0:
        resPoints.append((pointsList[0][0],
                          pointsList[0][1],
                          pointsList[0][2],
                          0))
    if firstFlag == 0:
        resPoints.append((pointsList[-1][0],
                          pointsList[-1][1],
                          pointsList[-1][2],
                          0))
    return resPoints


def writeFile(path, content):
    """
    append content to the file of variable path

    Args:
         path: file path and file name
         content: string type, you need to deliver string type
    """
    fileObj = open(path, 'a+')
    fileObj.write(content + '\n')
    fileObj.close()


if __name__ == '__main__':
    # f1 = compareTime('36.9848416666667,111.8207,1,2444.00000371488,39209.7241087963,2007/05/07,17:22:43',
    #                 '36.9846633333333,111.820741666667,0,2472.00000375744,39209.7241319444,2007/05/07,17:22:45')
    # print(f1)
    print(compareTime2('2009/9/28 8:29:35',
                       '2009/9/28 9:06:32', '2009/9/28 9:07:32'))

    # output: 896532.7847032619
    print(getDistance(32.060255, 118.796877, 39.904211, 116.407395))
    # output: 84.74286724141308
    print(getDistance(39.9660666666667, 116.352433333333,
                      39.9659666666667, 116.353416666667))
    # output: 84.74286724141308
    print(getDistance(39.9659666666667, 116.353416666667,
                      39.9660666666667, 116.352433333333))

    # output: 43s
    print(getTimeInterval("2008/04/30 21:54:12", "2008/04/30 21:54:55"))

    # output: 97.5579543643621
    print(getDegree(39.9660666666667, 116.352433333333,
                    39.9659666666667, 116.353416666667))

    # output: 96.5126242349993
    print(getDegree(39.099912, -94.581213,
                    38.627089, -90.200203))

    # arr = np.array([34, 54, 23, 23, 34, 44, 60])
    # print(np.sort(arr))
    # showNormalDistr(np.sort(arr))

    # output: 29.4   17.2116239792
    distArray = np.array([13, 23, 12, 44, 55])
    mu, sigma = getMuAndSigma(distArray)
    print(mu)
    print(sigma)

    #  output: 0.0853
    print(getDistance2(39.9660666666667, 116.352433333333,
                       39.9660666666667, 116.352434333333))
