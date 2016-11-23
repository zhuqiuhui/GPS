import func
import DBUtil

N = 10  # contant value
M = 8  # contant value
pointNum = 21  # the least the point number of segment
distInterval = 50  # combining short segment


def labelSpec(DBPath, i):
    """
    modify the GPS point label using greedy thought
    """
    conn = DBUtil.get_conn(DBPath)
    # find all points
    fetchAllSql = 'select id,point_label ' + \
        'from GPS_points_' + str(i)
    allRecords = DBUtil.fetchAll(conn, fetchAllSql)
    if allRecords is None:
        print('fetch point set Fail!')
        return
    """
    records: type list-> [(1, 'non-walk-point').....]
    (id, point_label)
    id: 0
    point_label: 1
    """
    index = 0
    segment = []
    while index < len(allRecords):
        cur = allRecords[index]
        if cur[1] == 'none' or index == len(allRecords) - 1:
            if index == len(allRecords) - 1:
                segment.append(cur)
            if len(segment) != 0:
                print(segment)
                # process the segment
                parameters = modifyPlointLab(segment)
                # update the point_label into database
                updateSql = 'update GPS_points_' + str(i) + \
                    ' set point_label=? where id=?'
                DBUtil.update(conn, updateSql, parameters)
                parameters.clear()
                segment.clear()
        segment.append(cur)
        index += 1
    DBUtil.closeDB(conn)


def getTranPoint(DBPath, i):
    """
    get the transition points based on sudden change point
    """
    conn = DBUtil.get_conn(DBPath)
    # find all points
    fetchAllSql = 'select id,point_label ' + \
        'from GPS_points_' + str(i)
    allRecords = DBUtil.fetchAll(conn, fetchAllSql)
    if allRecords is None:
        print('fetch point set Fail!')
        return
    """
    records: type list-> [(1, 'non-walk-point').....]
    (id, point_label)
    id: 0
    point_label: 1
    """
    index = 0
    segment = []
    while index < len(allRecords):
        cur = allRecords[index]
        if cur[1] == 'none' or index == len(allRecords) - 1:
            if index == len(allRecords) - 1:
                segment.append(cur)
            if len(segment) != 0:
                print(segment)
                # process the segment
                parameters = getSuddenChangePointId(segment)
                # update the point_label into database
                updateSql = 'update GPS_points_' + str(i) + \
                    ' set is_predict_tp=1 where id=?'
                if len(parameters) != 0:
                    DBUtil.update(conn, updateSql, parameters)
                parameters.clear()
                segment.clear()
        segment.append(cur)
        index += 1
    DBUtil.closeDB(conn)


def combineSeg(DBPath, i):
    """
       Combining short segment divide by candidate GPS point, first we
       should find every segment, then combining the short distance within
       the segment.
       Now we first don consider the stay point, after combining segment,
       we use final tranisition point and stay point to divide the trajectory.
    """
    conn = DBUtil.get_conn(DBPath)
    # find all points
    fetchAllSql = 'select id,distance,is_predict_tp,is_true_tp ' + \
        'from GPS_points_' + str(i)
    allRecords = DBUtil.fetchAll(conn, fetchAllSql)
    if allRecords is None:
        print('fetch point set Fail!')
        return
    """
    records: type list-> [(1, 7.9227361133195, 1, 0).....]
    (id, distance, is_predict_tp, is_true_tp)
    id: 0
    distance: 1
    is_predict_tp: 2
    is_true_tp: 3
    """
    index = 0
    segment = []
    totalTP = 0
    totalFindTP = 0
    correctTP = 0
    while index < len(allRecords):
        cur = allRecords[index]
        if cur[1] == 'none' or index == len(allRecords) - 1:
            if index == len(allRecords) - 1:
                segment.append(cur)
            if len(segment) != 0:
                print(segment)
                # combining the short distance
                parameters = getSuddenChangePointId(segment)
                # update the point_label into database
                updateSql = 'update GPS_points_' + str(i) + \
                    ' set is_predict_tp=1 where id=?'
                if len(parameters) != 0:
                    DBUtil.update(conn, updateSql, parameters)
                parameters.clear()
                segment.clear()
        segment.append(cur)
        index += 1
    DBUtil.closeDB(conn)


