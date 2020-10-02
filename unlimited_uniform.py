# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 15:06:53 2020

@author: Johan
"""


import numpy as np
from scipy.stats import hypergeom
from itertools import chain


def beta(u_i,i,n):
    #beta(i,u_i)=P(U_i=u_i)
    concat_range=chain(range(int(n/2)),range(int(n/2)+1,n+1))
    prob=0
    for j in concat_range:
        prob+=hypergeom.pmf(u_i,n,j,i)
    return prob/n
#beta(5,9,12) #riktig
#beta(6,10,12)#riktig
#beta(6,12,12)#riktig
#beta(12,12,12)#riktig

    
def rho(i,u_i,n):
    #=number of boxes
    #Rho(i,x) = P(u_12 >= 7 | u_i=x) = P(red majority given u_i=x)
    
    #numerator=P(u_12 >= 7 and u_i=x) = P(majority red and u_i=x)
    nume=0
    for j in range(int((n/2))+1,n+1):
        #P(u_i=x|u_n=j)=hypergeom.pmf(x,n,j,i)
        nume+=hypergeom.pmf(u_i,n,j,i)
    nume=nume/n    
    #denumerator=P(U_i=u_i)
    denume=beta(u_i,i,n)
    return nume/denume


#making functions to find loss2:
def gamma(k,u_i,i,n):
    #gamma(k,u_i,n)=P(X_i+1 | U_i=u_i)
    if u_i>k or k==int(n/2) or (k-u_i)>(n-i):
        return 0
    else :
        return (k-u_i)/(n-i)
    
#gamma(9,6,10,12)
#gamma(12,5,9,12)


def epsilon(u_i,i,n):
    #epsilon(u_i,i,n)=P(X_i+1 = 1 | U_i=u_i)
    prob=0
    b = beta(u_i,i,n)
    concat_range=chain(range(int(n/2)),range(int(n/2)+1,n+1))
    for k in concat_range:
        prob+=gamma(k,u_i,i,n)*hypergeom.pmf(u_i,n,k,i)
    prob=prob/(n*b)        
    return prob

#epsilon(5,9,12) #riktig
#epsilon(6,10,12)#riktig

def find_prob_loss_0_1(n,alpha):
    if n%2 != 0 or n==0:
            raise ValueError('Number of boxes must be an even number above zero.')
    
    m = np.zeros((n,n),dtype=dict)
    for i in range(0,n):
            for u_i in range(0,i+1):
                r=rho(i,u_i,n)
                L0=r #Expected loss when choosing yellow
                L1=1-r #Expected loss when chosing red 
                if i==(n-1):
                    #making the last "Loss2"=alpha
                    m[i,u_i]={"prob":r,"Loss0":L0,"Loss1":L1,"Loss2":alpha}
                else:
                    #don't know the rest of the "loss2" yet, just putting it tp a high value. 
                    m[i,u_i]={"prob":r,"Loss0":L0,"Loss1":L1,"Loss2":1000}
    return m

def find_loss2(matrix,n,alpha): 
    for i in range(n-2,-1,-1): 
        #looping from the second to last row of the matrix to the first one
        for u_i in range(0,i+1):
            #expected loss if the next one is yellow:
            EL_0 = min(matrix[i+1,u_i]["Loss0"],matrix[i+1,u_i]["Loss1"],matrix[i+1,u_i]["Loss2"])
            EL_1 = min(matrix[i+1,u_i+1]["Loss0"],matrix[i+1,u_i+1]["Loss1"],matrix[i+1,u_i+1]["Loss2"])
            eps=epsilon(u_i,i,n)
            matrix[i,u_i]["Loss2"]=alpha + (1-eps)*EL_0 + eps*EL_1    
    return matrix
#dette er riktig for loss2 for 9 og 10. 

 
#MAIN:
def make_matrix(n,alpha):
    matrix=find_prob_loss_0_1(n,alpha)
    matrix=find_loss2(matrix,n,alpha)
    return matrix
mat=make_matrix(12,0.2)
print(mat)

#Now the matrix is done, the next step is then to find the optimal solution:
#3 possible decisions after i boxes are opened:
# 0: choose Z=0 (yellow)
# 1: choose Z=1 (red)
# 2: choose r>i, open one more box. 
#choose the alternative with the samllest expected loss. 




#lage en funksjon med en while løkke, og for hver gang man åpenr en boks skrive inn hvilken farge det er
#på den boksen
#terminerer når loss0 eller loss1 er mindre en loss2. 
#while loss2 er minst fortsetter den å kjøre. 
#lage en variabel som summerer sammen hvor mange røde bokser det er . 
"""
def find_optimal(n,alpha):
    matrix=make_matrix(n,alpha)
    red=0
    loss0=1000
    loss1=1000
    loss2=0
    i=0
    
    while loss2<loss0 and loss2<loss1:
        print("Opening box nr", i+1)
        #skal jeg få brukeren til å skrive inn hvilken farge boksen har??? 
        #eller bare lage en slags matrise selv? 
        #evt andre måter å løse dette på?
        i=i+1
        loss2=loss2+500
  """      
    
    
    
#find_optimal(12,0.2)
    
    
    