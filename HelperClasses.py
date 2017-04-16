from operator import attrgetter

class LineToIntersect:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.intersectionPoints = list() # to use for splitting the line
        
        # calculate slope on line construction
        if(x2 <> x1):
            self.slope = ((y2 - y1)) / float(((x2 - x1)))
            self.slopeAbs = abs(self.slope)
        else:
            # vertical line
            self.slope = float('inf')
            self.slopeAbs = float('inf')

    def __str__(self):
        return "[({0},{1}), ({2},{3})]".format(self.x1, self.y1, self.x2, self.y2)

    def printInteresectionPoints(self):
        for p in self.intersectionPoints:
            print '({0},{1})'.format(p.x, p.y)

    def addIntersectionPoint(self, interestionPoint):
        self.intersectionPoints.append(interestionPoint)

    def sortIntersectionPoints(self):
        sortedByY = sorted(self.intersectionPoints, key=attrgetter('y'))
        sortedByXThenY = sorted(sortedByY, key = attrgetter('x'))
        self.intersectionPoints = sortedByXThenY

    
    # see determinant method here https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection
    # Useful for determining line intersection given 4 points (2 on each line).
    # Assumes parameters of type LineToIntersect.  Performs calculations and returns intersection point
    # with coordinates.  Note that coordinates may be the result of division that has truncated decimal places.
    #
    # Returns IntersectionPoint with valid set to True, or False if no intersection
    def find_intersection_int(self, otherLine):
        # print 'self slope = {0}, other slope = {1}'.format(self.slope, otherLine.slope)

        if (self.slope == otherLine.slope):
            return IntersectionPoint(0,0, False)
        else:
            # (x1y2 - y1x2)
            numeratorFirst = (self.x1 * self.y2 - self.y1 * self.x2) 

            # (x3y4 - y3x4)
            numeratorSecond = (otherLine.x1 * otherLine.y2 - otherLine.y1 * otherLine.x2)

            #(x1 -x2)(y3 - y4) - (y1 - y2)(x3 - x4)
            denominator = (self.x1 - self.x2) * (otherLine.y1 - otherLine.y2) - (self.y1 - self.y2) * (otherLine.x1 - otherLine.x2)

            xNumerator = (numeratorFirst) * (otherLine.x1 - otherLine.x2) - (self.x1 - self.x2) * numeratorSecond
            yNumerator = (numeratorFirst) * (otherLine.y1 - otherLine.y2) - (self.y1 - self.y2) * numeratorSecond

            # note that this will truncate if actual value has decimal places
            xCoordinate = xNumerator / denominator
            yCoordinate = yNumerator / denominator

            intersection = IntersectionPoint(xCoordinate, yCoordinate, True)
            return intersection


class IntersectionPoint:
    def __init__(self, x, y, valid):
        self.x = x
        self.y = y
        self.valid = valid

    def __str__(self):
        return "({0},{1}): valid = {2}".format(self.x, self.y, self.valid)

    # see http://stackoverflow.com/questions/390250/elegant-ways-to-support-equivalence-equality-in-python-classes
    def __eq__(self, other):
        """Override default Equals behavior"""
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __ne__(self, other):
        """Define a non-equality test"""
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def __hash__(self):
        """Override the default hash behavior (that returns the id or the object)"""
        return hash(tuple(sorted(self.__dict__.items())))