def mergeSeg(segment):
    """
        first, merge the candidate point according to the limitation of
        short distance.
        second, return the number of found point

        Args: segment, such as:
            [(1, 7.9227361133195, 1, 0).....]
                    (id, distance, is_predict_tp, is_true_tp)
                    id: 0
                    distance: 1
                    is_predict_tp: 2
                    is_true_tp: 3
            Returns:
                segment:
                       [(1, 7.9227361133195, 1, 0).....]
                    (id, distance, is_predict_tp, is_true_tp)
                totalTP: total actual transition points
                totalFindTP: total found transition points
                correctTP: found transition points which are correct
    """


def getSuddenChangePointId(segment):
    """
        get GPS point id who is in the condition that sudden change.
        Args:
             segment: GPS points set, such as
                     [(732708, 'none'), (732709, 'non-walk-point')...]
        Returns:
             parameters: GPS point id which is in sudden change
                         such as:
                             [(732708)...]
                         if parameters is null, then len(parameters)=0
    """
    parameters = []
    if len(segment) < pointNum:
        return parameters
    index = 0
    segLen = len(segment)
    while index < segLen:
        if index >= N and index <= segLen - N - 1:
            lcountNonWalk = 0
            lcountWalk = 0
            rcountNonWalk = 0
            rcountWalk = 0
            for item2 in segment[index - N:index]:
                if item2[1] == 'walk-point':
                    lcountWalk += 1
                if item2[1] == 'non-walk-point':
                    lcountNonWalk += 1
            for item3 in segment[index + 1:index + N + 1]:
                if item3[1] == 'walk-point':
                    rcountWalk += 1
                if item3[1] == 'non-walk-point':
                    rcountNonWalk += 1
            if lcountWalk >= M and rcountNonWalk >= M:
                parameters.append((segment[index][0],))
            if lcountNonWalk >= M and rcountWalk >= M:
                parameters.append((segment[index][0],))
        index += 1
    return parameters


def modifyPlointLab(segment):
    """
    process every segment using greedy method.
    Args:
         segment: GPS points set, such as
                 [(732708, 'none'), (732709, 'non-walk-point')...]
    Returns:
         parameters: the result after modification
                     such as:
                         [('walk-point', 732708)...]
    """
    # process segment whose GPS point number is lower than pointNum
    parameters = []
    if len(segment) < pointNum:
        for item1 in segment:
            parameters.append((item1[1], item1[0]))
        return parameters

    # processing
    index = 0
    segLen = len(segment)
    preSeg = []
    while func.isNotSame(preSeg, segment):
        preSeg = segment
        while index < segLen:
            if index < N:
                # processing left
                countNonWalk = 0
                countWalk = 0
                for item2 in segment[index + 1:index + N + 1]:
                    if item2[1] == 'walk-point':
                        countWalk += 1
                    if item2[1] == 'non-walk-point':
                        countNonWalk += 1
                if countWalk >= M:
                    te = (segment[index][0], 'walk-point')
                    segment[index] = te
                if countNonWalk >= M:
                    te = (segment[index][0], 'non-walk-point')
                    segment[index] = te
            elif index > segLen - N - 1:
                # processing right
                countNonWalk = 0
                countWalk = 0
                for item3 in segment[index - N:index]:
                    if item3[1] == 'walk-point':
                        countWalk += 1
                    if item3[1] == 'non-walk-point':
                        countNonWalk += 1
                if countWalk >= M:
                    te = (segment[index][0], 'walk-point')
                    segment[index] = te
                if countNonWalk >= M:
                    te = (segment[index][0], 'non-walk-point')
                    segment[index] = te
            else:
                # processing middle
                lcountNonWalk = 0
                lcountWalk = 0
                rcountNonWalk = 0
                rcountWalk = 0
                for item4 in segment[index - N:index]:
                    if item4[1] == 'walk-point':
                        lcountWalk += 1
                    if item4[1] == 'non-walk-point':
                        lcountNonWalk += 1
                for item5 in segment[index + 1:index + N + 1]:
                    if item5[1] == 'walk-point':
                        rcountWalk += 1
                    if item5[1] == 'non-walk-point':
                        rcountNonWalk += 1
                if lcountWalk >= M and rcountWalk >= M:
                    te = (segment[index][0], 'walk-point')
                    segment[index] = te
                if rcountNonWalk >= M and rcountNonWalk >= M:
                    te = (segment[index][0], 'non-walk-point')
                    segment[index] = te
            index += 1  # end while
    parameters.clear()
    for item6 in segment:
        parameters.append((item6[1], item6[0]))
    return parameters


