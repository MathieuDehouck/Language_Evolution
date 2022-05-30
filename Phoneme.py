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


ipa = IPA.get_IPA()


def tuple_2_list(tupl) :
    liste = list(tupl) 
    for el in liste :
        if type(el) == tuple :
            el = list(el)
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
    voice : bool 
        states if the phoneme is voiced or not
    syl : bool 
        states if the phoneme is center of a syllable
    
    
    Methods
    -------
    __init__() constructor taking all these information as input
    

    update_IPA  : finds the closest ipa character to represent a new phoneme
    
    """
    
    
    def __init__(self, voice=False, syl=False): 
        """
        a gentle Phoneme constructor
        """       
        self.ipa = None
        self.syl = False 
        self.voice = False
        self.rank_in_wd = None
       
        self.description = ""
        #UNICODE_TO_IPA[string] ._IPAChar__canonical_string
        
        self.features = None
        self.rank_in_wd = None
        self.isV = (type(self) == Vowel)
        
        
    def __str__(self):
        return str(self.ipa )+  " :  " + str(self.description ) + "\n" + str(self.features)

    def set_word_rank(self, rk) :
        self.rank_in_wd = rk 

    

    def isConsonant(self) :
        return type(self) == Consonant
        
    def set_rank_in_wd(self, rk) :
        self.rank_in_wd = rk

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

    def set_aspirated(self, bol) :
        
        
        if not self.isV : 
            """
            ft = tuple_2_list(self.features)
            
            ft[1][2] = int(bol)
            self.features = ft
            """
            #TODO

def get_phon(string) :
    """
    transform a string (we excpect the user to enter an ipa character) into the Phoneme object representing this character
    """
    if string not in ipa.alphabet.keys() :
        return
    return Phoneme(string, list(ipa.alphabet[string].features))






class Vowel(Phoneme) : 
    
    """
    A class representing a Vowel
    
    Semantic of a feature ;
    
    syl : field of the Phoneme
    voice : filed of the Phoneme
    
    Features :
        First tuple :
             
            "fronting" : int  btw 0 and 2
            "height", int btw 0 and 6
                
        Second tuple :
            
            "round" : bool
            "nasal" : bool
    
    ...

    Attributes
    ----------
    ipa : str
        the ipa representation of a phoneme
    features : list
        a list representing the features associated to the phonem
    description : str
        the verbose descritption of the phoneme
    voice : bool 
        states if the phoneme is voiced or not
    syl : bool 
        states if the phoneme is center of a syllable
    
    Methods
    -------
    __init__() constructor taking all these information as input
    
    update_IPA  : finds the closest ipa character to represent a new phoneme
    
    get_height
    get_front

    is_round
    is_nasal
    is_palatal
    
    linearize : get a representation of the phoneme as a single vector
    
    """
    
    def __init__(self, features):
        super().__init__(features[0], features[-1][0])
        self.features = features
        self.feat_semantics = ipa.vfeatures
        self.lin = self.linearize()
        self.ipa = ipa.get_char(self)
        
        
        
    def get_height(self) :
        return self.features[0][0]

    def get_front(self) :
        return self.features[0][1]

    def is_round (self) :
        return self.features[0][3]

    def is_nasal(self) :
        return self.features[1][1] == 1

    def is_voiced(self):
        return self.features[1][0] == 1
    
    def is_palatal(self, threshold):
        return self.features[0][1] > threshold


    def linearize(self) :
     
        #print(self.features)
        feat = []
        
        
        feat.append(self.features[0][0])
        feat.append(self.features[0][1])
        feat.append(self.features[0][2])
        feat.append(self.features[1][0])
        feat.append(self.features[1][1])
    
        return feat
    

class Consonant(Phoneme) : 
    
     
    """
    A class representing a Consonant
    
    Semantic of a feature ;
    
    syl : field of the Phoneme
    voice : filed of the Phoneme
    
    Features :
        First tuple :
            0 : 
            "place of articulation" : int 
            1 : list of 5 manner of articulation , each coded by a boolean
                "plosive"
                "fricative"
                "nasal"
                "trill"
                "lateral"
                
        Second tuple :
            
            "secondary place of articulation"  int (3 or 4 possibilities, same semantics as in place of articulation)
            "pren_nasal"  bool
            "aspiration" bool 
            
    
    ...

    Attributes
    ----------
    ipa : str
        the ipa representation of a phoneme
    features : list
        a list representing the features associated to the phonem
    description : str
        the verbose descritption of the phoneme
    voice : bool 
        states if the phoneme is voiced or not
    syl : bool 
        states if the phoneme is center of a syllable
    
    Methods
    -------
    __init__() constructor taking all these information as input
    
    update_IPA  : finds the closest ipa character to represent a new phoneme
    
    is_round
    is_nasal
    is_palatal
    
    get_place
    get_manner
    
    linearize : get the representation of the phoneme as a list of integers
    
    """
    
    
    
    def __init__(self, features):
        super().__init__(features[0], features[1][-1])
        self. features = features
        self.feat_semantics = ipa.cfeatures
        self.lin = self.linearize()
        self.isV = False
        self.ipa = ipa.get_char(self)
        

    def linearize(self) :
        
        feat = []
        
        feat.append(self.features[0][0])
        for manner in self.features[0][1] :
            feat.append(int(manner))
        feat.append(self.features[0][2])
        for manner in self.features[1] :
            feat.append(int(manner))
        return feat

    

    def is_round (self) :
        return self.features[0][0] == 11
    
    def is_labialised (self) :
        return self.features[1][0] == 11

    def is_palatal (self) :
        return self.features[0][0] == 3

    def is_uvular (self) :
        return self.features[0][0] == 1

    def is_nasal (self) :
        return self.features[0][1] == (1, 0, 0, 0, 0) or self.features[1][1] == 1

    def is_pre_nasalised(self):
        return self.features[1][1] == 1

    def is_aspirated (self) :
        return self.features[1][2] == 1
    
    def is_sonorant(self) :
        return self.features[0][1][0] == 0 and  self.features[0][1][0] == 1
 
    def has_sec_articulation (self) :
        return self.features[1][2]


def delinearize(isV, liste) :
   if isV : 
    tpl1 = (liste[0], liste[1], liste[2])
    tpl2 = (liste[3], liste[4])
    
   else :
    manner = (liste[1], liste[2], liste[3], liste[4], liste[5])
    tpl1 = (liste[0], manner, liste[6])
    tpl2 = (liste[7], liste[8], liste[9])
   return (tpl1, tpl2)
       
       




