import HelperClasses as hc

# Returns a dictionary keyed on begin and end points for each line
# Value associated with each key is a set consisting of neighboring points of each point
def getPointsAndNeighborsFromLineSegments(lines):
    neighborDictionary = dict()

    # Loop through every line and add endpoints to dictionary key and associated sets
    for line in lines:
        if(line.point1 not in neighborDictionary):
            neighborDictionary[line.point1] = set()

        if(line.point2 not in neighborDictionary):
            neighborDictionary[line.point2] = set()

        neighborDictionary[line.point1].add(line.point2)
        neighborDictionary[line.point2].add(line.point1)

    return neighborDictionary