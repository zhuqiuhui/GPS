import DBUtil
import func

"""
add cloumn to table GPS_points_i(such as 1, 2 et al.) of database GPS in SQLite
Table: GPS_points_1
Table: GPS_label_1
"""
TimeThreshold = 1200  # 1200s or 20min
StayPoinTiThd = 200  # stay points time threshold
StayPoinDistThd = 50  # stay points distance threshold
vThreshold = 1.6  # m/s
aThreshold = 0.8  # m/s2
changeAngle = 19  # change angle
changeRate = 0.50  # change rate
"""
    we find ransition point if its in the distance of
    actual transition point.
"""
transiPointDist = 150


def addMode(DBPath, i):
    """
    Time-consuing operation, please run GetIntegrationFile.java in the folder
    named code, then run importDate.py to import cloumn "mode"
    """
    conn = DBUtil.get_conn(DBPath)
    # find all the label lines
    fetchAllLabelSql = 'select * from GPS_label_' + str(i)
    allLabelRecords = DBUtil.fetchAll(conn, fetchAllLabelSql)
    if allLabelRecords is None:
        print('fetch label Fail!')
        return
    fetchAllPointsSql = 'select * from GPS_points_' + str(i)
    allPointsRecords = DBUtil.fetchAll(conn, fetchAllPointsSql)
    if allPointsRecords is None:
        print('fetch points Fail!')
        return

    """records: type list-> [(3102, 1, '2009/9/9 8:45:04', '2009/9/9 8:49:52',
     0, 'walk'),(3103, 1, '2009/9/9 8:49:52', '2009/9/9 8:59:46', 0,
     'bus')......]"""

    # labelLine type: tuple
    line = 1
    for labelLine in allLabelRecords:
        mode = labelLine[5]  # get mode in table GPS_label_i
        startStr = labelLine[2]  # get startTime in table GPS_label_i
        endStr = labelLine[3]  # get endTime in table GPS_label_i
        parameters = []
        pointl = 1
        for pointLine in allPointsRecords:
            # get timeStamp in table GPS_points_i
            pointTimeStamp = pointLine[4]
            f = func.compareTime2(startStr, endStr, pointTimeStamp)
            if f == 1:
                lineTuple = (mode, pointLine[0])
                parameters.append(lineTuple)
            print(pointl)
            pointl += 1
        updateSql = 'update GPS_points_' + \
            str(i) + ' set mode = ? where id = ?'
        if len(parameters) == 0:
            continue
        DBUtil.update(conn, updateSql, parameters)
        if line == 3:
            break
        line += 1
    DBUtil.closeDB(conn)  # close the database


def addAccLabel(DBPath, i):
    """
    add accelemeter and point_label (such as walk-point or non-walk-point)
    for every GPS point.
    -1 default there is no value (begin of the trajectory)
    "none" default there is no value (begin of the tajectory)
    """
    conn = DBUtil.get_conn(DBPath)
    # find all points
    fetchAllPointSql = 'select id, time_stamp, velocity from GPS_points_' + \
        str(i)
    allPointRecords = DBUtil.fetchAll(conn, fetchAllPointSql)
    if allPointRecords is None:
        print('fetch point set Fail!')
        return
    """
         allPointRecords contents:
               [(id, time_stamp, velocity)]
               [(1, '2008/04/30 21:48:31', 4.285027485451),...]
         parameters contents:
               [(accelermeter, point_label, id)]
    """
    parameters = []
    #  default pre[2] = -1, means the first GPS point's valocity is -1
    pre = allPointRecords[0]
    for index in range(len(allPointRecords)):
        cur = allPointRecords[index]
        print('point id: ' + str(cur[0]))
        if cur[2] == -1:
            parameters.append((-1, 'none', cur[0]))
            pre = cur
            continue
        #  pre = -1 and cur != -1
        if pre[2] == -1:
            parameters.append((-1, 'none', cur[0]))
            pre = cur
            continue
        timeInterval = func.getTimeInterval(pre[1], cur[1])
        #  if pre time equals cur time, we set timeInterval 1 second
        if timeInterval == 0:
            timeInterval = 1
        acc = abs(cur[2] - pre[2]) / timeInterval
        pointLabel = 'non-walk-point'
        if cur[2] < vThreshold and acc < aThreshold:
            pointLabel = 'walk-point'
        parameters.append((acc, pointLabel, cur[0]))
        pre = cur
    # print(parameters)
    #  update in the database
    updateSql = 'update GPS_points_' + \
        str(i) + ' set accelerometer = ?, point_label = ? where id = ?'
    DBUtil.update(conn, updateSql, parameters)
    DBUtil.closeDB(conn)


