# -*- coding: utf-8 -*-
"""
Created on Thu May  5 00:01:15 2022

@author: 3b13j
"""



import numpy as np
import os
from ipapy import *
from Natural_class import create_classes
from pathlib import Path


class archetype(object) :
    """
    A class to represent an archetypal phoneme (phoneme belonging to the IPA)
    These objects are not mutable

    ...

    Attributes
    ----------
    ipa : str
        character representing the phoneme in the IPA
    features : list
        list of integers following a template we defined to represent a phoneme ;
        each index of the list stores a numerical value which can be interpreted as a phonetic feature
    description : str
        precise description of the phoneme (obtained using the IPA python module)

    Methods
    -------
    __init__(str, liste) 
        the constructor, that takes the ipa and features as attributes
    """
    
    
    
    
    def __init__(self, string, liste):
        self.ipa = string 
        self.features = tuple(liste)
        self.description = UNICODE_TO_IPA[string] ._IPAChar__canonical_string
        
        
        
        
    def __str__(self):
        return self.ipa +  " :  " + self.description + "\n" + str(self.features)




class  IPA :
    """
    A class to represent the IPA viewed as a set of archetypal phonemes.

    ...

    Attributes
    ----------
    features : list
        list of the str corresponding to the name of the features used in this IPA to describe the phonemes
    phonemes : list
        list of archetypes objects , representing the canonical phonemes of the IPA 
    alphabet : dic
        dictionnary mapping an ipa character to the phoneme it describes
    f2ipa : dic
        dictionnary mapping a feature list to its ipa character 
    classes : list
        list of the name of the different natural classes we consider in our phonology (built using a csv file)
    dic_class : dic
        dictionnary mapping a class name to the class object that represents it

    Methods
    -------
    __init__() no argument, automatically generates the IPA from a CSV file we created
    """
    
    
    
    def __init__(self) :
        
        
        phonemes = [] 
        alphabet = {}
        
        folder = Path("phonetic/")
        path = folder / "PHONETIQUE.csv"
        
        # opening of the csv file 
        data = np.genfromtxt(path, delimiter = ',', dtype = str, encoding = "utf8")
        f = open(folder / "liste_sons.txt", 'w',   encoding = "utf8")
        f.write ("LIST OF THE IPA PHONEMS \n")
        
        # extraction of the feature list :
        features = data[0][1:]
        f.write(str(features))
        f.write('\n')
        
        #extraction of the features themselves
        for sound in data[1:]  :
            fts =  [int(x) for x in sound[1:] ]

            f.write (sound[0])
            f.write ( '  :   ')
            f.write(str(fts))
            f.write (" \n")
            
            phon = archetype( sound[0], fts)
            phonemes.append(phon)
            alphabet[sound[0]]= phon
    
        
        self.features = features
        self.alphabet = alphabet
        self.phonemes = phonemes
        
        
        #creation of the utilitary dictionnaries
        f2ipa = {}
        for ar in self.alphabet :
            arch = self.alphabet[ar]
            f2ipa[arch.features ] = arch.ipa
        self.f2ipa = f2ipa
        #nasalisation_voy(self)
        dic_class, classes = create_classes(self.alphabet)
        
        self.classes = classes
        self.dic_class = dic_class
        
    
    

"""
How to deal with diacritics ? Double the phonemes and add them with new ipa form in the phoneme list ? 
Maybe easier , or add checkers when we modify the corresponding features


"""
def nasalisation_voy(ipa) :
    dic = ipa.alphabet
    for phon in ipa.alphabet.copy() :
        feat = list(dic[phon].features).copy()
        if feat[0] == 1 and feat [9] == 0 :
            vnas = str(phon)+ "~"
            fnas = feat
            fnas[9] = 1
            dic [vnas] =  archetype(vnas, fnas)
            f = open("liste_sons.txt", 'a', encoding = "utf8")
            f.write (vnas)
            f.write ( '  :   ')
            f.write(str(fnas))
            f.write (" \n")
            
            ipa.phonemes.append(fnas)













