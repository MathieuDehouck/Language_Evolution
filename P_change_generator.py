# -*- coding: utf-8 -*-
"""
Created on Mon May 30 11:58:54 2022

@author: 3b13j
"""


import random 
from Effect import Effect
from Change import P_change
from Phoneme import change_feature
from utilitaries import mask_match



idxC = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]
idxV = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), ]

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
        
        
        
        
        print(change.target)
        print(change.effect)
        
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
    
    def extends_target(self, change, language) :
        
        
        
        if change.is_Vowel : idx = idxV
        else : idx = idxC
        
        
        
        feature_index = idx [ random.randint (0, len(idx)-1)]
        
        
        change.target = change_feature (change.target, change.is_Vowel, feature_index, -1) 
            
        impacted = []
        for phon in language.phonemes :
            if mask_match(change.target, phon.features, phon.is_Vowel) :
                impacted.append(phon.ipa)
                
        print()
        print("impacted", impacted)
        print()
        print(change.target)
    
    def create_change( self,language, rd = True, target = None, ci = None)  :
        
        
        change = super().create_change(language)
        
        self.extends_target(change, language)
        
        r = random.randint(0,1)
        #TODO paramétrisable
        if r : 
            self.extends_target(change, language)
            print("extension")
        
        print("Target after gen" , change.target)
        
        return change
    
    def select_effect(self, language, target) :
        
        effect = Effect(target.features)
        return effect 
        
    def set_conditions(self) :
        return
    
    """
    def create_change( self,language, random = True, target = None, ci = None) :
        
        return super().create_change
        
        
   """     
        
        
        
        
        
        
        
        

        