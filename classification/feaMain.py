import featureFunc
import sys
sys.path.append("..")
import preprocess.DBUtil as DB

numThd = 5


def getSegment(DBPath, i, busInfoPath):
    """
        get single trip, and call function insertSeg to
        calculate every feature of single segment divided
        by transition points.
    """
    conn = DB.get_conn(DBPath)
    # find all points
    fetchAllSql = 'select id,user_id,lat,lon,time_stamp,velocity,' + \
                  'accelerometer,distance,mode from GPS_points_' + str(i)
    allRecords = DB.fetchAll(conn, fetchAllSql)
    if allRecords is None:
        print('fetch point set Fail!')
        return
    """
    records: type list-> [(1, 2, 40.29, 116.150, '2009/07/29 18:12:14'
                           0.602996094223764, 0.00162000482825461,
                           53.666652385915, 'walk').....]
    (id,user_id,lat,lon,time_stamp,velocity,accelerometer,distance,mode)
    id: 0
    user_id: 1
    lat: 2
    lon: 3
    time_stamp: 4
    velocity: 5
    accelerometer: 6
    distance: 7
    mode: 8
    """
    # print(len(allRecords))
    trip = []
    tripId = 0
    allLen = len(allRecords)
    index = 1
    pre = allRecords[0]
    while index < allLen:
        cur = allRecords[index]
        if pre[6] == -1 and cur[6] != -1:
            # trip begin
            tripId += 1
            trip.append(cur)
        if pre[6] != -1 and cur[6] == -1 or index == allLen - 1:
            if index == allLen - 1:
                trip.append(cur)
            # another trip begin
            print(tripId)
            # print(trip)
            insertSeg(DBPath, i, trip, tripId, busInfoPath)
            trip.clear()
        if pre[6] != -1 and cur[6] != -1:
            # append normaly
            trip.append(cur)
        pre = cur
        index += 1
    #  output the last segment
    DB.closeDB(conn)


def insertSeg(DBPath, i, trip, tripId, busInfoPath):
    """
        Args:
            trip: such as, [(20202, 1, 1.415, 40.29, 116.150,
                              '2009/07/29 18:12:14', 0.013, 2.83, 'walk'), ...]
                  [(id,user_id,lat,lon,time_stamp,velocity,accelerometer,distance,mode)]
                                    id: 0
                                    user_id: 1
                                    lat: 2
                                    lon: 3
                                    time_stamp: 4
                                    velocity: 5
                                    accelerometer: 6
                                    distance: 7
                                    mode: 8
            tripId: the id of this trip
    """
    tripLen = len(trip)
    if tripLen < numThd:
        print('trip from ' + str(trip[0][0]) +
              ' to ' + str(trip[-1][0]) + ' is abandon!')
        return
    conn = DB.get_conn(DBPath)
    segmentId = 1
    index = 1
    pre = trip[0]
    segment = []
    #  get every segment from every trip
    while index < tripLen:
        cur = trip[index]
        if cur[-1] != pre[-1] or index == tripLen - 1:
            # another segment begin
            segment.append(pre)
            if index == tripLen - 1:
                segment.append(cur)
            print('segmentId: ' + str(segmentId) + ': from ' +
                  str(segment[0][0]) + ' to ' +
                  str(segment[-1][0]) + ' :' + str(segment[-1][-1]))
            # print(segment)
            # calculate column value from every segment
            userId = i
            startPointId = segment[0][0]
            endPointId = segment[-1][0]
            pointNum = len(segment)
            if pointNum < numThd:
                segment.clear()
                pre = cur
                index += 1
                continue
            distSum = featureFunc.getSegDist(segment)
            preFea = (userId, tripId, segmentId, startPointId,
                      endPointId, pointNum, distSum)
            fea = getFeatures(segment, busInfoPath)
            trueClass = segment[-1][-1]
            totalColumn = preFea + fea + (trueClass,)
            print(totalColumn)
            parameters = []
            parameters.append(totalColumn)

            # insert segment into datebases, 37 features, total 40 features
            # except field: id, is_deleted, predicted_class
            insertSql = 'insert into GPS_segments (user_id,trip_id,' + \
                        'segment_id,start_point_id,end_point_id,point_num,' + \
                        'distance,_85thV,MaxV1,MaxV2,MedianV,MinV,MeanV,' + \
                        'Ev,Dv,HVR,MVR,LVR,_85thA,MaxA1,MaxA2,MedianA,MinA' + \
                        ',MeanA,Ea,Da,HAR,MAR,LAR,TS,ACR,BSR,ACP,HCR,SR,' + \
                        'VCR,true_class) values (?,?,?,?,?,?,?,?,?,?,?,?,' + \
                        '?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
            DB.insert(conn, insertSql, parameters)
            segmentId += 1
            parameters.clear()
            segment.clear()
        else:
            segment.append(pre)
        pre = cur
        index += 1
    DB.closeDB(conn)


def getFeatures(segment, busInfoPath):
    """
        Args: segment: such as, [(20202, 1, 1.41, 40.29, '2009/07/29 18:12:14',
                                  116.150, 0.013, 2.83, 'walk'), ...]
                  [(id,user_id,lat,lon,time_stamp,velocity,accelerometer,distance,mode)]
                                    id: 0
                                    user_id: 1
                                    lat: 2
                                    lon: 3
                                    time_stamp: 4
                                    velocity: 5
                                    accelerometer: 6
                                    distance: 7
                                    mode: 8
               busInfoPath: bus information path file
        Returns: 29 features
               velocity features:
                      (85thV,MaxV1,MaxV2,MedianV,MinV,MeanV,Ev,Dv,HVR,MVR,LVR)
               accelerometer features:
                      (85thA,MaxA1,MaxA2,MedianA,MinA,MeanA,Ea,Da,HAR,MAR,LAR)
               behavior features:
                      (TS,ACR,BSR,ACP,HCR,SR,VCR)
    """
    vFea = featureFunc.getVFeature(segment)
    aFea = featureFunc.getAFeature(segment)
    TS = featureFunc.getTS(segment)
    ACR = featureFunc.getACR(segment)
    BSR = featureFunc.getBSR(segment, busInfoPath)
    ACP = featureFunc.getACP(segment)
    HCR = featureFunc.getHCR(segment)
    SR = featureFunc.getSR(segment)
    VCR = featureFunc.getVCR(segment)
    bFea = (TS, ACR, BSR, ACP, HCR, SR, VCR)
    fea = vFea + aFea + bFea
    return fea


def main():
    DBPath = '../DB/GPS.db'
    busInfoPath = '../data/busInfo.txt'
    i = 1
    while i <= 32:
        getSegment(DBPath, i, busInfoPath)
        print('user ' + str(i) + 'done!')
        i += 1
    print('all user done!')


if __name__ == '__main__':
    main()
