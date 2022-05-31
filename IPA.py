# -*- coding: utf-8 -*-
"""
Created on Thu May  5 00:01:15 2022

@author: 3b13j
"""

import numpy as np
from ipapy import *
from copy import deepcopy
#from Natural_class import create_classes



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
    
    def __init__(self, string, feats):
        self.ipa = string
        self.features = feats
        try:
            self.description = UNICODE_TO_IPA[string]._IPAChar__canonical_string
        except:
            self.description = 'No description'
        self.lin = linearize(feats)
        self.isV = None




    def __str__(self):
        return self.ipa +  " :  " + self.description + "\n" + str(self.features)

 



    def set_isV(self, b) : self.isV = b





manner_enc = {'A' :  (0, 0, 0, 0, 0), # approximant
              'N' :  (1, 0, 0, 0, 0), # nasal
              'P' :  (0, 1, 0, 0, 0), # plosive
              'S' :  (0, 0, 1, 0, 0), # fricative / sibilant
              'F' :  (0, 0, 1, 0, 0), # fricative
              'Fl':  (0, 0, 0, 1, 0), # flap
              'T':  (0, 0, 0, 2, 0), # trill
              'L':   (0, 0, 0, 0, 1), # lateral
              'Lf':  (0, 0, 1, 0, 1), # lateral fric
              'Lt':  (0, 0, 0, 1, 1),# lateral trill
              'Afr' : (0, 1, 1, 0, 0)}  #Africates





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
                phon.set_isV(False)

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
                phon.set_isV(True)
            
        
      



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
        if isV == None :
            isV = phon.isV
            
            
        # We look directly in the dict of features to ipa if we find something
        if phon.features in self.feat2ipa:
            return self.feat2ipa[phon.features]

        # we did not find a perfect match, so we build it
        if isV:
            # a basic vowel is voiced and unnasalised
            base = phon.features[:-1] + ((1,0),)
            out = self.feat2ipa[base]
            
            if phon.is_nasal(): # nasal
                out += u'\u0303'

            if not phon.is_voiced(): # unvoiced
                out += u'\u0325'


        else:
            base = phon.features[:-1] + ((0,0,0),)
            if base in self.feat2ipa :  out = self.feat2ipa[base]            
            else  :
                part = phon.features[0][0]
                voiced =  phon.features[0][2]
                tpl1 = ((part, (1, 0, 0, 0 ,0) , voiced),)
                base = tpl1 + ((0, 0, 0),)
                out = self.feat2ipa[base]
            

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