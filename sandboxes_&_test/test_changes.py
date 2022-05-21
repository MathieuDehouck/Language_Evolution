# -*- coding: utf-8 -*-
"""
Created on Tue May 17 10:44:07 2022

@author: 3b13j
"""

from usual_changes import nasalisation
from language import get_language
from word import Word

latin = get_language('latin_classique.txt') 

def test_nasalisation_abs():
    wd = latin.voc['virdia']
    wd = Word([wd.syllables[-2]])
    change = nasalisation

    fts = wd.phonemes
    #fts = [f.features for f in fts]

    for f in fts:
        print(f.ipa, f.features)

    print(nasalisation)

    out = change.apply_word(wd, True)

    fts = out.phonemes
    #fts = [f.features for f in fts]

    for f in fts:
        print(f.ipa, f.features)
    
    assert(out.ipa == 'mmmnmm')
