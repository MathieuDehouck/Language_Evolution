# -*- coding: utf-8 -*-
"""
Created on Thu May  5 00:01:15 2022

@author: 3b13j
"""

import numpy as np
from ipapy import *
from copy import deepcopy
from IPA_utils import manner_enc
from Phoneme import Vowel, Consonant



def linearize (LISTE, liste = [], reset = True) :
    """
    transforme une liste complexe en une liste linéarisée

    Parameters
    ----------
    LISTE : TYPE
        DESCRIPTION.
    liste : TYPE, optional
        DESCRIPTION. The default is [].
    reset : TYPE, optional
        DESCRIPTION. The default is True.

    Returns
    -------
    liste : TYPE
        DESCRIPTION.

    """
    if reset : liste = []
    for ft in list(LISTE) : 
        if type(ft) == int : 
            liste.append(ft)
            LISTE.remove(ft)
        else :
            
            liste = linearize (list(ft), liste, False)      
    return liste




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
    
    def __init__(self, string, feats, vow=False):
        self.ipa = string
        self.features = feats
        self.vow = vow
        try:
            self.description = UNICODE_TO_IPA[string]._IPAChar__canonical_string
        except:
            self.description = 'No description'
        self.lin = linearize(feats)


    def __str__(self):
        return self.ipa +  " :  " + self.description + "\n" + str(self.features)


    def is_Vowel(self):
        return self.vow

    def is_Consonant(self):
        return not self.vow
    

    def get_one(self, extra_feats):
        """
        I'll change this eventually
        """
        base = self.features[0]
        print(self.features, extra_feats)
        if self.vow:
            extra = [1, 0]
            if 'nasalised' in extra_feats:
                extra[1] = 1
            return Vowel((1, base ,tuple(extra)), IPA.get_IPA())
        else:
            extra = [0, 0, 0]
            if 'pre_nasal' in extra_feats:
                extra[1] = 1
            if 'aspirated' in extra_feats:
                extra[2] = 1
            if 'labialised' in extra_feats:
                extra[0] = 11

            return Consonant((0, base, tuple(extra)), IPA.get_IPA())


        

class IPA() :
    """
    A singleton class to represent the IPA viewed as a set of archetypal phonemes.

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

    __instance = None





    @staticmethod
    def get_IPA():
      """ Static access method. """
      if IPA.__instance == None:
         IPA.__instance = IPA()
      return IPA.__instance




    
    def __init__(self) :
        self.vfeatures = 'Syllabic', ('Backness', 'Height', 'Round'), ('Voiced', 'Nasal')
        self.cfeatures = ('Syllabic', ('place of articulation', ('nasal', 'plosive', 'fricative', 'trill', 'lateral'), 'Voiced'),
                          ('secondary place of articulation', 'pre_nasal' , 'aspiration'))
                          
        self.phonemes = [] 
        self.alphabet = {}
        self.feat2ipa = {}

        # reading consonants
        consonants = np.loadtxt('phonetic/consonants.tsv', delimiter='\t', dtype=str, encoding = 'utf8')
        arts = [int(x) for x in consonants[0][1:]]
        for line in consonants[1:]:
            manner = line[0]
            if 'v' in manner:
                voiced = 1
                manner = manner[:-1]
            else:
                voiced = 0
                
            for i, ch in enumerate(line[1:]):
                if ch == '-':
                    continue
                fts = (arts[i], manner_enc[manner], voiced), (0, 0, 0)
                phon = archetype(ch, fts)

                self.phonemes.append(phon)
                self.alphabet[ch] = phon
                self.feat2ipa[fts] = ch

        # reading vowels
        vows = np.loadtxt('phonetic/vowels.tsv', delimiter='\t', dtype=str, encoding = 'utf8')
        front = [int(x) for x in vows[0][1:]]
        for line in vows[1:]:
            height = line[0]
            if 'r' in height:
                rounded = 1
                height = int(height[:-1])
            else:
                rounded = 0
                height = int(height)

            for i, ch in enumerate(line[1:]):
                if ch == '-':
                    continue
                fts = (height, front[i], rounded), (1, 0)
                phon = archetype(ch, fts)

                self.phonemes.append(phon)
                self.alphabet[ch] = phon
                self.feat2ipa[fts] = ch


    def get_char(self, phon, isV= None,  verbose=False):
        """
        returns a string representing the input phoneme's features

        Parameters
        ----------
        phon : 
            A phoneme
        verbose : bool, optional
            As usual. Verbose with me means verry verbose. The default is False.

        Returns 
        -------
        string

        """
        # We look directly in the dict of features to ipa if we find something
        if phon.features in self.feat2ipa:
            return self.feat2ipa[phon.features]

        # we did not find a perfect match, so we build it
        if phon.is_Vowel():
            # a basic vowel is voiced and unnasalised
            base = (phon.features[0], (1,0))
            out = self.feat2ipa[base]
            
            if phon.is_nasal(): # nasal
                out += u'\u0303'

            if not phon.is_voiced(): # unvoiced
                out += u'\u0325'


        else:
            base = (phon.features[0], (0,0,0))
            if base in self.feat2ipa:
                out = self.feat2ipa[base]
            else:
                print(base)
                out = ((base[0][0], base[0][1], 1), base[1])

            if phon.is_labialised() : # round w
                out += 'ʷ'
            
            if phon.is_aspirated() : # aspirated
                out += 'ʰ'

            if phon.is_pre_nasalised() : # prenasal
                nasal = (phon.features[0][0], (1, 0, 0, 0, 0), 1), (0, 0, 0)
                try:
                    n = self.feat2ipa[nasal]
                except:
                    n = 'n'
                out = n + u'\u035c' + out
            

            
        return out
    
ipa = IPA.get_IPA()
print(ipa.feat2ipa.values())
