# -*- coding: utf-8 -*-
"""
Created on Tue Jun 14 10:43:17 2022

@author: 3b13j
"""

# PROFILING

import re
import cProfile
from sys import platform
from pathlib import Path
from IPA import IPA  
from Wiki_utilities import get_language
from P_change_generator import Baby_P_change_generator
from log_utilities import change2log, langcomp2log,  samples2log, extract_changed_words, purge_log, changes2machinelog
from rd_changer import Tree_changer



i = IPA.get_IPA()

path = "tuesday"

depth = 500 # depth of a branch
nbranches = 1 # number of branches



# We choose a language to play with 

lang = get_language("English.txt", "latin")

#st = State(lang)

#lang = get_language("tokipona.txt", "tokipona")

#lang = get_language("greek.txt", "greek")



origin = lang
bb = Baby_P_change_generator()

time = Tree_changer(lang, bb) 

ml = time.make_evolution( lang , nbranches, depth) 



"""
liste = [[0, [0,0,0,1,0], 1] , [3, 1 ,0]]

from utilitaries import list_2_tuple, list_2_tuple2

print("recursive")
cProfile.run("for i in range (100000) : tu = list_2_tuple2(liste)")
print("imperative")
cProfile.run("for i in range (100000) : tu = list_2_tuple(liste)")
#cProfile.run("time.evoluate(lang, 1, 200)")


TEST POUR 200 CHANGEMENTS
version brute
216(list_2_tuple)
467618    2.399    0.000    2.559    0.000 utilitaries.py

version récursive
232(list_2_tuple)
      200    0.776    0.004    5.079    0.025 utilitaries.py
"""






# CCL : La méthode la plus gourmande en temps est list_2_tpl