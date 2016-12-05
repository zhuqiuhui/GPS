from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import train_test_split
import pandas as pd
import numpy as np
import sys
sys.path.append("..")
import preprocess.DBUtil as DB


features = ['distance', '_85thV', 'MaxV1', 'MaxV2',
            'MedianV', 'MinV', 'MeanV', 'Ev',
            'Dv', 'HVR', 'MVR', 'LVR',
            '_85thA', 'MaxA1', 'MaxA2', 'MedianA',
            'MinA', 'MeanA', 'Ea', 'Da',
            'HAR', 'MAR', 'LAR', 'TS',
            'ACR', 'BSR', 'ACP', 'HCR',
            'SR', 'VCR']


def getSegFea(DBPath):
    """
        get all segment with features, for example:

        [(id, user_id, trip_id, segment_id, start_point_id, end_point_id,
          point_num, distance, _85thV, MaxV1, MaxV2, MedianV, MinV, MeanV,
          Ev, Dv, HVR, MVR, LVR, _85thA, MaxA1, MaxA2, MedianA, MinA, MeanA,
          Ea, Da, HAR, MAR, LAR, TS, ACR, BSR, ACP, HCR, SR, VCR, is_deleted,
          predicted_class, true_class), (....]
    """
    conn = DB.get_conn(DBPath)
    # find all points
    fetAllSegFea = 'select * from GPS_segments'
    data = pd.read_sql(fetAllSegFea, conn)
    # allRecords = DB.fetchAll(conn, fetAllSegFea)
    DB.closeDB(conn)
    # print(data["TS"])
    # data = pd.DataFrame(columns=["id", "user_id", "trip_id", "segment_id",
    #                              "start_point_id","end_point_id","point_num",
    #                              "distance", "_85thV", "MaxV1", "MaxV2",
    #                              "MedianV", "MinV", "MeanV", "Ev","Dv","HVR",
    #                              "MVR", "LVR", "_85thA", "MaxA1","MaxA2",
    #                              "MedianA", "MinA", "MeanA", "Ea","Da","HAR",
    #                              "MAR", "LAR", "TS", "ACR", "BSR","ACP",
    #                              "HCR", "SR", "VCR", "is_deleted",
    #                              "predicted_class", "true_class"])
    return data


def getSegFea1(DBPath):
    """
        get all segment with features, for example:

        [(id, user_id, trip_id, segment_id, start_point_id, end_point_id,
          point_num, distance, _85thV, MaxV1, MaxV2, MedianV, MinV, MeanV,
          Ev, Dv, HVR, MVR, LVR, _85thA, MaxA1, MaxA2, MedianA, MinA, MeanA,
          Ea, Da, HAR, MAR, LAR, TS, ACR, BSR, ACP, HCR, SR, VCR, is_deleted,
          predicted_class, true_class), (....]
    """
    conn = DB.get_conn(DBPath)
    # find all points
    fetAllSegFea = 'select * from GPS_segments'
    data = pd.read_sql(fetAllSegFea, conn)
    # allRecords = DB.fetchAll(conn, fetAllSegFea)
    DB.closeDB(conn)
    train = data[:-2315]
    test = data[-2315:]
    return train, test


def randomForest(data):
    randomSeed = 2
    trainXY = data.drop(['id', 'user_id', 'trip_id',
                         'segment_id', 'start_point_id',
                         'end_point_id', 'point_num',
                         'is_deleted', 'predicted_class'],
                        axis=1)
    train, val = train_test_split(trainXY, test_size=0.3,
                                  random_state=randomSeed)
    # train y
    y = train.true_class
    # train x
    x = train.drop(['true_class'], axis=1)
    # test y
    valY = val.true_class
    # test x
    valX = val.drop(['true_class'], axis=1)
    rf = RandomForestClassifier(n_estimators=100,
                                # max_depth=13,
                                n_jobs=2)
    rf.fit(x, y)
    predictY = rf.predict(valX)
    # [bike, bus, car, plane, train, walk]
    predictYProba = rf.predict_proba(valX)
    totalInstance = len(valY)
    correct = 0
    for y, preY, preYPro in zip(valY, predictY, predictYProba):
        print('class: ' + str(y) + ' preClass: ' +
              str(preY) + ' pro: ' + str(preYPro))
        if y == preY:
            correct += 1
    print('----------------------Accuracy:-------------------------')
    print(correct / totalInstance)
    print('----------------------Feature Importance:-------------------------')
    feaImportance = rf.feature_importances_
    feaLen = len(features)
    feaIndex = 0
    while feaIndex < feaLen:
        print(features[feaIndex] + ' : ' + str(feaImportance[feaIndex]))
        feaIndex += 1


