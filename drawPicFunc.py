#-*- coding: utf-8 -*-
import pylab as pl
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import preprocess.DBUtil as DB
from matplotlib.font_manager import FontProperties
from matplotlib.ticker import MultipleLocator, FormatStrFormatter


font = FontProperties(fname=r"c:/Windows/Fonts/simsun.ttc", size=14)


def drawLineGraph(x, y, labelSet, title, xAxisLa, yAxisLa,
                  xStart, xLime, yStart, yLime):
    """
    show line Graph ( one or more line in one graph )

    about parameter:
         some options for the color character are:
                         'r' = red
                         'g' = green
                         'b' = blue
                         'c' = cyan
                         'm' = magenta
                         'y' = yellow
                         'k' = black
                         'w' = white
         options for line style are:
                         '-' = solid
                         '--' = dashed
                         ':' = dotted
                         '-.' = dot-dashed
                         '.' = points
                         'o' = filled circles
                         '^' = filled triangles
    Args:
         x: such as [[10, 20], [2, 3]]
         y: such as [[4, 9], [90, 30]]
           note: The dimensions of the X axis and the Y axis are in agreement
         labelSet: the description of line,
                   x's length = y's length = labelSet's length
         title: title string
         xAxisLa: x axis's label
         yAxisLa: y axis's label
         xStart, xLime: xStart~xLime
         yStart, yLime: yStart~yLime
    """
    plotSet = []
    colorSet = ['r', 'b', 'k', 'g', 'm']
    # colorSet = ['-', '--', ':', '-.', 'o']
    # labelSet = ['user 1']
    for lx, ly, co, la in zip(x, y, colorSet, labelSet):
        plotSet.append(pl.plot(lx, ly, co, label=la))
    pl.title(title)
    pl.xlabel(xAxisLa)
    pl.ylabel(yAxisLa)
    pl.xlim(xStart, xLime)
    pl.ylim(yStart, yLime)
    pl.legend()
    pl.show()


def userAngleRate():
    x = []
    y = []
    xAxis = [10, 20, 30, 40, 50, 60, 70, 80]
    #  user 1
    y1 = [107, 107, 104, 99, 95, 76, 27, 2]
    #  user 2
    y2 = [140, 140, 140, 140, 135, 99, 24, 6]
    #  user 5
    y3 = [49, 47, 46, 44, 29, 16, 6, 2]
    #  user 6
    y4 = [53, 53, 53, 52, 41, 14, 3, 0]
    #  user 10
    y5 = [77, 77, 77, 76, 73, 51, 8, 2]
    x.append(xAxis)
    y.append(y1)
    x.append(xAxis)
    y.append(y2)
    x.append(xAxis)
    y.append(y3)
    x.append(xAxis)
    y.append(y4)
    x.append(xAxis)
    y.append(y5)
    title = 'Select value for variable angleRate through' + \
            ' the number of stay points'
    drawLineGraph(x, y, ['user 1', 'user 2', 'user 3', 'user 4', 'user 5'],
                  title, 'angleRate (%)', 'the number of stay point',
                  0, 100, 0, 150)


