# -*- coding: utf-8 -*-
"""
Created on Sun Jul  3 11:57:33 2022

@author: 3b13j
"""

from sys import platform
from pathlib import Path
import os
import pickle 

from utilitaries import *
from IPA import IPA  
from Wiki_utilities import get_language
from P_change_generator import Baby_P_change_generator
from log_utilities import change2log, langcomp2log, evolution_2_log, samples2log, extract_changed_words, purge_log, changes2machinelog
from rd_changer import Tree_changer, Log_changer
from encoder_decoder import encoded_changes2log, encode_f 
from Condition import Condition
from Change import decode_log, Change

from Language import State


i = IPA.get_IPA()

path = "debug_logs"

depth = 110 # depth of a branch
nbranches = 1 # number of branches
 

lang = get_language("latin_classique.txt", "Latin")


origin = lang
bb = Baby_P_change_generator()
time = Tree_changer(lang, bb) 




l = lang
for i in range(depth) :
    nl, ch, w = time.change_u(l)
    """
    print()
    print("we encode this")
    print()
    print()
    print(ch)
    print()
    """
    
    st = ch.encode_change()
    ncopy_ch = Change.decode_change(st)
    nl2 , cw = ncopy_ch.apply_language(l)
    
    change = False
    for key, value in nl2.voc.items() :
        if value != nl.voc[key] :
            print()
            print("dif wd")
            print()
            print(value)
            print(nl.voc[key])
            change = True
        
    if change :
        
    
    #if ch != ncopy_ch :
     
        print()
        print()
        print ("copy failure")
        print(i)
        print("old")
        print(ch)
        print("new")
        print(ncopy_ch)
        break

    l = nl







