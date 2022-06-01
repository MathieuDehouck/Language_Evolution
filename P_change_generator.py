# -*- coding: utf-8 -*-
"""
Created on Mon May 30 11:58:54 2022

@author: 3b13j
"""


import random 
from Effect import Effect
from Change import P_change 


class P_change_generator(object) :
    
    
    def __init__(self):
        return
        


    def select_target(self,language) :
        """
        

        Parameters
        ----------
        language : Language

        Returns
        -------
        targets : list of the phonemes we want to apply a change to

        """
        
        
        targets = []
        
        return targets
        
        
    
    def select_effect(self, language, target) :
        """
        

        Parameters
        ----------
        language : Language
        target : list of Phonemes
            
        Returns
        -------
        Two configurations representing the change we are going to apply

        """
        
        NotImplemented
        
    
    
    
    
    
    def set_conditions(self,change) :
        
        NotImplemented
        
        
        
        
        
    def create_change( self,language, random = True, target = None, ci = None)  :
        
        target = self.select_target(language) 
        effect = self.select_effect(language, target)
        change = P_change(effect, target)
        print(change.applicable(language ))
        while not change.applicable(language ) : 
            change = self.create_change( language, random, target = None, ci = None)
            print( "unacceptable change")
        
        
        
        #self.set_conditions(change)
        return change
       
        
       
        
class Baby_P_change_generator(P_change_generator) :
    
    
    
    def __init__(self) :
        super().__init__() 
        
        
        
        
        
    def select_target(self, language) :
        
        index = random.randint(0, len(language.phonemes)-1)
        target = language.phonemes[index]
        return target
    
    def select_effect(self, language, target) :
        
        effect = Effect(target)
        return effect 
        
    def set_conditions(self) :
        return
    
    """
    def create_change( self,language, random = True, target = None, ci = None) :
        
        return super().create_change
        
        
   """     
        
        
        
        
        
        
        
        

        