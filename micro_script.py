# -*- coding: utf-8 -*-
"""
Created on Sun May 29 21:36:10 2022

@author: 3b13j
"""
from utilitaries import *
from IPA import IPA  , linearize
from Natural_class import *
from wiki_utilities import get_language
from Configuration import Configuration 
from P_change_generator import Baby_P_change_generator


i = IPA.get_IPA()
for f in i.phonemes : 
    
    print(f.features)
    print(f.lin)

dc, c = create_classes(i)

latin = get_language("latin_classique.txt", "latin")
wd = latin.voc['werrizo']

pho = wd.phonemes [3]
"""
ci = Configuration(pho.lin)
print("CI", ci)
cf = ci.get_output()
print("CF", cf)
"""

bb = Baby_P_change_generator()
ch = bb.create_change(latin)
print(ch)

wd2 = ch.apply_word(wd, True)
print(wd2)


for phon in wd.phonemes :
    print(phon.ipa)
    print(phon.features)
    print(phon.lin)
