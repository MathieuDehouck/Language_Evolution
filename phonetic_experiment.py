# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 12:01:10 2022

@author: 3b13j
"""

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

path = "likkle_exp"
depth = 20 # depth of a branch
nbranches = 20 # number of branches



# We choose a language to play with 
mother = get_language("Estonian.txt", "Estonian")

lang = mother
origin = mother
bb = Baby_P_change_generator()
time = Tree_changer(mother, bb) 
ml = time.make_evolution( lang , nbranches, depth) 

daughters = [x.language for x in time.tree.get_leaves()]

wds = random.choices(list(mother.voc.keys()), k=5)
#wds = [wd.ipa for wd in wds]

time.tree.history_to_graph(wds)


# creation of a csv


import csv 
    
# field names 
fields = ['Language id', 'word1', 'word2', 'word3', 'word4', 'word5', "Phonetic inventory similarity ", "Exact Phoneme match similarity ", "Levensthein distance (nltk implementaiton", "Feature match similarity"] 



rows = []
# creation of the rows 

for i, leaf in enumerate(daughters) :
    row = []
    st = "language " +str(i)
    row.append(st)
    
    for wd in wds :
        row.append (leaf.voc[wd].ipa)
    
    invent_sim , diff = mother.inventory_comparison(leaf)
    phon_sim = mother.phoneme_comparison(leaf)
    feat_sim = mother.feature_comparison(leaf)
    lev = mother.Levensthein(leaf)
    
    row.append(invent_sim)
    row.append(phon_sim)
    row.append(feat_sim)
    row.append(lev)
    rows.append(row)


 
filename = "phonetic experiment.csv"
    
# writing to csv file 
with open(filename, 'w', encoding = 'utf8') as csvfile: 
    # creating a csv writer object 
    csvwriter = csv.writer(csvfile) 
        
    # writing the fields 
    csvwriter.writerow(fields) 
        
    # writing the data rows 
    csvwriter.writerows(rows)



