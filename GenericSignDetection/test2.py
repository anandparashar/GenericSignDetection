import numpy as np
import cv2
import preProcessing.preProcessor
import preProcessing.histogram
import polyDetect.getAllPoly as gp
import polyDetect.polyshape
import polyDetect.cycleDetection as cd


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
    #read image

    # img= cv2.imread("D:/Study/CS-682ComputerVision/LISATrafficSignDatabase/signDatabasePublicFramesOnly/aiua120306-1/"
    #                 "frameAnnotations-DataLog02142012_003_external_camera.avi_annotations/pedestrianCrossing_1333395860.avi_image17.png")
    # "frameAnnotations-DataLog02142012_003_external_camera.avi_annotations/curveRight_1333396823.avi_image4.png

    #img = cv2.imread("/home/joseph/cs682/final/Data/aiua120306-1/"
    # "frameAnnotations-DataLog02142012_003_external_camera.avi_annotations/curveRight_1333396823.avi_image4.png")

    #img = cv2.imread("/home/joseph/cs682/final/Data/vid8/"
    #                "frameAnnotations-MVI_0120.MOV_annotations/speedLimit_1324866418.avi_image7.png")

    # img = cv2.imread("/home/joseph/cs682/final/Data/aiua120306-1/"
    # "frameAnnotations-DataLog02142012_003_external_camera.avi_annotations/curveRight_1333395619.avi_image10.png")

    img = cv2.imread("/home/joseph/cs682/final/Data/aiua120306-1/"
    "frameAnnotations-DataLog02142012_003_external_camera.avi_annotations/dip_1333396129.avi_image7.png")

    trimmed = np.delete(img, range(img.shape[0] - 16, img.shape[0]), axis=0)

    if img.shape[2] == 3:
        gray = cv2.cvtColor(trimmed, cv2.COLOR_BGR2GRAY)
    else:
        gray = trimmed

    vmask = np.tile( [[0, 0], [1, 0]], (gray.shape[0]/2, gray.shape[1]/2))

    noise = np.ma.array(gray, mask=vmask)

    filterKern = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])*(1.0/8.0)

    mfiltered = cv2.filter2D(gray, 0, filterKern).astype(np.uint8)

    mmasked = np.ma.array(mfiltered, mask=np.logical_not(vmask))

    cleaned = mmasked.filled(0) + noise.filled(0)

    cv2.imshow('Cleaned', cleaned)
    cv2.waitKey(0)
    # cv2.imwrite('/home/joseph/cleaned.png', cleaned)

    fixed = cleaned
    # fixed = preProcessing.histogram.gammaCorrect(cleaned)
    fixedequal = cv2.equalizeHist(fixed)

    fixedFull = cv2.cvtColor(fixed, cv2.COLOR_GRAY2BGR)
    displayResized("fixed full", fixedFull)
    # cv2.waitKey(0)

    threshold = preProcessing.histogram.estimateThreshold(fixedFull)

    processed, p2, lines = preProcessing.preProcessor.process(image=fixedFull, canny_param1=threshold / 2,
                                       canny_param2=threshold,
                                       harriscorner_blockSize=2,
                                       harriscorner_kSize=3,
                                       harriscorner_freeparam=0.4,
                                       smallsegmentremoval_ratio=0.02,
                                       hough_threshold=25,
                                       hough_minLen=15,
                                       hough_maxGap=7
                                       )

    lineImg = np.copy(fixedFull)
    for (p1, p2) in lines:
        cv2.line(lineImg, p1, p2, color=(0, 0, 255), thickness=1)

    cv2.imshow('Lines', lineImg)
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
    # shapes = cd.determineCycles(lines, 4)

    # thinner = skeletonize(processed)
    # sdImage = np.ones( (processed.shape[0] + 2, processed.shape[1] + 2), dtype=np.uint8 )
    # sdImage[1:processed.shape[0] + 1, 1:processed.shape[1] + 1] = processed
    shapes = gp.getAllPoly(processed, 100, 12000)

    imshape = img.shape

    outImg = np.copy(fixedFull)

    cv2.imshow('Final', processed)

    for s in shapes:
        s.drawBoundingRect(outImg, (0, 255, 0))
        if s.isGoodSignCandidate(12):
            color = (0, 0, 255)
            s.drawContour(outImg, color)

    cv2.imshow('Shapes', outImg)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


main()