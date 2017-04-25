import numpy as np
import cv2

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

    output:
    processed image ready for hough transform and line verification
'''
def process(image, canny_param1, canny_param2, harriscorner_blockSize , harriscorner_kSize, harriscorner_freeparam, smallsegmentremoval_ratio):
    edgeImg = cannyEdgeDetection(image, canny_param1, canny_param2)
    displayResized("edge image", edgeImg)

    # Call to corner detector
    edgeImgProcessed = edgeImg
    edgeImgProcessed = cornerDetector(edgeImg, harriscorner_blockSize, harriscorner_kSize, harriscorner_freeparam)
    displayResized("Corners detected!", edgeImgProcessed)

    # Small segment Removal
    processedImage = smallSegmentRemovalContours(edgeImgProcessed, smallsegmentremoval_ratio)
    displayResized("after contour removal", processedImage)
    cv2.waitKey(0)
    return processedImage

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
    cv2.imshow(message, cv2.resize(imageDisp, (width, int(height))))


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
def smallSegmentRemovalContours(image, ratio):
    image, contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    maxLen=0
    for contour in contours:
        arcLength = cv2.arcLength(contour, False)
        if arcLength >= maxLen:
            maxLen = arcLength
    # print maxLen* ratio
    for i in range(len(contours)):
        if cv2.arcLength(contours[i], False) < maxLen * ratio:
            image = cv2.drawContours(image, contours, i, color=(0,0,0))
    # displayResized("after contour removal", image)
    return image


