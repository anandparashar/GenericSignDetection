import numpy as np
import cv2
import preProcessing.preProcessor as pp
import preProcessing.histogram as hist
import polyDetect.getAllPoly as gp
import preProcessing.InterlacingRemoval as ilr
import polyDetect.polyshape
import polyDetect.cycleDetection as cd
from datetime import datetime
import ntpath
import math


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

def colorEdgeDetect(img, cthresh1, cthresh2):

    grads = []
    edges = []
    y, u, v = cv2.split(cv2.cvtColor(img, cv2.COLOR_BGR2YUV))

    uv_mag, uv_angles = cv2.cartToPolar(u.astype(np.float32), v.astype(np.float32), angleInDegrees=True)

    edge_channels = [y, uv_angles]

    yf = y.astype(np.float32)

    sig = (uv_angles%90 - 45)

    sig = np.abs(sig) - 15
    sig /= sig.max()
    sig *= 255

    # sig_gaussian = cv2.GaussianBlur(sig, (3, 3), 1.25)
    ang_gaussian = cv2.GaussianBlur(uv_angles, (3, 3), 1.25)

    sig_gaussian = sig

    ang_gx = cv2.Sobel(ang_gaussian, cv2.CV_32F, 1, 0)
    ang_gy = cv2.Sobel(ang_gaussian, cv2.CV_32F, 0, 1)

    sig_gx = cv2.Sobel(sig_gaussian, cv2.CV_32F, 1, 0)
    sig_gy = cv2.Sobel(sig_gaussian, cv2.CV_32F, 0, 1)

    ang_mag = cv2.magnitude(ang_gx, ang_gy)
    sig_mag = cv2.magnitude(sig_gx, sig_gy)

    ang_mag /= ang_mag.max()

    sig_mag /= sig_mag.max()

    combined = np.round(ang_mag * sig_mag * 255)

    sorted = np.sort(combined.copy().flatten())

    threshold = sorted[ int(sorted.size*0.99) ]

    edge_guess = cv2.Canny(combined.astype(np.uint8), threshold, threshold/3)
    edge_guess = cv2.morphologyEx(edge_guess, cv2.MORPH_CLOSE, np.ones((2, 2)))

    cv2.imshow('Edges from color', edge_guess)

    e2 = pp.skeltonize(edge_guess)
    e2gray = e2
    normCanny = cv2.Canny(img, cthresh1, cthresh2)

    edgeImg = cv2.bitwise_or( normCanny, e2gray )

    cv2.imshow('CE rough edges', edgeImg)




    cv2.imshow('Significant matrix', combined.astype(np.uint8)*8)
    cv2.waitKey(0)


    return edgeImg





