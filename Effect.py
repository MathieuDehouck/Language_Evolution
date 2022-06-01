# -*- coding: utf-8 -*-
"""
Created on Wed Jun  1 09:55:33 2022

@author: 3b13j
"""


from Sampling import MatricesV, MatricesC, manner_2_ind, manner_list

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
    
    def __init__(self, target, r = True, index = None)  :

        self.target = target
        t = target 
        if type(t) == list : t = t [0]
        
        self.isV = t.isV
        self.idx = t.feature_indices() 
        self.effect = {}
        borne = len(self.idx)-1
        
        elisabeth = random.randint(0, borne)
        if r : inde = self.idx[elisabeth]
        else : inde = index
        self.set_output( inde)


        
    def set_output(self, index) :

        if self.isV : Trinity = MatricesV 
        else : Trinity = MatricesC
        
        #TODO cas si un seul changement, généraliser
        
        original_value = self.target.features[index[0]][index[1]]
        manner = False
        if type(original_value) == tuple :
            original_value = manner_2_ind[original_value]
            manner = True
        matrix =  Trinity[index[0]][index[1]]
        line = matrix [:, original_value]
        
        # we pick an element depending on the weights we gave
        
        output_value = random.choices(range(len(line)), weights = line, k=1)[0]
        
        print(output_value)
        
        self.effect[index] = output_value
        if manner :  self.effect[index] = manner_list [output_value]
        
           
        
    def __str__(self) :
        
        s =  str(self.effect)
        return s
        

        
        
        
        
