# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 14:06:03 2020

@author: Johan
"""


def visualize_optimal(matrix,filename, radius):
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
    
    
    #The first node, before opening any boxes:
    l0 = matrix[0][0]["Loss0"]
    l1 = matrix[0][0]["Loss1"]
    l2 = matrix[0][0]["Loss2"]
    
    E0=l1+l2
    E1=l0+l2
    E2=l0+l2
    
    colour1="green"
    colour2="green"
    if l0<l2 and l0<l1: #Yellow has least loss
        colour1 = "yellow"
        colour2 = "yellow"
    elif l1<l2 and l1<l0: #red has the least loss
        colour1 = "red"
        colour2 = "red"
    elif l0<=l2 and l1<=l2 and l0==l1: #least loss to choose, but same loss for red and yellow.
        colour1 = "yellow"
        colour2 = "red"        
    #Here, if the least loss is green and either red or yellow (they are equal), then we are stopping
       
    string = "\DoNode{N0}{" + str(E0) + "}{" + str(E1) + "}{1}{" + colour1 + "}{" + colour2 + "}{" + str(radius) + "}"
    file.write(string)
    
    #maybe make a list of all the nodes that are in the level of the tree that you are at??
    #here the list would only consist of N0
       
    
    #maybe make a recursive function? dont think the while-loop will catch every brach of the tree. 
    while l2<l0 and l2<l1: #the least loss to continue opening boxes
        
        
    
    
    
    
    
    end_of_file= r"""
\end{tikzpicture}
"""
    file.write(end_of_file)
    
    file.close()
    
    
    
    
    

visualize_optimal(mat,"latex_test7.tex",1.2)    
    