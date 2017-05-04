#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Observer
#
# Created:     25/04/2017
# Copyright:   (c) Observer 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import math
import numpy as np
import cv2
from matplotlib import pyplot as plt

'''  Estimates edge threshold from image gradient

    img - Source image
    returns: Scalar threshold value

'''
def estimateThreshold(img):
    # Blur image and calculate Sobel gradient magnitude
    blurred = cv2.GaussianBlur(img, (3, 3), 1.5)
    grad_x = cv2.Sobel(blurred, cv2.CV_32F, 1, 0)
    grad_y = cv2.Sobel(blurred, cv2.CV_32F, 0, 1)
    grad = abs(grad_x) + abs(grad_y)

    # Flatten and sort array
    gsorted = grad.flatten()
    gsorted.sort()

    # Threshold value will leave the upper 8% of edge pixels intact
    threshold =  gsorted[ int(gsorted.size*0.96)]
    return threshold

''' Calculates a 32 bin histogram from a grayscale image 
    
    img - Source image
    
    returns: Array representing histogram
'''

def getGrayscaleHistogram(img):
    hist = cv2.calcHist([img], [0], None, [32], [0, 256] )
    return hist

''' Attempts to automatically correct gamma for a source image

    img - Source image
    returns: Gamma corrected image
'''
def gammaCorrect(img):
    hist = getGrayscaleHistogram(img)

    # Get the maximum value index
    p1 = np.argmax(hist)

    # Get two sequences to find the next highest peak
    seq1 = hist[0:p1-6]
    seq2 = hist[p1+6:]

    # Check for empty sequences due to the the highest peak being too close to a luminance boundary
    if len(seq1) > 0:
        c1 = np.argmax(seq1)
    else:
        c1 = -1

    if len(seq2) > 0:
        c2 = np.argmax(seq2) + p1+6
    else:
        c2 = -1

    if c2 == c1:
        return img
    elif c1 == -1:
        p2 = c2
        step = 1
    elif c2 == -1:
        p2 = c1
        step = -1
    elif hist[c2] >= hist[c1]:
        p2 = c2
        step = 1
    else:
        p2 = c1
        step = -1

    diff = p1 - p2

    # Calculate the valley
    v = np.argmin(hist[p1:p2:step])

    print p1, p2

    # Make sure the next highest peak is significant enough to care about
    if hist[p1]/hist[p2] < 4:
        # Gamma correct and merge

        s1 = sum(hist[0:v])
        s2 = sum(hist[v+1:])

        masked1 = np.copy(img)
        masked2 = np.copy(img)

        masked1 = np.ma.masked_less_equal(masked1, v*8)
        masked2 = np.ma.masked_greater(masked2, v*8)


        mean1 = masked1.mean()
        mean2 = masked2.mean()

        ratio1 = mean1/(v*8)
        ratio2 = mean2/(v*8)

        l1 = math.log(ratio1, 2)
        l2 = math.log(ratio2, 2)

        gamma1 = 1.0/l1
        gamma2 = 0.5 - l2

        gamma = (gamma2 if (255.0 - mean2) < mean1 else gamma2)

        print gamma
        print gamma1, gamma2

        simple = (img*(1.0/255.0)) ** (1.0/gamma)
        simple = (simple*255).astype(np.uint8)


        return simple
    else:
        return img



