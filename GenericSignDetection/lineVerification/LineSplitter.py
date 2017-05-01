import HelperClasses as hc
import cv2

'''
Given a list of lines (of type LineToIntersect), this
1) Clips all lines against the specified height and width
2) Calculates intersections of all lines, but only if that intersection occurs within image bounds
3) Splits each line based on intersections on the line
4) Returns the new list of split line segments
'''
def splitLinesBasedOnIntersections(lines, h, w):
    splitLines = list()

    # First - clip line against the imageSize to make sure we only return line segments with coordinates inside image
    for i in range(0, len(lines)):
        currentLine = lines[i]

        (x1, y1), (x2,y2) = cv2.cv.ClipLine((w, h), (currentLine.point1.x, currentLine.point1.y), (currentLine.point2.x, currentLine.point2.y))

        # replace array item with equivalent line that has been clipped to image size
        lines[i] = hc.LineToIntersect(x1,y1,x2,y2)

    for i in range(0, len(lines)):
        currentLine = lines[i]

        currentLine.point1.x = x1
        currentLine.point1.y = y1
        currentLine.point2.x = x2
        currentLine.point2.y = y2

        # find all intersections of this line with other lines in list
        for j in range(i+1, len(lines)):
            lineToTest = lines[j]

            intersectionPoint = currentLine.find_intersection_int(lineToTest)

            # If valid intersection point, and it lies within bounds of image, add current intersection point
            if(intersectionPoint.valid
                and (intersectionPoint.x >= 0 and intersectionPoint.x <= (w-1))
                and (intersectionPoint.y >= 0 and intersectionPoint.y <= (h-1))):
                currentLine.addIntersectionPoint(intersectionPoint)
                # print 'intersection point: {0}'.format(intersectionPoint)

                # Add this intersection to the other line, too, since we won't revisit currentLine again
                lineToTest.addIntersectionPoint(intersectionPoint)

        currentLinePoint1 = hc.IntersectionPoint(currentLine.x1, currentLine.y1, True)
        currentLinePoint2 = hc.IntersectionPoint(currentLine.x2, currentLine.y2, True)

        # add these to intersection points of current line only to make sure they are accounted for in sort.
        # This will ensure line segmentation is correct.
        currentLine.addIntersectionPoint(currentLinePoint1)
        currentLine.addIntersectionPoint(currentLinePoint2)

        # now have all intersections on current line.  Sort them so we can split the line.
        currentLine.sortIntersectionPoints()

        lengthIntersectionPoints = len(currentLine.intersectionPoints)

        for splitPointIndex in range(0, lengthIntersectionPoints):
            # If this is not the last split point, so another segment is possible...
            if(splitPointIndex < lengthIntersectionPoints - 1):
                
                beginSegment = currentLine.intersectionPoints[splitPointIndex]
                endSegment = currentLine.intersectionPoints[splitPointIndex + 1]

                # Now just make sure the start and end points don't identify the same point
                if(beginSegment != endSegment):
                    splitLines.append(hc.LineToIntersect(beginSegment.x, beginSegment.y, endSegment.x, endSegment.y))
    
    return splitLines
