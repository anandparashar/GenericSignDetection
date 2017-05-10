'''
Created on Apr 23, 2017

@author: Erich O'Saben
'''

"""
Main entry point to the Generic Sign Detection
"""

'''
Created on May 7, 2017

@author: Erich O'Saben
'''

import evaluate as eval
import utils as u

import os 
import sys
import numpy as np

import cv2
import preProcessing.preProcessor as pp
import preProcessing.histogram as hist
import polyDetect.getAllPoly as gp
import preProcessing.InterlacingRemoval as ilr
import polyDetect.histogramMatching as hm
from datetime import datetime


def writeShapePredictionsToFile(out_file_name, bestShapes):
    #imageFileNameOnly = path_leaf(imageFileName)

    with open(out_file_name, "w") as text_file:
        for line in bestShapes:
            #print line
            img_file = line[0]
            shapes = line[1]
            type = line[2]
            
            if type == "no_shape":
                text_file.write('{0};{1};{2};{3};{4}\n'.format(img_file, 0,0,0,0))
            else:
                #print shapes
                for shape in shapes:
                    text_file.write('{0};{1};{2};{3};{4}\n'.format(img_file, shape.bx, shape.by, shape.bx + shape.bwidth, shape.by + shape.bheight))
                        
            
    
def main(version, is_gray_only):
    
    
    groundTruth_file_name = os.path.join("test_data", "testGroundTruthFileNames{}.txt".format(version))
    
    img_files = [x.strip() for x in open(groundTruth_file_name,'r').readlines()]
        
    out_file_name = "predictions{}.txt".format(version)
    
    print "Generating Predictions from images in file: ", groundTruth_file_name
    print "Writing Predictions to: ", out_file_name
    
    if is_gray_only:
        print "Generating Predictions based only on gray scaled images"
    
    
    
    
    predictions = []
    

    for i, img_file in enumerate(img_files):
        if i % 50 == 0:
            print i, "images have been processed", len(img_files), "total"
        
        
        #ann_fields = img_file.split(";")

        file_name = img_file#ann_fields[0]
        #print "working on {}".format(file_name)
        
        
        
        
        img = cv2.imread(os.path.join(u.DATA_ROOT_PATH,file_name))
        
        #if is_gray_only, convert to the negative image to a 3 channel gray scale
        if is_gray_only and "negative" in file_name:
            #cv2.imshow('orig', img)
            img = cv2.cvtColor( img, cv2.COLOR_RGB2GRAY )
            img = cv2.cvtColor( img, cv2.COLOR_GRAY2RGB )
            #print img.shape
            #cv2.imshow('gray', img)
            #cv2.waitKey(0)
            
        
        
        # Screen for images that need additional cleanup and apply it if necessary
        needsCleanup = "aiua12" in file_name

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
        processed, p2, lines = pp.process(image=fixedFull, canny_param1=threshold / 2,
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
        shapes = gp.getAllPoly(processed, 169, 12000, 5, 8, 4)

        imshape = img.shape

        outImg = np.copy(fixedFull)

        # Filter for regular shapes
        goodShapes = [s for s in shapes if s.isGoodSignCandidate(12)]

        #print 'Found ' + str(len(goodShapes)) + ' candidate shapes'

        bestMask = [True for i in range(0, len(goodShapes))]

        # Eliminate overlapping shapes
        for i in range(0, len(goodShapes)):
            for j in range(i + 1, len(goodShapes)):
                goodShapes[i].drawBoundingRect(outImg, (0, 255, 0))
                if goodShapes[i].boundingIoU(goodShapes[j]) > 0.5:
                    if goodShapes[i].area > goodShapes[j].area:
                        bestMask[j] = False
                    else:
                        bestMask[i] = False

        bestShapes = [s for (s, j) in zip(goodShapes, bestMask) if j == True]

        # Check against known histograms
        finalShapes = []
        for bs in bestShapes:
            extracted = bs.extractPolyImg(fixedFull, (255, 255, 255), (255, 255, 255))
            if hm.checksign(extracted, "hist_match_candidates/", 0.99):
                finalShapes.append(bs)



        if finalShapes:
        

            predictions.append([file_name, finalShapes, "shape"])
                
        
        
        else:
            predictions.append([file_name, [0,0,0,0], "no_shape"])
        
        
        
        
    writeShapePredictionsToFile(out_file_name, predictions)

if __name__ == '__main__':
    
    usage = "Both args are optional. first position is the version number. if left blank, the default file is used.\nThe second argument is -g for gray images only"
    version = ""
    is_gray_only = "-g" in sys.argv
    
    # version and -g
    if (len(sys.argv) == 3 and is_gray_only):
        version = sys.argv[1]
        main(version, is_gray_only)
    #version and not -g
    elif (len(sys.argv) == 2) and not is_gray_only:
        version = sys.argv[1]
        main(version, is_gray_only)
        
    #no version and -g
    elif (len(sys.argv) == 2) and is_gray_only:
        main(version, is_gray_only)
    
    #base setting
    elif len(sys.argv) == 1:
        main(version, is_gray_only)
    else:
        print "something went wrong"
        print usage
    
    