# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 13:34:45 2020

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
    
def rho(i,u_i,n):
    #=number of boxes
    #Rho(i,x) = P(u_12 >= 7 | U_i=u_i) = P(red majority given U_i=u_i)
    
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


def epsilon(u_i,i,n):
    #epsilon(u_i,i,n)=P(X_i+1 = 1 | U_i=u_i)
    prob=0
    b = beta(u_i,i,n)
    concat_range=chain(range(int(n/2)),range(int(n/2)+1,n+1))
    for k in concat_range:
        prob+=gamma(k,u_i,i,n)*hypergeom.pmf(u_i,n,k,i)
    prob=prob/(n*b)        
    return prob


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
"""
def find_loss2(matrix,n,alpha,beta):
#def find_loss2(matrix,n,alpha): 
    for i in range(n-2,-1,-1): 
        #looping from the second to last row of the matrix to the first one
        #P(T=i+1|T>i) = 1/(12-i) =  P(get stopped in next | not stopped until now) = PT
        PT = 1/(n-i)    
        print(PT)
        for u_i in range(0,i+1):
            #expected loss if the next one is yellow:
            EL_0 = min(matrix[i+1,u_i]["Loss0"],matrix[i+1,u_i]["Loss1"],matrix[i+1,u_i]["Loss2"])
            #expected loss if the next one is red. 
            EL_1 = min(matrix[i+1,u_i+1]["Loss0"],matrix[i+1,u_i+1]["Loss1"],matrix[i+1,u_i+1]["Loss2"])
            eps=epsilon(u_i,i,n)
            matrix[i,u_i]["Loss2"]=alpha + (1-PT)*((1-eps)*EL_0 + eps*EL_1) + PT*beta    
    return matrix
"""
def find_loss2(matrix,n,alpha,beta):
#def find_loss2(matrix,n,alpha): 
    for i in range(n-2,-1,-1): 
        #looping from the second to last row of the matrix to the first one
        #P(T=i+1|T>i) = 1/(12-i) =  P(get stopped in next | not stopped until now) = PT
        PT = 1/(n-i)
        if i==0: #P(T=1|T>0)=0. means that you are able to open the first box without getting stopped
            PT = 0
        print(PT)
        for u_i in range(0,i+1):
            #expected loss if the next one is yellow:
            EL_0 = min(matrix[i+1,u_i]["Loss0"],matrix[i+1,u_i]["Loss1"],matrix[i+1,u_i]["Loss2"])
            #expected loss if the next one is red. 
            EL_1 = min(matrix[i+1,u_i+1]["Loss0"],matrix[i+1,u_i+1]["Loss1"],matrix[i+1,u_i+1]["Loss2"])
            eps=epsilon(u_i,i,n)
            matrix[i,u_i]["Loss2"]=alpha + (1-PT)*((1-eps)*EL_0 + eps*EL_1) + PT*beta    
    return matrix
 

def make_matrix(n,alpha, beta):
    matrix=find_prob_loss_0_1(n,alpha)
    matrix=find_loss2(matrix,n,alpha,beta)
    return matrix



#Now the matrix is done, the next step is then to find the optimal solution:
def make_node_matrix(matrix):
    node_mat=np.zeros_like(matrix)
    n = len(matrix)
    
    for i in range(n):
        for j in range(i+1):
            l0 = matrix[i][j]["Loss0"]
            l1 = matrix[i][j]["Loss1"]
            l2 = matrix[i][j]["Loss2"]
            e0 = round(l1+l2,14) #=sum of losses - l0
            e1 = round(l0+l2,14)
            e2 = round(l0+l1,14)
            
            col1 = "green"
            col2 = "green"
            
            if l0<l2 and round(l0,3)<round(l1,3): #if yellow has the smallest loss
                col1 = "yellow"
                col2 = "yellow"
            elif l1<l2 and round(l1,3)<round(l0,3): #red has the smallest loss
                col1 = "red"
                col2 = "red"
            elif l0<l2 and round(l0,3) == round(l1,3): #red and yellow has the smallest loss, but they are equal
                col1 = "yellow"
                col2 = "red"
             
            name = "N" + str(i) + "-" + str(j)
            node_mat[i][j] = {"name":name, "col1":col1, "col2":col2, "e0":e0, "e1":e1, "e2":e2}
    
    return node_mat





