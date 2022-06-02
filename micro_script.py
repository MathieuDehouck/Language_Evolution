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
from Phoneme import list_2_tuple , tuple_2_list
from Effect import Effect
from Condition import P_condition, rd_p_condition

i = IPA.get_IPA()




lang = get_language("latin_classique.txt", "latin")

#lang = get_language("tokipona.txt", "tokipona")

#lang = get_language("greek.txt", "greek")



origin = lang
bb = Baby_P_change_generator()

modifs = []

for i in range(1):
    
    
    
    ch = bb.create_change(lang, True, verbose = True)
    lang , chs_wds = ch.apply_language(lang)
    
    modifs.append(chs_wds)
    print(chs_wds)
    print(ch)

if len(ch.conditions) != 0 :
 print(   "we test a condition ")
 cond = ch.conditions[0]
 
