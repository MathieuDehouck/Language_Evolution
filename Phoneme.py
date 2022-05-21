# -*- coding: utf-8 -*-
"""
Created on Tue May  3 00:08:43 2022

@author: 3b13j
"""

from utilitaries import *
import os
from numpy.linalg import norm
from IPA import IPA
from ipapy import UNICODE_TO_IPA
import numpy as np


ipa = IPA()



def rank_finder (config) : 
    """
    gives back the list of ranks of non 0 features

    Parameters
    ----------
    config : list
        feature list representing a phoneme 

    Returns
        
    -------
    i : int
        the rank of the first non wildcarded feature
    """
    liste = []
    for  i in range (len(config)) :
        if config[i] != -1 :
            liste.append(i)
    return liste



class Phoneme(object) :
    """
    A class representing a phoneme
    
    ...

    Attributes
    ----------
    ipa : str
        the ipa representation of a phoneme
    features : list
        a list representing the features associated to the phonem
    description : str
        the verbose descritption of the phoneme
    
    
    Methods
    -------
    __init__() constructor taking all these information as input
    
        
    isV : checks whether the phoneme is a vowell
    equals
    update_IPA  : finds the closest ipa character to represent a new phoneme
    
    """
    
    
    
    def __init__(self, string, liste): 
        """
        a gentle Phoneme constructor
        """
        
        self.ipa = string 
        self.features = liste
        
        if self.ipa[-1] == "*" :
            string = self.ipa[:-1]
        self.description = UNICODE_TO_IPA[string] ._IPAChar__canonical_string
        
        
        
    def isV(self):
        """ 
        checks if a Phoneme is a vowell or not
        """
        return self.features[0] ==1 
        
    
        
    def __str__(self):
        return self.ipa +  " :  " + self.description + "\n" + str(self.features)



    def equals(self, phonemes ) :
        return self.features == phonemes.features



    def update_IPA(self, config, verbose = False) :
        """
        updates the ipa field of the Phoneme it is applied to. 

        Parameters
        ----------
        config : list
            A list representingthe feature we want 
        verbose : bool, optional
            As usual. Verbose with me means verry verbose. The default is False.

        Returns 
        -------
        None.

        """
        
        # STEP 1 : we check if the archetypal IPA contains a phoneme exactly matching the features of the phoneme we are looking at
        for phoneme in ipa.phonemes :
            
            if verbose :
                print()
                print(phoneme.ipa)
                print(list(phoneme.features))
                print(self.features)

            if phoneme.features == self.features :
                if verbose :
                    print(list(phoneme.features))
                    print(self.features)
                    print("NEW VALUE FOUND")
                self.ipa = phoneme.ipa
                return    
            
                
            
        # STEP2: if there is no perfect match, we want to evaluate the closest phoneme.
        
        
      
        
        
        
        # we want the change that just happened (encoded by a configuration) to be a restriction on the natural class we are going to pick 
        # the new phoneme from. 
        # we compute the potential candidates before selecting the one with the minimal distance to the feature template
        
        
        # we compute the booleans features that have been modified
        changes = []
        for ind, val in enumerate(config.state) :
            if config.state[ind] != -1:
                changes.append(ind)
        if 2 in changes : changes.remove(2)
        if 3 in changes : changes.remove(3)
        
        
        
        
        
        # from the changes we restrict the number of candidates
        candidates = ipa.phonemes.copy()
        tested_classes = []
        for classe in ipa.classes[1:12] :
            tpl = classe.template
            for i in range(len(tpl)) :
                if i in changes and tpl[i] != -1 and config.state[i] != -1 :
                    tested_classes.append(classe)
            if verbose : 
                print("examined category", len(tested_classes))
                printl(tested_classes)
                        
        # we eliminate all candidates that do not belong to the target class
            
        for classe in tested_classes :
            if verbose : print("we test for the class ", classe)
            i = rank_finder(classe.template)
            if len(i) != 0 :
                for rank in i :
                    val = config.state[rank]
                    verbose : print("VAL of rank", val)
                    for phon in candidates.copy() :
                        if phon.features[rank] != val :
                            candidates.remove(phon)
        
        if verbose : 
                print("Survivors : ")
                print(len(candidates))
                printl(candidates)
                print()
                
        if len(candidates) == 1 : 
                winner = candidates[0] 
                self.ipa = winner.ipa
        elif len(candidates) == 0 :
                if verbose : print("no survivor ")
        else :
        # we compute the distance for each candidate and returns the best one, the argmin of the distance
            
                target_vector = self.features[2:4]
                dic_vect = {}
                for cand in candidates :
                    dic_vect[cand] = cand.features[2:4]
                dist_min = 42  # unreachable value for such small coefficients
                best_cand = None
                for cand in candidates :
                    a = np.array(target_vector)
                    b = np.array(dic_vect[cand])
                    d = norm(a-b)
                    if verbose :
                        print (a, b)
                        print(d, dist_min, cand)
                    if d < dist_min :
                        dist_min = d
                        best_cand = cand
                        
                if verbose : print('the winner is ', best_cand)
                
                #as a result, we update the ipa character
                
                #TODO  C'est ici que l'on propose de placer la distinction entre cons et voy, quitte à raffiner plus tard, pour qu'une cs ne soit pas  encodée par une voy et vice versa
                
                if best_cand.features[0] == self.features[0] and best_cand.features[1] == self.features[1] :
                
                
                
                
                    self.ipa = best_cand.ipa



def get_phon(string) :
    """
    transform a string (we excpect the user to enter an ipa character) into the Phoneme object representing this character
    """
    if string not in ipa.alphabet.keys() :
        return
    return Phoneme(string, list(ipa.alphabet[string].features))
















