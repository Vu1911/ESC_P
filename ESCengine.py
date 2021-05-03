import cv2
import numpy as np
import matplotlib.pyplot as plt
import ImgPreProcess as imgpre
import ImgSkew as skew
import THPTQGutils as utils
import ESCengine as engine

def getAnswerFromAnswerSheet(img, widthImg, heightImg):
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

    return answers