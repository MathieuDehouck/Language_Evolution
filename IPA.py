# -*- coding: utf-8 -*-
"""
Created on Thu May  5 00:01:15 2022

@author: 3b13j
"""

import numpy as np
from ipapy import *
from copy import deepcopy
from Natural_class import create_classes


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
            

    def __str__(self):
        return self.ipa +  " :  " + self.description + "\n" + str(self.features)




class IPA() :
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
        self.features = ['Syllabic', 'Consonant', 'Height', 'Backness',
                         'Round',    'Voiced',    'Nasal',
                         'Plosive',  'Fricative', 'Lateral', 'Trill', 'Aspirated']
        self.phonemes = [] 
        self.alphabet = {}
        self.feat2ipa = {}

        # reading consonants
        consonants = np.loadtxt('phonetic/consonants.tsv', delimiter='\t', dtype=str, encoding = 'utf8')
        arts = [int(x) for x in consonants[0][1:]]
        for line in consonants[1:]:
            manner = line[0]
            base = 0, 0, [0, 0, 0, 0, 0]
            if 'v' in manner:
                base[5] = 1
                manner = manner[:-1]

            if manner == 'N':
                base[6] = 1
            elif manner == 'P':
                base[7] = 1
            elif manner == 'S':
                base[8] = 1 # fricative, high
                base[3] = 2
            elif manner == 'F':
                base[8] = 1 # fricative, not so heigh
                base[3] = 1
            elif manner == 'A':
                base[8] = 1 # fricative, low = approximant
                base[3] = 0
            elif manner == 'Fl':
                base[10] = 1 # flap
            elif manner == 'T':
                base[10] = 2 # trill
            elif manner == 'Lf':
                base[9] = 1
                base[8] = 1
            elif manner == 'L':
                base[9] = 1
            elif manner == 'Lt':
                base[9] = 1
                base[10] = 1
                
                
            for i, ch in enumerate(line[1:]):
                if ch == '-':
                    continue
                feats = base.copy()
                feats[3] = arts[i]

                fts = tuple(feats)
                phon = archetype(ch, fts)

                self.phonemes.append(phon)
                self.alphabet[ch] = phon
                self.feat2ipa[fts] = ch

        # reading vowels
        vows = np.loadtxt('phonetic/vowels.tsv', delimiter='\t', dtype=str)
        front = [int(x) for x in vows[0][1:]]
        for line in vows[1:]:
            height = line[0]
            base = [1, 1, [0, 0], [0, 0]]
            if 'r' in height:
                base[3][0] = 1
                height = int(height[:-1])
            else:
                height = int(height)

            base[2][0] = height
                
            for i, ch in enumerate(line[1:]):
                if ch == '-':
                    continue
                feats = deepcopy(base)
                feats[2][1] = front[i]

                fts = tuple([tuple(f) if type(f) != int else f for f in feats])
                phon = archetype(ch, fts)

                self.phonemes.append(phon)
                self.alphabet[ch] = phon
                self.feat2ipa[fts] = ch
            
        
        #dic_class, classes = create_classes(self.alphabet)
        
        #self.classes = classes
        #self.dic_class = dic_class



    def get_char(self, phon, verbose=False):
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
        if phon.isVowel():
            # a basic vowel is voiced and unnasalised
            base = [x if i < 5 else 0 for i, x in enumerate(phon.features)]
            base[5] = 1
            base = tuple(base)
            out = self.feat2ipa[base]
            
            if phon.features[6] == 1: # nasal
                out += u'\u0303'

            if phon.features[5] == 0: # unvoiced
                out += u'\u0325'


        elif phon.isCons():
            base = [x for x in phon.features]
            base[11] = 0
            base[4] = 0
            if base[6] == 1:
                base[7] = 0
                base[8] = 0

            base = tuple(base)
            out = self.feat2ipa[base]            

            if phon.features[4] == 1: # round w
                out += 'ʷ'
            
            if phon.features[11] == 1: # aspirated
                out += 'ʰ'
            
        return out
    
