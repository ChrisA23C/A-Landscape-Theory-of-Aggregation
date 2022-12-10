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

def genericmatrixsymones(n): #Генерация матрицы плюс-минус единиц с симметричными ребрами
    matrix = np.array([])
    for i in range(n):
        row = np.array([])
        for j in range(n):
            if i<j: c = np.random.choice([-1,1])
            else: c = 0
            row = np.append(row,c)
        matrix = np.append(row,matrix)
    matrix = np.reshape(matrix,(n,n))
    matrix = np.fliplr(matrix)
    matrix = np.tril(matrix) + np.triu(matrix.T, 1)
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
    for i in range(1,len(s)+1):
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
    global imparr
    x = np.transpose(matrix)
    x = np.matmul(combmatrix,x)
    x = x*combmatrix
    arr = np.amin(x, axis = 1)
    arr2 = np.where(arr >= 0)[0]
    if p == True:
        print('Sustainable coalitions: ',np.array(setopt,dtype='object')[arr2])
        print(arr2)
        print(x[arr2])
        print(x)
        #print(x)
    elif (p == False) and (len(np.array(setopt,dtype='object')[arr2])>0):
        #print(np.array(setopt,dtype='object')[arr2])
        return 0
    elif (p == False) and (len(np.array(setopt,dtype='object')[arr2])==0):
        return 1

def save(d,countname,matrix): #Сохранение матрицы в файл
    if d == 0:
        np.savetxt('filestxt/ex'+str(countname)+'.txt',i)
        np.save('filesnpy/ex'+str(countname)+'.npy',i)

def NumSymmetricEdges(matrix): #Счет симметричных ребер
    c = 0
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if (matrix[i][j]==matrix[j][i]) and (i!=j): c+=1
    return(c//2)

def main(n,setopt,combmatrix): #Кол-во графов без равновесий
    print(n,'peaks')
    print(2**(n*(n-1)),'iterations expected')
    c = 0
    start_time = time.time()
    for count,i in enumerate(genericallcombones(n)):
        if int(count%countprint)==0: print(count,'iteration -',(time.time() - start_time),'seconds')
        d = psearch(i,combmatrix,setopt,False)
        c += d
    print(c,'/',2**(n*(n-1)),'matrices without equilibria')
    print('Search time = %s seconds' % (time.time() - start_time))

def NumBadEdges(matrix,combmatrix,setopt): #Кол-во плохих ребер ломающих граф
    #matrix = genericmatrixsymones(n)
    x = psearch(matrix,combmatrix,setopt,False)
    if x==1:
         return 0
         exit
    last = []
    a = 0
    b = 0
    for i in range(1,((n*(n-1))//2)+1):
        while True:
            a = random.randrange(n)
            b = random.randrange(n)
            if ([a,b] not in last) and (([b,a]) not in last) and a!=b: break
        last.append([a,b])
        matrix[a][b] = matrix[a][b]*-1
        x = psearch(matrix,combmatrix,setopt,False)
        if x==1:
             #if i==1:
                 #print(matrix, a, b)
                 #psearch(matrix,combmatrix,setopt,True)
                 #matrix[a][b] = matrix[a][b]*-1
                 #print(matrix, a, b)
                 #psearch(matrix,combmatrix,setopt,True)
             return i #Кол-во ребер ломающих граф
    return -1 #Если граф не ломает ни одно плохое ребро

def DoBadEdgeBreak(matrix,combmatrix,setopt): #Ломают ли одно плохое ребро матрицу?
    #matrix = genericmatrixsymones(n)
    x = psearch(matrix,combmatrix,setopt,False)
    last = []
    a = 0
    b = 0
    for i in range(1,((n*(n-1))//2)+1):
        while True:
            a = random.randrange(n)
            b = random.randrange(n)
            if ([a,b] not in last) and (([b,a]) not in last) and a!=b: break
        last.append([a,b])
        matrix2 = np.copy(matrix)
        matrix2[a][b] = matrix2[a][b]*-1
        x = psearch(matrix2,combmatrix,setopt,False)
        if x==0:
            print(matrix)
            print(psearch(matrix,combmatrix,setopt,True))
            print(matrix2)
            print(psearch(matrix2,combmatrix,setopt,True))
            print(a,b)
            return True
    return matrix2

def NumAllSymEdges(setopt,combmatrix): #Статистика по кол-ву симметричных ребер в матрицах с разбиениями
    d = {}
    for i in range(0,n*(n-1)//2+1):
        d[i]=0
    for i in genericallcombones(n):
        x = psearch(i,combmatrix,setopt,False)
        if x==0:
            a = NumSymmetricEdges(i)
            d[a]+=1
    print('Among variants with stable partitions, n symmetric edges for the following number of graphs:',d)

#const
n = 4
maxw = 1
countprint = 10000
###

setopt = genericcomb(n)
combmatrix = gencombmatrix(n,setopt)

#main(n,setopt,combmatrix)
#NumAllSymEdges(setopt,combmatrix)

