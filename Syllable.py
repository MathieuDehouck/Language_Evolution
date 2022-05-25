# -*- coding: utf-8 -*-
"""
Created on Wed May  4 11:33:05 2022

@author: 3b13j

Module containing the syllable class and its associated methods
"""

class Syllable(object) :
    """
    A class to represent a syllable.

    ...

    Attributes
    ----------
    phonemes : list
        list of the phonemes composing the syllable
    stress : bool 
        indicate whether the syllable bears stress or not
    length : bool 
        indicate if the vowell in the syllable have more than 2 mora.
    i_center : int
        index of the phoneme which is at the heart of the syllable
    center: phoneme : 
        phoneme which is at the heart of the syllable

    Methods
    -------
    init__()__
        constructor that takes as input the list of phonemes in the syllable
        
    set_stress(bool) :
        allow the programm to change the stress of a syllable
        
    set_length(bool) : 
        allow the programm to change thelength of a syllable
    
    """
    
    
    
    def __init__(self, phonemes , stress = False, length = False, tone = None) :
        self.phonemes = phonemes
        self.stress = stress 
        self.length = length
        self.tone = tone
    
        i_center = 0 
        for phon in self.phonemes :   
            if phon.features[0] == 1 :
                i_center = self.phonemes.index(phon)
                self.i_center = i_center
                break 
        self.center = self.phonemes[i_center]
          
        s = ""
        for phoneme in self.phonemes :
            s += phoneme.ipa
            if phoneme == self.center and self.length :
                s += ":"
        self.ipa = s
       
        
        
    def __str__(self) :
        return self.ipa  + "\nstress : "+str(self.stress)+"    length : "+ str(self.length)
    
    
    
    def set_stress(self, stress) :
        """
        Allow the program to change the stress of a syllable

        Parameters
        ----------
        stress : bool
            The new value 

        Returns
        -------
        None.

        """
        
        self.stress = stress
        
        
        
    def set_length(self, length) :
        """
        Allow the program to change the stress of a syllable

        Parameters
        ----------
        stress : bool
            The new value 

        Returns
        -------
        None.

        """
        
        self.length =  length
        
    
    
    
    
    
    
        