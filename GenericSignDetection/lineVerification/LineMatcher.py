import cv2


# Returns gradient angles for pixels in the image
def getGradientAngles(image):
    scale = 1
    delta = 0
    ddepth = cv2.CV_32FC1

    # see http://stackoverflow.com/questions/22381704/sobel-operator-for-gradient-angle
    # and http://docs.opencv.org/2.4/modules/core/doc/operations_on_arrays.html#phase

    # X gradient
    xGradient = cv2.Sobel(image, ddepth, 1, 0, dst=None, ksize=3, scale = scale, delta = delta)

    # Y gradient
    yGradient = cv2.Sobel(image, ddepth, 0, 1, dst=None, ksize=3, scale = scale, delta = delta)


    gradientAngles = cv2.phase(xGradient, yGradient, angle=None, angleInDegrees=True)

    return gradientAngles


# Returns a tuple containing the min and max angle to be used for determining
# if gradient is within the acceptability wedge, as well as a flag indicating
# if some of that wedge spans the 360 degree mark
def getFlagAndMinMaxAngles(averageGradient, angleThreshold):
    minAngle = 0
    maxAngle = 0
    bAdd360 = False

    if (averageGradient + angleThreshold) > 360: # passing 0 degrees again
        minAngle = averageGradient - angleThreshold
        bAdd360 = True
    elif (averageGradient - angleThreshold < 0): # need to rotate starting angle to before 360
        minAngle = 360 + (averageGradient - angleThreshold)
        bAdd360 = True
    else:
        minAngle = averageGradient - angleThreshold

    maxAngle = minAngle + (2 * angleThreshold) # now we have a angle range

    #print 'flag = {0}, min = {1}, max = {2}'.format(bAdd360, minAngle, maxAngle)
    return (bAdd360, minAngle, maxAngle)


# Takes the line (defined by 2 points) and uses Bresenham to examine pixels from the line on the supplied smooth image.
# Calculates what percentage of pixels have gradients within certain number of degrees of average of all gradients
# on the line, and returns True if the line has enough pixels within gradient range over the threshold.
#
# TODO - Bresenham part should be ok, but code after that may need to be adjusted to further match with 
# Generic Sign Board Detection in Images paper
# Bresenham from http://www.roguebasin.com/index.php?title=Bresenham%27s_Line_Algorithm
def matchLineUsingBresenham(x1, y1, x2, y2, smoothedImage):

    #print 'in drawBresenham2 with line ({0},{1}) to ({2}, {3})'.format(x1, y1, x2, y2)
    gradientAngles = getGradientAngles(smoothedImage)


        # Setup initial conditions
    # x1, y1 = start
    # x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1
 
    # Determine how steep the line is
    is_steep = abs(dy) > abs(dx)
 
    # Rotate line
    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
 
    # Swap start and end points if necessary and store swap state
    swapped = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        swapped = True
 
    # Recalculate differentials
    dx = x2 - x1
    dy = y2 - y1
 
    # Calculate error
    error = int(dx / 2.0)
    ystep = 1 if y1 < y2 else -1

    gradientCount = 0
    gradientAverage = 0.0
    gradientSum = 0.0
    gradientList = list()

 
    # Iterate over bounding box generating points between start and end
    y = y1
    for x in range(x1, x2 + 1):
        #coord = (y, x) if is_steep else (x, y)

        if(is_steep): # x and y reversed
            #print 'gradient at {0},{1} = {2}'.format(y, x, gradientAngles[x][y])
            gradientSum += gradientAngles[x][y]
            gradientList.append(gradientAngles[x][y])
            #image[x][y] = red
        else:
            #print 'gradient at {0},{1} = {2}'.format(x, y, gradientAngles[y][x])
            gradientSum += gradientAngles[y][x]
            gradientList.append(gradientAngles[y][x])
            #image[y][x] = red

        
        # points.append(coord)
        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx
 
    # code below is my original code
    gradientCount = len(gradientList)
    gradientAverage = gradientSum / gradientCount

    # allow this many degrees of error for a match.  This is +/-, for a total (generous)
    # deviation of +/- 30 degrees
    angleThreshold = 30
    bAdd360, minAngle, maxAngle = getFlagAndMinMaxAngles(gradientAverage, angleThreshold)

    matchThreshold = .8 # this % of points must have gradient angles must be within threshold
    minMatchCount = int(matchThreshold * gradientCount)
    matchCount = 0
    matched = False
    matchedLines = list()

    for g in gradientList:
        if (g < 180 and bAdd360):
            g += 360 # need to add 360 to put edge case angles in "acceptability wedge"
        if(g >= minAngle and g <= maxAngle):
            matchCount += 1
            if(matchCount >= minMatchCount):
                matched = True
                break

    return matched





