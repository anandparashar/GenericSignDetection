import HelperClasses as hc

def splitLinesBasedOnIntersections(lines):
    splitLines = list()

    for i in range(0 to len(lines)):
        currentLine = lines[i]

        # find all intersections of this line with other lines in list
        for (j in range(i to len(lines))):
            lineToTest = lines[j]

            intersectionPoint = currentLine.find_intersection_int(lineToTest)

            if(intersectionPoint.valid):
                # valid intersection point.  Find intersections for current line
                #TODO - calc. intersection points, add to lists for other lines so don't calculate later.
                # Then, at end for current line, sort the intersections, then split, then add split line segments to splitLines list.  Go to next
                # line and repeat, but don't recalculate previous intersections since they should already be in new line's
                # intersection list.