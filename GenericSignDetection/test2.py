import numpy as np
import cv2
import preProcessing.preProcessor as pp
import preProcessing.histogram as hist
import polyDetect.getAllPoly as gp
import preProcessing.InterlacingRemoval as ilr
import polyDetect.polyshape
import polyDetect.cycleDetection as cd
from datetime import datetime


#Function to display re-sized image
def displayResized(message, imageDisp):
    print ("Displaying "+message)
    height = imageDisp.shape[0]
    width = imageDisp.shape[1]
    if width>800 or height >600:
        aspectratio = float(width) / float(height)
        width = 800
        height = width / aspectratio
    cv2.imshow(message, cv2.resize(imageDisp, (width, int(height))))


def main():

    print cv2.__version__
    #read image

    # img= cv2.imread("D:/Study/CS-682ComputerVision/LISATrafficSignDatabase/signDatabasePublicFramesOnly/aiua120306-1/"
    #                 "frameAnnotations-DataLog02142012_003_external_camera.avi_annotations/pedestrianCrossing_1333395860.avi_image17.png")
    # "frameAnnotations-DataLog02142012_003_external_camera.avi_annotations/curveRight_1333396823.avi_image4.png

    img = cv2.imread("C:/Code/cs682/final/Data/aiua120306-1/"
    "frameAnnotations-DataLog02142012_003_external_camera.avi_annotations/curveRight_1333396823.avi_image4.png")

    # img = cv2.imread("C:/Code/cs682/final/Data/vid8/"
    #                 "frameAnnotations-MVI_0120.MOV_annotations/speedLimit_1324866418.avi_image7.png")

    #img = cv2.imread("C:/Code/cs682/final/Data/aiua120306-1/"
    # "frameAnnotations-DataLog02142012_003_external_camera.avi_annotations/curveRight_1333395619.avi_image10.png")

    #img = cv2.imread("C:/Code/cs682/final/Data/aiua120306-1/"
    # "frameAnnotations-DataLog02142012_003_external_camera.avi_annotations/dip_1333396129.avi_image7.png")

    # img = cv2.imread("C:/Code/cs682/final/Data/vid9/frameAnnotations-MVI_0121.MOV_annotations/speedLimit_1324866741.avi_image5.png")

    # Get rid of the non-image junk at the bottom of the aiua* direct images
    trimmed = np.delete(img, range(img.shape[0] - 16, img.shape[0]), axis=0)

    # Convert to grayscale if the image is in color
    if img.shape[2] == 3:
        gray = cv2.cvtColor(trimmed, cv2.COLOR_BGR2GRAY)
    else:
        gray = trimmed

    # Clean interlacing, only necessary in the aiua* data folders
    cleaned = ilr.clean(trimmed)

    cv2.imshow('Cleaned', cleaned)
    cv2.waitKey(0)
    # cv2.imwrite('/home/joseph/cleaned.png', cleaned)

    fixed = cleaned
    # fixed = hist.gammaCorrect(cleaned)


    # Back to full color
    fixedFull = cv2.cvtColor(fixed, cv2.COLOR_GRAY2BGR)
    displayResized("fixed full", fixedFull)
    # cv2.waitKey(0)

    # Estimate a threshold value for the edge detector
    threshold = hist.estimateThreshold(fixedFull)

    processed, p2, lines = pp.process(image=fixedFull, canny_param1=threshold /2,
                                       canny_param2=threshold,
                                       harriscorner_blockSize=2,
                                       harriscorner_kSize=3,
                                       harriscorner_freeparam=0.4,
                                       smallsegmentremoval_ratio=0.02,
                                       hough_threshold=25,
                                       hough_minLen=15,
                                       hough_maxGap=7
                                       )

    '''
    lineImg = np.copy(fixedFull)
    for (p1, p2) in lines:
        cv2.line(lineImg, p1, p2, color=(0, 0, 255), thickness=1)
    cv2.imshow('Lines', lineImg)
    '''

    cv2.imshow('Final', processed)

    cv2.waitKey(0)

    '''
    bigKern = np.ones( (2,2), dtype=np.uint8)

    bigger = cv2.dilate(processed, bigKern)

    lineImg = np.copy(fixedFull)

    for (p1, p2) in lines:
        cv2.line(lineImg, p1, p2, (0, 0, 255), thickness=1)

    cv2.imshow('Processed', processed)
    cv2.imshow('Lines', lineImg)
    cv2.waitKey(0)

    '''

    # Stuff for processing time management
    polystart = datetime.now()

    # Workhorse function for polygon detection
    shapes = gp.getAllPoly(processed, 169, 12000, 5, 8, 4)

    imshape = img.shape

    outImg = np.copy(fixedFull)

    # Filter for regular shapes
    goodShapes = [s for s in shapes if s.isGoodSignCandidate(12)]

    bestMask = [True for i in range(0, len(goodShapes)) ]

    # Eliminate overlapping shapes
    for i in range(0, len(goodShapes)):
        for j in range(i+1, len(goodShapes)):
            if goodShapes[i].overlaps(goodShapes[j]):
                if goodShapes[i].area > goodShapes[j].area:
                    bestMask[j] = False
                else:
                    bestMask[i] = False

    bestShapes = [s for (s, j) in zip(goodShapes, bestMask) if j == True]

    polyend = datetime.now()

    # Display results
    for bs in bestShapes:
        color = (0, 0, 255)
        bs.drawContour(outImg, color)

    print "Found " + str( len(bestShapes) ) + " potential signs in " + str((polyend - polystart).microseconds/1000) + 'ms'

    cv2.imshow('Shapes', outImg)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


main()