# -*- coding: utf-8 -*-
"""
Created on Mon May 30 11:58:54 2022

@author: 3b13j
"""


import random 
from Effect import Effect
from Change import P_change
from Condition import rd_p_condition, P_condition

from utilitaries import mask_match,  change_pattern, tpl_2_candidates, words_containing, bewilder_pattern, printl, feature_indices

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
        
    
    
    
    
    
  
        
        
        
    def create_change( self,language, random = True, target = None, ci = None)  :
        
        
        NotImplemented
        
       
        
class Baby_P_change_generator(P_change_generator) :
    
    
    
    def __init__(self) :
        super().__init__() 
     
        
        
        
        
    def select_target(self, language) :
        
        index = random.randint(0, len(language.phonemes)-1)
        target = language.phonemes[index]
        
        
        return target
    
    def extends_target(self, change, language) :
        
        
        
        if change.concerns_V : idx = idxV
        else : idx = idxC
        
        
        
        feature_index = idx [ random.randint (0, len(idx)-1)]
        
        
        change.target = change_pattern (change.target, change.concerns_V, feature_index, -1) 
            
        impacted = []
        for phon in language.phonemes :
            if mask_match(change.target, phon.features, phon.is_Vowel) :
                impacted.append(phon.ipa)
                
        print()
        print("impacted", impacted)
        print()
        print(change.target)
    
    def generate_P_change( self,language, rd = True, target = None, ci = None, verbose = False ) :
        
        
        #selection of the target
        target = self.select_target(language).features 
        if verbose : print("Target", target)
        
        #selection of the effect
        effect = self.select_effect(language, target)
        change = P_change(target, effect)
        
        if verbose : print("Effect", effect)
        
        self.extends_target(change, language)
        
        
        
        r = random.randint(0,1)
        #TODO paramétrisable
        
        if r : 
            self.extends_target(change, language)
            if verbose : 
                print()
                print("Generalization")
        
       
        
       
        
       
        #we add conditions
        if verbose : print('Conditions')
        
        self.set_conditions( language, change )
        
        
        if verbose :
            print()
            print("CHANGE SUCCESSFULLY CREATED")
            print(change)
            print()
            
        return change
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    def select_effect(self, language, target) :
        
        effect = Effect(target, True)
        return effect 
        
    
    
    
    
    def set_conditions(self, language, change, verbose = False ) :
        
        
        #TODO dirty work incoming
        
        potential_contexts = words_containing(change.target, language)
        
       
        rd_context = random.choice(potential_contexts)
        
        for i, pho in enumerate(rd_context.phonemes ) : 
            if mask_match(change.target, pho.features , change.concerns_V ): 
                idx_in_wd = i
                break
        
        if verbose : 
            print( rd_context)
            print("THIS IS THE INDEX OF THE CHANGED WD", i)
        
        
        #TODO we set randomly between 1 and 3 conditions . to be parametrized 
        
        nb_cond  = random.randint(0,2) 
        if verbose : print("We will add ", nb_cond, " conditions")
        
        forbidden_rel_pos = [] 
        for loop in range(nb_cond) :
            
            print("setting condition ", loop)
            
            rel_pos = -666
            index = i +rel_pos
            while index not in range(len(rd_context.phonemes)) or rel_pos in forbidden_rel_pos :
                rel_pos = rd_rel_pos()
                index = i +rel_pos
            
            forbidden_rel_pos.append(rel_pos)
            
            
            
            conditioner = rd_context.phonemes[index].features
            idx_cond = feature_indices(conditioner)
            
            if verbose : 
                print("THIS IS THE INDEX OF THE CONDITIONER", index)
                print("CONDITIONNER", )
                print(rd_context.phonemes[index])
                print(rd_context.phonemes[index].features)
                print()
            
            #TODO second approximation : one change over 2 the effect is selected.
            effect_tf_id = random.choice( list( change.effect.effect.keys()))
            rd_ft_id = random.choice (feature_indices(rd_context.phonemes[index].features))
            ft_id = random.choice( [effect_tf_id, rd_ft_id])
            
        
            #TODO third approximation, the number of wildcards
            nb_wild = random.randint(0,5) 
            for l in range  (nb_wild) :
                
                effect_tf_id = random.choice( list( change.effect.effect.keys()))
                rd_ft_id = random.choice (feature_indices(rd_context.phonemes[index].features))
                ft_id = random.choice( [effect_tf_id, rd_ft_id])
                if ft_id in idx_cond : conditioner = bewilder_pattern(conditioner, ft_id)
            
            continu = random.randint(0,1)
            
            
            cond = P_condition(conditioner, rel_pos )
            if verbose : 
                print()
                print("conditions settled")
                print(cond)
        
      
            change.add_condition(cond)
        
            
            
            #TODO délocaliser la génération des P_conditions ailleurs (dans le générateur général ? )
        
       
    
    
        
        
def rd_rel_pos()  :
    
        #TODO first approximation, we estimate that dissimilation has a max range of 3
        
        ran = random.randint (1, 2) 
        sign = random.choice ([-1, 1])
        rel_pos = ran * sign
        return rel_pos
        #TODO simplifie pour test
        
        

        