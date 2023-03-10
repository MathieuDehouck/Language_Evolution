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





# PARAMETRISATION OF THE PHONETIC CHANGE. 



# First step : small methods to create matrices

def fill_matrix(rang) :
    """
    creates a matrix that simulate the change from a numerical value to another, the change is gradual and have a bigger chance to happen between close values

    """  
    mat = np.zeros((rang+1, rang+1))
    for ran in range(rang+1) : 
        for rang2 in range (rang+1) :
            if (abs(ran-rang2)) == 1 : mat[ran, rang2] = 4 
            elif  (abs(ran-rang2)) == 2: mat[ran, rang2] = 2
            elif  (abs(ran-rang2)) == 3 : mat[ran, rang2] = 1 
            
    return mat





def mat_to_adj (mat) :
    """ 
    Converts a matrix into its representation as an adjacency list
    """
    dic = {}
    for rang in range ( mat.shape[0]  )  :
        liste = []
        for ind, el in enumerate ( mat[:,rang])   :

            if el != 0 : liste.append ([ind, el])
        dic[rang] = liste
    
    return dic
    





def dislike (liste, mat, coef = 3) :
    """
    Diminish the weight of values we do not want to see too often. 
    """
    x, y = mat.shape
    for j in range(0, x) : 
      for i in range(0,y) :
        if j in liste :
            mat[i][j] = mat[i][j]  / coef
            
    return mat





# VOWELS



#Tuple 1 



#feature 1 : height, values btw 0 and 6

f1v = fill_matrix(6)
disliked_heights = [5, 2, 1]
f1v = dislike(disliked_heights, f1v)



#feature 2 : weight, values btw 0 and 6

f2v = fill_matrix(2)



# feature 3 : round 

f3v = fill_matrix(1)



#Tuple2 



#feature 4 : nasalised

f4v = fill_matrix(1)



#feature 5 : nasalised

f5v = fill_matrix(1)



#All information condensed : 
MatricesV = ((f1v, f2v, f3v),( f4v, f5v))
inputsV = ((range(0,7), range(0, 4), range(0,2) ), (range(0,2), range(0,2)))





#CONSONANT



#Tuple 1 



#feature 1 : place of articulation

f1c = fill_matrix(11)
disliked_articulation_place  = [0, 1, 2, 6]
f1c = dislike(disliked_articulation_place, f1c)



#feature 2 : manner of articulation

manner_2_ind  =  { (0, 0, 0, 0, 0) : 1, # approximant
                (1, 0, 0, 0, 0) : 1, # nasal
                (0, 1, 0, 0, 0) : 1, # plosive
                (0, 0, 1, 0, 0) : 1, # fricative / sibilant
                (0, 0, 1, 0, 0) : 1, # fricative
                (0, 0, 0, 1, 0) : 1, # flap
                (0, 0, 0, 2, 0) : 1, # trill
                (0, 0, 0, 0, 1) : 1, # lateral
                (0, 0, 1, 0, 1) : 1, # lateral fric
                (0, 0, 0, 1, 1) : 1,# lateral trill
                (0, 1, 1, 0, 0) : 1 }  #Africates



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


secondary_place = [ 0, 1, 5, 11]

sec_place_2_ind = { 11 : 3 , 1 : 1 , 0:0 , 5 : 2}

l = len(manner_list) 
f2c = np.ones((l, l))

def interpret_manner (mat) :
    """
    small function to covnerts non linear values to their position in the matrix
    """
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
f4c = fill_matrix(3)



def interpret_sec_manner (mat) :
    dic = mat_to_adj(mat)
    dic_sem = {}
    for k in dic :
        liste = []
        for v in dic[k] :
            liste.append([secondary_place[v[0]]  , v[1] ])
        dic_sem [secondary_place[k]] = liste
    return dic_sem

sec_manner_adj  =  interpret_sec_manner(f4c)

#feature 5 : pre nasal

f5c = fill_matrix(1)



#feature 6 : aspirated

f6c = fill_matrix(1)



# Every information sum up
MatricesC = ((f1c, f2c, f3c),( f4c, f5c, f6c))
inputsC = ((range(0,11), manner_list, range(0,2) ), (secondary_place, range(0,2), range(0,2)))










# PARAMETRISATION OF THE CHANGE GENERATION



#Parametrisation of the type of change applied
change_types = ["P", "M", "S"]
weights_change_type = [10, 7, 2 ]



#Parametrisation of the number of condition
weights_nb_cond = [3, 5, 3, 2]
weights_same_feature = [5, 5]



#parametrisation of the probability a feature is modified
featureV_weights = [4, 4, 2, 3, 2]
featureC_weights = [5,5, 4, 4, 1, 3]



nb_rel_cond = [0 , 1, 2, 3 , 4]
weights_nb_rel_cond = [ 2, 8, 7, 3, 1]
weights_nb_rel_cond_normal = np.random.normal(
    loc= 2.0,       # The mean of the distribution
    scale=1.0,      # The standard deviation 
    size=5     # The size or shape of your array
)



weight_Scond = [2, 8]
weigt_A_R = [2, 4]

weights_rel_pos = [4, 2, 1]
weights_abs_pos = [4, 2, 1]



#Parametrization of the number of condition
nb_extensions = [0, 1, 2, 3, 4, 5]
weights_extensions = [8, 4, 6, 3,2, 2]
weights_extensions2 = [12, 8, 3, 1,1, 1]

weights_extensions_normal = np.random.normal(
    loc= 2.0,       # The mean of the distribution
    scale=1.0,      # The standard deviation 
    size=6       # The size or shape of your array
)