def addDistVelocity(DBPath, i):
    """
    if time interval between cur and pre record is greater than 20min,
    then we consider the begin of another trajectory, the first record's
    distance and velocity of trajectory is -1 default.
    we can say value "-1" can understand as the begin of single trajectory
    """
    conn = DBUtil.get_conn(DBPath)
    # find all points
    fetchAllPointSql = 'select * from GPS_points_' + str(i)
    allPointRecords = DBUtil.fetchAll(conn, fetchAllPointSql)
    if allPointRecords is None:
        print('fetch point set Fail!')
        return
    """
    records: type list-> [(1, 3, 39.9752333333333, 116.330066666667,
    '2008/04/29 17:15:24', -1, -1, -1, 'non', 0, 0, 0, 0, 'none')......]
    the index of time is 4
    lat: 2 lon: 3
    distance: 7
    velocity: 5
    """
    pre = allPointRecords[0]
    # print(preRecord)
    parameters = []
    for index in range(len(allPointRecords)):
        cur = allPointRecords[index]
        if index == 0:
            parameters.append((-1, -1, cur[0]))
            continue
        timeInterval = func.getTimeInterval(pre[4], cur[4])
        # if pre time equals cur time, we set timeInterval 1 second
        if timeInterval == 0:
            timeInterval = 1
        if timeInterval >= TimeThreshold:
            parameters.append((-1, -1, cur[0]))
            pre = cur
            continue
        print("points id: " + str(cur[0]))
        dist = func.getDistance(pre[2], pre[3], cur[2], cur[3])
        lineTuple = (dist, dist / timeInterval, cur[0])
        parameters.append(lineTuple)
        pre = cur
    updateSql = 'update GPS_points_' + \
        str(i) + ' set distance = ?, velocity = ? where id = ?'
    DBUtil.update(conn, updateSql, parameters)
    DBUtil.closeDB(conn)
    print("update distance and velocity successfully!")


def addStayPoint(DBPath, i):
    """
    caculate stay point value in table GPS_points_i,
    value: 1 denotes the point is stay point
    value: 0 denotes the normal stap point
     step 1: find stay point according to rule:
                Distance(p1, p2)<D and TimeDiff(p1, p2)>T
     step 2: use direction change to drop extra stay points
     step 3: noise filtering
    """
    conn = DBUtil.get_conn(DBPath)
    # find all points
    fetchAllPointSql = 'select * from GPS_points_' + str(i)
    allPointRecords = DBUtil.fetchAll(conn, fetchAllPointSql)
    if allPointRecords is None:
        print('fetch point set Fail!')
        return
    """
    records: type list-> [(1, 3, 39.9752333333333, 116.330066666667,
    '2008/04/29 17:15:24', -1, -1, -1, 'non', 0, 0, 0, 0, 'none')......]
    id: 0
    time: 4
    lat: 2
    lon: 3
    distance: 7
    velocity: 5
    """
    parameters = []
    stayPointSet = []
    recordLen = len(allPointRecords)
    index = 0
    while index < recordLen:
        cur = allPointRecords[index]
        j = index + 1
        token = 0
        while j < recordLen:
            aft = allPointRecords[j]
            # if another trajectory bagins
            if aft[7] == -1:
                index = j
                token = 1
                break
            dist = func.getDistance(cur[2], cur[3], aft[2], aft[3])
            if dist > StayPoinDistThd:
                curTimeDiff = func.getTimeInterval(cur[4], aft[4])
                if curTimeDiff > StayPoinTiThd:
                    #  index ~ j points are added to stayPointSet
                    sIndex = index
                    while sIndex < j:
                        temp = allPointRecords[sIndex]
                        stayPointSet.append((temp[0], temp[2], temp[3]))
                        sIndex += 1
                    #  output the stay points set
                    # print(stayPointSet)
                    """
                        check stay points set 1,
                        abandon the case of traffic congestion
                    """
                    # isTraCong = func.isTrafficCongestion(stayPointSet,
                    #                                      changeAngle,
                    #                                      changeRate)
                    # if isTraCong == 1:
                    #     stayPointSet.clear()
                    #     break
                    """
                        check stay points set 2 (noise filtering),
                        get content:
                        [(39, 39.8146666666667, 119.476816666667, 0),......],
                    """
                    resPointList = func.noiseFilter(stayPointSet, 3)
                    """
                        insert stay points into table GPS_points_i
                        field: is_stay_point
                    """
                    for item in resPointList:
                        parameters.append((item[3], item[0]))
                    # print("resPointList's size:" + str(len(resPointList)))
                    # print(resPointList)
                    func.writeFile('stay_point_set_result.txt',
                                   "resPointList's size: " + str(len(resPointList)))
                    func.writeFile('stay_point_set_result.txt',
                                   str(resPointList))
                    func.writeFile('stay_point_set_result.txt',
                                   "\n\n")
                    updateSql = "update GPS_points_" + str(i) + \
                        " set is_stay_point = 1, is_deleted = ? where id = ?"
                    # DBUtil.update(conn, updateSql, parameters)
                    #  clear the stay points set
                    resPointList.clear()
                    stayPointSet.clear()
                    parameters.clear()
                    index = j
                    token = 1
                    break
                else:
                    break
            j += 1  # end while
        if token != 1:
            index += 1
    DBUtil.closeDB(conn)


