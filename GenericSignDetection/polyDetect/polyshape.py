
import cv2
import numpy as np

class polyshape:
    ''' Class representing a detected polygonal shape '''

    def __init__(self, contours):

        self.points = cv2.convexHull(contours, returnPoints = True)
        self.points = cv2.approxPolyDP(self.points, 1, closed = True)
        # self.points = contours
        self.sides = len(self.points)
        self.area = cv2.contourArea(self.points)
        moments = cv2.moments(self.points)
        bx, by, width, height = cv2.boundingRect(self.points)
        self.bx = bx
        self.by = by
        self.bwidth = width
        self.bheight = height
        # self.centroid = ( moments.m10/moments.m00, moments.m01/moments.m00 )

    ''' Creates a mask containing the region coressponding to the pixels
        contained within polygon detected in the source image

        source: Source image, can be grayscale or color, but maskValue must match
        maskValue: Scalar value for grayscale that the pixels of the resulting
                   image will have, or tuple for color images
    '''
    def createMask(self, source, maskValue):
        maskImg = np.zeros(source.shape, dtype = np.uint8)
        cv2.drawContours(maskImg, [self.points], -1, color = maskValue, thickness = -1 )
        return maskImg


    ''' Extracts the target polygon from the image, masks it and crops
        to the minimum bounding rectangle

        source: Image to extract the polygon from
    '''
    def extractPolyImg(self, source, maskValue):
        maskImg = self.createMask(source, maskValue)
        masked = cv2.bitwise_and(source, maskImg)
        extracted = masked[self.by:self.by+self.bheight, self.bx:self.bx+self.bwidth]
        return extracted

    ''' Determines a matching value between two polygons using Hu Momements:
        See cv2.matchShapes for detailed overview

        other: Image to compare the current polygon object against
    '''
    def matchPoly(self, other):
        result = cv2.matchShapes(self.points, other.points, method = cv2.cv.CV_CONTOURS_MATCH_I2)
        return result

    def drawBoundingRect(self, img, color):
        cv2.rectangle(img, (self.bx, self.by), (self.bx+self.bwidth, self.by+self.bheight), color)

    def drawContour(self, img, color):
        cv2.drawContours(img, [self.points], -1, color, thickness=-1)

    def getBoundingCenter(self):
        return (self.bx + self.width/2, self.by + self.height/2)


    def verify(self):
        # TODO: Line/edge verification here
        pass
