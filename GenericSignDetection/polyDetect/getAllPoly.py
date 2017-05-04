import cv2
import numpy as np
from polyshape import polyshape
import random
import math

def getAllPoly(srcImg, minArea, maxArea):
    im2, contours, heirarchy = cv2.findContours(srcImg, mode = cv2.RETR_TREE, method = cv2.CHAIN_APPROX_TC89_KCOS)

    cImg = cv2.cvtColor(srcImg, cv2.COLOR_GRAY2BGR)

    polys = []

    threshold = 7

    newshapes = []

    for c in contours:

        if len(c) > 3:
            c = cv2.approxPolyDP(c, 7, closed=True)
            area = cv2.contourArea(c)
        if minArea <= area <= maxArea:
            for i in range(0, len(c)):
                for j in range(i + 1, len(c)):
                    v1 = np.array(c[i][0], dtype=np.float32)
                    v2 = np.array(c[j][0], dtype=np.float32)

                    v3 = v1 - v2

                    dist = math.sqrt(np.dot(v3, v3))

                    if dist <= threshold or dist >= 10:
                        newshapes.append(c[i:j])
                        if i > 1:
                            newshapes.append(c[0:i])
                        if len(c) - j > 1:
                            newCurve = list(c[j:]) + list(c[0:i])
                            newshapes.append( np.asarray(newCurve, dtype=np.int32))



    contours.extend(newshapes)

    for c in contours:

        b = random.randint(0, 255)
        g = random.randint(0, 255)
        r = random.randint(0, 255)

        rcolor = (b, g, r)

        approx = cv2.approxPolyDP(c, 7, closed=True)

        # approx = cv2.convexHull(approx)
        area = cv2.contourArea(approx)

        cv2.drawContours(cImg, [approx], -1, rcolor, thickness = 2)

        '''
        if area > 50:
            oneImg = cv2.cvtColor(srcImg, cv2.COLOR_GRAY2BGR)

            cv2.drawContours(oneImg, [approx], -1, rcolor, thickness = 1)

            cv2.imshow('Current contour', oneImg)
            cv2.waitKey()
        '''

        p = polyshape(approx)
        if p.sides <= 8 and p.area <= maxArea and p.area >= minArea:
            print p.sides
            polys.append(p)
        else:
            # TODO: Should attempt a circle fit
            pass

    cv2.imshow('All contours', cImg)
    cv2.waitKey(0)

    return polys
