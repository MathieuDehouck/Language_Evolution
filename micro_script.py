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


latin = get_language("latin_classique.txt", "latin")
wd = latin.voc['werrizo']


"""
ci = Configuration(pho.lin)
print("CI", ci)
cf = ci.get_output()
print("CF", cf)

"""
bb = Baby_P_change_generator()

ch = bb.create_change(latin)

print(ch)



latin2 , chs_wds = ch.apply_language(latin)
#latin.print_both(latin2)
print(chs_wds)
