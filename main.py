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

img = cv2.imread(pathImage)
imgResize = cv2.resize(img, (widthImg, heightImg))  # RESIZE IMAGE
answer = engine.getAnswerFromAnswerSheet(imgResize, widthImg, heightImg)

print(answer)
