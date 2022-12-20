import random
import time

import numpy as np
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

def genericallmatrixsymones(n): #Генерация всех возможных симметричных матриц из единиц и минус единиц
    for i in product([1,-1], repeat=(n*(n-1)//2)):
        arr = np.array([])
        matrix = np.array([])
        arri = np.array(list(i))
        for j in range(0,n):
            arr = np.array([0]*(n-j))
            if j!=0: arrin = arri[((((j+1)*j)//2)-j):((j+1)*j)//2]
            else: arrin = []
            arr2 = np.hstack([arrin,arr])
            matrix = np.hstack([matrix,arr2])
        matrix = np.reshape(matrix,(n,n))
        matrix = (matrix + matrix.T)
        yield matrix

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
    if p == 1:
        print('Sustainable coalitions: ',np.array(setopt,dtype='object')[arr2])
        print(x[arr2])
        #print(x)
    elif p == 2:
        return len(np.array(setopt,dtype='object')[arr2])
    elif (p == 0) and (len(np.array(setopt,dtype='object')[arr2])>0):
        #print(np.array(setopt,dtype='object')[arr2])
        return 0
    elif (p == 0) and (len(np.array(setopt,dtype='object')[arr2])==0):
        return 1 #Если нет равновесий

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
        d = psearch(i,combmatrix,setopt,0)
        c += d
    print(c,'/',2**(n*(n-1)),'matrices without equilibria')
    print('Search time = %s seconds' % (time.time() - start_time))

def NumBadEdges(matrix,combmatrix,setopt): #Кол-во плохих ребер ломающих граф
    #matrix = genericmatrixsymones(n)
    x = psearch(matrix,combmatrix,setopt,0)
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
        x = psearch(matrix,combmatrix,setopt,0)
        if x==1:
             #if i==1:
                 #print(matrix, a, b)
                 #psearch(matrix,combmatrix,setopt,1
                 #matrix[a][b] = matrix[a][b]*-1
                 #print(matrix, a, b)
                 #psearch(matrix,combmatrix,setopt,1)
             return i #Кол-во ребер ломающих граф
    return -1 #Если граф не ломает ни одно плохое ребро

def DoBadEdgeBreak(matrix,combmatrix,setopt): #Ломают ли одно плохое ребро матрицу?
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
        x = psearch(matrix2,combmatrix,setopt,0)
        if x==1:
            #matrix2[a][b] = matrix2[a][b]*-1
            #print(matrix2)
            #psearch(matrix2,combmatrix,setopt,1)
            #matrix2[a][b] = matrix2[a][b]*-1
            #print(matrix2)
            #psearch(matrix2,combmatrix,setopt,1)
            
            return matrix2 #Если есть плохое ребро ломающее равновесие
    return False

def NumAllSymEdges(setopt,combmatrix): #Статистика по кол-ву симметричных ребер в матрицах с разбиениями
    d = {}
    for i in range(0,n*(n-1)//2+1):
        d[i]=0
    for i in genericallcombones(n):
        x = psearch(i,combmatrix,setopt,0)
        if x==0:
            a = NumSymmetricEdges(i)
            d[a]+=1
    print('Among variants with stable partitions, n symmetric edges for the following number of graphs:',d)

def AreThereBadEdgesDntBreakEq(n,setopt,combmatrix): #Существуют ли симметричные матрицы где не существует плохого ребра ломающего равновесия
    s = ''
    a = 0
    c = 0
    for i in genericallmatrixsymones(n):
        a +=1
        x = DoBadEdgeBreak(i,combmatrix,setopt)
        if type(x)==bool:
            s = 'There are symmetric matrices where there is no edge of breaking equilibrium'
            # Матрицы где плохие ребра не ломают равновесие
        else:
            c+=1
            print(x)
            if c==20: break
    print('The number of symmetric matrices is equal to', a)
    if s=='':
        s = "There aren't symmetric matrices where there is no edge of breaking equilibrium"
    print(s)
    print('count =',c)

def CountOfEqSymMatrix(n,setopt,combmatrix): #Зависимость числа таких равновесий от количества равновесий в графе
    print(n,'peaks')
    s = ''
    a = 0
    c = 0
    d = {}
    for i in genericallmatrixsymones(n):
        a +=1
        x = psearch(i,combmatrix,setopt,2)
        if x not in list(d.keys()): d[x] = 1
        else: d[x]+=1
        #if x == :
        #    print(i)
        #    psearch(i,combmatrix,setopt,1)
        #    break
    print('The number of symmetric matrices is equal to', a)
    d = dict(sorted([[x, d[x]] for x in d.keys()]))
    print('The dependence of the number of such equilibria on the number of equilibria in the graph:',d)

#const
n = 6 #Размер матрицы
maxw = 1 #Максимальный вес
countprint = 10000
###

setopt = genericcomb(n) #Матрица всех возможных коалиций
combmatrix = gencombmatrix(n,setopt) #Матрица всех возможных разбиений (в 1 и -1)
#main(n,setopt,combmatrix)
#NumAllSymEdges(setopt,combmatrix)
#AreThereBadEdgesDntBreakEq(n,setopt,combmatrix)
#CountOfEqSymMatrix(n,setopt,combmatrix)


