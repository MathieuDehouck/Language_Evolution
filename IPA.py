# -*- coding: utf-8 -*-
"""
Created on Thu May  5 00:01:15 2022

@author: 3b13j
"""

import numpy as np
from IPA_utils import manner_enc
from Phoneme import Vowel, Consonant
from ipapy import UNICODE_TO_IPA


class archetype(object) :
    """
    A class to represent an archetypal phoneme (phoneme belonging to the IPA)
    These objects are not mutable

    ...

    Attributes
    ----------
    ipa : str
        character representing the phoneme in the IPA
    features : tuple in a format we defined that represent key informations to define a phoneme's property'
    description : str
        precise description of the phoneme (obtained using the IPA python module)

    Methods
    -------
    __init__(str, liste) 
        the constructor, that takes the ipa and features as attributes
        
        
    is_Vowel
    is_Consonant
    get_one
    """
    
    def __init__(self, string, feats, vow):
        self.ipa = string
        self.features = feats
        self.vow = vow
        try:
            self.description = UNICODE_TO_IPA[string]._IPAChar__canonical_string
        except:
            self.description = 'No description'
       
        
       


    def __str__(self):
        return self.ipa +  " :  " + self.description + "\n" + str(self.features)

    def is_Vowel(self):
        return self.vow

    def is_Consonant(self):
        return not self.vow
    

    def get_one(self, extra_feats, syllabic):
        """
        I'll change this eventually
        """
        base = self.features[0]
        
        if self.vow:
            extra = [1, 0]
            if 'nasalised' in extra_feats:
                extra[1] = 1
            return Vowel((base ,tuple(extra)), syllabic, IPA.get_IPA())
        else:
            extra = [0, 0, 0]
            if 'pre_nasal' in extra_feats:
                extra[1] = 1
            if 'aspirated' in extra_feats:
                extra[2] = 1
            if 'labialised' in extra_feats:
                extra[0] = 11
            if 'unvoiced' in extra_feats:
                base = base[0], base[1], 0

            return Consonant((base, tuple(extra)), syllabic, IPA.get_IPA())




def cons_dist(features, consonants):
    """
    computes the distance between a cons features and a set of consonants
    """
    dists = []
    (xplace, xmanner, xvoice), _ = features
    for ((place, manner, voice), _), ch in consonants.items():
        if manner == xmanner:
            dists.append(((place - xplace)**2 + (voice - xvoice)**2 / 2, (place, voice), ch))
    dists.sort()

    return dists




def vowel_dist(features, vowels):
    """
    computes the distance between a vow features and a set of vowells
    """
    dists = []
    (xh, xb, xr), _ = features
    for ((yh, yb, yr), _), ch in vowels.items():
        dists.append(((xh-yh)**2 + (xb-yb)**2 + (xr-yr)**2 - (yh-3)**2/100, (yh, yb, yr), ch))
    dists.sort()

    return dists
        
        
        
        

class IPA() :
    """
    A singleton class to represent the IPA viewed as a set of archetypal phonemes.

    ...

    Attributes
    ----------
    cfeatures or vfeatures : list
        list of the str corresponding to the name of the features used in this IPA to describe the phonemes . it describe their semantics
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
        self.vfeatures = ('Height','Backness', 'Round'), ('Voiced', 'Nasal')
        self.cfeatures = ('place of articulation', ('nasal', 'plosive', 'fricative', 'trill', 'lateral'), 'Voiced'), ('secondary place of articulation', 'pre_nasal' , 'aspiration')
        self.phonemes = [] 
        self.alphabet = {}
        self.feat2ipa = {}
        self.cons2ipa = {}
        self.vow2ipa = {}

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
                phon = archetype(ch, fts, False)

                if fts in self.feat2ipa:
                    continue
                self.phonemes.append(phon)
                self.alphabet[ch] = phon
                self.feat2ipa[fts] = ch
                self.cons2ipa[fts] = ch

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
                phon = archetype(ch, fts, True)

                self.phonemes.append(phon)
                self.alphabet[ch] = phon
                self.feat2ipa[fts] = ch
                self.vow2ipa[fts] = ch





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

        # We did not find a perfect match, so we build it
        feats = phon.features
        if phon.is_Vowel():
            # a basic vowel is voiced and unnasalised
            base = feats[0], (1, 0)
            if base in self.vow2ipa:
                out = self.vow2ipa[base]
            else:
                # try flip round
                base = (feats[0][0], feats[0][1], 1-feats[0][2]), (1, 0)
                if base in self.vow2ipa:
                    out = self.vow2ipa[base]
                    if feats[0][2] == 1:
                        out += u'\u0339'
                    elif feats[0][2] == 0:
                        out += u'\u031C'
                else:
                    # compute distance in the vowel space
                    dist = vowel_dist(feats, self.vow2ipa)
                    xh, xb, xr = feats[0]
                    #print(dist)
                    _, (yh, yb, yr), out = dist[0]

                    if xh > yh:
                        out += u'\u031E'
                    elif xh < yh:
                        out += u'\u031D'

                    if xr == 1 and xr != yr:
                        out += u'\u0339'
                    elif xr == 0 and xr != yr:
                        out += u'\u031C'

                
            if phon.is_nasal(): # nasal
                out += u'\u0303'

            if not phon.is_voiced(): # unvoiced
                out += u'\u0325'


        else:
            base = feats[0], (0, 0, 0)
            if base in self.cons2ipa:
                out = self.cons2ipa[base]
            elif feats[0][1] == (0, 1, 1, 0, 0):
                # thats an affricate
                plos = (feats[0][0], (0, 1, 0, 0, 0), feats[0][2]), (0, 0, 0)
                fric = (feats[0][0], (0, 0, 1, 0, 0), feats[0][2]), (0, 0, 0)

                if plos in self.cons2ipa:
                    out = self.cons2ipa[plos]

                elif feats[0][0] in [6, 8]:
                    plos = (7, (0, 1, 0, 0, 0), 1-feats[0][2]), (0, 0, 0)
                    out = self.cons2ipa[plos]
                else:
                    plos = (feats[0][0], (0, 1, 0, 0, 0), 1-feats[0][2]), (0, 0, 0)
                    out = self.cons2ipa[plos]

                if fric in self.cons2ipa:
                    out += u'\u035c' + self.cons2ipa[fric]
                else:
                    fric = (feats[0][0], (0, 0, 1, 0, 0), 1-feats[0][2]), (0, 0, 0)
                    out += u'\u035c' + self.cons2ipa[fric]

            else:
                # try flipping voicing
                base = (feats[0][0], base[0][1], 1-feats[0][2]), (0, 0, 0)
                if base in self.cons2ipa:
                    #print(base, feats)
                    out = self.cons2ipa[base]

                    if feats[0][2] == 1:
                        out += u'\u032C'
                    elif feats[0][2] == 0:
                        out += u'\u0325'

                else:
                    dist = cons_dist(feats, self.cons2ipa)
                    
                    _, (part, voice), out = dist[0]
                    
                    if feats[0][2] == 1 and feats[0][2] != voice:
                        #print(out)
                        out += u'\u032C'
                    elif feats[0][2] == 0 and feats[0][2] != voice:
                        out += u'\u0325'
                    
                    direction = feats[0][0] - part
                    #print(direction)
                    if direction < 0:
                        for _ in range(abs(direction)):
                            #out += u'\u034F'
                            out += u'\u0320'
                    else:
                        for _ in range(abs(direction)):
                            #out += u'\u034F'
                            out += u'\u031F'



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
