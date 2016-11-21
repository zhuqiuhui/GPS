import DBUtil


def import_GPS_points(dbPath, path, i):
    """向数据库GPS表GPS_points_i导入数据, i为插入第i个表"""
    conn = DBUtil.get_conn(dbPath)
    # 一次性读入整个文件
    pointsFile = open(path)
    try:
        allLines = pointsFile.readlines()
    finally:
        pointsFile.close()
    # 处理每一行
    parameters = []
    lineNum = 1
    for line in allLines:
        line = line.strip('\n')
        lineList = line.split(',')
        lineTuple = (lineList[0], lineList[1],
                     lineList[2], lineList[3],
                     lineList[4])
        parameters.append(lineTuple)
        lineNum += 1
    print(len(parameters))
    insertSql = 'insert into GPS_points_' + \
        str(i) + '("id", "lat", "lon", "time_stamp", "mode")' + \
        'values (?,?,?,?,?)'
    DBUtil.insert(conn, insertSql, parameters)
    DBUtil.closeDB(conn)


def import_GPS_label(dbPath, path, i):
    """向数据库GPS表GPS_label_i导入数据, i为插入第i个表"""
    conn = DBUtil.get_conn(dbPath)
    # 一次性读入整个文件
    labelFile = open(path)
    try:
        allLines = labelFile.readlines()
    finally:
        labelFile.close()
    # 处理每一行
    parameters = []
    lineNum = 1
    for line in allLines:
        line = line.strip('\n')
        lineList = line.split('	')
        lineTuple = (lineList[0] + ' ' + lineList[1],
                     lineList[0] + ' ' + lineList[2], lineList[3])
        if lineNum != 1:
            parameters.append(lineTuple)
        lineNum += 1
    insertSql = 'insert into GPS_label_' + \
        str(i) + '("start_time", "end_time", "mode") values (?,?,?)'
    DBUtil.insert(conn, insertSql, parameters)
    DBUtil.closeDB(conn)
    # print(parameters)
    # print(lineNum)


def main():
    dbPath = '../DB/GPS.db'
    commonPrefix = '../../data/integration_process'
    # for i in range(1):
    # labelFile = commonPrefix + '/labels_' + str(3) + '.txt'
    # import_GPS_label(dbPath, labelFile, 3)
    i = 12
    pointFile = commonPrefix + '/integration_' + str(i) + '.txt'
    import_GPS_points(dbPath, pointFile, i)


if __name__ == '__main__':
    main()
