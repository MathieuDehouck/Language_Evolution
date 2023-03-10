# -*- coding: utf-8 -*-
"""
Created on Sun May 29 21:36:10 2022

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
from Change import decode_log

from Language import State


i = IPA.get_IPA()

path = "slava"

depth = 20 # depth of a branch
nbranches = 1 # number of branches



# We choose a language to play with 

lang = get_language("Ukrainian.txt", "Latin")

#st = State(lang)

#lang = get_language("tokipona.txt", "tokipona")

#lang = get_language("greek.txt", "greek")



origin = lang
bb = Baby_P_change_generator()

time = Tree_changer(lang, bb) 
ml = time.make_evolution( lang , nbranches, depth) 
#origin.print_both(new_language)
#origin.compare(nlp)


# we write two logs to keep track of the changes
purge_log(path+"_changes.txt")
purge_log(path+"_dic.txt")
purge_log(path+"_machine_log.txt")


lgs, changes, wc = time.tree.get_a_change_path(ml)
new_language = lgs[-1]


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



print("We will now retro engineer the changes")

lc = Log_changer(origin, path3)
test_retro , ch = lc.change(origin, depth)
test_retro.print_both(new_language)



#time.tree.print_history_to_graph("virdia")

#k,e = time.tree.elaborate_history_graph('virdia')
#print(lang.voc)
#time.tree.history_to_graph(['virdia', 'abante'])
#time.tree.history_to_graph(['virdia', 'abante'])
#t = time.tree.get_final_state_of_the_evolution()
#for l in t : print (l.voc['virdia'])

#time.tree.print_history_to_graph_reduced("virdia")

#time.show_of_the_evolution(10)

#lf = random.choice(t)
#lf.evaluate_proximity(origin)

print(decode_log("logs/tuesday_machine_log.txt"))


evolution_2_log(time, "raw_data.txt")














# sale 


def get_couples(changer, clean_diacritics = False) :
    
    
    exs_set = []
    lvs = changer.tree.get_leaves ()
    root  = changer.tree.language
    
    
    for key, value in root.voc.items() :
       
        
        val = value.ipa
        
        if clean_diacritics :
        
            val = val.replace(":", "")
            val = val.replace("'", "")
            val = val.replace(".", "")
            val = val.replace(".", "")
            val = val.replace("'", "")
            val = val.replace("'", "")
        
       
        form_list = []
        for lf in lvs : 
            if lf.language.voc[key].ipa not in form_list :
                form = lf.language.voc[key].ipa
          
                if clean_diacritics :
                
                    form = form.replace(":", "")
                    form = form.replace("'", "")
                    form = form.replace(".", "")
                    form = form.replace(".", "")
                    form = form.replace("'", "")
                    form = form.replace("'", "")
                    
                
                    
                    
                form_list.append(form)
        for form in form_list : 
           exs_set.append([val , form ])
    
    return exs_set


couples = get_couples(time, True)

os.chdir('../')
fp = open("shared.pkl","wb")
pickle.dump(couples, fp)
print("done")