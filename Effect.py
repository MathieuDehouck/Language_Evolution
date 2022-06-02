# -*- coding: utf-8 -*-
"""
Created on Wed Jun  1 09:55:33 2022

@author: 3b13j
"""


from Sampling import MatricesV, MatricesC, manner_2_ind, manner_list, sec_place_2_ind, secondary_place 
from Phoneme import feature_indices
import random



class Effect (object) :
    """
    A class representing the effect of a change
    
    The effect is encoded as a dictionnary, taking as key the index of the feature to be modified, and
    as value the new value it sould have.
    
    An effect could be built using a target
    
    ...

    Attributes
    ----------
    target  : (optionnal ) tuple
        a feature pattern representing the phonemes the change can be applied to
    
    Methods
    -------
    __init__() constructor taking all these information as input
    

    random_effect 
    
    """
    
    def __init__(self, target, r = False, index = None)  :

        self.target = target
        t = target 
        if type(t) == list : t = t [0]
        
        
        self.idx = feature_indices( self.target) 
        self.isV = (len(self.idx) == 5)
        self.effect = {}
        self.impacted_idx = []
         
        if r : 
            inde = self.idx[random.randint(0, len(self.idx)-1)]
        
            self.set_output( inde)


    def add_effect (self, key, value) :
        self.effect[key] = value

        
    def set_output(self, index) :

        if self.isV : Trinity = MatricesV 
        else : Trinity = MatricesC
        
        
        
        original_value = self.target[index[0]][index[1]]
        manner = False
        sec_manner = False 
        
        if type(original_value) == tuple :
            original_value = manner_2_ind[original_value]
            manner = True
        if not self.isV and index == (1, 0) :
            original_value = sec_place_2_ind [original_value]
            sec_manner = True
        
        matrix =  Trinity[index[0]][index[1]]
        
        print()
        print(self.target)
        print(index)
        print(original_value)
        
        line = matrix [original_value]
        
        # we pick an element depending on the weights we gave
        
        output_value = random.choices(range(len(line)), weights = line, k=1)[0]
        
        
        self.impacted_idx .append(index)
        
        
        if manner : output_value  = manner_list [output_value]
        if sec_manner :  output_value = secondary_place[output_value]
        value = ( original_value, output_value) 
        self.effect[index] = value
        
    def __str__(self) :
        
        s =  str(self.effect)
        return s
        

        
        
        
        
