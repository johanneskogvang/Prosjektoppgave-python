# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 09:27:31 2020

@author: Johan
"""

import numpy as np
import unlimited_uniform


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

nodes=make_node_matrix(unlimited_uniform.mat)
print(nodes)



def visualize_optimal(mat,filename, radius):
    file_location_and_name=r"C:\\Users\\Johan\\OneDrive\\Documents\\NTNU-Host-2020\\Prosjektoppgave\\Prosjektoppgave-python\\" + filename 
    file = open(file_location_and_name,"a")

    start_of_doc=r"""
\begin{tikzpicture}[
    treenodeT/.style={
      circle, align=center},
    node distance=2.4cm,
    ]
    """
    file.write(start_of_doc)
    
    #the first node:
    string = "\DoNode{N0-0}{" + str(mat[0][0]["e0"]) + "}{" + str(mat[0][0]["e1"]) + "}{1}{" + str(mat[0][0]["col1"]) + "}{" + str(mat[0][0]["col2"]) + "}{" + str(radius) + "};\n    "
    file.write(string)
    
    n = len(mat)
    for i in range(1,n):
        for j in range(i+1):
            
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
    
visualize_optimal(nodes,"latex_test4.tex",1.2)
#file2 = open("latex_test2.tex",'a')
#file2.close()
