import cv2
import numpy as np
import matplotlib.pyplot as plt
import ImgPreProcess as imgpre
import ImgSkew as skew
import THPTQGutils as utils

########################################################################
pathImage = "22.jpg"
heightImg = 4060
widthImg  = 3020
########################################################################

img = cv2.imread(pathImage)
imgResize = cv2.resize(img, (widthImg, heightImg)) # RESIZE IMAGE
imgPre = imgpre.preprocessForContourDetect(img)

contours, hierarchy = cv2.findContours(imgPre, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # FIND ALL CONTOURS
biggestRectangle, max_area = imgpre.biggestRectangle4Point(contours)
rectanglePoints = imgpre.reorderRectangleContour(biggestRectangle)

imgSkewedColored = skew.skewRectanglePerspective(img, rectanglePoints, widthImg, heightImg)
imgSkewedShadeRemoved = imgpre.shadeRemove(imgSkewedColored)
imgSkewedGrayShadeRemoved = cv2.cvtColor(imgSkewedShadeRemoved, cv2.COLOR_BGR2GRAY)

imgPre2 = imgpre.preprocessForContourDetect(imgSkewedShadeRemoved)

contours2, hierarchy2 = cv2.findContours(imgPre2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

horizontalAlignPoints, verticalAlignPoints, horizontalAlignContours, verticalAlignContours = utils.getAllAlignPoints(contours2, widthImg, heightImg)

imgTables = utils.cutToTables(imgSkewedGrayShadeRemoved, horizontalAlignPoints[11:], verticalAlignPoints[1:])

answers = utils.getAnswers(imgTables)

imgTest = imgSkewedShadeRemoved.copy()

for horizontalAlignPoint in horizontalAlignPoints :
    # print(horizontalAlignPoint)
    imgTest = cv2.circle(imgTest, tuple(horizontalAlignPoint), radius=10, color=(0, 0, 255), thickness=-1)

for verticalAlignPoint in verticalAlignPoints :
    # print(horizontalAlignPoint)
    imgTest = cv2.circle(imgTest, tuple(verticalAlignPoint), radius=10, color=(0, 0, 255), thickness=-1)

print(len(verticalAlignContours))
imgTest = cv2.drawContours(imgTest, verticalAlignContours[1:17], -1, (0, 255, 0), 10)
imgTest = cv2.drawContours(imgTest, horizontalAlignContours[11:], -1, (0,255,0), 10)

plt.figure(figsize=(30, 22))
plt.imshow(imgTest)
plt.show()