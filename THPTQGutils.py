import cv2
import matplotlib.pyplot as plt
import numpy as np
import ImgPreProcess as imgpre

# used after skew and preprocess to
# be a perfect black white image
# if the preprocess phrase is not
# working well, all these functions are
# fail to work

def getClosestRightPointToX(contours, x_mark):
    closestRightPointToX = [0,0]

    for i in range(x_mark, 0, -10):
        for contour in contours:
            for point in contour:
                x = point[0][0]
                if x > i-5 and x < i+5:
                    closestRightPointToX = point[0]
                    break
            if closestRightPointToX[0] != 0:
                break
        if closestRightPointToX[0] != 0:
            break

    return closestRightPointToX

def getClosestLowerPointToY(contours, y_mark):
    closestLowerPointToY = [0,0]

    for j in range(y_mark, 0, -10):
        for contour in contours:
            for point in contour:
                y = point[0][1]
                if y > j-5 and y < j+5:
                    closestLowerPointToY = point[0]
                    break
            if closestLowerPointToY[0] != 0:
                break
        if closestLowerPointToY[0] != 0:
            break

    return closestLowerPointToY

def getHorizontalAlignmentY(contours, widthImg): # Checked
    horizontalClosestPoint = getClosestRightPointToX(contours, widthImg)
    horizontalAlignY = horizontalClosestPoint[0]

    return horizontalAlignY

def getVerticalAlignmentX(contours, heightImg): # Checked
    verticalClosestPoint = getClosestLowerPointToY(contours, heightImg)
    verticalAlignX = verticalClosestPoint[1]

    return verticalAlignX

def getHVContoursInTheAlignment(contours, horizontalAlignY, verticalAlignX): # Checked
    horizontalAlignContours = []
    verticalAlignContours = []

    for contour in contours:
        for point in contour:
            x = point[0][0]
            y = point[0][1]
            if x > horizontalAlignY - 50 and x < horizontalAlignY + 50 and y < verticalAlignX - 50:
                # contour = imgpre.reorderContourByY(contour)
                horizontalAlignContours.append(contour)
                break
            if y > verticalAlignX - 60 and y < verticalAlignX + 60 and x < horizontalAlignY - 100:
                # contour = imgpre.reorderContourByX(contour)
                verticalAlignContours.append(contour)
                break
    horizontalAlignContours = sorted(horizontalAlignContours, key= lambda x:x[0][0][1])
    verticalAlignContours = sorted(verticalAlignContours, key= lambda x:x[0][0][0])
    return horizontalAlignContours, verticalAlignContours

def get40HorizontalAlignPoint(horizontalAlignContours):
    count = 0
    horizonAlignPoints = []
    while (count < len(horizontalAlignContours)):
        horizontalPoint = horizontalAlignContours[count][0][0]
        horizonAlignPoints.append(horizontalPoint)
        count+=1

    return horizonAlignPoints

def get16VerticalAlignPoint(verticalAlignContours):
    count = 0
    verticalAlignPoints = []

    while (count < len(verticalAlignContours)):
        verticalPoint = verticalAlignContours[count][3][0]
        verticalAlignPoints.append(verticalPoint)
        count+=1

    return verticalAlignPoints

def getAllAlignPoints(contours, widthImg, heightImg):
    horizontalAlignY = getHorizontalAlignmentY(contours, widthImg)
    verticalAlignX = getVerticalAlignmentX(contours, heightImg)

    horizontalAlignContours, verticalAlignContours = getHVContoursInTheAlignment(contours,
                                                                                  horizontalAlignY,
                                                                                  verticalAlignX)
    horizontalAlignPoints = get40HorizontalAlignPoint(horizontalAlignContours)
    verticalAlignPoints = get16VerticalAlignPoint(verticalAlignContours)

    # horizontalAlignPoints.sort(key= lambda x:x[1])
    # verticalAlignPoints.sort(key= lambda x:x[0])

    return horizontalAlignPoints, verticalAlignPoints, horizontalAlignContours, verticalAlignContours

def cutToTables(imgSkewed, horizontalAlignPoints, verticalAlignPoints):
    tables = []

    for y in range(0, 16, 4):
        for x in range(0, 30, 5):
            up = 30
            if (x == 0 and y == 0):
                up = 60
            table = imgSkewed[
                    horizontalAlignPoints[x][1] - 30: horizontalAlignPoints[x + 4][1] + 30,
                    verticalAlignPoints[y][0] - 10: verticalAlignPoints[y + 3][0] + 50]
            # cv2.imshow("la", table)
            # cv2.waitKey()
            tables.append(table)
    return tables

def getAnswers(tables):
    question_count = 0
    question_matrix = []
    min = 99999999
    max = 0
    for table in tables:
        table = cv2.resize(table, (500, 400))
        rows = np.vsplit(table, 5)
        row_matrix = []
        for row in rows:
            question_count += 1
            columns = np.hsplit(row, 4)
            column_matrix = []
            for column in columns:
                column = cv2.threshold(column, 215, 255, cv2.THRESH_BINARY)[1]
                column = cv2.medianBlur(column, 17)
                pixel = cv2.countNonZero(column)
                if pixel > max:
                    max = pixel
                if pixel < min:
                    min = pixel
                column_matrix.append(pixel)
            row_matrix.append(column_matrix)
        question_matrix.append(row_matrix)

    answers = []
    question_number = 0
    for table in question_matrix:
        rows = []
        for row in table:
            question_number+=1
            columns = []
            c = 0
            for column in row:
                if column > 8800:
                    c = 0
                else:
                    c = 1
                columns.append(c)
            rows.append(columns)
        answers.append(rows)
    return answers