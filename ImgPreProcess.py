import cv2
import numpy as np
import matplotlib.pyplot as plt

# blur, gray, canny the img, preparing for contour detecting phase
def preprocessForContourDetect(img):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (5,5), 0)
    imgThreshold = cv2.threshold(imgBlur, 100, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    imgCanny = cv2.Canny(imgThreshold, 75, 200)
    kernel = np.ones((5,5))
    imgDilate = cv2.dilate(imgCanny, kernel, iterations=2)  # APPLY DILATION
    imgErode = cv2.erode(imgDilate, kernel, iterations=1)  # APPLY EROSION
    imgResult = imgErode
    return imgResult

# find the biggest rectangle paper shape contour from
# a list of contours
def biggestRectangle4Point(contours):
    biggestRectangle = np.array([])
    max_area = 0

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 5000:
            peri = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
            # if this contour has approx shape of a rectangle and the area
            # is greater than the current max area
            if area > max_area and len(approx) == 4:
                biggestRectangle = approx
                max_area = area

    return biggestRectangle, max_area

# take in four point of a rectangle contour, correct the order of
# the edge and return the right order points list
def reorderRectangleContour(points):
    myPoints = points.reshape((4,2))
    myResultPoints = np.zeros((4,1,2), dtype=np.int32)
    add = myPoints.sum(1)

    myResultPoints[0] = myPoints[np.argmin(add)]
    myResultPoints[3] = myPoints[np.argmax(add)]

    diff = np.diff(myPoints, axis=1)

    myResultPoints[1] = myPoints[np.argmin(diff)]
    myResultPoints[2] = myPoints[np.argmax(diff)]

    return myResultPoints

def reorderContourByX(contour):
    reorderByX = sorted(contour, key= lambda x: x[0][0])
    return reorderByX

def reorderContourByY(contour):
    reorderByY = sorted(contour, key= lambda y: y[0][1])
    return reorderByY

def shadeRemove(img):
    rgb_planes = cv2.split(img)

    result_planes = []
    result_norm_planes = []
    for plane in rgb_planes:
        dilated_img = cv2.dilate(plane, np.ones((7, 7), np.uint8))
        bg_img = cv2.medianBlur(dilated_img, 89)
        diff_img = 255 - cv2.absdiff(plane, bg_img)
        norm_img = cv2.normalize(diff_img, None, alpha=110, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
        result_planes.append(diff_img)
        result_norm_planes.append(norm_img)

    result = cv2.merge(result_planes)
    return result


