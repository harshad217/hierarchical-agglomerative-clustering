__author__ = 'harshad'

import numpy as np

def getGroundTruths(mat):
    groundTruths = mat[:,1]
    return groundTruths

def getClusterIds(mat):
    clusterIds = mat[:,0]
    return clusterIds

def createIndexToClusterList(map,elements_size):
    cluster_list = np.zeros(elements_size)
    print cluster_list
    i=0
    for elements in map:
        for each in elements:
            cluster_list[each-1] = i
        i += 1

    j=0
    for each in cluster_list:
        # print 'point=',j,'  cluster=',each
        j = j + 1

    return cluster_list
