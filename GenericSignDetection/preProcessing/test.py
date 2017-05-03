import numpy as np
import cv2
import preProcessor
import InterlacingRemoval as ilr
import histogram as hist

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
    img= cv2.imread("D:/Study/CS-682ComputerVision/LISATrafficSignDatabase/signDatabasePublicFramesOnly/aiua120306-1/"
                     "frameAnnotations-DataLog02142012_003_external_camera.avi_annotations/curveRight_1333396823.avi_image4.png")

    cleaned = ilr.clean(img)

    fixed = hist.gammaCorrect(cleaned)
    fixedequal = cv2.equalizeHist(fixed)

    fixedFull = cv2.cvtColor(fixed, cv2.COLOR_GRAY2BGR)

    threshold = hist.estimateThreshold(fixedFull)

    processed, lines = preProcessor.process(image=img, canny_param1= threshold/2,
                         canny_param2=threshold,
                         harriscorner_blockSize=2,
                         harriscorner_kSize=3,
                         harriscorner_freeparam=0.4,
                         smallsegmentremoval_ratio=0.04,
                         hough_threshold=10,
                         hough_minLen=7,
                         hough_maxGap=2
                         )
    return processed, lines


main()