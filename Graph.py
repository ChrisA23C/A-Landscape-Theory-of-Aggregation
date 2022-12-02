import random
import numpy as np
import time
from itertools import *

def printmatrix(matrix): #Красивый вывод матрицы
    for i in matrix:
        s = ''
        for j in i:
            s+=str(j)+' '*(4-len(str(j)))
        print(s)

def genericmatrix(n,maxw): #Генерация матрицы
    matrix = np.random.randint(-maxw, maxw+1, (n,n))
    np.fill_diagonal(matrix, 0)
    return matrix

def genericmatrixones(n): #Генерация матрицы плюс-минус единиц
    matrix = np.array([])
    for i in range(n):
        row = np.array([])
        for j in range(n):
            c = np.random.choice([-1,1])
            row = np.append(row,c)
        matrix = np.append(row,matrix)
    matrix = np.reshape(matrix,(n,n))
    np.fill_diagonal(matrix, 0)
    return matrix

def genericallcombones(n): #Генерация всех возможных матриц из единиц и минус единиц
    for i in product([1,-1], repeat=(n*(n-1))):
        arr = np.array(list(i))
        for j in range(0,n**2+1,n+1):
            arr = np.insert(arr,j,0)
        arr = np.reshape(arr,(n,n))
        yield arr

def genericcomb(n): #Генерация всех возможных коалиций
    s = ''.join(list(map(str,range(0,n))))
    setopt = []
    for i in range(2,len(s)+1):
        for j in combinations(s, i):
            setopt.append(list(map(int, j)))
    return setopt
 
def gencombmatrix(n,setopt): #Генерация матрицы всех возможных коалиций
    v = np.ones(n,int)
    combmatrix = np.array([])
    for i in setopt:
        v2 = np.copy(v)
        for j in range(n):
            if j not in i: v2[j]=-1
        combmatrix = np.append(combmatrix,v2)
    combmatrix.shape = int(len(combmatrix)/n),n
    return combmatrix
    
def psearch(matrix,combmatrix,setopt,p): #Поиск устойчивых коалиций
    x = np.matmul(combmatrix,matrix)
    x = x*combmatrix
    arr = np.amin(x, axis = 1)
    arr2 = np.where(arr >= 0)[0]
    if p == True: print('Sustainable coalitions: ',np.array(setopt,dtype='object')[arr2])

def main(matrix,setopt,combmatrix,p):
    psearch(matrix,combmatrix,setopt,p)
    
#const     
n = 4
maxw = 1
countprint = 1000
###
setopt = genericcomb(n)
combmatrix = gencombmatrix(n,setopt)
start_time = time.time()
print(2**(n*(n-1)),'iterations expected')
for count,i in enumerate(genericallcombones(n)):
    if int(count%countprint)==0: print(count,'-',(time.time() - start_time),'seconds')
    main(i,setopt,combmatrix,False)
print('Search time = %s seconds' % (time.time() - start_time))

