__author__ = 'harshad'
import numpy as np
from scipy.spatial import distance
from io import StringIO
import sys

def printMat(mat):
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            sys.stdout.write(str(mat[i][j])+' ')
        print ''
    print '*********************************************************'

def loadData(path):
    file = open(name=str(path),mode='r')
    mat = np.loadtxt(file)
    # printMat(mat)
    return mat

def getDistMat(mat):
    distMat = np.zeros(shape=(len(mat),len(mat)))
    file = open('outputfile.txt','w')
    for i in range(len(mat)):
        vector_a  = mat[i,:]
        for j in range(len(mat)):
            if i == j:
                distMat[i,j] = 0.0
            else:
                vector_b = mat[j,:]
                distMat[i,j] = distance.euclidean(vector_a,vector_b)
                # print distMat[i,j]
    # for row in distMat:
    #     value = str(row) + '\n'
    #     file.write(value)
    # file.close()
    return distMat

# pathInput = str(raw_input('Please Enter the path of the input txt file'))
pathCho = '/Users/harshad/PycharmProjects/Project2/cho.txt'
pathIyer = '/Users/harshad/PycharmProjects/Project2/iyer.txt'
matCho = loadData(pathCho)
matIyer = loadData(pathIyer)
matCho = np.delete(matCho, (0,1), axis=1)
matIyer = np.delete(matIyer, (0,1), axis=1)

# print 'matrix for cho.txt after removing ground truths'
# printMat(matCho)
# print 'matrix for iyer.txt after removing ground truths'
# printMat(matIyer)

distCho = getDistMat(matCho)
distIyer = getDistMat(matIyer)
