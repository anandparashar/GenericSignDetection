'''
Created on May 7, 2017

@author: Erich O'Saben
'''



"""
TP = A predicted sign was found in the image within a NxN pixel window (default is 20x20)
FP = A predicted sign was not found in the image within a NxN pixel window

TN = There were no predicted signs in an image with no visible signs
FN = All signs in images that were not found.
"""

import csv



def evaluate(detectionFilePath, truthFilePath,version="", minWidth=20, minHeight=20):

    detections = [x.strip() for x in open(detectionFilePath, 'r').readlines()]
    annotations = [x.strip() for x in open(truthFilePath, 'r').readlines()]
    
    final_annotations = []
    #numAnnotations = len(annotations)
    # Remove any annotations that are too small:
    for i, annotation in enumerate(annotations):
        annFields = annotation.split(';')
        ann_final = annotation
        
        
        #negative images get written with blank colums after the file name so trim that down to length 1
        if annFields[1] == "":
            annFields = annFields[:1]
            ann_final = annFields[0]
        
        #print len(annFields)
        #print annotation
        #print annFields[4], annFields[2], annFields[5], annFields[3]
        
        #check the positive samples if they are large enough to consider
        if len(annFields) > 1:
            if (int(float(annFields[4]))-int(float(annFields[2])) < minWidth or int(float(annFields[5]))-int(float(annFields[3])) < minHeight):
                #annotations.remove(annotation)
                #numAnnotations -= 1
                #print "Sign is too small, skipping annotation in line: {}".format(i+1)#, annotation # i starts at 0, line numbers start at 1
                continue
        final_annotations.append(ann_final)
            
    
    fpCount = 0
    tpCount = 0
    tnCount = 0

    
    numDetections = len(detections)
    numAnnotations = len(final_annotations)
    
    
    results = []
    for line_num, detection in enumerate(detections):
        r = "FP"  #TP/FP/FN/FP - Default is FP bc if a prediction is not in the annotations, then it won't fit in any category
        fields = detection.split(';')
        potentialAnnotations = [line for line in final_annotations if fields[0] in line]
        
        predBox = [int(x.strip()) for x in fields[1:]]
        if (int(fields[3])-int(fields[1]) < minWidth or int(fields[4])-int(fields[2]) < minHeight) and sum(predBox) != 0:
            numDetections -= 1
            print line_num+1, "prediction is too small"
            r = "NA" #skipping bc too small
            continue
        
        sign_type = "unknown" #FP Match so don't know what it was trying to match
        tp_match = False
        tn_match = False
        for annotation in potentialAnnotations:
            annFields = annotation.split(';')
            r  = "FN" # set this back to default of FN bc if it gets all the way through the loop, 
                        #it's a FN
            
            
            #negative picture
            if len(annFields) < 11:
                sign_type = "NoSign"
                tn_match = sum([int(x) for x in fields[1:]]) == 0
                if tn_match:
                    final_annotations.remove(annotation)
                    #tnCount += 1
                    r = "TN"
                    
                else:
                    #fpCount +=1
                    r = "FP"
                break
            else:
                sign_type = annFields[1]
                #print annFields
                diffs = [abs(int(float(annFields[i+2]))-int(float(fields[i+1]))) for i in range(4)]
                tp_match = (len([x for x in diffs if x > 10]) == 0)
                if tp_match:
                    final_annotations.remove(annotation)
                    #tpCount += 1
                    
                    #print "match at line", annotation
                    r = "TP"
                else:
                    #fpCount += 1
                    r = "FP"
                break 
            
        
        #print line_num+1, r
        if r == "TP":
            tpCount +=1
        if r == "TN":
            tnCount +=1
        if r == "FP":
            fpCount += 1

        results.append([r, sign_type] + detection.split(";"))
    
    
    for f in final_annotations:
        annFields = f.split(";")
        if len(annFields) < 11:
            sign_type = "NoSign"
        else:
            sign_type = annFields[1]
        
        results.append(["FN", sign_type, annFields[0], "NA", "NA", "NA", "NA"])
        
    
    #results += [["FN", x] for x in final_annotations]

    fnCount = len(final_annotations)
    accuracy = round((tpCount + fnCount )/ (numAnnotations * 1.0), 4)
    precision = round(tpCount/(tpCount + fpCount * 1.0), 4)
    recall = round(tpCount / (tpCount + fnCount * 1.0), 4)
    F_score = round(2 * (precision * recall) / ( (precision + recall)*1.0), 4)
    
    print('\n\n------')
    print('Number of predictions: %d' % numDetections)
    print('Number of annotations: %d' % numAnnotations)
    print('------')
    print("True positives: %d" % tpCount)
    print("True negatives: %d" % tnCount)
    print("False positives: %d" % fpCount)
    print("False negatives: %d" % fnCount)
    print('------')
    
    print 
    print ("Accuracy: {}".format(accuracy))
    print ("Precision: {}".format(precision))
    print ("Recall: {}".format(recall))
    print ("F Score: {}".format(F_score))
    
    with open("results{}.csv".format(version), "wb") as f:
        writer = csv.writer(f)
        writer.writerows(results)
    
    