#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Observer
#
# Created:     23/04/2017
# Copyright:   (c) Observer 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import polyshape
from getAllPoly import getAllPoly
import cv2
import sys
import numpy as np

def main():
    imFile = "C:/Code/cs682/final/Data/vid8/frameAnnotations-MVI_0120.MOV_annotations/intersection_1324866305.avi_image0.png"

    colorImg = cv2.imread(imFile)
    grayImg = cv2.cvtColor(colorImg, cv2.COLOR_BGR2GRAY)
    blurImg = cv2.GaussianBlur(colorImg, (3,3), sigmaX = 1.5, sigmaY = 1.5)
    edgeImg = cv2.Canny(colorImg, 20, 80)
    kernel = np.ones( (2, 2), dtype=np.uint8)
    dImg = cv2.dilate(edgeImg, kernel, iterations=1)

    '''
    lineImg = np.zeros(edgeImg.shape, dtype=np.uint8)
    lines = cv2.HoughLinesP(edgeImg, 1, 3.14/180, 5, minLineLength = 8, maxLineGap = 2)
    for line in lines[0]:
        p1 = tuple(line[0:2])
        p2 = tuple(line[2:4])
        cv2.line(lineImg, p1, p2, (255, 255, 255))

    cv2.imshow('Lines', lineImg)
    '''
    cv2.imshow('Edges', edgeImg)
    cv2.imshow('Dilated', dImg)
    polys = getAllPoly(dImg, 100, 1800)

    for p in polys:
        p.drawBoundingRect(colorImg, (0, 200, 0))
        p.drawContour(colorImg, (200, 0, 0))

    cv2.imshow('Blurred', blurImg)
    cv2.imshow('Polygons', colorImg)

    cv2.imshow('Region of interest', roi1)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    sys.exit(0)

if __name__ == '__main__':
    main()
