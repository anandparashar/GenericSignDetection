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
import polyDetect.polyshape
import polyDetect.cycleDetection as cd
from datetime import datetime
import ntpath


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
                        
            
    


def main():
    
    
       
    img_files = [x.strip() for x in open(os.path.join("..", "create_testset", "testGroundTruthFileNames.txt"),'r').readlines()]
    annotations = open(os.path.join("..", "create_testset", "testGroundTruth.csv"), 'r').readlines()
                       
    #print annotations[:5]
    
    
    out_file_name = "predictions3.txt"
    predictions = []
    for i, img_file in enumerate(img_files):
        if i % 50 == 0:
            print i, "images have been processed", len(img_files), "total"
        
        
        #ann_fields = img_file.split(";")

        file_name = img_file#ann_fields[0]
        #print "working on {}".format(file_name)
        
        
        
        
        img = cv2.imread(os.path.join(u.DATA_ROOT_PATH,file_name))
        
        # Get rid of the non-image junk at the bottom of the aiua* direct images
        trimmed = np.delete(img, range(img.shape[0] - 16, img.shape[0]), axis=0)
        
        # Convert to grayscale if the image is in color
        if img.shape[2] == 3:
            gray = cv2.cvtColor(trimmed, cv2.COLOR_BGR2GRAY)
        else:
            gray = trimmed
        
        
        # Clean interlacing, only necessary in the aiua* data folders
        cleaned = ilr.clean(trimmed)
        
        fixed = cleaned
        # fixed = hist.gammaCorrect(cleaned)
        
        
        # Back to full color
        fixedFull = cv2.cvtColor(fixed, cv2.COLOR_GRAY2BGR)
        #displayResized("fixed full", fixedFull)
        
        
        # Estimate a threshold value for the edge detector
        threshold = hist.estimateThreshold(fixedFull)
    
        processed, p2, lines = pp.process(image=fixedFull, canny_param1=threshold /2,
                                           canny_param2=threshold,
                                           harriscorner_blockSize=2,
                                           harriscorner_kSize=3,
                                           harriscorner_freeparam=0.4,
                                           smallsegmentremoval_ratio=0.015,
                                           hough_threshold=25,
                                           hough_minLen=15,
                                           hough_maxGap=7
                                           )
        
        
        
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
        
        
        if bestShapes:
        

            predictions.append([file_name, bestShapes, "shape"])
                
        
        
        else:
            predictions.append([file_name, [0,0,0,0], "no_shape"])
        
        
        
        
    writeShapePredictionsToFile(out_file_name, predictions)

if __name__ == '__main__':
    main()