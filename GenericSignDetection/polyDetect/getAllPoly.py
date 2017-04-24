import cv2
import numpy as np
from polyshape import polyshape


def getAllPoly(srcImg, minArea, maxArea):
    contours, heirarchy = cv2.findContours(srcImg, mode = cv2.cv.CV_RETR_LIST, method = cv2.cv.CV_CHAIN_APPROX_SIMPLE)

    polys = []
    for c in contours:
        p = polyshape(c)
        if p.sides <= 8 and p.area <= maxArea and p.area >= minArea:
            print p.sides
            polys.append(p)
        else:
            # TODO: Should attempt a circle fit
            pass
    return polys
