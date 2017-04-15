import HelperClasses as hc


line1 = hc.LineToIntersect(1,1,1,4)
line2 = hc.LineToIntersect(1,4,4,4)
line3 = hc.LineToIntersect(1,1,4,4)
line4 = hc.LineToIntersect(1,4,4,1)
line5 = hc.LineToIntersect(1,1,4,1)
line6 = hc.LineToIntersect(4,1,4,4)

intersectionPoint1 = line1.find_intersection_int(line2) # should be True
intersectionPoint2 = line3.find_intersection_int(line4) # should be True
intersectionPoint3 = line2.find_intersection_int(line5) # should be False
intersectionPoint4 = line6.find_intersection_int(line1) # should be False

print "intersection of line {0} with line {1} calculated to be {2}".format(line1, line2, intersectionPoint1)
print "intersection of line {0} with line {1} calculated to be {2}".format(line3, line4, intersectionPoint2)
print "intersection of line {0} with line {1} calculated to be {2}".format(line2, line6, intersectionPoint3)
print "intersection of line {0} with line {1} calculated to be {2}".format(line5, line1, intersectionPoint4)


line1.addIntersectionPoint(hc.IntersectionPoint(1,1, True))
line1.addIntersectionPoint(hc.IntersectionPoint(1,3, True))
line1.addIntersectionPoint(hc.IntersectionPoint(1,2, True))

print 'unsorted intersection points:'
line1.printInteresectionPoints()

print '\nsorted intersection points:'
line1.sortIntersectionPoints()
line1.printInteresectionPoints()