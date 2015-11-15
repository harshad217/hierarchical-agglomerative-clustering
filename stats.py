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

def calculatePMatrix(groundTruths):
    P = np.zeros(shape=(len(groundTruths),len(groundTruths)))
    for i in range(len(groundTruths)):
        for j in range(len(groundTruths)):
            # index + 1 = point number
            if i!=j:
                if groundTruths[i] == groundTruths[j]:
                    P[i,j] = 1
            elif i==j:
                P[i,j] = 0
    print P
    return P

def calculateCorr(D,C):
    meanD = np.mean(D)
    meanC = np.mean(C)
    D = D - meanD
    C = C - meanC
    #get the dot product
    numMat = np.multiply(D,C)
    numSum = np.sum(numMat)

    denom1 = math.sqrt(np.sum(np.multiply(D,D)))
    denom2 = math.sqrt(np.sum(np.multiply(C,C)))

    denom = denom1 * denom2
    r = numSum/denom
    return r

def calculateCorrelation(D, C):
    # flatMatA = np.ndarray.flatten(matA)
    # flatMatB = np.ndarray.flatten(matB)
    # corr = np.corrcoef(flatMatA,flatMatB)
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

def calculateExternalIndex(P,C):
    SS = 0
    DD = 0
    SD = 0
    DS = 0

    for i in range(len(P)):
        for j in range(len(P[0])):
            if P[i,j] == 1 and C[i,j] == 1:
                SS = SS + 1
            elif P[i,j] == 0 and C[i,j] == 0:
                DD = DD + 1
            elif P[i,j] == 1 and C[i,j] == 0:
                DS = DS + 1
            elif P[i,j] == 0 and C[i,j] == 1:
                SD = SD + 1
    # print 'SS = ',SS
    # print 'DD = ',DD
    # print 'SD = ',SD
    # print 'DS = ',DS
    RAND = float(SS + DD) / float( SS + SD + DS + DD )
    JACCARD = float(SS) / float(SS + SD + DS)
    return RAND,JACCARD