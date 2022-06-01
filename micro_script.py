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

i = IPA.get_IPA()




latin = get_language("latin_classique.txt", "latin")
toki = get_language("tokipona.txt", "tokipona")


wd = latin.voc['werrizo']
pho = wd.phonemes[0]
ci = Configuration(pho)



c = ci.state
print(pho)
for loop in range(20) :
    ef = Effect(pho)
    print(ef)
    print()



lang = toki

bb = Baby_P_change_generator()
ch = bb.create_change(lang, True)
latin2 , chs_wds = ch.apply_language(lang)


#latin.print_both(latin2)
print(chs_wds)

