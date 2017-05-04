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
import math
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
        v1 = p1
        v2 = p2

        point_indexes.append(len(vertices))
        vertices.append(v1)
        point_indexes.append(len(vertices))
        vertices.append(v2)

    rolling_offset = 0

    for i in range(0, len(vertices)):
        v1 = vertices[i]
        if v1 == (-1, -1):
            rolling_offset += 1
            continue
        for j in range(i+1, len(vertices)):
            v2 = vertices[j]
            dist = math.sqrt( (v1[0] - v2[0])**2 + (v1[1] - v2[1])**2 )
            if dist <= maxGap:
                vertices[j] = (-1, -1)
                point_indexes[j] = i - rolling_offset

    vertices = [v for v in vertices if v != (-1, -1)]

    for i in range(0, len(point_indexes), 2):
        edges.append((point_indexes[i], point_indexes[i+1]))

    print "Found " + str(len(vertices)) + " vertices after merging"

    sgraph = nx.Graph()

    sgraph.add_edges_from(edges)
    basis = nx.cycle_basis(sgraph)

    contours = []

    for b in basis:
        con = [ vertices[v] for v in b]
        contours.append(con)

    '''
    for i in range(0, len(vertices)):
        # sgraph.add_edge(i, i, weight=9)
        paths = nx.all_simple_paths(sgraph, i, i, cutoff=40)
        print 'Processed vertice ' + str(i)
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
    '''


    print "Found " + str(len(contours)) + " contours"

    polys = []


    for c in contours:
        shape = polyDetect.polyshape.polyshape(np.array(c, dtype=np.int32) )
        if shape.area < 2400:
            polys.append(shape)
        else:
            print shape.area
            if shape.area == 0.0:
                print c

    return polys


def main():
    pass

if __name__ == '__main__':
    main()
