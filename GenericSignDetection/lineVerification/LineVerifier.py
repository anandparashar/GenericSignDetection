import LineSplitter as ls
import LineMatcher as lm


# Given a set of lines (LineToIntersect), splits the lines based on intersections.  
# Then verifies the resulting segments against the image.
# Returns only those segments that pass verification.
def getVerifiedLines(lines, smoothedImage):
    verifiedLines = list()

    # First, split the lines based on intersections
    splitLines = ls.splitLinesBasedOnIntersections(lines)

    # Now verify the line
    for line in splitLines:
        if(lm.matchLineUsingBresenham(line.x1, line.y1, line.x2, line.y2, smoothedImage)):
            # it passed our matching requirements, so add it to the list of verified lines
            verifiedLines.append(line)

    return verifiedLines