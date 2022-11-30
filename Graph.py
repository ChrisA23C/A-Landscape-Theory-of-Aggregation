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

def genericcomb(n):
    s = ''.join(list(map(str,range(0,n))))
    setopt = []
    for i in range(2,len(s)+1):
        for j in combinations(s, i):
            setopt.append(list(map(int, j)))
    return setopt
 
def psearch(matrix,n,setopt):
    v = np.ones(n,int)
    for i in setopt:
        v2 = np.copy(v)
        for j in range(n):
            if j not in i: v2[j]=-1
        x = np.dot(v2,matrix)
        x = x*v2
        if (x>=0).all(): print('Sustainable coalitions: ',i,'; Win difference: ',x)

   
start_time = time.time()
#const     
n = 3
maxw = 10
###
#matrix = genericmatrix(n,maxw)
matrix = np.array([[0,1,2],[1,0,-1],[2,-1,0]])
print(matrix)
#printmatrix(matrix)
#start_time = time.time()
setopt = genericcomb(n)
#start_time = time.time()
psearch(matrix,n,setopt)
print('time = %s seconds' % (time.time() - start_time))
