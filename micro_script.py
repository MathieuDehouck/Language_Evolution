# -*- coding: utf-8 -*-
"""
Created on Sun May 29 21:36:10 2022

@author: 3b13j
"""

from sys import platform
from pathlib import Path
import os

from utilitaries import *
from IPA import IPA  
from Wiki_utilities import get_language
from P_change_generator import Baby_P_change_generator
from log_utilities import change2log, langcomp2log,  samples2log, extract_changed_words, purge_log, changes2machinelog
from rd_changer import Tree_changer, Log_changer
from encoder_decoder import encoded_changes2log, encode_f 
from Condition import Condition
from Change import P_change 

from Language import State


i = IPA.get_IPA()

path = "tuesday"

depth = 100 # depth of a branch
nbranches = 42 # number of branches



# We choose a language to play with 

lang = get_language("latin_classique.txt", "latin")

#st = State(lang)

#lang = get_language("tokipona.txt", "tokipona")

#lang = get_language("greek.txt", "greek")



origin = lang
bb = Baby_P_change_generator()

time = Tree_changer(lang, bb) 
time.make_evolution( lang , nbranches, depth) 
#origin.print_both(new_language)
#origin.compare(nlp)


# we write two logs to keep track of the changes
purge_log(path+"_changes.txt")
purge_log(path+"_dic.txt")
purge_log(path+"_machine_log.txt")
"""
for i in range(len(changes))  :
    change2log(changes[i], path+"_changes.txt" ,new_language,  True, i+1)
    samples2log(path+"_changes.txt", wc[i])
    changes2machinelog(path+"_machine_log.txt", changes[i])
langcomp2log (origin, new_language, path + "_dic.txt")
extract_changed_words(path + "_dic.txt", True)


# we open
folder = Path("logs/")

path1 = path+"_changes.txt"
path2 = path + "_dic.txt"
path3 = path + "_machine_log.txt"

path1 = folder / path1
path2 = folder / path2
path3 = folder / path3



if platform != 'linux':
    os.startfile(path1 )
    os.startfile(path2 )
    os.startfile(path3 )

"""
"""
print("We will now retro engineer the changes")

lc = Log_changer(origin, path3)
test_retro , ch = lc.change(origin, nb_changes)
test_retro.print_both(new_language)
"""


#time.tree.print_history_to_graph("virdia")

#k,e = time.tree.elaborate_history_graph('virdia')
#print(lang.voc)
#time.tree.history_to_graph(['virdia', 'abante'])
#time.tree.history_to_graph(['virdia', 'abante'])
t = time.tree.get_final_state_of_the_evolution()
#for l in t : print (l.voc['virdia'])

#time.tree.print_history_to_graph_reduced("virdia")

time.show_of_the_evolution(5)
