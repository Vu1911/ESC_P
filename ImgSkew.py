import cv2
import numpy as np
import ImgPreProcess as imgpre

# skew given image at given points to a new img with given target
# width and height
def skewRectanglePerspective(img, fourPoints,widthTarget, heightTarget):
    points = imgpre.reorderRectangleContour(fourPoints)
    pts1 = np.float32(points)
    pts2 = np.float32([[0, 0],[widthTarget, 0], [0, heightTarget],[widthTarget, heightTarget]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgWarp = cv2.warpPerspective(img, matrix, (widthTarget, heightTarget))
    imgWarp = imgWarp[100:imgWarp.shape[0] - 120, 100:imgWarp.shape[1] - 120]
    imgWarp = cv2.resize(imgWarp, (widthTarget, heightTarget))
    return imgWarp