import numpy as np
import json
import sys
import datetime
import math
sys.path.append("..")
import preprocess.func as func


# not sure (need to statistic the velocity and acceleration distribution)
vth1 = 2.3  # divide velocity into low and middle level
vth2 = 5.2  # divide velocity into middle and high level
ath1 = 0.3  # divide acceleration into low and middle level
ath2 = 1.0  # divide acceleration into middle and high level

perTh = 0.85  # 85% of velocity and acceleration
Ar = 0.25  # ACR threshold value

# not sure
lowVth = 0.36  # near 0 point veloctiy
lowAth = 0.1  # near 0 point acceleration
busDistTh = 50  # the distance between bus top and low velocity point

degreeTh = 15  # the bais of angle (feaature HCR and ACP)
Vr = 0.36  # VCR threshold value
Vs = 3.2  # SR threshold value


def loadJsonFile(filePath):
    with open(filePath, encoding='utf-8') as jsonFile:
        data = json.load(jsonFile, encoding='utf-8')
        return data


def getBusInfo(rFilePath, wFilePath):
    """
    get bus information and write to file, such as:
        39.99975526301185,116.45155896898568,世安家园
        40.028746757346454,116.34170909875485,清河
        .......
    Args:
        rFilePath: read file path
        wFilePath: write file path
    """
    data = loadJsonFile(rFilePath)
    busData = data["features"]
    # print(len(busData))
    for item in busData:
        busType = item["properties"]["type"]
        # print(busType)
        if busType == 'bus_stop':
            name = item["properties"]["name"]
            if name is None:
                name = '空'
            lat = item["geometry"]["coordinates"][1]
            lon = item["geometry"]["coordinates"][0]
            tempList = []
            tempList.append(str(lat))
            tempList.append(str(lon))
            tempList.append(name)
            tempStr = ','.join(tempList)
            func.writeFile(wFilePath, tempStr)
    # print(busData)


def getSegDist(segment):
    """
    Args: segment: such as, [(202, 1, 1.41, 40.29, '2009/07/29 18:12:14',
                              116.150, 0.013, 2.83, 'walk'), ...]
              [(id,user_id,lat,lon,time_stamp,velocity,accelerometer,distance,mode)]
                 0,   1,    2,  3,    4,        5,          6,        7,  8
    Returns:
           distance of the segment
    """
    distSum = 0.0
    index = 1
    segLen = len(segment)
    while index < segLen:
        cur = segment[index]
        distSum += cur[7]
        index += 1
    return distSum


def getVFeature(segment):
    """
        Args: segment: such as, [(20202, 1, 1.41, 40.29, '2009/07/29 18:12:14',
                                  116.150, 0.013, 2.83, 'walk'), ...]
                  [(id,user_id,lat,lon,time_stamp,velocity,accelerometer,distance,mode)]
                     0,   1,    2,  3,    4,        5,          6,        7,  8
        Returns:
               85thV, MaxV1, MaxV2, MedianV, MinV, MeanV, Ev, Dv, HVR, MVR, LVR
    """
    vSet = []
    hNum = 0
    mNum = 0
    lNum = 0
    for point in segment:
        cur = point[5]
        vSet.append(cur)
        if cur <= vth1:
            lNum += 1
        elif cur >= vth2:
            hNum += 1
        else:
            mNum += 1
    vSetArray = np.array(vSet)
    vSetArray.sort()
    vLen = len(vSetArray)
    _85thIndex = round(vLen * perTh)
    if _85thIndex >= vLen:
        _85thIndex = vLen - 2
    _85thV = vSetArray[_85thIndex]
    MaxV1 = vSetArray[-1]
    MaxV2 = vSetArray[-2]
    MedianV = np.median(vSetArray)
    MinV = vSetArray[0]
    MeanV = np.mean(vSetArray)
    Ev = np.mean(vSetArray)
    Dv = np.var(vSetArray)
    HVR = hNum / vLen
    MVR = mNum / vLen
    LVR = lNum / vLen
    res = (_85thV, MaxV1, MaxV2, MedianV, MinV, MeanV, Ev, Dv, HVR, MVR, LVR)
    return res


