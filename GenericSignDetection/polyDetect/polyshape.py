
import cv2
import numpy as np
import math

class polyshape:
    ''' Class representing a detected polygonal shape '''

    def __init__(self, contours):


        self.points = contours
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

    # Returns a tuple representing the center of the bounding rectangle
    def getBoundingCenter(self):
        return (self.bx + self.width/2, self.by + self.height/2)

    # Returns a tuple containing the bounding rectangle in the form (x, y, width, height)
    # Set cv2.boundingRect for more information
    def getBoundingTuple(self):
        return (self.bx, self.by, self.bwidth, self.bheight)

    '''
    Tests a polygon for angle regularity(All angles being approximately the same)
    
    sides - Expected number of sides
    angle - Expected angle at each vertex
    threshold - Maximum absolute difference an angle can have from the expect angle
    
    Returns - True if the polygon is regular within the limits specified, False otherwise
    '''
    def compareRegularPoly(self, sides, angle, threshold):
        # Check sides
        if sides != self.sides:
            return False

        for i in range(0, sides):
            # Create two directional vectors for calculation of the dot product
            vect1 = np.subtract(self.points[i], self.points[(i+1)%sides])
            vect2 = np.subtract(self.points[(i+1)%sides], self.points[(i+2)%sides])

            # Calculate the magnitude of each vector
            mag1 = np.linalg.norm(vect1)
            mag2 = np.linalg.norm(vect2)
            # Dot product
            dp = np.vdot(vect1, vect2)

            # Extract the angle and convert to degrees
            measure_angle = math.acos( max(-1, min(dp/(mag1*mag2), 1)))*(180/np.pi)

            # Check the calculated angle against the threshold provided
            if abs(angle - measure_angle) > threshold:
                return False

        # If no angle failed the test then the polygon is angle regular
        return True

    '''
    Checks if a shape is an angle-regular polygon and as such, a good sign candidate
    
    threshold: See compareRegularPoly
    
    Returns - True if the polygon is a good sign candidate, False if it is not
    '''
    def isGoodSignCandidate(self, threshold):
        # Check if it's rectangular, including squares
        if self.compareRegularPoly(4, 90, threshold):
            return True
        # Check check if it's an octagon
        if self.compareRegularPoly(8, 135, threshold):
            return True
        # Check if it's an isosceles triangle
        if self.compareRegularPoly(3, 60, threshold):
            return True

        return False

    # Checks if one polyshape object overlaps another
    def overlaps(self, other):
        for p in other.points:
            if cv2.pointPolygonTest(self.points, tuple(p[0]), False) > 0:
                return True
        return False

    def verify(self):
        # TODO: Line/edge verification here
        pass
