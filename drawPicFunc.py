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
    colorSet = ['r', 'b']
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


def drawHist():
    pass


def main():
    #  test drawLineGraph
    x = []
    y = []
    x1 = [10, 20, 30, 40, 50, 60, 70, 80]
    y1 = [107, 107, 104, 99, 95, 76, 27, 2]
    x2 = [10, 20, 30, 40, 50, 60]
    y2 = [140, 140, 140, 140, 135, 99]
    x.append(x1)
    # x.append(x2)
    y.append(y1)
    # y.append(y2)
    print(x)
    print(y)
    drawLineGraph(x, y, ['user 1'], 'angleRate and stay points',
                  'angleRate (%)', 'the number of stay point',
                  0, 100, 0, 150)


if __name__ == '__main__':
    main()
