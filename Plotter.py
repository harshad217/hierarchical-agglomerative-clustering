
import sys
import numpy as np
import columns
from scipy.spatial import distance
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.decomposition import PCA
import pylab as pl
import matplotlib.pyplot as plt
from io import StringIO

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
    for row in distMat:
        value = str(row) + '\n'
        file.write(value)
    file.close()
    return distMat

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


def getGroundTruths(mat):
    groundTruths = mat[:,1]
    return groundTruths

def Main(args_list):

    path = str(args_list[1].strip())
    clusters_file_path = str(args_list[2].strip())
    
    # print args_list[1]
    # print args_list[2]

    # path = 'iyer.txt'
    # clusters_file_path = 'k-means.txt'

    mat = loadData(path)
    groundTruths = getGroundTruths(mat)
    mat = np.delete(mat, (0,1), axis=1)
    distMat = getDistMat(mat)

    clusters_file = open(clusters_file_path,'r')
    cluster_list = []
    for each_line in clusters_file:
        each_line = each_line.strip()
        cluster_id = float(each_line)
        cluster_list.append(cluster_id)

    P = calculatePMatrix(groundTruths)
    print cluster_list
    pca = PCA(n_components=2)
    pca.fit(mat)
    mat_reduced = pca.transform(mat)
    print "Reduced dataset shape:", mat_reduced.shape
    plt.scatter(mat_reduced[:, 0],mat_reduced[:, 1], c=cluster_list, )
    plt.show()

args = []
for arg in sys.argv:
    args.append(arg)
Main(args)