import numpy as np
import cv2
import math


'''
    Calls individual modules inside pre-processing stage and returns the final processed Image
    Modules called are,
    1. Canny Edge Detection
    2. Corner Detection using Harris Corner Detector
    3. Small Segment removal using Contours

    parameters:
    image                       = candidate image for sign board detection
    canny_param1                = Canny Edge Dectector Threshold 1
    canny_param2                = Canny Edge Dectector Threshold 2
    harriscorner_blockSize      = Neighbourhood size for Harris Corner Detector
    harriscorner_kSize          = k size for Sobel filter
    harriscorner_freeparam      = Harris detector free parameter
    smallsegmentremoval_ratio   = ratio of (length of smallest segment included/length of longest segment in image)
    hough_threshold   = threshold for Probabilistic Hough Transform
    hough_minLen = minimum length of line segment to be detetected
    hough_maxGap = maximum gap between two line segments to join them as a continuous line segment

    output:
    processed image ready for hough transform and line verification
'''
def process(image, canny_param1, canny_param2, harriscorner_blockSize , harriscorner_kSize, harriscorner_freeparam,
            smallsegmentremoval_ratio, hough_threshold, hough_minLen, hough_maxGap):

    bImage = image
    bImage = cv2.GaussianBlur(image, (3, 3), 1.25)

    edgeImg = cannyEdgeDetection(bImage, canny_param1, canny_param2)

    #displayResized("edge image", edgeImg)

    #Morphological

    kernel = np.ones((2, 2), np.uint8)
    edgeImgProcessed = cv2.morphologyEx(edgeImg, cv2.MORPH_CLOSE, kernel)
    #displayResized("after morphological transform 1", edgeImgProcessed)

    preRemove = np.copy(edgeImgProcessed)

    # Call to corner detector
    edgeImgProcessed = cornerDetector(edgeImgProcessed, harriscorner_blockSize, harriscorner_kSize, harriscorner_freeparam)
    # displayResized("Corners detected!", edgeImgProcessed)

    # Small segment Removal
    processedImage = edgeImgProcessed
    processedImage = smallSegmentRemovalContours(edgeImgProcessed, preRemove, smallsegmentremoval_ratio)

    #displayResized("after contour removal", processedImage)

    
    kernel = np.ones((2, 2), np.uint8)
    processedImage = dilation = cv2.dilate(processedImage, kernel, iterations=1)
    # kernel = np.ones((3, 3), np.uint8)

    processedImage = cv2.morphologyEx(processedImage, cv2.MORPH_CLOSE, kernel)
    # kernel = np.ones((3, 3), np.uint8)
    processedImage = cv2.erode(processedImage, kernel, iterations=1)
    #displayResized("after Morphological Transform 2", processedImage)

    # processedImage = skeltonize(processedImage)
    # displayResized("after skeltonization", processedImage)

    houghLines = lineDetectionProbHough(processedImage, hough_threshold, hough_minLen, hough_maxGap)
    # houghLines = lineDetectionStandardHough(processedImage)

    cv2.waitKey(0)
    return processedImage, processedImage, houghLines


def skeltonize(img):
    size = np.size(img)
    skel = np.zeros(img.shape, np.uint8)

    ret, img = cv2.threshold(img, 127, 255, 0)
    element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    done = False

    while (not done):
        eroded = cv2.erode(img, element)
        temp = cv2.dilate(eroded, element)
        temp = cv2.subtract(img, temp)
        skel = cv2.bitwise_or(skel, temp)
        img = eroded.copy()

        zeros = size - cv2.countNonZero(img)
        if zeros == size:
            done = True

    #cv2.imshow("skel", skel)
    return skel


'''
    Helper function to display re-sized image while maintaining aspect ratio
'''
def displayResized(message, imageDisp):
    print ("Displaying "+message)
    height = imageDisp.shape[0]
    width = imageDisp.shape[1]
    if width>800 or height >600:
        aspectratio = float(width) / float(height)
        width = 800
        height = width / aspectratio
    #cv2.imshow(message, cv2.resize(imageDisp, (width, int(height))))


'''
    Function to perform Canny-edge detection
    This is the first step of the pre-processing phase,
     parameters:
     image = image to be processed
     param1 = Canny Edge Dectector Threshold 1
     param2 = Canny Edge Dectector Threshold 2

     output:
     image with edges detected
'''
def cannyEdgeDetection(image, param1, param2):
    #perform canny edge detection
    #Generally, param2=param1*3
    img_canny = cv2.Canny(image, param1, param2)
    return img_canny


