#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      joseph
#
# Created:     17/04/2017
# Copyright:   (c) joseph 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import cv2
import numpy as np
import scipy.sparse.csgraph as csg
import polyDetect.polyshape
import networkx as nx

def determineCycles(linePoints, maxGap):

    print 'Searching ' + str(len(linePoints)) + ' lines for connected components...'
    vertices = []
    edges = []
    point_indexes = []
    et = []
    for (p1, p2) in linePoints:

        i1 = -1;
        i2 = -1;
        v1 = np.array(p1, np.float32)
        v2 = np.array(p2, np.float32)

        c1 = [i for i in range(0, len(vertices)) if np.linalg.norm(vertices[i] - v1) <= maxGap ]
        c2 = [i for i in range(0, len(vertices)) if np.linalg.norm(vertices[i] - v2) <= maxGap ]

        if not c1:
            point_indexes.append(len(vertices))
            vertices.append(v1)
        else:
            point_indexes.append(c1[0])
        if not c2:
            point_indexes.append(len(vertices))
            vertices.append(v2)
        else:
            point_indexes.append(c2[0])

        edges.append( (point_indexes[-1], point_indexes[-2]) )
        # print edges[-1], p1, p2

    sgraph = nx.Graph()

    sgraph.add_edges_from(edges)

    contours = []

    for i in range(0, len(vertices)):
        # sgraph.add_edge(i, i, weight=9)
        paths = nx.all_simple_paths(sgraph, i, i, cutoff=300)
        lp = list(paths)
        for p in lp:
            valid = True
            for j in range(1, len(p)):
                for k in range(j+1, len(p)):
                    if p[j] == p[k]:
                        valid = False
            if valid and len(p) > 3:
                curve = []
                for j in range(0, len(p)-1):
                    curve.append( vertices[p[j]])
                contours.append(curve)

        pass



    print "Found " + str(len(contours)) + " contours"

    polys = []


    for c in contours:
        shape = polyDetect.polyshape.polyshape(np.array(c, dtype=np.int32) )
        polys.append(shape)

    return polys


def main():
    pass

if __name__ == '__main__':
    main()
