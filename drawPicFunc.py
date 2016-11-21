import pylab as pl


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


def drawHist():
    pass


def main():
    #  test drawLineGraph
    userAngleRate()
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


if __name__ == '__main__':
    main()
