"""
Final contour detection and polygon and splitting code

CS682 - Final Project - Generic Sign Detection
Spring 2017

Author: Joseph Kinzel

"""

import cv2
import numpy as np
from polyshape import polyshape
import random
import math

'''
    Attempt to extract all polygons from a binary edge image
    
    srcImg - Binary edge image
    minArea - Minimum area threshold
    maxArea - Maximum area threshold
    approxDist - Approximation tuning distance for cv2.approxPolyDP
    maxGap - Maximum gap to 'jump' and split polygons upon
    maxDoubleMergeSides - Maximum number of lines two subregions of a contour can have before being merged at two points.
     
    Note: A double merge is basically a situation that occur in a large contour outlining a set of objects like a sign
    on a pole where there might be two gaps in the shape of sign.  Both of these gaps needs to be eliminated to extract 
    the sign and the 'maxToPointSides' parameter puts a limit on the number of edges on each of the two side regions.
    
    Returns: List of detected polyShapes
'''

def getAllPoly(srcImg, minArea, maxArea, approxDist, maxGap, maxDoubleMergeSides):
    # NOTE: OPTIONAL INIT FOR CONTOUR IMAGE
    cImg = cv2.cvtColor(srcImg, cv2.COLOR_GRAY2BGR)

    srcCopy = np.copy(cImg)

    # Extract all contours from the edge image
    im2, contours, hierarchy = cv2.findContours(srcImg, mode = cv2.RETR_TREE, method = cv2.CHAIN_APPROX_TC89_KCOS)

    polys = []

    newshapes = contours[:]

    slice = newshapes[:]
    old_size = len(newshapes)

    iter = 0

    while len(slice) and iter < 1:

        for c in slice:
            # Ignore any lines
            if len(c) > 2:
                # approxDist = cv2.arcLength(c, closed=True)*epsilon
                # Approximate the polygon shape to remove redundant points due to noise or aliasing
                approx = cv2.approxPolyDP(c, approxDist, closed=True)
                area = cv2.contourArea(approx)
                con_area = cv2.contourArea(c)

                # No use looking at any feature too small to recognize
                if minArea <= area:
                    mergeList = []
                    for i in range(0, len(approx)):
                        for j in range(i + 1, len(approx)):
                            # Calculate the euclidean distance between all points
                            v1 = np.array(approx[i][0], dtype=np.float32)
                            v2 = np.array(approx[j][0], dtype=np.float32)

                            v3 = v1 - v2

                            dist = math.sqrt( np.dot(v3, v3) )
                            # If the distance is below mark those edges as possible locations for splits
                            if dist <= maxGap:
                                mergeList.append((i, j, dist))
                    for i in range(0, len(mergeList)):
                        (idx1, idx2, dist) = mergeList[i]

                        slice1 = np.append( approx[idx2:], approx[0:idx1], axis = 0)
                        if 2 < len(slice1) <= 8:
                            newshapes.append(slice1)

                        slice2 = approx[idx1:idx2]
                        if 2 < len(slice2) <= 8:
                            newshapes.append(slice2)

                        for j in range(i+1, len(mergeList)):
                            idx3, idx4, d2 = mergeList[j]
                            if idx3 - idx1 > maxDoubleMergeSides or idx4 - idx2 > maxDoubleMergeSides:
                                break
                            sub1 = approx[idx1:idx3+1]
                            sub2 = approx[idx2:idx4+1]
                            sub = np.append(sub1, sub2[::-1], axis=0)
                            newshapes.append(sub)

        slice = newshapes[old_size:]
        old_size = len(newshapes)
        iter += 1

    # We only care about new shapes and old ones that passed the minimum area requirement to begin with
    validShapes = newshapes

    for c in validShapes:


        # print c
        # print len(c)
        # Approximate polygon shape

        approx = cv2.approxPolyDP(c, approxDist, closed=True)

        # approx = cv2.convexHull(approx)
        area = cv2.contourArea(approx)
        con_area = cv2.contourArea(c)

        # Create a polyshape object
        p = polyshape(approx)
        # Threshold by total number of sides and area, if it passes put it on the list for further testing
        if p.sides <= 8 and minArea <= p.area <= maxArea:
            polys.append(p)
        else:
            # TODO: Should attempt a circle fit
            cv2.minEnclosingCircle(c)



        # START OPTIONAL RENDER CODE
        b = random.randint(0, 255)
        g = random.randint(0, 255)
        r = random.randint(0, 255)

        rcolor = (b, g, r)

        cv2.drawContours(cImg, [c], -1, rcolor, thickness = 2)
        # END OPTIONAL RENDER CODE



    # START OPTIONAL CONTOUR IMAGE DISPLAY + WAIT CODE
    original_contours = cv2.cvtColor(srcImg, cv2.COLOR_GRAY2BGR)

    for i in range(0, len(contours)):
        b = random.randint(0, 255)
        g = random.randint(0, 255)
        r = random.randint(0, 255)

        rcolor = (b, g, r)
        cv2.drawContours(original_contours, contours, i, rcolor, thickness=1)

    cv2.imshow('Original contours', original_contours)
    cv2.imshow('All contours', cImg)
    cv2.waitKey(0)
    # END OPTIONAL CONTOUR DISPLAY + WAIT CODE


    return polys
