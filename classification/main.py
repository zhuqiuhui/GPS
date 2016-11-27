import sys
sys.path.append("..")
import preprocess.DBUtil as DB
import featureFunc


def getSegment(DBPath, i):
    """
        get single segment, and calculate every feature of this segment
    """
    conn = DB.get_conn(DBPath)
    # find all points
    fetchAllSql = 'select id,user_id,velocity,accelerometer,distance,mode ' + \
        'from GPS_points_' + str(i)
    allRecords = DB.fetchAll(conn, fetchAllSql)
    if allRecords is None:
        print('fetch point set Fail!')
        return
    """
    records: type list-> [(1, 2, 0.602996094223764, 0.00162000482825461,
                           53.666652385915, 'walk').....]
    (id,user_id,velocity,accelerometer,distance,mode)
    id: 0
    user_id: 1
    velocity: 2
    accelerometer: 3
    distance: 4
    mode: 5
    """
    # print(len(allRecords))
    displayPoint = []
    index = 1
    pre = allRecords[0]
    temp = []
    while index < len(allRecords):
        if index == len(allRecords) - 1:
            temp.append(allRecords[index][0])
        cur = allRecords[index]
        if pre[3] == -1 and cur[3] != -1:
            temp.append(cur)
        if pre[3] != -1 and cur[3] == -1:
            temp.append(pre[0])
            displayPoint.append(temp)
            temp.clear()
        pre = cur
        index += 1
    #  output the last segment
    DB.closeDB(conn)


def main():
    DBPath = '../DB/GPS.db'
    i = 1
    segment = getSegment(DBPath, i)


if __name__ == '__main__':
    main()
