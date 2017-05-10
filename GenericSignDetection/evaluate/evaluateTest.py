'''
Created on Apr 23, 2017

@author: Erich O'Saben
'''
import os

import utils as u
import evaluate as eval


VERSION = "6"

#eval.evaluate(os.path.join("testData", "testAnnotations.txt"), os.path.join("testData", "testGroundTruth.txt"))

eval.evaluate(os.path.join("..", "predictions{}.txt".format(VERSION)), os.path.join("..","test_data","testGroundTruth{}.csv".format(VERSION)), VERSION)