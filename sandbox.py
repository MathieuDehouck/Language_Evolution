# -*- coding: utf-8 -*-
"""
Created on Tue May 24 14:54:48 2022

@author: 3b13j
"""
from utilitaries import printl
from wiki_utilities import get_language
from log_utilities import change2log, langcomp2log, lgs2log, samples2log, tpl2phons
from rd_changer import Tree_changer, Log_changer
from encoder_decoder import encoded_changes2log, decode_change, encode_p_change, encode_f , decode_log
import argparse
from IPA import IPA 
from Change import S_change

ipa = IPA() 
fts = ipa.features


latin = get_language("latin_classique.txt", "latin")

from Generator import Change_Generator
from Condition import S_condition

gen = Change_Generator()
ch = gen.generate_S_cond(latin)
#print(ch)

def print_non_wildcard(tpl) :
    for i, ft in enumerate(tpl) :
        if ft != -1 :
            print (fts[i], "  :  ", str(ft)  )

    
def pretty_print_change(change, lang) :
    print("Target : ")
    print(change.target)
    #printl(tpl2phons(change.target, latin.phonemes ))
    print()
    print("Effect : ")
    for i, ft in enumerate(change.config_initiale.state ) : 
        if ft != -1 :
            print (fts[i], "  :  ", str(change.config_initiale.state[i]) ,"  >  ", str(change.config_finale.state[i]) )
     
    print()
    print("Conditions  : ")
    for i,  cond in enumerate (change.conditions) :
        print("C ", str(i), " : ", str(cond.template) )
        print_non_wildcard(cond.template)
    print("Modified phonemes :")
    print([phon.ipa for phon   in tpl2phons(change.target, latin.phonemes ) ])
    
    
    
#pretty_print_change(ch, latin)












wd = latin.voc["virdia"]

"""
print(wd)
print()
printl(wd.syllables)
print ("TEST")
for  i in range(len(wd.syllables)) :
    print(i, ch.test(wd, i, latin))
"""

sc = S_change([None, True, None], [None, False, None])
#TODO gérer les None, cas om c estg non spécifié

wd2 = sc.apply_word(wd)


print(wd.get_stess_patter())
print(wd2.get_stess_patter())


for word in latin.voc.values() :
    print(word.get_stess_patter())
    print(word.ipa)
    wd2 = sc.apply_word(word)
    
    print(wd2.get_stess_patter())
    print()