import cv2
import numpy as np
import matplotlib.pyplot as plt
import ImgPreProcess as imgpre
import ImgSkew as skew
import THPTQGutils as utils
import ESCengine as engine

########################################################################
pathImage = "test_imgs/oppo-a3s-12mp/OPPO_A3S_1.jpeg"
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
    answersInput = open('answerOppoTest.txt')
    countCorrectAns = 0
    i, j, k = 0, 0, 0
    while True:
        k += 1
        ans = str(answersInput.readline()).strip()
        # skip condition len(checkQues(userAnswers[i][j]))==1 when u calculate Accuracy

        # for accuracy
        if (ans == checkQues(userAnswers[i][j])):
        # for calculation mark
        # if( ans == checkQues(userAnswers[i][j]) and len(checkQues(userAnswers[i][j]))==1):
            countCorrectAns += 1
            print(k, ".", "Key:", ans, "UserAnswer: ", checkQues(userAnswers[i][j]),"Current Score:", countCorrectAns*10/120)
        else:
            print(k, ".", "Key:", ans, "UserAnswer: ", checkQues(userAnswers[i][j]))
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
    answers = engine.getAnswerFromAnswerSheet(imgResize, widthImg, heightImg)
    print(answers)
    markCalculation(answers)
