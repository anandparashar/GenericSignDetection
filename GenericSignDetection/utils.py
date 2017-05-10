'''
Created on Apr 23, 2017

@author: Erich O'Saben
'''

import os
import sys




#enter path to the root of your image directory here

DATA_ROOT_PATH = "/Volumes/ExDrive/CS682/signDatabasePublicFramesOnly"

assert os.path.isdir(DATA_ROOT_PATH), "set DATA_ROOT_PATH to your data directory"

ALL_ANNOTATIONS = os.path.join(DATA_ROOT_PATH, "allAnnotations.csv")


#images with no signs in them
NEGATIVES_PATH = os.path.join(DATA_ROOT_PATH, "negatives", "negativePics")


pathSep = os.path.sep

IMAGE_DIRS = {}
for dir in os.walk(DATA_ROOT_PATH):
    dirSplit = dir[0].split("Only{}".format(pathSep))
    
    if len(dirSplit) > 1:
        subDir = dirSplit[1].split(pathSep)
        
        if len(subDir) > 1:
            key = subDir[0]
            #print key
            #print dir[0]
            IMAGE_DIRS[key] = {"path": dir[0] , "aFile": os.path.join(dir[0], "frameAnnotations.csv")}
    
    