def getVA(DBPath):
    conn = DB.get_conn(DBPath)
    carArr = []
    busArr = []
    bikeArr = []
    walkArr = []
    trainArr = []
    planeArr = []
    i = 1
    while i <= 32:
        fetSql = 'select velocity,accelerometer,mode from GPS_points_' + str(i)
        allRecords = DB.fetchAll(conn, fetSql)
        for item in allRecords:
            if item[2] == 'car':
                carArr.append((item[0], item[1]))
            if item[2] == 'bus':
                busArr.append((item[0], item[1]))
            if item[2] == 'bike':
                bikeArr.append((item[0], item[1]))
            if item[2] == 'walk':
                walkArr.append((item[0], item[1]))
            if item[2] == 'train':
                trainArr.append((item[0], item[1]))
            if item[2] == 'plane':
                planeArr.append((item[0], item[1]))
        i += 1
    DB.closeDB(conn)
    carArr = np.array(carArr)
    busArr = np.array(busArr)
    bikeArr = np.array(bikeArr)
    walkArr = np.array(walkArr)
    trainArr = np.array(trainArr)
    planeArr = np.array(planeArr)
    # user 1~10
    drawHist(carArr, 'Car Velocity (m/s)', 'Frequency',
             'Car Acceleration (m/s$^2$)', 'Frequency',
             0, 50, 0, 2.5, 10000, 70000)
    # drawHist(carArr, '汽车速度 (m/s)', '频率',
    #          '汽车加速度 (m/s$^2$)', '频率',
    #          0, 50, 0, 2.5, 10000, 70000)
    # user 1~10
    # drawHist(busArr, 'Bus Velocity (m/s)', 'Frequency',
    #          'Bus Acceleration (m/s$^2$)', 'Frequency',
    #          0, 25, 0, 2.5, 60000, 50000)
    # drawHist(busArr, '公交车速度 (m/s)', '频率',
    #          '公交车加速度 (m/s$^2$)', '频率',
    #          0, 25, 0, 2.5, 60000, 50000)
    # user 1~10
    # drawHist(bikeArr, 'Bike Velocity (m/s)', 'Frequency',
    #          'Bike Acceleration (m/s$^2$)', 'Frequency',
    #          0, 12, 0, 3, 10000, 20000)
    # drawHist(bikeArr, '自行车速度 (m/s)', '频率',
    #          '自行车加速度 (m/s$^2$)', '频率',
    #          0, 12, 0, 3, 10000, 20000)
    # user 1~10
    # drawHist(walkArr, 'Walk Velocity (m/s)', 'Frequency',
    #          'Walk Acceleration (m/s$^2$)', 'Frequency',
    #          0, 10, 0, 4, 50000, 80000)
    # drawHist(walkArr, '步行速度 (m/s)', '频率',
    #          '步行加速度 (m/s$^2$)', '频率',
    #          0, 10, 0, 4, 50000, 80000)
    #  user 1~10
    # drawHist(trainArr, 'Train Velocity (m/s)', 'Frequency',
    #          'Train Acceleration (m/s$^2$)', 'Frequency',
    #          0, 40, 0, 4, 10000, 30000)
    # drawHist(trainArr, '火车速度 (m/s)', '频率',
    #          '火车加速度 (m/s$^2$)', '频率',
    #          0, 40, 0, 4, 10000, 30000)
    # user 1~32
    # drawHist(planeArr, 'Plane Velocity (m/s)', 'Frequency',
    #          'Plane Acceleration (m/s$^2$)', 'Frequency',
    #          0, 300, 0, 2, 1000, 5000)
    # drawHist(planeArr, '飞机速度 (m/s)', '频率',
    #          '飞机加速度 (m/s$^2$)', '频率',
    #          0, 300, 0, 2, 1000, 5000)


def getVAFigure(DBPath):
    conn = DB.get_conn(DBPath)
    # velocity list
    carVArr = []
    busVArr = []
    bikeVArr = []
    walkVArr = []
    trainVArr = []
    planeVArr = []
    # acceleration list
    carAArr = []
    busAArr = []
    bikeAArr = []
    walkAArr = []
    trainAArr = []
    planeAArr = []
    i = 1
    while i <= 32:
        fetSql = 'select velocity,accelerometer,mode from GPS_points_' + str(i)
        allRecords = DB.fetchAll(conn, fetSql)
        for item in allRecords:
            if item[2] == 'car':
                carVArr.append(item[0])
                carAArr.append(item[1])
            if item[2] == 'bus':
                busVArr.append(item[0])
                busAArr.append(item[1])
            if item[2] == 'bike':
                bikeVArr.append(item[0])
                bikeAArr.append(item[1])
            if item[2] == 'walk':
                walkVArr.append(item[0])
                walkAArr.append(item[1])
            if item[2] == 'train':
                trainVArr.append(item[0])
                trainAArr.append(item[1])
            if item[2] == 'plane':
                planeVArr.append(item[0])
                planeAArr.append(item[1])
        i += 1
    DB.closeDB(conn)
    vBox = []
    vBox.append(carVArr)
    vBox.append(busVArr)
    vBox.append(bikeVArr)
    vBox.append(walkVArr)
    vBox.append(trainVArr)
    vBox.append(planeVArr)

    aBox = []
    aBox.append(carAArr)
    aBox.append(busAArr)
    aBox.append(bikeAArr)
    aBox.append(walkAArr)
    aBox.append(trainAArr)
    aBox.append(planeAArr)

    # drawCDF(vBox, 'Velocity (m/s)')
    drawCDF(aBox, 'Acceleration (m/s$^2$)')


