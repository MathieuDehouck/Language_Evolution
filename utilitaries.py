# -*- coding: utf-8 -*-
"""
Created on Wed May  4 11:30:09 2022

@author: 3b13j

Module containing general functions used to print complex objects or write logs
"""

import random 
#from usual_conditions import class_conditions
import copy 


idxC = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1) , (1,2)]
idxV = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1) ]


# functions interacting with features.


def feature_indices(features):
    """
    Gives the coordinates of the indices of a template

    Parameters
    ----------
    features : TYPE
        DESCRIPTION.

    Returns
    -------
    idx : TYPE
        DESCRIPTION.

    """
    idx = []
    for i,fs in enumerate(features):
        for j, f in enumerate(fs):
            idx.append((i,j))

    return idx


def mask_match(mask, phon, voy):
   
    idx = feature_indices(mask)
    idx2 = feature_indices(phon) 
    if idx != idx2 : return False
    
    for ind in idx :
        if mask[ind[0]][ind[1]] != -1 and mask[ind[0]][ind[1]] != phon[ind[0]][ind[1]] :
             
            return False
        
    return True 
    


def get_random_pattern(language) :
    
    
    # TODO ajouter distribution de probabilité sur le nombre de wildcards ? 
    phon = random.choice(language.phonemes)
    base = phon.features
    nb_wild = random.randint(0,len(feature_indices(base)) - 2)
    for i in range(nb_wild ) :
        base = bewilder_pattern(base)
    return base
    
def change_pattern (pattern , vowel,  index, new_value) :
    
    if not vowel :
        ft = [[0, 0, 0],[0,0,0]]
        idx =  [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]
        
    
    else : 
        ft =  [[ 0, 0 , 0],[0,0]]
        idx = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1) ]
    
    
    for ind in idx : 
        
        if ind == index :
            ft[ind[0]][ind[1]] = new_value
        else :
            ft[ind[0]][ind[1]] = pattern[ind[0]][ind[1]]

    
    ft = list_2_tuple(ft)
    return ft
    
   
    
def bewilder_pattern(pattern, index = None, verbose = False) :
    
    idx = feature_indices(pattern)
    
    if type(index ) != tuple : index = random.choice(idx)
    
    if verbose : 
        print(pattern)
        print(idx)
        print(index)
        
    while pattern[index[0]][index[1]] == -1 :
        index = random.choice(idx)
    
    return change_pattern(pattern, len(idx)==5, index, -1)
    


    
    
    
    

def feature_match(f1, f2, verbose=False):
    """input : two feature list 
        returns whether the second is compatible with the first.
        It is therefore required to give the most general one as first input.
    """
    for i in range(len(f1)):
        if f1[i] != -1 :  # not the  wildcard
            if f1[i] != f2[i]:
                if verbose:
                    print("the indexes do not match ", i, "  we expected : ", f1[i], " but read ", f2[i])
                return False
    return True



def vowell(feat):
    """
    checks wether or not the feature given as input encodes a vowell. 
    """
    return feat[0] == 1 and feat[1] == 0



def feature_random_generator():
    
    """
    Used to generate a feature randomly

    Returns
    -------
    feature : feature
        randomly generated
    """
    
    feature = [] 
    # we force  the programm to choose whether the phonem that will be modified will be a cs vw or glode
    # we do not want both values to be set to one (rare and problematic case of a sonorant playing the role of syllable center)
    sy = random.randint (0,1)
    vo = random.randint (0,1)
    while sy == vo and vo == -1 :
        sy = random.randint (0,1)
        vo = random.randint (0,1)
    
    # we check if we 
    # TODO offer the possibility to parametrize the probability to get a wildcard
    # TODO implement roundness as a discrete feature
    
    #height
    wild = random.randint(0,1) 
    if wild == 1 :
        he = -1
    else : 
        he = random.randint(0,3)
        
    #back
    wild = random.randint(0,1) 
    if wild == 1 :
        adv = -1
    else : 
        adv = random.randint(0,3)
        
    feature.append(sy)
    feature.append(vo)
    feature.append(he)
    feature.append(adv)
    
    # all the other boolean features
    for i in range(8) :
        wild = random.randint(0,1) 
        if wild == 1 :
            ft = -1
        else : 
            ft = random.randint(0,1)
        feature.append(ft)
    
    return feature
    


# functions interacting with Language objects

def tuple_2_list(tupl) :
    
    
    liste = []
    for el in tupl : 
        if type(el) == tuple : 
            liste.append(tuple_2_list(el))
        else : liste.append(el)
    return liste


def list_2_tuple(tupl) :
    
    liste = tuple([])
    for el in tupl : 
        if type(el) == list : 
            liste += (list_2_tuple(el),)
        else : liste +=(el,)
        
    return tuple(liste)




def phon_in_dic(dic, phon):
    
    for key in dic : 
        if key == phon : return True
    return False




def tpl_2_candidates(lang, tpl, verbose = False) :
    """
    gives the list of the phonemes of a language that satisfy a conditionned feature template

    Parameters
    ----------
    lang : language
        the language we want to extract candidates from 
    tpl : list
        feature template that we want to be satisfieds

    Returns
    -------
    cands : list
    """
    
    candidates = []
    for phoneme in lang.phonemes :
        if mask_match(tpl, phoneme.features, phoneme.is_Vowel() ) :
            candidates.append(phoneme)
    if verbose :
        print("In ", lang.name, " the following pattern is satisfied by the following list of phonems")
        print(tpl)
        print()
        printl(candidates)
        
    return candidates



def words_containing(mask, language) :
    
    
    wds = []
    for wd in language.voc.values() :
        
        for phon in wd.phonemes : 
            if mask_match(mask, phon.features, phon.is_Vowel) : wds.append(wd)
    return wds



# Functions used to print an object



def printl(liste):
    """Takes a list of complex objects as input and prints them, one per line"""
    for el in liste : print(str(el))



def printd(liste):
    """ Takes a dictionnary as input and print the first object and the second object, and not the address in memory of the object"""
    if liste != None :
        for el in liste :
            if el != None : print(el, "   :   ", str(liste[el]))







