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
from log_utilities import change2log, langcomp2log, lgs2log, samples2log, extract_changed_words, purge_log
from rd_changer import Tree_changer, Log_changer
from encoder_decoder import encoded_changes2log, decode_change, encode_p_change, encode_f , decode_log


import os 

i = IPA.get_IPA()

path = "friday"


#lang = get_language("latin_classique.txt", "latin")

#lang = get_language("tokipona.txt", "tokipona")

lang = get_language("greek.txt", "greek")



origin = lang
bb = Baby_P_change_generator()

time = Tree_changer(lang, bb) 
new_language , changes, wc = time.change(lang, 50,True)
origin.print_both(new_language)
#origin.compare(nlp)


# we write two logs to keep track of the changes
purge_log(path+"_changes.txt")
purge_log(path+"_dic.txt")
for i in range(len(changes))  :
    change2log(changes[i], path+"_changes.txt" ,new_language,  True, i+1)
    samples2log(path+"_changes.txt", wc[i])
langcomp2log (lang, new_language, path + "_dic.txt")
extract_changed_words(path + "_dic.txt", True)

 # we open
folder = Path("logs/")

path1 = path+"_changes.txt"
path2 = path + "_dic.txt"

path1 = folder / path1
path2 = folder / path2
os.startfile(path1 )
os.startfile(path2 )