def visualize_optimal(mat,filename, radius):
    file_location_and_name=r"C:\\Users\\Johan\\OneDrive\\Documents\\NTNU-Host-2020\\Prosjektoppgave\\Prosjektoppgave-python\\Tikz-trees\\" + filename 
    file = open(file_location_and_name,"a")

    start_of_doc=r"""
\begin{tikzpicture}[
    treenodeT/.style={
      circle, align=center},
    node distance=1.5cm,
    ]
    """
    file.write(start_of_doc)
    
    #the first node:
    string = "\DoNode{N0-0}{" + str(mat[0][0]["e0"]) + "}{" + str(mat[0][0]["e1"]) + "}{1}{" + str(mat[0][0]["col1"]) + "}{" + str(mat[0][0]["col2"]) + "}{" + str(radius) + "};\n    "
    file.write(string)
    
    n = len(mat)
    for i in range(1,n):
        #lage en loop her med sånn, hvis ingen av nodene i raden over er grønne, break out of these for loops. 
        #could have made a while loop of this as well, but for now this is a for loop
        g=0
        if i>1:
            for j in range(i):
                if str(mat[i-1][j]["col1"]) == "green": #checing if any of the nodes in the row above are green
                    g=1
            if g == 0: #if none of the nodes on the row above are green, break out of the for loop
                    #break out of the for loop
                print("breaking loop at row", i)
                break

        #if some of the nodes above are green, we continue to build the tree:        
        for j in range(i+1):
            #if mat[i-1][j-1]["col1"]!="green" and mat[i-1][j]["col1"] != "green": #if neither of the top nodes are parents
            
            if j==0: #we are at the left side of the tree. the only possible parent i at (i-1,j)
                if mat[i-1][j]["col1"] == "green": #if we continue to open boxes in the last node
                    string = "\DoNode[below of=" + mat[i-1][j]["name"] + ", left of= " + mat[i-1][j]["name"] + "]{"+ mat[i][j]["name"] +"}{" + str(mat[i][j]["e0"]) + "}{" + str(mat[i][j]["e1"]) + "}{1}{" + str(mat[i][j]["col1"]) + "}{" + str(mat[i][j]["col2"]) + "}{" + str(radius) + "};\n    "
                    file.write(string)
                    string2 = "\draw[->] (" + str(mat[i-1][j]["name"]) + ") -- (" + mat[i][j]["name"] + ");\n    "
                    file.write(string2)
            elif j==i: #we are at the right side of the tree. the only possible parent is at (i-1,j-1)
                if mat[i-1][j-1]["col1"] == "green": #if we continue to open boxes in the last node.
                    string = "\DoNode[below of=" + mat[i-1][j-1]["name"] + ", right of= " + mat[i-1][j-1]["name"] + "]{"+ mat[i][j]["name"] +"}{" + str(mat[i][j]["e0"]) + "}{" + str(mat[i][j]["e1"]) + "}{1}{" + str(mat[i][j]["col1"]) + "}{" + str(mat[i][j]["col2"]) + "}{" + str(radius) + "};\n    "
                    file.write(string)
                    string2 = "\draw[->] (" + str(mat[i-1][j-1]["name"]) + ") -- (" + mat[i][j]["name"] + ");\n    "
                    file.write(string2)
            else: #we are not on either side of the tree
                if mat[i-1][j-1]["col1"]=="green": #if the left top node is a parent
                    string = "\DoNode[below of=" + mat[i-1][j-1]["name"] + ", right of= " + mat[i-1][j-1]["name"] + "]{"+ mat[i][j]["name"] +"}{" + str(mat[i][j]["e0"]) + "}{" + str(mat[i][j]["e1"]) + "}{1}{" + str(mat[i][j]["col1"]) + "}{" + str(mat[i][j]["col2"]) + "}{" + str(radius) + "};\n    "
                    file.write(string)
                    string2 = "\draw[->] (" + str(mat[i-1][j-1]["name"]) + ") -- (" + mat[i][j]["name"] + ");\n    "
                    file.write(string2)
                    if mat[i-1][j]["col1"] == "green": #if the top right node also is a parent
                        string3 = "\draw[->] (" + str(mat[i-1][j]["name"]) + ") -- (" + mat[i][j]["name"] + ");\n    "
                        file.write(string3)
                elif mat[i-1][j-1]["col1"] != "green" and mat[i-1][j]["col1"]=="green": #left is not a parent, but the right is
                    string = "\DoNode[below of=" + mat[i-1][j]["name"] + ", left of= " + mat[i-1][j]["name"] + "]{"+ mat[i][j]["name"] +"}{" + str(mat[i][j]["e0"]) + "}{" + str(mat[i][j]["e1"]) + "}{1}{" + str(mat[i][j]["col1"]) + "}{" + str(mat[i][j]["col2"]) + "}{" + str(radius) + "};\n    "
                    file.write(string)
                    string2 = "\draw[->] (" + str(mat[i-1][j]["name"]) + ") -- (" + mat[i][j]["name"] + ");\n    "
                    file.write(string2)
                    
    end_of_file= r"""
\end{tikzpicture}
"""
    file.write(end_of_file)
    
    file.close()
    


def main(n,alpha,beta, filename, node_radius):
    mat_losses=make_matrix(n,alpha,beta)
    print(mat_losses)
    nodes=make_node_matrix(mat_losses)
    visualize_optimal(nodes,filename, node_radius)
    
#main(12,0.2,0.5,"limited_uniform_a0.2_b0.5.tex", 0.6)    
main(12,0.2,0.5,"limited_uniform_a0.2_b0.5.tex", 0.6)    
#print(make_matrix(12,0.0000000000000000001))
    
    
    
    
    
    
    
    
    
    
    
    
    
    