def drawHist(data, xla1, yla1, xla2, yla2, xStart1, xLime1,
             xStart2, xLime2, vbins, abins):
    """
    n rows * 2 cloumn (0: velocity 1:acceleration)
    """
    # mode velocity distribution
    plt.subplot(2, 1, 1)
    plt.hist(data[:, 0], bins=vbins)
    plt.xlim(xStart1, xLime1)
    plt.xlabel(xla1)
    plt.ylabel(yla1)
    # plt.xlabel(xla1, fontproperties=font)
    # plt.ylabel(yla1, fontproperties=font)

    plt.subplots_adjust(hspace=0.3)

    # mode accleration distribution
    plt.subplot(2, 1, 2)
    plt.hist(data[:, 1], bins=abins)
    plt.xlim(xStart2, xLime2)
    plt.xlabel(xla2)
    plt.ylabel(yla2)
    # plt.xlabel(xla2, fontproperties=font)
    # plt.ylabel(yla2, fontproperties=font)
    plt.show()


def drawScatter(carArr, busArr, bikeArr, walkArr, trainArr, planeArr):
    """
    n rows * 2 cloumn (0: velocity 1:acceleration)
    """
    # car velocity distribution
    pass


def drawScatter1():
    x = np.random.rand(50, 30)
    f1 = plt.figure(1)
    plt.subplot(2, 2, 1)
    plt.scatter(x[:, 1], x[:, 0])
    print(type(x[:, 1]))

    plt.subplot(2, 2, 2)
    label = list(np.ones(20)) + list(2 * np.ones(15)) + list(3 * np.ones(15))
    label = np.array(label)
    plt.scatter(x[:, 1], x[:, 0], 15.0 * label, 15.0 * label)

    plt.subplot(2, 2, 3)
    plt.scatter(x[:, 1], x[:, 0])

    plt.subplot(2, 2, 4)
    plt.scatter(x[:, 1], x[:, 0])

    # with legend
    f2 = plt.figure(2)
    idx_1 = np.where(label == 1)
    p1 = plt.scatter(x[idx_1, 1], x[idx_1, 0], marker='x',
                     color='m', label='1', s=30)
    idx_2 = np.where(label == 2)
    p2 = plt.scatter(x[idx_2, 1], x[idx_2, 0], marker='+',
                     color='c', label='2', s=50)
    idx_3 = np.where(label == 3)
    p3 = plt.scatter(x[idx_3, 1], x[idx_3, 0], marker='o',
                     color='r', label='3', s=15)
    plt.legend(loc='upper right')
    plt.show()


def drawBox(data):
    """
    Args: data
        data: 6 rows * n column
    """
    fig = plt.figure(1, figsize=(9, 6))
    ax = fig.add_subplot(111)
    bp = ax.boxplot(data, patch_artist=True)
    # change outline color, fill color and linewidth of the boxes
    for box in bp['boxes']:
        # change outline color
        box.set(color='#7570b3', linewidth=2)
        # change fill color
        box.set(facecolor='#1b9e77')

    # change color and linewidth of the whiskers
    for whisker in bp['whiskers']:
        whisker.set(color='y', linewidth=2)

    # change color and linewidth of the caps
    for cap in bp['caps']:  # 上下的帽子
        cap.set(color='#7570b3', linewidth=2)

    # change color and linewidth of the medians
    for median in bp['medians']:  # 中值
        median.set(color='r', linewidth=2)

    # change the style of fliers and their fill
    for flier in bp['fliers']:  # 异常值
        flier.set(marker='o', color='k', alpha=0.5)
    plt.xlabel('mode')
    plt.ylabel('velocity')
    ax.set_xticklabels(['car', 'bus', 'bike', 'walk', 'train', 'plane'])
    plt.show()


