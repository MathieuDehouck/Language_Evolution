# -*- coding: utf-8 -*-
"""
Created on Sun May 29 21:36:10 2022

@author: 3b13j
"""
from utilitaries import *
from IPA import IPA  , linearize
from Natural_class import *
from wiki_utilities import get_language

i = IPA()
for f in i.phonemes : 
    
    print(f.features)
    print(f.lin)

dc, c = create_classes(i)

printl(c)

latin = get_language("latin_classique.txt", "latin")
printd(latin.voc)

wd = latin.voc['werrizo']