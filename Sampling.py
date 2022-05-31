# -*- coding: utf-8 -*-
"""
Created on Tue May 31 12:42:01 2022

sampling : 

@author: 3b13j
"""

""" This file contains matrices (or way to generate them) to rafine phonetic changes. Each feature can be changed according to certain 
parameter, following a proba weighting represented by a matrix. 

"""
import numpy  as np


def fill_matrix(rang) :
    
    mat = np.zeros((rang+1, rang+1))
    
    
    for ran in range(rang+1) :
        liste = []
        for rang2 in range (rang+1) :
            if (abs(ran-rang2)) == 1 : mat[ran, rang2] = 4 
            elif  (abs(ran-rang2)) == 2: mat[ran, rang2] = 2
            elif  (abs(ran-rang2)) == 3 : mat[ran, rang2] = 1 
            
    return mat

def mat_to_adj (mat) :
    dic = {}
    for rang in range ( mat.shape[0]  )  :
        liste = []
        for ind, el in enumerate ( mat[:,rang])   :

            if el != 0 : liste.append ([ind, el])
        dic[rang] = liste
    
    return dic
    
# voc matrices 

#TODO  : fonction qui pourrait faire ça à partir de csv





# VOWELS




#Tuple 1 


#feature 1 : front , values btw 0 and 2

f1v = fill_matrix(2)

#feature 2 : weight, values btw 0 and 6

f2v = fill_matrix(6)



#Tuple2 


# feature 3 : round 

f3v = fill_matrix(1)

#feature 4 : nasalised

f4v = fill_matrix(1)

#feature 5 : nasalised

f5v = fill_matrix(1)


MatricesV = [f1v, f2v, f3v, f4v, f5v]








#CONSONANT





#Tuple 1 


#feature 1 : place of articulation

f1c = fill_matrix(11)

#feature 2 : manner of articulation


manner_list  =  [ (0, 0, 0, 0, 0), # approximant
                (1, 0, 0, 0, 0), # nasal
                (0, 1, 0, 0, 0), # plosive
                (0, 0, 1, 0, 0), # fricative / sibilant
                (0, 0, 1, 0, 0), # fricative
                (0, 0, 0, 1, 0), # flap
                (0, 0, 0, 2, 0), # trill
                (0, 0, 0, 0, 1), # lateral
                (0, 0, 1, 0, 1), # lateral fric
                (0, 0, 0, 1, 1),# lateral trill
                (0, 1, 1, 0, 0) ]  #Africates

l = len(manner_list) 
f2c = np.ones((l, l))


def interpret_manner (mat) :
    dic = mat_to_adj(mat)
    dic_sem = {}
    for k in dic :
        liste = []
        for v in dic[k] :
            liste.append([manner_list[v[0]]  , v[1] ])
        dic_sem [manner_list[k]] = liste
    return dic_sem

manner_adj = interpret_manner(f2c)






#feature 3 : voiced 

f3c = fill_matrix(1)



#Tuple2 







# feature 4 : secondary articulation

# 4 valeurs, -1, 11, and two others.TODO conversion of indexes
f4c = fill_matrix(4)

#feature 5 : pre nasal

f5c = fill_matrix(1)

#feature 6 : aspirated

f6c = fill_matrix(1)


MatricesC = [f1c, f2c, f3c, f4c, f5c, f6c]










"""

être generique, choisir une manière

manière de remplir, vitef

mais manière de les construire
design fort,  choix qui a un sens , cohérent et on le tient , ou qqc de numérique, générique 




le vecteur de feats est composé de deux bouts. 
ds ces 2 bouts, on a des index,

chaque attribut à deu

deux boucles for imbriquées. enumeration des turcs du premier niveau ,ceux du second niceau. 
faire des paires 
on tire au hasard une paire A B 
phon.feature (A B )


crer matrices,  on les met dans des structures qui ont la même forme que les features



"""








#





