def getStartEndPoint(DBPath, i):
    """
    get the segment start GPS point id, end GPS point id,
    the number of segment GPS points, such as:
    [[1,67,56],...] means point 1~point 67 have 56 GPS points.

        start id: 1742 end id: 2250 num: 509
        start id: 4009 end id: 4728 num: 720
    """
    conn = DBUtil.get_conn(DBPath)
    # find all points
    fetchAllSql = 'select id,point_label ' + \
        'from GPS_points_' + str(i)
    allRecords = DBUtil.fetchAll(conn, fetchAllSql)
    if allRecords is None:
        print('fetch point set Fail!')
        return
    """
    records: type list-> [(1, 'non-walk-point').....]
    (id, point_label)
    id: 0
    point_label: 1
    """
    # print(allRecords)
    displayPoint = []
    count = 1
    index = 1
    pre = allRecords[0]
    temp = []
    totalTraNum = 0
    while index < len(allRecords):
        if index == len(allRecords) - 1:
            temp.append(allRecords[index][0])
            temp.append(count - 1)
        cur = allRecords[index]
        if pre[1] == 'none' and cur[1] != 'none':
            temp.append(pre[0])
        if pre[1] != 'none' and cur[1] == 'none':
            temp.append(pre[0])
            temp.append(count - 1)
            print('start id: ' + str(temp[0]) + ' end id: ' +
                  str(temp[1]) + ' num: ' + str(count - 1))
            displayPoint.append(temp)
            temp.clear()
            count = 0
            totalTraNum += 1
        pre = cur
        count += 1
        index += 1
    #  output the last segment
    print('start id: ' + str(temp[0]) + ' end id: ' +
          str(temp[1]) + ' num: ' + str(count - 1))
    print('total segment number: ' + str(totalTraNum))
    DBUtil.closeDB(conn)


def testModifyPlointLab():
    """
    teset the function of modifyPlointLab
    """
    segment = [(12940, 'none'), (12941, 'walk-point'),
               (12942, 'non-walk-point'), (12943, 'non-walk-point'),
               (12944, 'non-walk-point'), (12945, 'non-walk-point'),
               (12946, 'walk-point'), (12947, 'walk-point'),
               (12948, 'walk-point'), (12949, 'walk-point'),
               (12950, 'walk-point'), (12951, 'walk-point'),
               (12952, 'walk-point'), (12953, 'walk-point'),
               (12954, 'walk-point'), (12955, 'walk-point'),
               (12956, 'walk-point'), (12957, 'walk-point'),
               (12958, 'non-walk-point'), (12959, 'non-walk-point'),
               (12960, 'walk-point'), (12961, 'walk-point'),
               (12962, 'walk-point'), (12963, 'walk-point'),
               (12964, 'walk-point'), (12965, 'walk-point'),
               (12966, 'walk-point'), (12967, 'walk-point'),
               (12968, 'walk-point'), (12969, 'walk-point'),
               (12970, 'walk-point'), (12979, 'walk-point'),
               (12980, 'walk-point'), (12981, 'walk-point'),
               (12982, 'walk-point'), (12983, 'non-walk-point'),
               (12984, 'walk-point'), (12985, 'walk-point'),
               (12986, 'walk-point'), (12987, 'walk-point'),
               (12988, 'walk-point'), (12989, 'walk-point'),
               (12990, 'walk-point'), (12991, 'walk-point'),
               (12992, 'walk-point'), (12993, 'walk-point'),
               (12994, 'walk-point'), (12995, 'walk-point'),
               (12996, 'walk-point'), (12997, 'non-walk-point'),
               (12998, 'walk-point'), (12999, 'walk-point')]
    result = modifyPlointLab(segment)
    print(result)


def main():
    DBPath = '../DB/GPS.db'
    i = 2
    """
        step 1: show the segment that from startId to toId.
                show information, such as:
                 start id: 1742 end id: 2250 num: 509
    """
    # getStartEndPoint(DBPath, i)
    """
        step 2: modification of label specification
    """
    labelSpec(DBPath, i)
    """
        step 3: get candidate transition point set
    """
    """
        step 4: get final transition point set
    """
    """
        test the function
    """
    # testModifyPlointLab()


if __name__ == '__main__':
    main()