def getAFeature(segment):
    """
     Args: segment: such as, [(202, 1, 1.41, 40.29, '2009/07/29 18:12:14',
                              116.150, 0.013, 2.83, 'walk'), ...]
              [(id,user_id,lat,lon,time_stamp,velocity,accelerometer,distance,mode)]
                 0,   1,    2,  3,    4,        5,          6,        7,  8
    Returns:
           85thA, MaxA1, MaxA2, MedianA, MinA, MeanA, Ea, Da, HAR, MAR, LAR
    """
    aSet = []
    hNum = 0
    mNum = 0
    lNum = 0
    for point in segment:
        cur = point[6]
        aSet.append(cur)
        if cur <= ath1:
            lNum += 1
        elif cur >= ath2:
            hNum += 1
        else:
            mNum += 1
    aSetArray = np.array(aSet)
    aSetArray.sort()
    aLen = len(aSetArray)
    _85thIndex = round(aLen * perTh)
    if _85thIndex >= aLen:
        _85thIndex = aLen - 2
    _85thA = aSetArray[_85thIndex]
    MaxA1 = aSetArray[-1]
    MaxA2 = aSetArray[-2]
    MedianA = np.median(aSetArray)
    MinA = aSetArray[0]
    MeanA = np.mean(aSetArray)
    Ea = np.mean(aSetArray)
    Da = np.var(aSetArray)
    HAR = hNum / aLen
    MAR = mNum / aLen
    LAR = lNum / aLen
    res = (_85thA, MaxA1, MaxA2, MedianA, MinA, MeanA, Ea, Da, HAR, MAR, LAR)
    return res


def getTS(segment):
    """
    Args: segment: such as, [(202, 1, 1.41, 40.29, '2009/07/29 18:12:14',
                              116.150, 0.013, 2.83, 'walk'), ...]
              [(id,user_id,lat,lon,time_stamp,velocity,accelerometer,distance,mode)]
                 0,   1,    2,  3,    4,        5,          6,        7,  8
    Returns:
           1: denotes T_busy (7:00-10:00 am 16:00-21:00)
           0: denotes T_idle
    """
    busyNum = 0
    idleNum = 0
    for point in segment:
        cur = point[4]
        t = datetime.datetime.strptime(cur, '%Y/%m/%d %H:%M:%S')
        h = t.hour
        if h >= 7 and h < 10 or h >= 16 and h < 21:
            busyNum += 1
        else:
            idleNum += 1
    if busyNum >= idleNum:
        return 1
    else:
        return 0


def getACR(segment):
    """
    Args: segment: such as, [(202, 1, 1.41, 40.29, '2009/07/29 18:12:14',
                              116.150, 0.013, 2.83, 'walk'), ...]
              [(id,user_id,lat,lon,time_stamp,velocity,accelerometer,distance,mode)]
                 0,   1,    2,  3,    4,        5,          6,        7,  8
    Returns:
           ACR value of segment
    """
    pre = segment[0]
    index = 1
    distSum = 0.0
    segLen = len(segment)
    num = 0
    while index < segLen:
        cur = segment[index]
        distSum += cur[7]
        if pre[6] == 0:
            ARate = 1
        else:
            ARate = abs(cur[6] - pre[6]) / pre[6]
        if ARate >= Ar:
            num += 1
        pre = cur
        index += 1
    if distSum == 0.0:
        return num
    else:
        return num / distSum


def getBSR(segment, busInfoPath):
    """
    Args: segment: such as, [(202, 1, 1.41, 40.29, '2009/07/29 18:12:14',
                              116.150, 0.013, 2.83, 'walk'), ...]
              [(id,user_id,lat,lon,time_stamp,velocity,accelerometer,distance,mode)]
                 0,   1,    2,  3,    4,        5,          6,        7,  8
          busInfoPath: bus information file
    Returns:
           BSR value of segment
    """

    # open bus information file
    busInfoFile = open(busInfoPath)
    try:
        allLines = busInfoFile.readlines()
    finally:
        busInfoFile.close()

    # get BSR value
    segLen = len(segment)
    num = 0
    lowNum = 0
    index = 0
    while index < segLen:
        cur = segment[index]
        min = 999999
        if cur[5] < lowVth and cur[6] < lowAth:
            # get near 0 point
            lowNum += 1
            for line in allLines:
                line = line.strip('\n')
                lineList = line.split(',')
                busLat = lineList[0]
                busLon = lineList[1]
                tempDist = func.getDistance(
                    cur[2], cur[3], float(busLat), float(busLon))
                if tempDist < min:
                    min = tempDist
            if min < busDistTh:
                num += 1
        index += 1
    if lowNum == 0:
        return 0
    else:
        return num / lowNum


