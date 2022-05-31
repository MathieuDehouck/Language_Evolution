# -*- coding: utf-8 -*-
"""
Created on Tue May 31 12:42:01 2022

sampling : 

@author: 3b13j
"""

""" This file contains matrices (or way to generate them) to rafine phonetic changes. Each feature can be changed according to certain 
parameter, following a proba weighting represented by a matrix. 

"""



def fill_matrix(rang) :
    
    dic = {} 
    for ran in range(rang+1) :
        liste = []
        for rang2 in range (rang+1) :
            if (abs(ran-rang2)) == 1 : liste.append(4)
            elif  (abs(ran-rang2)) == 2: liste.append(2)
            elif  (abs(ran-rang2)) == 3 : liste.append(1)
            else : liste.append(0)
        dic[ran] = liste
    
    
    
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



#feature 3 : voiced 

f3c = fill_matrix(1)



#Tuple2 




f2c =  {}

tpl_to_ = {'A' :  (0, 0, 0, 0, 0), # approximant
              'N' :  (1, 0, 0, 0, 0), # nasal
              'P' :  (0, 1, 0, 0, 0), # plosive
              'S' :  (0, 0, 1, 0, 0), # fricative / sibilant
              'F' :  (0, 0, 1, 0, 0), # fricative
              'Fl':  (0, 0, 0, 1, 0), # flap
              'T':  (0, 0, 0, 2, 0), # trill
              'L':   (0, 0, 0, 0, 1), # lateral
              'Lf':  (0, 0, 1, 0, 1), # lateral fric
              'Lt':  (0, 0, 0, 1, 1),# lateral trill
              'Afr' : (0, 1, 1, 0, 0)}  #Africates

manner_to_enc = {'A' : 0, # approximant
              'N' :  1 , # nasal
              'P' :  (0, 1, 0, 0, 0), # plosive
              'S' :  (0, 0, 1, 0, 0), # fricative / sibilant
              'F' :  (0, 0, 1, 0, 0), # fricative
              'Fl':  (0, 0, 0, 1, 0), # flap
              'T':  (0, 0, 0, 2, 0), # trill
              'L':   (0, 0, 0, 0, 1), # lateral
              'Lf':  (0, 0, 1, 0, 1), # lateral fric
              'Lt':  (0, 0, 0, 1, 1),# lateral trill
              'Afr' : (0, 1, 1, 0, 0)}  #Africates













# feature 4 : secondary articulation

# 4 valeurs, -1, 11, and two others.TODO conversion of indexes
f4c = fill_matrix(4)

#feature 5 : pre nasal

f5c = fill_matrix(1)

#feature 6 : aspirated

f6c = fill_matrix(1)


MatricesC = [f1c, f2c, f3c, f4c, f5c, f6c]



















#





















