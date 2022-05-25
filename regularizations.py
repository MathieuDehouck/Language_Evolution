# -*- coding: utf-8 -*-
"""
Created on Wed May 25 14:26:38 2022

@author: 3b13j
"""
import random



def regularize_stress(index, word) :
    
    
   
    nb_syl = len(word.syllables)
    if nb_syl == 1 : return 
    ran = range(nb_syl)
    if word.syllables[index] == 1 :
        if nb_syl-1 in ran : word.syllables[nb_syl-1].stress = False
        if nb_syl+1 in ran : word.syllables[nb_syl + 1].stress = False
            
    else :
        progressif = 0
        regressif = 0
        if index-1 not in ran  :
            word.syllables[index+1].stress = True
            return 
        else : 
            if word.syllables[index-1].length : regressif += 2
            
        if index+1 not in ran  : 
            word.syllables[index -1].stress = True
            return 
        
        else : 
            if word.syllables[index+1].length : progressif += 2
        
        r = random.randint(0, 1) 
        if r : progressif += 1 
        else : regressif += 1
        
        if progressif > regressif :
            word.syllables[index-1].stress = True
        else : 
            word.syllables[index +1].stress = True
        
        
def regularize_structure(word) :
    print(word)
    return
    
    
    
    
    
    
    
    
    
    