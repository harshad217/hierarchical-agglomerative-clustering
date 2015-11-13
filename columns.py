__author__ = 'harshad'

import numpy as np

def getGroundTruths(mat):
    groundTruths = mat[:,1]
    return groundTruths

def getClusterIds(mat):
    clusterIds = mat[:,0]
    return clusterIds