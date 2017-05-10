'''
Created on Apr 23, 2017

@author: Erich O'Saben
'''
import os

import utils as u
import evaluate_new as eval


#eval.evaluate(os.path.join("testData", "testAnnotations.txt"), os.path.join("testData", "testGroundTruth.txt"))

eval.evaluate(os.path.join("predictions3.txt"), os.path.join("..","create_testset","testGroundTruth.csv"))