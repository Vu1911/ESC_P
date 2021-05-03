import cv2
import numpy as np
import matplotlib.pyplot as plt
import ImgPreProcess as imgpre
import ImgSkew as skew
import THPTQGutils as utils
import ESCengine as engine

########################################################################
pathImage = "22.jpg"
heightImg = 4060
widthImg  = 3020
########################################################################

def checkQues(ans):
    defi = {0:'A', 1:'B', 2:'C', 3:'D'}
    str = ''
    for i in range(0, len(ans)):
        if(ans[i] == 1):
            str += defi[i]
    return str

def markCalculation(userAnswers):
    answersInput = open('answerInput.txt')
    countCorrectAns = 0
    i, j, k = 0, 0, 0
    while True:
        k += 1
        ans = str(answersInput.readline()).strip()
        # skip condition len(checkQues(userAnswers[i][j]))==1 when u calculate Accuracy
        if( ans == checkQues(userAnswers[i][j]) and len(checkQues(userAnswers[i][j]))==1):
            countCorrectAns += 1
            print(k, ans, checkQues(userAnswers[i][j]), countCorrectAns*10/120)
        else:
            print(k, ans, checkQues(userAnswers[i][j]))
        j += 1
        if( j == 5 ):
            i += 1
            j = 0
        if( i == 24 ):
            break
    print("TOTAL Score:", countCorrectAns*10/120)

if __name__ == '__main__':
    img = cv2.imread(pathImage)
    imgResize = cv2.resize(img, (widthImg, heightImg))  # RESIZE IMAGE
    imgPre = imgpre.preprocessForContourDetect(img)

    contours, hierarchy = cv2.findContours(imgPre, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # FIND ALL CONTOURS
    biggestRectangle, max_area = imgpre.biggestRectangle4Point(contours)
    rectanglePoints = imgpre.reorderRectangleContour(biggestRectangle)

    imgSkewedColored = skew.skewRectanglePerspective(img, rectanglePoints, widthImg, heightImg)
    imgSkewedShadeRemoved = imgpre.shadeRemove(imgSkewedColored)
    imgSkewedGrayShadeRemoved = cv2.cvtColor(imgSkewedShadeRemoved, cv2.COLOR_BGR2GRAY)

    imgPre2 = imgpre.preprocessForContourDetect(imgSkewedShadeRemoved)

    contours2, hierarchy2 = cv2.findContours(imgPre2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    horizontalAlignPoints, verticalAlignPoints, horizontalAlignContours, verticalAlignContours = utils.getAllAlignPoints(
        contours2, widthImg, heightImg)

    imgTables = utils.cutToTables(imgSkewedGrayShadeRemoved, horizontalAlignPoints[11:], verticalAlignPoints[1:])

    answers = utils.getAnswers(imgTables)

    imgTest = imgSkewedShadeRemoved.copy()

    for horizontalAlignPoint in horizontalAlignPoints:
        # print(horizontalAlignPoint)
        imgTest = cv2.circle(imgTest, tuple(horizontalAlignPoint), radius=10, color=(0, 0, 255), thickness=-1)

    for verticalAlignPoint in verticalAlignPoints:
        # print(horizontalAlignPoint)
        imgTest = cv2.circle(imgTest, tuple(verticalAlignPoint), radius=10, color=(0, 0, 255), thickness=-1)
    print(len(verticalAlignContours))
    markCalculation(answers)
    imgTest = cv2.drawContours(imgTest, verticalAlignContours[1:17], -1, (0, 255, 0), 10)
    imgTest = cv2.drawContours(imgTest, horizontalAlignContours[11:], -1, (0, 255, 0), 10)

    plt.figure(figsize=(30, 22))
    plt.imshow(imgTest)
    plt.show()