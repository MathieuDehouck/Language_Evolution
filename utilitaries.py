# -*- coding: utf-8 -*-
"""
Created on Wed May  4 11:30:09 2022

@author: 3b13j

Module containing general functions used to print complex objects or write logs
"""

import random 
import Sampling
#from usual_conditions import class_conditions


#TODO : remplacer par une instance de Voy ou de C pour éviter la perte de généralisation en cas de changement de la forme générale d'un feature.
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
    """
    Retuen True if the feature template of a phoneme matches the restriction imposed by a mask

    Parameters
    ----------
    mask : list
        A feature template (potentially with wildcards)
    phon : list 
        The feature template of a phoneme.
    voy :  bool
        does the  feature template examined concerns vowells ? 

    
    """
    if voy :  idx =  idxV
    else : idx = idxC
             
    if len(mask[1]) != len(phon[1]) : return False
    
    for ind in idx :
        if mask[ind[0]][ind[1]] != -1 and mask[ind[0]][ind[1]] != phon[ind[0]][ind[1]] :
            return False      
    return True 
    




def syl_match(s1, s2):
    """ 
    Computes whether a syllable does have the same stress pattern as another. 
    Less restrictive than the equals method. 
    """
    return s1.stress == s2.stress and s1.length == s2.length and s1.tone == s2.tone





def get_random_pattern(language) :
    """
    Creates a random feature pattern that can be satisfied in a given language
    """
    phon = random.choice(language.phonemes)
    base = phon.features
    nb_wild = random.choices(Sampling.nb_extensions, Sampling.weights_extensions)[0]
    for i in range(nb_wild ) :
        base = bewilder_pattern(base)
    return base
    




#TODO : can we computationnally improve this part ?
def change_pattern (pattern , vowel,  index, new_value) :
    """

    Parameters
    ----------
    pattern : list
        feature pattern
    vowel : bool
        does the pattern match a vowel ? 
    index : index that must be modified
    new_value : output value

    Returns
    -------
    ft : the new feature pattern, with the change applied.

    """
    
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
    
   
    
    
   
#TODO modify to improve computation efficiency
def bewilder_pattern(pattern, index = None, verbose = False) :
    """
    Transforms an index of a pattern into a wildcard

    Parameters
    ----------
    pattern : list
        patter to bewilder
    index : TYPE, optional
        DESCRIPTION. The default is None.
    verbose : TYPE, optional
        DESCRIPTION. The default is False.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    idx = feature_indices(pattern)
    
    if type(index ) != tuple : index = random.choices(idx)[0]
    
    if verbose : 
        print(pattern)
        print(idx)
        print(index)
    
    while pattern[index[0]][index[1]] == -1 :
        index = random.choice(idx)
    
    return change_pattern(pattern, len(idx)==5, index, -1)
    
    



# functions interacting with Language objects
def tuple_2_list(tupl) :
    """
    Transforms a tuple into a list
    """
    
    liste = []
    for el in tupl : 
        if type(el) == tuple : 
            liste.append(tuple_2_list(el))
        else : liste.append(el)
    return liste






def list_2_tuple(liste) :
    """
    Transforms any kind of list into a tuple.
    Iterative version checking if the list represents a Consonant or a Vowel.
    Proven to be computationnaly speaking better than its recursive counterpart.
    """
    
    tpl1 = ()
    for el in liste[0] : 
        if type(el) == list : el = tuple(el)
        tpl1+= ( el,)
        
    
    tpl2 = ()
    for el in liste [1] : tpl2+= ( el,)
    
    return (tpl1, tpl2)





def list_2_tuple2(tupl) :
    """
    Transforms any kind of list into a tuple.
    Recursive version twice slower than the other one.
    """
    
    liste = tuple([])
    for el in tupl : 
        if type(el) == list : 
            liste += (list_2_tuple2(el),)
        else : liste +=(el,)
        
    return tuple(liste)





def phon_in_dic(dic, phon):
    """ 
    Checks whether a phoneme is in a dic or not.
    """
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




#TODO brute methods that makes the program really slower. Do profiling here
#Idea to speed computation, try applying this before changing the word ? Not really better bcs same number of application than mask_match
def words_containing(mask, language) :
    """
    Return the list of words in a language that 
    """
    wds = []
    for wd in language.voc.values() :    
        for phon in wd.phonemes : 
            if mask_match(mask, phon.features, phon.is_Vowel) : wds.append(wd)
    return wds





# Functions used to print an object





def printl(liste):
    """
    Takes a list of complex objects as input and prints them, one per line
    """
    for el in liste : print(str(el))





def printd(liste):
    """ 
    Takes a dictionnary as input and print the first object and the second object, and not the address in memory of the object
    """
    if liste != None :
        for el in liste :
            if el != None : print(el, "   :   ", str(liste[el]))







