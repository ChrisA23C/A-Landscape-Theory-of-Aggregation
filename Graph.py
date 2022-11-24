import random
import numpy as np
import time
from itertools import *

def printmatrix(matrix):
    for i in matrix:
        s = ''
        for j in i:
            s+=str(j)+' '*(4-len(str(j)))
        print(s)

def genericmatrix(n,maxw):
    matrix = np.random.randint(-maxw, maxw, (n, n))
    np.fill_diagonal(matrix, 0)
    return matrix

def psearch(matrix,n):
    s = ''.join(list(map(str,range(1,n+1))))
    setopt = []
    for i in range(2,len(s)+1):
        for j in combinations(s, i):
            setopt.append(list(map(int, j)))
    for i in setopt:
        matrix2 = np.copy(matrix)
        for k in range(len(matrix)):
            if (k+1 not in i): matrix2[k] = -1*matrix2[k]
        n = np.sum(matrix2,axis = 0)
        for k in range(len(n)):
            if (k+1 not in i): n[k] = -1*n[k]
        #print(i,n)
        if (n>=0).all(): print('Sustainable coalitions: ',i,'; Win difference: ',n)
        
    

   
start_time = time.time()
#const     
n = 4
maxw = 10
###
matrix = genericmatrix(n,maxw)
#matrix = np.array([[0,1,2],[1,0,-1],[2,-1,0]])
print(matrix)
#printmatrix(matrix)
psearch(matrix,n)
print('time = %s seconds' % (time.time() - start_time))