'''
    Function to perform Harris Corner Detection

    parameters:
    edgeImg = image to be processed
    blockSize      = Neighbourhood size for Harris Corner Detector
    kSize          = k size for Sobel filter
    freeParam      = Harris detector free parameter

    output:
    image with corners detected for small segment removal
'''
def cornerDetector(edgeImg, blockSize, kSize, freeParam):
    # edgeImg = np.float32(edgeImg)
    # dst = cv2.cornerHarris(edgeImg, 2, 3, 0.4)
    dst = cv2.cornerHarris(edgeImg, blockSize, kSize, freeParam)
    # dst_norm = dst
    # dst_norm = cv2.normalize(dst, dst_norm, 0, 255, cv2.NORM_MINMAX, cv2.CV_32FC1)
    # dst_abs = cv2.convertScaleAbs(dst_norm)

    # Threshold for an optimal value
    edgeImg[dst > 0.97 * dst.max()] = [0]
    return edgeImg


'''
    Function to perform Contour detection and removal for small segments in the image

    parameters:
    image   = image to be processed
    ratio   = ratio of (length of smallest segment included/length of longest segment in image)

    output:
    image with small segments removed
'''
def smallSegmentRemovalContours(image, preCornerImage,  ratio):
    image, contours, heirarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    maxLen=0
    for contour in contours:
        arcLength = cv2.arcLength(contour, False)
        if arcLength >= maxLen:
            maxLen = arcLength
    # print maxLen* ratio
    for i in range(len(contours)):
        if cv2.arcLength(contours[i], False) < maxLen * ratio:
            preCornerImage = cv2.drawContours(preCornerImage, contours, i, color=(0,0,0))

    for i in range(len(contours)):
        if cv2.arcLength(contours[i], False) >= maxLen * ratio:
            cv2.drawContours(preCornerImage, contours, i, color=(255, 255, 255))
    # displayResized("after contour removal", image)
    return preCornerImage

def StandardHoughTransform(image, rho, theta, threshold, srn, stn):
    #perfrom Standard Hough transform
    lines = cv2.HoughLines(image, rho, theta, threshold, srn=srn, stn=stn)
    return lines

def ProbabilisticHoughTransform(image, rho, theta, threshold, minLength, maxGap):
    #perfrom Probabilistic Hough transform
    lines = cv2.HoughLinesP(image, rho, theta, threshold, minLineLength=minLength, maxLineGap=maxGap)
    return lines

'''
    Function to perform Contour detection and removal for small segments in the image

    TODO - CHange to Gradient Hough Transform if required

    parameters:
    image   = image to be processed
    threshold   = threshold for Probabilistic Hough Transform
    minLen = minimum length of line segment to be detetected
    maxGap = maximum gap between two line segments to join them as a continuous line segment

    output:
    lines detected
'''
def lineDetectionProbHough(image, threshold, minLen, maxGap):
    houghLines = []
    #Probabilistic Hough Transform
    lines = ProbabilisticHoughTransform(image, rho=1, theta=np.pi/360, threshold=threshold, minLength=minLen, maxGap=maxGap)
    # print (len(lines))
    for points in lines:
        # print (points)
        for x1, y1, x2, y2 in points:
            # cv2.line(img=image, pt1=(x1, y1), pt2=(x2, y2),color=(125, 125,125), thickness=2)
            houghLines.append(((x1, y1), (x2, y2)))
    # displayResized("Hough Lines Probabilistic", image)
    return houghLines

def lineDetectionStandardHough(image):
    # Standard Hough Transform
    houghLines=[]
    lines = StandardHoughTransform(image, rho=1, theta=np.pi/180, threshold=150, srn=0, stn=0)
    for points in lines:
        for rho, theta in points:
            a=np.cos(theta)
            b=np.sin(theta)
            x0=a*rho
            y0=b*rho
            x1 = int(np.around(x0 + 1000 * (-b)))
            y1 = int(np.around(y0 + 1000 * (a)))
            x2 = int(np.around(x0 - 1000 * (-b)))
            y2 = int(np.around(y0 - 1000 * (a)))
            cv2.line(img=image, pt1=(x1, y1), pt2=(x2, y2),color=(255, 255, 255), thickness=1)
            houghLines.append(((x1,y1), (x2,y2)))
    displayResized("Hough Lines Standard", image)
    return houghLines