def getACP(segment):
    """
    Args: segment: such as, [(202, 1, 1.41, 40.29, '2009/07/29 18:12:14',
                              116.150, 0.013, 2.83, 'walk'), ...]
              [(id,user_id,lat,lon,time_stamp,velocity,accelerometer,distance,mode)]
                 0,   1,    2,  3,    4,        5,          6,        7,  8
    Returns:
           ACP (angle change percent) value of segment
    """
    segLen = len(segment)
    index = 2
    num = 0
    pre = segment[1]
    preDegree = func.getDegree(segment[0][2], segment[0][3], pre[2], pre[3])
    while index < segLen:
        cur = segment[index]
        curDegree = func.getDegree(pre[2], pre[3], cur[2], cur[3])
        if abs(curDegree - preDegree) >= degreeTh:
            num += 1
        preDegree = curDegree
        pre = cur
        index += 1
    return num / segLen


def getHCR(segment):
    """
    Args: segment: such as, [(202, 1, 1.41, 40.29, '2009/07/29 18:12:14',
                              116.150, 0.013, 2.83, 'walk'), ...]
              [(id,user_id,lat,lon,time_stamp,velocity,accelerometer,distance,mode)]
                 0,   1,    2,  3,    4,        5,          6,        7,  8
    Returns:
           HCR (heading change rate) value of segment
    """
    segLen = len(segment)
    index = 2
    num = 0
    distSum = 0.0
    pre = segment[1]
    preDegree = func.getDegree(segment[0][2], segment[0][3], pre[2], pre[3])
    while index < segLen:
        cur = segment[index]
        distSum += cur[7]
        curDegree = func.getDegree(pre[2], pre[3], cur[2], cur[3])
        if abs(curDegree - preDegree) >= degreeTh:
            num += 1
        preDegree = curDegree
        pre = cur
        index += 1
    if distSum == 0.0:
        return num
    else:
        return num / distSum


def getSR(segment):
    """
    Args: segment: such as, [(202, 1, 1.41, 40.29, '2009/07/29 18:12:14',
                              116.150, 0.013, 2.83, 'walk'), ...]
              [(id,user_id,lat,lon,time_stamp,velocity,accelerometer,distance,mode)]
                 0,   1,    2,  3,    4,        5,          6,        7,  8
    Returns:
           SR (stop rate) value of segment
    """
    num = 0
    distSum = 0.0
    index = 0
    segLen = len(segment)
    while index < segLen:
        cur = segment[index]
        if index != 0:
            distSum += cur[7]
        if cur[5] < Vs:
            num += 1
        index += 1
    if distSum == 0.0:
        return num
    else:
        return num / distSum


def getVCR(segment):
    """
    Args: segment: such as, [(202, 1, 1.41, 40.29, '2009/07/29 18:12:14',
                              116.150, 0.013, 2.83, 'walk'), ...]
              [(id,user_id,lat,lon,time_stamp,velocity,accelerometer,distance,mode)]
                 0,   1,    2,  3,    4,        5,          6,        7,  8
    Returns:
           VCR (velocity change rate) value of segment
    """
    pre = segment[0]
    index = 1
    distSum = 0.0
    segLen = len(segment)
    num = 0
    while index < segLen:
        cur = segment[index]
        distSum += cur[7]
        if pre[5] == 0:
            VRate = 1
        else:
            VRate = abs(cur[5] - pre[5]) / pre[5]
        if VRate >= Vr:
            num += 1
        pre = cur
        index += 1
    if distSum == 0.0:
        return num
    else:
        return num / distSum


def main():
    # rfilePath = '../data/beijing_china_transport_points.geojson'
    # wfilePath = '../data/busInfo.txt'
    # getBusInfo(rfilePath, wfilePath)
    timeStr1 = '2009/07/29 10:12:12'
    timeStr2 = '2008/06/20 18:40:22'
    timeList = []
    timeList.append((timeStr1,))
    timeList.append((timeStr2,))
    print(getTS(timeList))


if __name__ == '__main__':
    main()
