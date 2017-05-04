import numpy as np
import cv2
import preProcessing.preProcessor
import preProcessing.histogram
import polyDetect.getAllPoly as gp
import polyDetect.polyshape


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

    img = cv2.imread("D:/Study/CS-682ComputerVision/LISATrafficSignDatabase/signDatabasePublicFramesOnly/vid8/"
                     "frameAnnotations-MVI_0120.MOV_annotations/speedLimit_1324866418.avi_image7.png")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

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

    processed, lines = preProcessing.preProcessor.process(image=fixedFull, canny_param1=threshold / 2,
                                       canny_param2=threshold,
                                       harriscorner_blockSize=2,
                                       harriscorner_kSize=3,
                                       harriscorner_freeparam=0.4,
                                       smallsegmentremoval_ratio=0.02,
                                       hough_threshold=15,
                                       hough_minLen=7,
                                       hough_maxGap=7
                                       )

    bigKern = np.ones( (2,2), dtype=np.uint8)

    bigger = cv2.dilate(processed, bigKern)



    shapes = gp.getAllPoly(bigger, 100, 1000)

    imshape = img.shape

    outImg = np.copy(fixedFull)

    cv2.imshow('Final', processed)

    for s in shapes:
        s.drawBoundingRect(outImg, (0, 255, 0))
        s.drawContour(outImg, (255, 0, 0))

    cv2.imshow('Shapes', outImg)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


main()