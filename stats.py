__author__ = 'harshad'

import numpy as np
import math

def calculateIncidenceMatrix(map,size):
    C = np.zeros(shape=(size,size))
    for clusters in map:
        for cluster_id1 in clusters:
            for cluster_id2 in clusters:
                if cluster_id1==cluster_id2:
                    C[cluster_id1-1,cluster_id2-1] = 0
                else:
                    C[cluster_id1-1,cluster_id2-1] = 1
    return C

def calculateCorrelation(D, C):
    # flatMatA = np.ndarray.flatten(matA)
    # flatMatB = np.ndarray.flatten(matB)
    # corr = np.correlate(flatMatA,flatMatB)
    meanD = np.mean(D)
    meanC = np.mean(C)
    numerator = 0.0
    denom1 = 0.0
    denom2 = 0.0
    for i in range(len(D)):
        for j in range(len(D)):
            numerator = numerator + ( (D[i,j]-meanD)*(C[i,j]-meanC) )

    for i in range(len(D)):
        for j in range(len(D)):
            denom1 = denom1 + ( (D[i,j]-meanD)*(D[i,j]-meanD) )
    denom1 = math.sqrt(denom1)

    for i in range(len(D)):
        for j in range(len(D)):
            denom2 = denom2 + ( (C[i,j]-meanC)*(C[i,j]-meanC) )
    denom2 = math.sqrt(denom2)
    r = numerator / (denom1 * denom2)

    return r