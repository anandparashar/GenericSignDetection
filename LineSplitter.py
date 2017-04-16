import HelperClasses as hc

def splitLinesBasedOnIntersections(lines):
    splitLines = list()

    for i in range(0, len(lines)):
        currentLine = lines[i]

        # find all intersections of this line with other lines in list
        for j in range(i+1, len(lines)):
            lineToTest = lines[j]

            intersectionPoint = currentLine.find_intersection_int(lineToTest)

            # If valid intersection point.  Find intersections for current line
            if(intersectionPoint.valid):
                currentLine.addIntersectionPoint(intersectionPoint)

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