def randomForest1(train, test):
    trainXY = train.drop(['id', 'user_id', 'trip_id',
                          'segment_id', 'start_point_id',
                          'end_point_id', 'point_num',
                          'is_deleted', 'predicted_class'],
                         axis=1)
    testInf = pd.DataFrame({'id': test.id,
                            'user_id': test.user_id,
                            'trip_id': test.trip_id,
                            'segment_id': test.segment_id,
                            'start_point_id': test.start_point_id,
                            'end_point_id': test.end_point_id,
                            'point_num': test.point_num,
                            'distance': test.distance})
    testXY = test.drop(['id', 'user_id', 'trip_id',
                        'segment_id', 'start_point_id',
                        'end_point_id', 'point_num',
                        'is_deleted', 'predicted_class'],
                       axis=1)
    # train y
    y = trainXY.true_class
    # train x
    x = trainXY.drop(['true_class'], axis=1)
    # test y
    valY = testXY.true_class
    # test x
    valX = testXY.drop(['true_class'], axis=1)
    rf = RandomForestClassifier(n_estimators=100,
                                n_jobs=2)
    rf.fit(x, y)
    predictY = rf.predict(valX)
    # [bike, bus, car, plane, train, walk]
    predictYProba = rf.predict_proba(valX)
    totalInstance = len(valY)
    correct = 0
    for id, userId, tripId, segmentId, dist, y, preY, preYPro in zip(testInf.id,
                                                                     testInf.user_id,
                                                                     testInf.trip_id,
                                                                     testInf.segment_id,
                                                                     testInf.distance,
                                                                     valY,
                                                                     predictY,
                                                                     predictYProba):
        print('id: ' + str(id) + ' user_id: ' + str(userId) + ' trip_id: ' +
              str(tripId) + ' segment_id: ' + str(segmentId) +
              ' distance: ' + str(dist) +
              ' ' + str(preY) + ' ' + str(y) +
              ' pro: ' + str(preYPro))
        if y == preY:
            correct += 1
    print('----------------------Accuracy:-------------------------')
    print(correct / totalInstance)
    print('----------------------Feature Importance:-------------------------')
    feaImportance = rf.feature_importances_
    feaLen = len(features)
    feaIndex = 0
    while feaIndex < feaLen:
        print(features[feaIndex] + ' : ' + str(feaImportance[feaIndex]))
        feaIndex += 1
    print('----------------------Confusion Matrix:-------------------------')
    print('predictY: ' + str(len(predictY)) + ' Y: ' + str(len(valY)))
    getConfuseMatrix(predictY, valY)


def getConfuseMatrix(preY, Y):
    """
       car  bus  bike  walk  train  plane
        0    1    2     3     4      5
    """
    modePd = pd.DataFrame({'car': [0],
                           'bus': [1],
                           'bike': [2],
                           'walk': [3],
                           'train': [4],
                           'plane': [5]})
    # carList = [0, 0, 0, 0, 0, 0]
    # busList = [0, 0, 0, 0, 0, 0]
    # bikeList = [0, 0, 0, 0, 0, 0]
    # walkList = [0, 0, 0, 0, 0, 0]
    # trainList = [0, 0, 0, 0, 0, 0]
    # planeList = [0, 0, 0, 0, 0, 0]
    modeMatrix = np.zeros((6, 6), dtype=np.int64)
    for c1, c2 in zip(preY, Y):
        addNum(c1, c2, modePd, modeMatrix)
    mode = ['car', 'bus', 'bike', 'walk', 'train', 'plane']
    print('       car bus bike walk train plane')
    i = 0
    while i < 6:
        print(mode[i] + ': ' + str(modeMatrix[i]))
        i += 1
    print('sum:' + str(np.sum(modeMatrix)))


def addNum(c1, c2, modePd, modeMatrix):
    index1 = modePd[c1][0]
    index2 = modePd[c2][0]
    modeMatrix[index2][index1] = modeMatrix[index2][index1] + 1


def getTransitionMatrix(DBPath):
    """
       get transition matrix of transportation mode
    """
    conn = DB.get_conn(DBPath)
    fetchSql = 'select id,trip_id,segment_id,true_class from GPS_segments'
    # data = pd.read_sql(fetchSql, conn)
    data = DB.fetchAll(conn, fetchSql)
    print(data)
    DB.closeDB(conn)
    modePd = pd.DataFrame({'car': [0],
                           'bus': [1],
                           'bike': [2],
                           'walk': [3],
                           'train': [4],
                           'plane': [5]})
    modeMatrix = np.zeros((6, 6), dtype=np.int64)
    pre = data[0]
    index = 1
    while index < len(data):
        cur = data[index]
        if cur[2] == 1:
            pre = cur
            index += 1
            continue
        else:
            index1 = modePd[pre[3]][0]
            index2 = modePd[cur[3]][0]
            modeMatrix[index1][index2] = modeMatrix[index1][index2] + 1
            pre = cur
            index += 1
    print(modeMatrix)


def main():
    DBPath = '../DB/GPS.db'
    # segFea = getSegFea(DBPath)
    # data = getSegFea(DBPath)
    # randomForest(data)
    train, test = getSegFea1(DBPath)
    randomForest1(train, test)

    # test
    # preY = ['car', 'bus', 'car', 'walk']
    # Y = ['car', 'car', 'car', 'bus']
    # getConfuseMatrix(preY, Y)

    # getTransitionMatrix(DBPath)


if __name__ == '__main__':
    main()