def drawBox1():
    """
    Args: data
        data: 6 rows * n column
    """
    np.random.seed(10)
    data = [np.random.normal(100, 10, 200),
            np.random.normal(80, 30, 200),
            np.random.normal(90, 20, 200),
            np.random.normal(70, 25, 200),
            np.random.normal(70, 25, 100),
            np.random.normal(70, 25, 200)]
    fig = plt.figure(1, figsize=(9, 6))
    ax = fig.add_subplot(111)
    bp = ax.boxplot(data, patch_artist=True)
    # change outline color, fill color and linewidth of the boxes
    for box in bp['boxes']:
        # change outline color
        box.set(color='#7570b3', linewidth=2)
        # change fill color
        box.set(facecolor='#1b9e77')

    # change color and linewidth of the whiskers
    for whisker in bp['whiskers']:
        whisker.set(color='y', linewidth=2)

    # change color and linewidth of the caps
    for cap in bp['caps']:  # 上下的帽子
        cap.set(color='#7570b3', linewidth=2)

    # change color and linewidth of the medians
    for median in bp['medians']:  # 中值
        median.set(color='r', linewidth=2)

    # change the style of fliers and their fill
    for flier in bp['fliers']:  # 异常值
        flier.set(marker='o', color='k', alpha=0.5)
    plt.xlabel('mode')
    plt.ylabel('velocity')
    ax.set_xticklabels(['car', 'bus', 'bike', 'walk', 'train', 'plane'])
    plt.show()


