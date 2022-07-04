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


"""
# TEST 1 : debug at each step 

l = lang
for i in range(depth) :
    nl, ch, w = time.change_u(l)
  
 
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


    diff = nl.evaluate_proximity(nl2)
    if diff != 1 : break 
    l = nl

"""    
    





# target qui faisaitt bugger ((7, (0, 0, 0, 2, 0), 1), (11, 0, 0))


# TEST 2 compute similarity globally 

l = lang
l2 = lang

for i in range(depth) :
    
    nl, ch, w = time.change_u(l)
    
    st = ch.encode_change()
    ncopy_ch = Change.decode_change(st)
    
    nl2 , cw = ncopy_ch.apply_language(l2)
    

    
    
    diff = nl.evaluate_proximity(nl2)
    if diff != 1 :
        
        # TODO
        # Le problème semble venir des métathèses , le changement n'est pas appliqué à la langue 2 
        # PB during the application of metathesis. 
        
        """
        for key, value in nl2.voc.items() :
            if value != nl.voc[key] :
                print()
                print("dif wd")
                print()
                print("l")
                print(l.voc[key])
                print("l2")
                print(l2.voc[key])
                print("nl")
                print(nl.voc[key])
                print("nl2")
                print(nl2.voc[key])
                
                change = True
                
            
        print()
        print("old)")
        print(ch)
        print()
        print("new")
        print(ncopy_ch)
        """
        
        print()
        print("we lost at ",i)
        
    
    l = nl
    l2 = nl2

print("verdict")
l.evaluate_proximity(l2)