def main():

    print cv2.__version__
    #read image
    # imageFileName = "C:/Code/cs682/final/Data/vid8/frameAnnotations-MVI_0120.MOV_annotations/speedLimit_1324866418.avi_image7.png"
    # imageFileName = "C:/Code/cs682/final/Data/aiua120306-1/frameAnnotations-DataLog02142012_003_external_camera.avi_annotations/curveRight_1333396823.avi_image4.png"
    # imageFileName = "C:/Code/cs682/final/Data/aiua120306-1/frameAnnotations-DataLog02142012_003_external_camera.avi_annotations/curveRight_1333395619.avi_image10.png"
    # imageFileName = "C:/Code/cs682/final/Data/aiua120306-1/frameAnnotations-DataLog02142012_003_external_camera.avi_annotations/pedestrianCrossing_1333395580.avi_image17.png"
    # imageFileName = "C:/Code/cs682/final/Data/aiua120306-1/frameAnnotations-DataLog02142012_003_external_camera.avi_annotations/dip_1333396129.avi_image7.png"
    # imageFileName = "C:/Code/cs682/final/Data/aiua120214-2/frameAnnotations-DataLog02142012_002_external_camera.avi_annotations/curveRight_1331866657.avi_image18.png"
    # imageFileName = "C:/Code/cs682/final/Data/aiua120214-2/frameAnnotations-DataLog02142012_002_external_camera.avi_annotations/laneEnds_1331866559.avi_image7.png"
    # imageFileName = "C:/Code/cs682/final/Data/aiua120214-2/frameAnnotations-DataLog02142012_002_external_camera.avi_annotations/merge_1331866392.avi_image6.png"
    # imageFileName = "C:/Code/cs682/final/Data/aiua120214-2/frameAnnotations-DataLog02142012_002_external_camera.avi_annotations/merge_1331866676.avi_image10.png"
    # imageFileName = "C:/Code/cs682/final/Data/aiua120214-2/frameAnnotations-DataLog02142012_002_external_camera.avi_annotations/merge_1331866749.avi_image1.png"

    # imageFileName = "C:/Code/cs682/final/Data/vid9/frameAnnotations-MVI_0121.MOV_annotations/speedLimit_1324866741.avi_image5.png"
    # imageFileName = "C:/Code/cs682/final/Data/vid8/frameAnnotations-MVI_0120.MOV_annotations/keepRight_1324866323.avi_image1.png"
    # imageFileName = "C:/Code/cs682/final/Data/vid9/frameAnnotations-MVI_0121.MOV_annotations/pedestrianCrossing_1324866507.avi_image0.png"
    # imageFileName = "C:/Code/cs682/final/Data/vid9/frameAnnotations-MVI_0121.MOV_annotations/speedLimit_1324866786.avi_image4.png"
    # imageFileName = "C:/Code/cs682/final/Data/vid9/frameAnnotations-MVI_0121.MOV_annotations/speedLimit_1324866741.avi_image3.png"
    # imageFileName = "C:/Code/cs682/final/Data/vid8/frameAnnotations-MVI_0120.MOV_annotations/keepRight_1324866323.avi_image5.png"
    # imageFileName = "C:/Code/cs682/final/Data/vid8/frameAnnotations-MVI_0120.MOV_annotations/pedestrianCrossing_1324866135.avi_image5.png"
    imageFileName = "C:/Code/cs682/final/Data/vid8/frameAnnotations-MVI_0120.MOV_annotations/speedLimit_1324866175.avi_image4.png"
    # imageFileName = "C:/Code/cs682/final/Data/vid10/frameAnnotations-MVI_0122.MOV_annotations/signalAhead_1324866992.avi_image17.png"
    # imageFileName = "C:/Code/cs682/final/Data/vid11/frameAnnotations-MVI_0123.MOV_annotations/pedestrianCrossing_1324867104.avi_image2.png"
    # imageFileName = "C:/Code/cs682/final/Data/vid11/frameAnnotations-MVI_0123.MOV_annotations/signalAhead_1324867127.avi_image15.png"
    # imageFileName = "C:/Code/cs682/final/Data/vid11/frameAnnotations-MVI_0123.MOV_annotations/speedLimit_1324867178.avi_image5.png"
    # imageFileName = "C:/Code/cs682/final/Data/vid9/frameAnnotations-MVI_0121.MOV_annotations/pedestrianCrossing_1324866507.avi_image7.png"

    img = cv2.imread(imageFileName)


    #img = cv2.imread()

    # img = cv2.imread()
    cv2.imshow('Original', img)

    # Screen for images that need additional cleanup and apply it if necessary
    needsCleanup = "aiua12" in imageFileName

    if needsCleanup:

        # Get rid of the non-image junk at the bottom of the aiua* direct images
        trimmed = np.delete(img, range(img.shape[0] - 16, img.shape[0]), axis=0)
        # Remove screen effect
        cleaned = ilr.clean(trimmed)

        fixedFull = cv2.cvtColor(cleaned, cv2.COLOR_GRAY2BGR)
        # Fix contrast if necessary
        fixedFull = hist.contrastCorrect(fixedFull, 151, 1, 0.8, 0.25)
    else:
        fixedFull = hist.contrastCorrect(img, 151, 3, 0.8, 0.25)

    # Estimate a threshold value for the edge detector
    threshold = hist.estimateThreshold(fixedFull)

    # Run the rest of the preprocessing
    processed, p2, lines = pp.process(image=fixedFull, canny_param1=threshold /3,
                                       canny_param2=threshold,
                                       harriscorner_blockSize=2,
                                       harriscorner_kSize=3,
                                       harriscorner_freeparam=0.4,
                                       smallsegmentremoval_ratio=0.015,
                                       hough_threshold=25,
                                       hough_minLen=15,
                                       hough_maxGap=7
                                       )


    # Stuff for processing time management
    polystart = datetime.now()

    # Workhorse function for polygon detection
    shapes = gp.getAllPoly(processed, 169, 12000, 7, 15, 5)

    imshape = img.shape

    outImg = np.copy(fixedFull)

    # Filter for regular shapes
    goodShapes = [s for s in shapes if s.isGoodSignCandidate(12)]

    print 'Found ' + str(len(goodShapes)) + ' candidate shapes'

    bestMask = [True for i in range(0, len(goodShapes)) ]

    # Eliminate overlapping shapes
    for i in range(0, len(goodShapes)):
        for j in range(i+1, len(goodShapes)):
            goodShapes[i].drawBoundingRect(outImg, (0, 255, 0))
            if goodShapes[i].boundingIoU(goodShapes[j]) > 0.5:
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
        bs.drawBoundingRect(outImg, (0, 255, 0) )

    print "Found " + str( len(bestShapes) ) + " potential signs in " + str((polyend - polystart).microseconds/1000) + 'ms'

    cv2.imshow('Shapes', outImg)
    cv2.waitKey(0)

    writeShapePredictionsToFile(imageFileName, bestShapes)
    cv2.destroyAllWindows()


def writeShapePredictionsToFile(imageFileName, bestShapes):
    imageFileNameOnly = path_leaf(imageFileName)

    with open("predictions.txt", "w") as text_file:
        for shape in bestShapes:
            text_file.write('{0};{1};{2};{3};{4}\n'.format(imageFileNameOnly, shape.bx, shape.by, shape.bx + shape.bwidth, shape.by + shape.bheight))

    # for shape in bestShapes:
    #     # print '{0} {1}; width = {2}, height = {3}'.format(shape.bx, shape.by, shape.bwidth, shape.bheight)
    #     print '{0};{1};{2};{3};{4}'.format(imageFileNameOnly, shape.bx, shape.by, shape.bx + shape.bwidth, shape.by + shape.bheight)

#  see http://stackoverflow.com/questions/8384737/extract-file-name-from-path-no-matter-what-the-os-path-format
def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


main()