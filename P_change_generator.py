# -*- coding: utf-8 -*-
"""
Created on Mon May 30 11:58:54 2022


A file used to generate instances of different kind of P_change_generator

@author: 3b13j
"""


import random 
from Effect import Effect
from Change import P_change
from Condition import rd_p_condition, P_condition, S_condition
import Sampling

from utilitaries import mask_match,  change_pattern, tpl_2_candidates, words_containing, bewilder_pattern, syl_match,  printl, feature_indices

idxC = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]
idxV = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), ]





class P_change_generator(object) :
    """
    A class representing a generator that randomly generates P changes
    
    The way webuild the random changes heavily depend on choices of implementation. 
    Several kinds of generators could be implemented since this is an abstract class.
    """
    
    
    
    
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
        """
        Central method of a class, where the Change is generated

        """
        
        NotImplemented
        
       
        
       
        
class Baby_P_change_generator(P_change_generator) :
    
    """
    First instance of the abstract class.
    
    We make a first approximation of the way to generate a change.
    We stick to the following recipee :
        - we pick a target among the phonemes 
        - we choose an effect following specific parameters (choice of a domain and an effect)
        - we choose a range of conditions after that.
    """
    
    
    def __init__(self) :
        super().__init__() 
     
        
        
        
        
    def select_target(self, language) :
        """
        We randomy pick a phoneme among all the phonemes of a language.
        #TODO parametrize : do not pick a phoneme twice . ponder the chance to pick a phoneme ???

        Parameters
        ----------
        language : Language 
            The language we want to evoluate

        the pattern of the feature we will modify

        """
        
        #TODO Is there a way to parametrize the 
        
        index = random.randint(0, len(language.phonemes)-1)
        target = language.phonemes[index].features
        
        return target, language.phonemes[index].is_Vowel()
    
    
    
    
    
    def extends_target(self, change, language, n, verbose = False) :
        """
        Replaces some of the index values of the target with wildcards

        Parameters
        ----------
        change : the change we study
        .
        language : Language
        .
        n : Number of wildcards (randomly chosen but parametrized we integrate)
        
        verbose : TYPE, optional
            DESCRIPTION. The default is False.

       

        """
        
        
        # we make sure n corresponds to the number of wildcards will get at the end. 
        impossible_idx = []
        
        
        
        for i in range(n) :
        
            if change.concerns_V : 
                idx = idxV
                w = Sampling.featureV_weights
            else : 
                idx = idxC
                w = Sampling.featureC_weights
            
            
            
            feature_index = random.choices(idx, w)[0]
            
            while feature_index in impossible_idx : feature_index = random.choices(idx, w)[0]
            impossible_idx . append(feature_index)
            
            change.target = change_pattern (change.target, change.concerns_V, feature_index, -1) 
                
            impacted = []
            for phon in language.phonemes :
                if mask_match(change.target, phon.features, phon.is_Vowel) :
                    impacted.append(phon.ipa)
                    
            if verbose :       
                print()
                print("impacted", impacted)
                print()
                print(change.target)
        
        
    
    
        
    
    
    
    def generate_P_change( self,language, rd = True, target = None, ci = None, verbose = False ) :
        """
        

        Parameters
        ----------
        language : Language
        
        All the other values are optional, but can be manually selected if provided as parameter
        
        rd : bool : is the change random ?
            DESCRIPTION. The default is True.
        target : TYPE, optional
            DESCRIPTION. The default is None.
        ci : TYPE, optional
            DESCRIPTION. The default is None.
        verbose : TYPE, optional
            DESCRIPTION. The default is False.

        Returns
        -------
        change : TYPE
            DESCRIPTION.

        """
        
        #selection of the target
        target, concerns_V  = self.select_target(language)
        if verbose : print("Target", target)
        
        
       
        
        
        #selection of the effect
        effect = self.select_effect(language, target, concerns_V)
        change = P_change(target, effect)
        
        if verbose : print("Effect", effect)
        
        
        nb_ext = random.choices (range(0,6), Sampling.weights_extensions)[0]
        self.extends_target(change, language, nb_ext)
        
        
       
        #we add conditions
        if verbose : print('Conditions')
        
        self.set_conditions( language, change )
        
        
        if verbose :
            print()
            print("CHANGE SUCCESSFULLY CREATED")
            print(change)
            print()
            
        return change
    
    
    

    

    def compute_outcome (self,index, input_value, matrix, isV) :
       """
        Computes the output value of a feature value, given its original value and the parameter matrix we chose

        Parameters
        ----------
        index : TYPE
            DESCRIPTION.
        input_value : TYPE
            DESCRIPTION.
        matrix : TYPE
            DESCRIPTION.
        isV : TYPE
            DESCRIPTION.

        Returns
        -------
        output_value 

        """
       
       manner = False
       sec_manner = False 
       if type(input_value) == tuple :
           input_value = Sampling.manner_2_ind[input_value]
           manner = True
       if not isV and index == (1, 0) :
           input_value = Sampling.sec_place_2_ind [input_value]
           sec_manner = True
        
       
       line = matrix [input_value]
       output_value = random.choices(range(len(line)), weights = line, k=1)[0]
       if manner : output_value  = Sampling.manner_list [output_value]
       if sec_manner :  output_value = Sampling.secondary_place[output_value]
      
   
       return  output_value
   
    
   
    
   
    def set_funct( self, index, target  ) :
       """
       Automatically computes the outcome 

       #sampler colonner ?



       Parameters
       ----------
       index : TYPE
           DESCRIPTION.

       Returns
       -------
       None.

       """
       effect={}
       
       #TODO isV doit etre passéc en argument 
       isV = len(feature_indices(target)) == 5 
       if isV : Trinity = Sampling.MatricesV 
       else : Trinity = Sampling.MatricesC
       
       
       matrix =  Trinity[index[0]] [index[1]]
       
       #TODO implement cyclic / multiplu changes
       input_val = target[index[0]][index[1]]
       outcome = self.compute_outcome( index, input_val, matrix, isV)
       
       effect[input_val] = outcome
       
       return effect
       
       
       
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    def select_effect(self, language, target, concerns_V) :
        """
        Randomly builds an effect from a target we already know

        Parameters
        ----------
        language : TYPE
            DESCRIPTION.
        target : TYPE
            DESCRIPTION.
        concerns_V : bool

        
        """
        
        
        idx = feature_indices(target)
        
        if concerns_V : 
            w = Sampling.featureV_weights 
        else : 
            w = Sampling.featureC_weights 
            
        domain = random.choices(idx, w )[0]
        #TODO paramétriser 
        ef = self.set_funct(domain, target)
        
       
        effect = Effect(domain, ef)
        
        return effect 
    
    
    
    
    
    def set_S_condition (self, potential_contexts, change, verbose = False ) : 
        """
        Generates a possible S_condition given potential contexts it could be applied to in a given language

        Parameters
        ----------
        potential_contexts : TYPE
            DESCRIPTION.
        change : TYPE
            DESCRIPTION.
        verbose : TYPE, optional
            DESCRIPTION. The default is False.

        Returns
        -------
        Condition
        
        Potential candidates provided that they satisfy the new condition

        """
        
        
        
        rd_context = random.choice(potential_contexts) 
        
        
        # TODO baby phase, checke a l indice fixe
        for phon in rd_context.phonemes :
            if mask_match(change.target, phon.features, change.concerns_V) : break
        syl = rd_context.syllables[phon.in_syl]
        
        candidates = []
        for cand in potential_contexts :
            ok = False 
            for s in cand.syllables :
                if syl_match(s, syl) :
                    #TODO approx
                    for pho in s.phonemes :
                        if mask_match(change.target, pho.features, change.concerns_V) : ok = True
            
            
            
            if ok : candidates.append(cand)
        
        return   S_condition(42, 0, syl.length, syl.stress, syl.tone), candidates
    
    
    
    
    
    
    def set_abs_Pcondition(self, potential_contexts, change, verbose = False) :
        """
        Generate a P_condition with an absolute condition

        Parameters
        ----------
        potential_contexts : TYPE
            DESCRIPTION.
        change : TYPE
            DESCRIPTION.
        verbose : TYPE, optional
            DESCRIPTION. The default is False.

        Returns
        -------
        cond : TYPE
            DESCRIPTION.
        candidates : TYPE
            DESCRIPTION.

        """
        
        
        
        
        # TODO we make a first approximation considering that only the very beginning and the very end of the word provide specific positions
        # with abs positions, our goal is to make sure the target is in a certain abs position so the target of the change is simply the target itself.
        
        #we set which position is going to be absolute
        sign = random.randint(0,1) 
        
        if sign : rel_pos = random.choices(range(0,3), Sampling.weights_rel_pos)[0]
        else : rel_pos = -1 * random.choices(range(1, 4), Sampling.weights_rel_pos )[0]
        
        #we need to sort out possibles context :
        candidates = []
        for cand in potential_contexts :
            #TODON  pb short wds
            if len(cand.phonemes) <= abs(rel_pos) : continue
            
            if  mask_match(change.target, cand.phonemes[rel_pos].features ,change.concerns_V) : candidates.append(cand)
        
        if len(candidates) != 0 :
            cond  = P_condition(change.target, 0, rel_pos)
            return cond, candidates
        
        
        else : return None, potential_contexts
        
        
        
        
        
    def set_rel_Pconditions (self, potential_contexts, change, nb_cond, verbose =  False) :
        """
        Generates a set of P conditions concerning a change

        Parameters
        ----------
        potential_contexts : TYPE
            DESCRIPTION.
        change : TYPE
            DESCRIPTION.
        nb_cond : TYPE
            DESCRIPTION.
        verbose : TYPE, optional
            DESCRIPTION. The default is False.

        Returns
        -------
        conditions : list of Rel_P_conditions

        """
        
        
        #TODO : faire en sorte de privilégier le même feature que l'effect. Assimilation / dissimilation
        
        
        # we pick a context
        rd_context = random.choice(potential_contexts)
        
        if verbose : 
            print("RD_context")
            print(rd_context)
            
        
        # we find the position of a targetted phoneme in the context word
        for i, pho in enumerate(rd_context.phonemes ) : 
            if mask_match(change.target, pho.features , change.concerns_V ): 
                idx_in_wd = i
                break
        if verbose : 
            print( rd_context)
            print("THIS IS THE INDEX OF THE CHANGED WD", i)
            
        
        conditions = []
        forbidden_rel_pos = [] 
        
        for loop in range(nb_cond) :
            
            if verbose : print("setting condition ", loop)
            rel_pos = -666
            index = i +rel_pos
            avoid_inf_loops = 0
            while index not in range(len(rd_context.phonemes)) or rel_pos in forbidden_rel_pos and avoid_inf_loops< 100 :
                rel_pos = rd_rel_pos()
                avoid_inf_loops += 1
                index = i +rel_pos
            forbidden_rel_pos.append(rel_pos)
            
            if avoid_inf_loops == 100 : break
            
            same_as_target = random.choices([0,1], Sampling.weights_same_feature)[0]
        
            
            conditioner = rd_context.phonemes[index].features
            idx_cond = feature_indices(conditioner)
            
            if verbose : 
                print("THIS IS THE INDEX OF THE CONDITIONER", index)
                print("CONDITIONNER", )
                print(rd_context.phonemes[index])
                print(rd_context.phonemes[index].features)
                print()
            
            if rd_context.phonemes[index].is_Vowel()  : w = Sampling.featureV_weights
            else :w = Sampling.featureC_weights
            
            
            effect_tf_id = random.choice( list( change.effect.effect.keys()))
            rd_ft_id = random.choices (feature_indices(rd_context.phonemes[index].features), w)[0]
            
            ft_id = random.choices( [effect_tf_id, rd_ft_id], Sampling.weights_same_feature) [0]
            
        
            #TODO third approximation, the number of wildcards
            nb_wild = random.randint(0,5) 
            for l in range  (nb_wild) :
                
                effect_tf_id = random.choices( list( change.effect.effect.keys()))
                rd_ft_id = random.choice (feature_indices(rd_context.phonemes[index].features))
                ft_id = random.choice( [effect_tf_id, rd_ft_id])
                if ft_id in idx_cond : conditioner = bewilder_pattern(conditioner, ft_id)
            
            continu = random.randint(0,1)
            
            
            conditions.append ( P_condition(conditioner, rel_pos ) )
            
        return conditions
        
        
        
            
            
            
    
    def set_conditions(self, language, change, verbose = False ) :
        """
        Adds a parametrized number of condition to the change
        
        Parameters
        ----------
        language : TYPE
            DESCRIPTION.
        change : TYPE
            DESCRIPTION.
        verbose : TYPE, optional
            DESCRIPTION. The default is False.

    

        """
    
        
        
        #Due to implemetation strategies , we will generate conditions in a spectific order 
        
        # *  if necessary : abs pos P conditions 
        
        # * at last casual P conditions, for they need a very specific context to be studied
        
        # we only want to generate legit conditions, that 's why we ll decrease at each step of the function the number of potential context, still checking the change applies in at least one context
        
        #TODO paramétriser le nombre de condition par changement
        
        potential_contexts = words_containing(change.target, language) 
        
        #add syl condition :
        
        """
        rds = 0
        if not rds : 
            cond, potential_contexts = self.set_S_condition(potential_contexts, change)
            change.add_condition(cond)
        
        """
        
        # abs P_condition ?
        rd = random.choices([0,1], Sampling.weigt_A_R)[0]
        if not rd :
            cond, potential_contexts = self.set_abs_Pcondition(potential_contexts, change)
            if cond != None : 
                change.add_condition(cond)
        
        
        # rel_pos P_condition 
        else :
            nb_cond = random.choices(range(0,4), Sampling.weights_nb_cond)[0]
            if nb_cond :
                conditions = self.set_rel_Pconditions(potential_contexts, change,  nb_cond)    
                for c in conditions : change.add_condition(c)
        
        if verbose : print("Conditions setted")
        
        
        
        
def rd_rel_pos()  :
        """ returns a random rel position """

        ran = random.choices(range(1,4), Sampling.weights_rel_pos ) [0]
        sign = random.choice ([-1, 1])
        rel_pos = ran * sign
        return rel_pos