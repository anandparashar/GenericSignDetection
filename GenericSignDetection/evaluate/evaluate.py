'''
Created on Apr 23, 2017

@author: Erich O'Saben
'''


import utils
from fileinput import filename

from sklearn.metrics import confusion_matrix, classification_report,accuracy_score


def evaluate(detectionFilePath, truthFilePath, minWidth=20, minHeight=20):
    """
    evaluates the predicted signs agains the ground truth.
    
    a true (1) prediction means that a sign was detected on the photograph and the bounding box of the sign is within 10 pixels of the actual bounding box
    All signs in the photograph do not need to be found. 
    
      
    Paramaters:
    detectionFilePath => file path to the predicted sign locations
    truthFilePath => file path to the ground truth annotations
    
    minHeight/Width are the minimum size in pixels of the smallest sign that will be checked
    
    Output: Accuracy Score, Confusion Matrix, Classification Report  
    
    """
    
    
    detections = [x.trim() for x in open(detectionFilePath, 'r').readlines()]
    annotations = [x.trim() for x in open(truthFilePath, 'r').readlines()[1:]]
    
    assert (len(detections) == len(annotations)), "the ground truth and prediction files are different lengths"
    
    y_pred = []
    y_true = []
        
    signs = {}
    for ann in annotations:
        #this pic has no signs
        if "negativePics" in ann:
            signs[ann] = []
            y_true.append(0)
            continue
        
        
        annFields = ann.split(";")
        
        # Remove any annotations that are too small
        if (int(annFields[4])-int(annFields[2]) < minWidth or int(annFields[5])-int(annFields[3]) < minHeight):
            y_true.append(0)
            continue
        
        y_true.append(1)
        key = annFields[0]
        signBox = [int(x.strip()) for x in annFields[2:6]]#[annFields[2], annFields[3], annFields[4], annFields[5]]
        
        if key in signs.keys():
            signs[key].append(signBox)
        else:
            signs[key] = [signBox]
            
    
    #check the predicted boxes against the ground truth
    for detection in detections:
        #print len(y_true), len(y_pred)
        detSplit = detection.split(";")
        
        fileName = detSplit[0]
        predSignBox = [int(x.strip()) for x in detSplit[1:]]
        
        #if the fileName is not in signs, then the predicted sign doesn't actually exist
        #this case is when a real box is too small (less than minHeight or minWidth) but the predicted box is bigger than that so the actual box was filtered out (ie not a match)
        if fileName not in signs.keys():
            y_pred.append(1)
            continue
            
        else:
            #We predicted a box and the filename is in both files. Check if the annotations match
            
            #check if there were signs in the photo
            if len(signs[fileName]) > 0:
                #y_true.append(1)
                match = False
                #check all the boxes of the signs in the photo and see if we were within 10 pixels of any of them them
                for actSignBox in signs[fileName]:
                    diffs = [abs(int(actSignBox[i])-int(predSignBox[i])) for i in range(4)]
                    if len([x for x in diffs if x > 10]) == 0:
                        match = True
                        break
                if match:
                    y_pred.append(1)
                else:
                    y_pred.append(0) 
            
            #there were no signs in the photo
            else:
                
                #check if we predicted a box or not is sum == 0, then no box predicted in image
                if sum(predSignBox) == 0:
                    y_pred.append(0)
                
                
            
    
    
    assert (len(y_true) == len(y_pred)), "something went wrong. y_true and y_pred are different lengths y_true: {}, y_pred: {}".format(len(y_true), len(y_pred))
    
    print y_true
    print y_pred
    
        
    print "Accuracy: ", accuracy_score(y_true, y_pred)#scikit-learn.org/stable/modules/model_evaluation.html#classification-report
    print 
    print "Confusion Matrix:\n", confusion_matrix(y_true, y_pred) #http://scikit-learn.org/stable/modules/model_evaluation.html#confusion-matrix
    print 
    print "Classification Report:\n", classification_report(y_true, y_pred) #scikit-learn.org/stable/modules/model_evaluation.html#classification-report