def drawCDF(data, xDes):
    # xminorLocator = MultipleLocator(1)
    # ax = plt.subplot(111)
    # ax.xaxis.set_minor_locator(xminorLocator)
    colorSet = ['r', 'g', 'b', 'y', 'm', 'k']
    # shapeSet = ['*', '_', ',', 'o', '.', '+']
    index = 0
    while index < 6:
        mode = data[index]
        modeSorted = np.sort(mode)
        modLen = len(mode)
        p = 1. * np.arange(modLen) / (modLen - 1)
        plt.plot(modeSorted, p, c=colorSet[index], linewidth=1.5)
        # plt.plot(modeSorted, p, marker=shapeSet[index])
        index += 1
    plt.xlabel(xDes)
    plt.ylabel('CDF')
    # velocity setting
    plt.xlim(0, 25)
    # acceleration setting
    # plt.xlim(0, 3)
    plt.grid()
    modeName = ['car', 'bus', 'bike', 'walk', 'train', 'plane']
    plt.legend(modeName)
    # velocity setting
    # plt.xticks([0, 2.3, 4, 5.2, 8, 12, 16, 20, 24, 28])
    # acceleration setting
    # plt.xticks([0, 0.3, 0.5, 1, 2, 3])
    plt.yticks([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
    plt.show()


def drawALine(DBPath):
    """
           car,bus,bike,walk,train,plane
    """
    conn = DB.get_conn(DBPath)

    # find car segments
    # fetCarSql = 'select accelerometer from GPS_points_22 where id>204322 and id<206107'
    # carYData = pd.read_sql(fetCarSql, conn)
    # lenCar = len(carYData)
    # carX = np.linspace(0, 2 * lenCar - 2, lenCar)
    # plt.plot(carX, carYData.accelerometer, c='b')
    # plt.xlim(0, 1000)
    # plt.ylim(0, 2)
    # plt.ylabel('Car Acceleration (m/s$^2$)')
    # plt.xlabel('Time (s)')
    # # plt.xlabel('时间 (秒)', fontproperties=font)
    # # plt.ylabel('汽车加速度 (m/s$^2$)', fontproperties=font)

    # find bus segments
    # fetBusSql = 'select accelerometer from GPS_points_11 where id>273685 and id<275728'
    # busYData = pd.read_sql(fetBusSql, conn)
    # lenBus = len(busYData)
    # busX = np.linspace(0, 2 * lenBus - 2, lenBus)
    # plt.plot(busX, busYData.accelerometer, c='b')
    # plt.xlim(0, 1000)
    # plt.ylim(0, 2)
    # # plt.ylabel('Bus Acceleration (m/s$^2$)')
    # # plt.xlabel('Time (s)')
    # plt.xlabel('时间 (秒)', fontproperties=font)
    # plt.ylabel('公交车加速度 (m/s$^2$)', fontproperties=font)

    # find bike segments
    # fetBikeSql = 'select accelerometer from GPS_points_32 where id>284378 and id<285602'
    # bikeYData = pd.read_sql(fetBikeSql, conn)
    # lenBike = len(bikeYData)
    # bikeX = np.linspace(0, 2 * lenBike - 2, lenBike)
    # plt.plot(bikeX, bikeYData.accelerometer, c='b')
    # plt.xlim(0, 1000)
    # plt.ylim(0, 2)
    # plt.ylabel('Bike Acceleration (m/s$^2$)')
    # plt.xlabel('Time (s)')
    # # plt.xlabel('时间 (秒)', fontproperties=font)
    # # plt.ylabel('自行车加速度 (m/s$^2$)', fontproperties=font)

    # find walk segments
    # fetWalkSql = 'select accelerometer from GPS_points_27 where id>785915 and id<787725'
    # walkYData = pd.read_sql(fetWalkSql, conn)
    # lenWalk = len(walkYData)
    # walkX = np.linspace(0, 2 * lenWalk - 2, lenWalk)
    # plt.plot(walkX, walkYData.accelerometer, c='b')
    # plt.xlim(0, 1000)
    # plt.ylim(0, 2)
    # plt.ylabel('Walk Acceleration (m/s$^2$)')
    # plt.xlabel('Time (s)')
    # # plt.xlabel('时间 (秒)', fontproperties=font)
    # # plt.ylabel('步行加速度 (m/s$^2$)', fontproperties=font)

    # find train segments
    # fetTrainSql = 'select accelerometer from GPS_points_12 where id>801867 and id<802982'
    # trainYData = pd.read_sql(fetTrainSql, conn)
    # lenTrain = len(trainYData)
    # trainX = np.linspace(0, 2 * lenTrain - 2, lenTrain)
    # plt.plot(trainX, trainYData.accelerometer, c='b')
    # plt.xlim(0, 2000)
    # plt.ylim(0, 10)
    # # plt.ylabel('Train Acceleration (m/s$^2$)')
    # # plt.xlabel('Time (s)')
    # plt.xlabel('时间 (秒)', fontproperties=font)
    # plt.ylabel('火车加速度 (m/s$^2$)', fontproperties=font)

    # find plane segments
    fetPlaneSql = 'select accelerometer from GPS_points_1 where id>306601 and id<309414'
    planeYData = pd.read_sql(fetPlaneSql, conn)
    lenPlane = len(planeYData)
    planeX = np.linspace(0, 2 * lenPlane - 2, lenPlane)
    plt.plot(planeX, planeYData.accelerometer, c='b')
    plt.xlim(0, 1000)
    plt.ylim(0, 2)
    # plt.ylabel('Plane Acceleration (m/s$^2$)')
    # plt.xlabel('Time (s)')
    plt.xlabel('时间 (秒)', fontproperties=font)
    plt.ylabel('飞机加速度 (m/s$^2$)', fontproperties=font)

    plt.grid()
    # modeName = ['car', 'bus', 'bike', 'walk', 'train', 'plane']
    # plt.legend(modeName)
    # plt.ylim(0, 4)
    plt.show()
    DB.closeDB(conn)


def main():
    #  test drawLineGraph
    # userAngleRate()
    # x = []
    # y = []
    # x1 = [10, 20, 30, 40, 50, 60, 70, 80]
    # y1 = [107, 107, 104, 99, 95, 76, 27, 2]
    # x2 = [10, 20, 30, 40, 50, 60]
    # y2 = [140, 140, 140, 140, 135, 99]
    # x.append(x1)
    # # x.append(x2)
    # y.append(y1)
    # # y.append(y2)
    # print(x)
    # print(y)
    # drawLineGraph(x, y, ['user 1'], 'angleRate and stay points',
    #               'angleRate (%)', 'the number of stay point',
    #               0, 100, 0, 150)

    # test drawScatter function
    # drawScatter1()
    DBPath = 'DB/GPS.db'
    # getVA(DBPath)
    # getVAFigure(DBPath)
    drawALine(DBPath)


if __name__ == '__main__':
    main()
