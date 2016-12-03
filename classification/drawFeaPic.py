#-*- coding: utf-8 -*-
import sys
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
sys.path.append("..")
import preprocess.DBUtil as DB
from matplotlib.font_manager import FontProperties


font = FontProperties(fname=r"c:/Windows/Fonts/simsun.ttc", size=14)


def drawVABox(DBPath):
    """
           car,bus,bike,walk,train,plane
    """
    conn = DB.get_conn(DBPath)
    # find all segments
    fetSql = 'select _85thV,MaxV1,_85thA,MaxA1,true_class from GPS_segments'
    # data = DB.fetchAll(conn, fetSql)
    data = pd.read_sql(fetSql, conn)
    DB.closeDB(conn)
    carSet = data[data['true_class'].isin(['car'])]
    busSet = data[data['true_class'].isin(['bus'])]
    bikeSet = data[data['true_class'].isin(['bike'])]
    walkSet = data[data['true_class'].isin(['walk'])]
    trainSet = data[data['true_class'].isin(['train'])]
    planeSet = data[data['true_class'].isin(['plane'])]
    # print(busSet)true_class
    _85Vpd1 = pd.DataFrame({'car': carSet[carSet._85thV < 300]._85thV,
                            'bus': busSet[busSet._85thV < 300]._85thV,
                            'bike': bikeSet[bikeSet._85thV < 300]._85thV,
                            'walk': walkSet[walkSet._85thV < 300]._85thV,
                            'train': trainSet[trainSet._85thV < 300]._85thV,
                            'plane': planeSet[planeSet._85thV < 300]._85thV})
    _85Vpd2 = pd.DataFrame({'car': carSet[carSet._85thV < 40]._85thV,
                            'bus': busSet[busSet._85thV < 40]._85thV,
                            'bike': bikeSet[bikeSet._85thV < 40]._85thV,
                            'walk': walkSet[walkSet._85thV < 40]._85thV,
                            'train': trainSet[trainSet._85thV < 40]._85thV})
    maxVpd = pd.DataFrame({'car': carSet[carSet.MaxV1 < 60].MaxV1,
                           'bus': busSet[busSet.MaxV1 < 60].MaxV1,
                           'bike': bikeSet[bikeSet.MaxV1 < 60].MaxV1,
                           'walk': walkSet[walkSet.MaxV1 < 60].MaxV1,
                           'train': trainSet[trainSet.MaxV1 < 60].MaxV1})
    _85Apd = pd.DataFrame({'car': carSet[carSet._85thA < 3]._85thA,
                           'bus': busSet[busSet._85thA < 3]._85thA,
                           'bike': bikeSet[bikeSet._85thA < 3]._85thA,
                           'walk': walkSet[walkSet._85thA < 3]._85thA,
                           'train': trainSet[trainSet._85thA < 3]._85thA,
                           'plane': planeSet[planeSet._85thA < 3]._85thA})
    maxApd = pd.DataFrame({'car': carSet[carSet.MaxA1 < 20].MaxA1,
                           'bus': busSet[busSet.MaxA1 < 20].MaxA1,
                           'bike': bikeSet[bikeSet.MaxA1 < 20].MaxA1,
                           'walk': walkSet[walkSet.MaxA1 < 20].MaxA1,
                           'train': trainSet[trainSet.MaxA1 < 20].MaxA1,
                           'plane': planeSet[planeSet.MaxA1 < 20].MaxA1})
    # print(_85Vpd)
    # ax = sns.boxplot(data=_85Vpd1,
    #                  order=['car', 'bus', 'bike', 'walk', 'train', 'plane'])
    # ax = sns.boxplot(data=_85Vpd2,
    #                  order=['car', 'bus', 'bike', 'walk', 'train'])
    # ax = sns.boxplot(data=maxVpd,
    #                  order=['car', 'bus', 'bike', 'walk', 'train'])
    # ax = sns.boxplot(data=_85Apd,
    #                  order=['car', 'bus', 'bike', 'walk', 'train', 'plane'])
    ax = sns.boxplot(data=maxApd,
                     order=['car', 'bus', 'bike', 'walk', 'train', 'plane'])
    # 85thV
    # ax.set_xlabel('Transportation Mode')
    # ax.set_ylabel('85% Percentile Velocity (m/s)')
    # ax.set_xlabel('出行方式', fontproperties=font)
    # ax.set_ylabel('85%分位速度 (m/s)', fontproperties=font)
    # maxV
    # ax.set_xlabel('Transportation Mode')
    # ax.set_ylabel('Maximum Velocity (m/s)')
    # ax.set_xlabel('出行方式', fontproperties=font)
    # ax.set_ylabel('最大速度 (m/s)', fontproperties=font)
    # 85thA
    # ax.set_xlabel('Transportation Mode')
    # ax.set_ylabel('85% Percentile Acceleration (m/s$^2$)')
    # ax.set_xlabel('出行方式', fontproperties=font)
    # ax.set_ylabel('85%分位加速度 (m/s$^2$)', fontproperties=font)
    # maxA
    # ax.set_xlabel('Transportation Mode')
    # ax.set_ylabel('Maximum Acceleration (m/s$^2$)')
    ax.set_xlabel('出行方式', fontproperties=font)
    ax.set_ylabel('最大加速度 (m/s$^2$)', fontproperties=font)
    plt.show(ax)


def drawACRBox(DBPath):
    """
           car,bus,bike,walk,train,plane
    """
    conn = DB.get_conn(DBPath)
    # find all segments
    fetSql = 'select ACR,true_class from GPS_segments'
    # data = DB.fetchAll(conn, fetSql)
    data = pd.read_sql(fetSql, conn)
    DB.closeDB(conn)
    carSet = data[data['true_class'].isin(['car'])]
    busSet = data[data['true_class'].isin(['bus'])]
    bikeSet = data[data['true_class'].isin(['bike'])]
    walkSet = data[data['true_class'].isin(['walk'])]
    trainSet = data[data['true_class'].isin(['train'])]
    planeSet = data[data['true_class'].isin(['plane'])]
    ACRpd = pd.DataFrame({'car': carSet[carSet.ACR < 0.8].ACR,
                          'bus': busSet[busSet.ACR < 0.8].ACR,
                          'bike': bikeSet[bikeSet.ACR < 0.8].ACR,
                          'walk': walkSet[walkSet.ACR < 0.8].ACR,
                          'train': trainSet[trainSet.ACR < 0.8].ACR,
                          'plane': planeSet[planeSet.ACR < 0.8].ACR})
    ax = sns.boxplot(data=ACRpd,
                     order=['car', 'bus', 'bike', 'walk', 'train', 'plane'])
    # ax.set_xlabel('Transportation Mode')
    # ax.set_ylabel('ACR')
    ax.set_xlabel('出行方式', fontproperties=font)
    ax.set_ylabel('单位距离内加速度变化率 (ACR)', fontproperties=font)
    plt.show(ax)


def main():
    DBPath = '../DB/GPS.db'
    # drawVABox(DBPath)
    # drawACRBox(DBPath)


if __name__ == '__main__':
    main()
