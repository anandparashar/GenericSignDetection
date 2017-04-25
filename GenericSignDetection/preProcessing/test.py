import numpy as np
import cv2
import preProcessor

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
                    "frameAnnotations-DataLog02142012_003_external_camera.avi_annotations/pedestrianCrossing_1333395741.avi_image24.png")

    preProcessor.process(image=img, canny_param1=70,
                         canny_param2=210,
                         harriscorner_blockSize=2,
                         harriscorner_kSize=3,
                         harriscorner_freeparam=0.4,
                         smallsegmentremoval_ratio=0.05
                         )


main()