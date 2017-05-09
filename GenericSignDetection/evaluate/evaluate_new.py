'''
Created on May 7, 2017

@author: Erich O'Saben
'''

def evaluate(detectionFilePath, truthFilePath, minWidth=20, minHeight=20):

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
                print "Sign is too small, skipping annotation in line: {}".format(i+1)#, annotation # i starts at 0, line numbers start at 1
                continue
        final_annotations.append(ann_final)
            
    
    fpCount = 0
    tpCount = 0
    
    numDetections = len(detections)
    numAnnotations = len(final_annotations)
    id = 0
    widthsFound = []
    for detection in detections:
        fields = detection.split(';')
        potentialAnnotations = [line for line in final_annotations if fields[0] in line]
        
        predBox = [int(x.strip()) for x in fields[1:]]
        if (int(fields[3])-int(fields[1]) < minWidth or int(fields[4])-int(fields[2]) < minHeight) and sum(predBox) != 0:
            numDetections -= 1
            print "prediction is too small: ", detection
            continue
        
        
        
        match = False
        for annotation in potentialAnnotations:
            annFields = annotation.split(';')
            
            #negative picture
            if len(annFields) < 11:
                match = sum([int(x) for x in fields[1:]]) == 0
                if match:
                    final_annotations.remove(annotation)
                    break
            else:
                print annFields
                diffs = [abs(int(float(annFields[i+2]))-int(float(fields[i+1]))) for i in range(4)]
                match = (len([x for x in diffs if x > 10]) == 0)
                if match:
                    final_annotations.remove(annotation)
                    break    
                
        if match:
            tpCount += 1
            widthsFound.append(int(fields[3])-int(fields[1]))
            print "match at line", annotation
        else:
            fpCount += 1
            
            
        id += 1


    

    fnCount = len(final_annotations)
    accuracy = round(tpCount / (numAnnotations * 1.0), 4)
    precision = round(tpCount/(tpCount + fpCount * 1.0), 4)
    recall = round(tpCount / (tpCount + fnCount * 1.0), 4)
    
    
    print('\n\n------')
    print('Number of predictions: %d' % numDetections)
    print('Number of annotations: %d' % numAnnotations)
    print('------')
    print("True positives: %d" % tpCount)
    print("False positives: %d" % fpCount)
    print("False negatives: %d" % fnCount)
    print('------')
    
    print 
    print ("Accuracy: {}".format(accuracy))
    print ("Precision: {}".format(precision))
    print ("Recall: {}".format(recall))
    
    
    