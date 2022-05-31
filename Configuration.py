# -*- coding: utf-8 -*-
"""
Created on Thu May  5 10:29:21 2022

@author: 3b13j
"""

import random
from Phoneme import tuple_2_list, list_2_tuple
from Sampling import MatricesV, MatricesC
from copy import deepcopy

maxC = [11, 1, 1, 1, 1, 2, 1, 1 , 1 , 1]
maxV = [2, 6, 1 , 1 , 1]

class Configuration (object) :
    """
    A class to represent an abstract configuration of features

    ...

    Attributes
    ----------
    state : list
        representation of the features involved 
    nn : list
        list on non wildcards indexes

    Methods
    -------
    
    __init__() : classical constructor
       
    """
    
    def __init__(self, target , random = True) :
        
            self.isV = target.isV
               
            if random : state = Configuration.random_mono(target )
            else : state = target.feature
            self.state = state  
            
            
            
        
    def random_mono(target) : 
        """
        help to generate a random configuration with a non wildcarded feature
        
        Input : Target on which the configuration is based. we will just let one non wildcared value
        to prevent the change no to be applicable

        Returns
        -------
        state : list
            the random built state
        """
        
        
        base =  tuple_2_list(target.features)
        print(base)
        idx = target.feature_indices() 
        index = random.randint(0, len(idx)-1) 
        exception = idx[index] 
        
        
        for i in idx :
            if i != exception :
                    base[i[0]][i[1]] = -1
          
        print(base)
        base = list_2_tuple(base)
        print(base)
        return list_2_tuple(base)
    
    
    def __str__(self) :
         return str(self.state)

    def build_final_configuration(self, target) :
        
        
        # we pick randomly the feature to be modified
        idx = target.feature_indices() 
        index = random.randint(0, len(idx)+1) 
        
        if self.isV : Trinity = MatricesV 
        else : Trinity = MatricesC
        
        output_state = tuple_2_list( self.state)
        print(output_state)
        
        original_value = output_state[index[0],index[1]]
        matrix =  Trinity[index[0],index[1]]
        line = matrix [:, original_value]
        # we pick an element depending on the weights we gave
        output_value = random.choices(range(len(line)), weights = line, k=1)
        
        
        output_state[index[0],index[1]] = output_value
        
        return Configuration(list_2_tuple(output_state), False)
        
        
        
        
        


    """
    def get_output(self) :
        
        
       # feature_indices(self):
        
        state_fin = self.state.copy()
        #TODO peut être paramétré
        
            
        if self.isV : m = maxV 
        else : m = maxC
        
        i = random.randint(0,len(m) - 1)
            
        
        if m[i] == 1 :
                
                if state_fin[i] == 1 : state_fin[i] = 0 
                else : state_fin[i] = 1
            
        else :
                augmenter = bool (random.randint(0,1))
                
                if augmenter and  state_fin[i] < m[i] : state_fin[i] += 1
                elif state_fin[i]>0 : state_fin[i] -= 1 
        
        return Configuration(state_fin, False)
                    
                """

        

        