def addTrueCP(DBPath, i):
    """
       if the distance between an normal GPS points and actual
       transition points is within 150 m, we regard the GPS point
       is transition point.
    """
    conn = DBUtil.get_conn(DBPath)
    # find all points
    fetchAllPointSql = 'select id,lat,lon,accelerometer,mode,time_stamp ' + \
                       'from GPS_points_' + str(i)
    allPointRecords = DBUtil.fetchAll(conn, fetchAllPointSql)
    if allPointRecords is None:
        print('fetch point set Fail!')
        return
    """
    records: type list-> [(1, 39.9752333333333, 116.330066666667, 'none').....]
    id: 0
    lat: 1
    lon: 2
    accelerometer: 3
    mode: 4
    time_stamp: 5
    """
    parameters = []
    recordLen = len(allPointRecords)
    pre = allPointRecords[0]
    index = 1
    while index < recordLen:
        cur = allPointRecords[index]
        if cur[3] == -1:
            pre = cur
            index += 1
            continue
        tempTime = func.getTimeInterval(pre[5], cur[5])
        if cur[4] != pre[4] and tempTime < TimeThreshold:
            parameters.append((cur[0],))
            #  forward
            forStart = index - 1
            while forStart >= 0:
                forward = allPointRecords[forStart]
                tempDist = func.getDistance(cur[1], cur[2],
                                            forward[1], forward[2])
                if tempDist > transiPointDist:
                    break
                parameters.append((forward[0],))
                forStart -= 1
            #  afterward
            aftStart = index + 1
            while aftStart < recordLen:
                aftward = allPointRecords[aftStart]
                tempDist = func.getDistance(cur[1], cur[2],
                                            aftward[1], aftward[2])
                if tempDist > transiPointDist:
                    break
                parameters.append((aftward[0],))
                aftStart += 1
        # update into database
        if len(parameters) != 0:
            print(parameters)
            updateSql = "update GPS_points_" + str(i) + \
                " set is_true_tp = 1 where id = ?"
            DBUtil.update(conn, updateSql, parameters)
            parameters.clear()
        pre = cur
        index += 1
    DBUtil.closeDB(conn)


def addIsDeleted(DBPath, i):
    pass


def getStayPointPrecison(DBPath, i):
    """
       get stay point, calculate if the stay point is actual
       transition point.

       Returns:
            recall and percision of stay point as transition point
    """
    conn = DBUtil.get_conn(DBPath)
    # find all points
    fetchAllPointSql = 'select id,is_stay_point,is_true_tp ' + \
                       'from GPS_points_' + str(i)
    allPointRecords = DBUtil.fetchAll(conn, fetchAllPointSql)
    if allPointRecords is None:
        print('fetch point set Fail!')
        return
    """
    records: type list-> [(1, 0, 1).....]
    (id, is_stay_point, is_true_cp)
    id: 0
    is_stay_point: 1
    is_true_tp: 2
    """
    # print(allPointRecords)
    # correct stay point number
    spCorNum = 0
    # total stay point number
    sptotNum = 0
    # total actual transition point
    totalTP = 0
    sptotNum, totalTP = func.getClusNum(allPointRecords)
    f = 0
    for item in allPointRecords:
        if item[2] == 1:
            if item[1] == 1 and f == 0:
                # find
                spCorNum += 1
                f = 1
        else:
            f = 0
    print('total stay point: ' + str(sptotNum))
    print('total actual transition point: ' + str(totalTP))
    print('total find transition point: ' + str(spCorNum))
    DBUtil.closeDB(conn)


def main():
    DBPath = '../DB/GPS.db'
    i = 1
    """
        step 1
        add column value of Distance and velocity to the table GPS_points_i
    """
    # addDistVelocity(DBPath, i)
    """
        step 2
        add column value of Accelermeter and point_label to the
        table GPS_points_i
    """
    # addAccLabel(DBPath, i)
    """
        step 3
        add column value of is_stay_point to the table GPS_points_i
    """
    # addStayPoint(DBPath, i)
    """
        step 4
        add true transition point in the range of transiPointDist
    """
    addTrueCP(DBPath, i)
    """
        step 5
        check how many stay points are found, and how many stay points
        are actual transition points
    """
    # getStayPointPrecison(DBPath, i)


if __name__ == '__main__':
    main()
