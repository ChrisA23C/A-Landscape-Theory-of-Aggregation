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
    matrix = np.random.randint(-maxw, maxw+1, (n,n))
    np.fill_diagonal(matrix, 0)
    return matrix

def genericcomb(n):
    s = ''.join(list(map(str,range(0,n))))
    setopt = []
    for i in range(2,len(s)+1):
        for j in combinations(s, i):
            setopt.append(list(map(int, j)))
    return setopt
 
def gencombmatrix(n,setopt):
    v = np.ones(n,int)
    combmatrix = np.array([])
    for i in setopt:
        v2 = np.copy(v)
        for j in range(n):
            if j not in i: v2[j]=-1
        combmatrix = np.append(combmatrix,v2)
    combmatrix.shape = int(len(combmatrix)/n),n
    return combmatrix
    
def psearch(matrix,combmatrix,setopt):
    x = np.matmul(combmatrix,matrix)
    x = x*combmatrix
    arr = np.amin(x, axis = 1)
    arr2 = np.where(arr >= 0)[0]
    print('Sustainable coalitions: ',np.array(setopt,dtype='object')[arr2])
    
#const     
n = 6
maxw = 1
###
matrix = genericmatrix(n,maxw)
#matrix = np.array([[0,1,2],[1,0,-1],[2,-1,0]])
print(matrix)
#printmatrix(matrix)
#start_time = time.time()
setopt = genericcomb(n)
combmatrix = gencombmatrix(n,setopt)
start_time = time.time()
psearch(matrix,combmatrix,setopt)
print('Search time = %s seconds' % (time.time() - start_time))
