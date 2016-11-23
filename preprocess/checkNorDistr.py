import func


def main():
    filePath = 'checkStayPointNorDis.txt'
    allLines = func.readFile(filePath)
    lineNum = 1
    for line in allLines:
        line = line.strip('\n')
        line = eval(line)
        # print(line)
        # print(type(line))
        # print(lineNum)
        tempPointSet = []
        for item in line:
            tempPointSet.append((item[0:3]))
        # print(tempPointSet)
        f = func.isNormalDistr(tempPointSet)
        if f == 1:
            print('line ' + str(lineNum) + ' is normal distribution')
        else:
            print('line ' + str(lineNum) + ' is not normal distribution')
        lineNum += 1


if __name__ == '__main__':
    main()
