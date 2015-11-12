__author__ = 'harshad'

import numpy as np
from scipy.spatial import distance
from scipy.cluster.hierarchy import dendrogram, linkage
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
    for row in distMat:
        value = str(row) + '\n'
        file.write(value)
    file.close()
    return distMat

def agglomerativeClustering(distMat,K):
    cl_list = []
    map = [ ]
    for a in range(len(distMat)):
        map.append([a])
    for i in range(len(distMat)):
        cl_list.append([i])

    print 'original list ',cl_list
    dMat = distMat
    ind_i = -1
    ind_j = -1
    least = sys.float_info.max
    i = 0
    j = 0
    flag = False

    while 1:
        if len(dMat) == K and len(dMat[0])==K:
            print 'left dmat = ', dMat
            print 'cl_list ',cl_list
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
        print least
        print ind_i, ind_j

        # in1 = ind_i
        # in2 = ind_j
        # ind_i = min(in1,in2)
        # ind_j = max(in1,in2)
        ind_i,ind_j = getMinMax(ind_i,ind_j)

        temp1 = map[ind_i]
        temp2 = map[ind_j]
        temp3 = [ ]
        for each in temp1:
            temp3.append(each)
        for each in temp2:
            temp3.append(each)
        map[ind_i] = temp3

        # map[in1] = [map[in1],map[in2]]
        u1 = map.pop(ind_j)

        for k in range(len(dMat[0])):
             dMat[ind_i,k] = min(dMat[ind_i,k],dMat[ind_j,k])
        for k in range(len(dMat)):
             dMat[k,ind_i] = min(dMat[k,ind_i],dMat[k,ind_j])

        print 'merging clusters ',ind_i,' & ', ind_j,' with value= ',least

        #at ind_i index, we are storing the new distances of the newly formed cluster
        dMat = np.delete(dMat,ind_j,axis=0)
        dMat = np.delete(dMat,ind_j,axis=1)

        #remove b and merge that cluster with a cluster
        b = cl_list.pop(ind_j)
        print 'after removing merged cluster', cl_list
        a = cl_list[ind_i]
        temp = []
        temp.append(a)
        temp.append(b)
        cl_list[ind_i] = temp
        # org = map[ind_i]
        # to_add = map.pop(ind_j)
        # map[ind_i] = [org,to_add]
        print 'after updating cl lsit', cl_list
    # print 'final results map', map
    return cl_list,map

def Main():
    # pathInput = str(raw_input('Please Enter the path of the input txt file'))
    pathCho = '/Users/harshad/PycharmProjects/Project2/cho.txt'
    pathIyer = '/Users/harshad/PycharmProjects/Project2/iyer.txt'
    matCho = loadData(pathCho)
    matIyer = loadData(pathIyer)
    matCho = np.delete(matCho, (0,1), axis=1)
    matIyer = np.delete(matIyer, (0,1), axis=1)

    print len(matCho)
    link_matrix = linkage(matCho,'single')
    # print 'linkage matrix- ',link_matrix

    plt.figure(figsize=(20,8))
    plt.title("Hierarchical Agglomerative Clustering")
    dendrogram(link_matrix)
    plt.show()

    # print 'matrix for cho.txt after removing ground truths'
    # printMat(matCho)
    # print 'matrix for iyer.txt after removing ground truths'
    # printMat(matIyer)

    # toyMat = np.reshape([0, 7, 3 ,7 ,0 ,2, 3, 2, 0],(3,3))
    # ''' 0 7 3
    #     7 0 2
    #     3 2 0
    # '''
    # cl_list = agglomerativeClustering(toyMat)

    distCho = getDistMat(matCho)
    print distCho[298,0]
    # clusters = agglomerativeClustering(distCho)

    toyMat = np.reshape( [0,1,2,2,3,1,0,2,4,3,2,2,0,1,5,2,4,1,0,3,3,3,5,3,0],(5,5))

    cl,map = agglomerativeClustering(distCho,6)
    i=0
    for each in map:
        print 'for cluster',i,' ',each
        i = i + 1
    # clusters = agglomerativeClustering(distIyer)

if __name__ == '__main__':
    Main()