__author__ = 'harshad'

import stats as st
import columns
import numpy as np
from scipy.spatial import distance
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.decomposition import PCA
import pylab as pl
import matplotlib.pyplot as plt
from io import StringIO
import sys

def getMinMax(index1,index2):
    min_index = min(index1,index2)
    max_index = max(index1,index2)
    return min_index, max_index

def printMat(mat):
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            sys.stdout.write(str(mat[i][j])+' ')
        print ''
    print '---'

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

def agglomerativeClustering(distMat,K):
    cl_list = []
    map = [ ]
    for a in range(len(distMat)):
        map.append([a+1])
    for i in range(len(distMat)):
        cl_list.append([i])

    dMat = distMat
    ind_i = -1
    ind_j = -1
    least = sys.float_info.max
    i = 0
    j = 0
    flag = False

    while 1:
        if len(dMat) == K and len(dMat[0])==K:
            flag = True
            break

        it = 0
        ind_i = -1
        ind_j = -1
        least = sys.float_info.max
        for i in range(len(dMat)):
            for j in range(len(dMat[0])):
                if i!=j and dMat[i,j]!=-1:
                    if dMat[i,j]<least:
                        ind_i = i
                        ind_j = j
                        least = dMat[i,j]
        # print least
        # print ind_i, ind_j

        ind_i,ind_j = getMinMax(ind_i,ind_j)
        temp1 = map[ind_i]
        temp2 = map[ind_j]
        temp3 = [ ]
        for each in temp1:
            temp3.append(each)
        for each in temp2:
            temp3.append(each)
        map[ind_i] = temp3
        useless_variable = map.pop(ind_j)

        for k in range(len(dMat[0])):
             dMat[ind_i,k] = min(dMat[ind_i,k],dMat[ind_j,k])
        for k in range(len(dMat)):
             dMat[k,ind_i] = min(dMat[k,ind_i],dMat[k,ind_j])

        # print 'merging clusters ',ind_i,' & ', ind_j,' with value= ',least

        #at ind_i index, we are storing the new distances of the newly formed cluster
        dMat = np.delete(dMat,ind_j,axis=0)
        dMat = np.delete(dMat,ind_j,axis=1)

        #remove b and merge that cluster with a cluster
        b = cl_list.pop(ind_j)
        a = cl_list[ind_i]
        temp = []
        temp.append(a)
        temp.append(b)
        cl_list[ind_i] = temp

        # org = map[ind_i]
        # to_add = map.pop(ind_j)
        # map[ind_i] = [org,to_add]

    # print 'final results map', map
    return cl_list,map

def printClusters(map):
    i=0
    for each in map:
        print 'for cluster',i+1,' ',each
        i = i + 1

def drawDendrogram(distMat):
    linkage_matrix = linkage(distMat,method='single')
    plt.figure(figsize=(20,8))
    plt.title('H A C')
    plt.xlabel('cluster ID')
    dendrogram(linkage_matrix)
    plt.show()

def Main():
    toyMat = np.reshape( [0,1,2,2,3,1,0,2,4,3,2,2,0,1,5,2,4,1,0,3,3,3,5,3,0],(5,5))
    # pathInput = str(raw_input('Please Enter the path of the input txt file'))
    pathCho = '/Users/harshad/PycharmProjects/Project2/cho.txt'
    pathIyer = '/Users/harshad/PycharmProjects/Project2/iyer.txt'
    pathD2 = 'dataset1.txt'

    # path = pathIyer
    path = str(raw_input('Please enter the name of the dataset').strip())
    k_value = int(raw_input('Enter value of K'))
    dyn = str(raw_input('Do you want to draw dendrogram ?'))
    if dyn == 'y':
        drawD = 1
    elif dyn == 'n':
        drawD = 0
    # matCho = loadData(pathCho)
    # matIyer = loadData(pathIyer)

    mat = loadData(path)

    # distCho = getDistMat(matCho)
    # distIyer = getDistMat(matIyer)

    '''Get Groundtruths'''
    groundTruths = columns.getGroundTruths(mat)
    print 'ground truths are', groundTruths
    '''End'''

    mat = np.delete(mat, (0,1), axis=1)
    distMat = getDistMat(mat)
    cl,map = agglomerativeClustering(distMat,k_value)
    printClusters(map)

    '''Calculate external indexes'''
    C = st.calculateIncidenceMatrix(map,size=len(distMat))
    print 'C matrix = ', C
    P = st.calculatePMatrix(groundTruths)
    print 'P matrix = ', P
    RAND, JACCARD = st.calculateExternalIndex(P,C)
    print 'RAND & JACCARD indexes = ',RAND, JACCARD
    '''End'''


    '''Calculate internal indexes'''
    corr = st.calculateCorrelation(distMat,C)
    print 'correlation = ', corr

    # r = st.calculateCorr(distMat,C)
    # print 'dot corr = ', r
    # clusters = agglomerativeClustering(distIyer)
    '''End'''

    #create index/point to cluster list
    cluster_list = columns.createIndexToClusterList(map,len(distMat))

    pca = PCA(n_components=2)
    pca.fit(mat)
    mat_reduced = pca.transform(mat)
    print "Reduced dataset shape:", mat_reduced.shape
    pl.scatter(mat_reduced[:, 0],mat_reduced[:, 1], c=cluster_list)
    pl.show()

    '''Draw Dendrogram'''
    if drawD == None:
        pass
    if drawD==1:
        drawDendrogram(mat)
    '''End'''

if __name__ == '__main__':
    Main()