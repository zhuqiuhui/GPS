from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import train_test_split
import pandas as pd
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


def main():
    DBPath = '../DB/GPS.db'
    # segFea = getSegFea(DBPath)
    data = getSegFea(DBPath)
    randomForest(data)


if __name__ == '__main__':
    main()
