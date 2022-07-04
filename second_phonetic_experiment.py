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

path = "likkle_exp_2"
depth = 100 # depth of a branch
nbranches = 1



# We choose a language to play with 
mother = get_language("latin_classique.txt", "LAT")

lang = mother
origin = mother
bb = Baby_P_change_generator()

time = Tree_changer(mother, bb) 




wds = random.choices(list(mother.voc.keys()), k=5)



# creation of a csv


import csv 
    
# field names 
fields = ['Language id', 'word1', 'word2', 'word3', 'word4', 'word5', "Phonetic inventory similarity ", "Exact Phoneme match similarity ", "Feature match similarity", "Levensthein distance (nltk implementaiton"] 



rows = []
# creation of the rows 

current_1 = time.tree.language
current_2 = time.tree.language

ch_per_step = 5




row = [" mother language"]
for wd in wds :
    row.append (current_1.voc[wd].ipa)
row.append(1)
row.append(1)
row.append(1)
row.append(0)
rows. append(row)

for j in range(10) :
    
        rows.append (["# with "+str(ch_per_step*(j+1))+" changes"])
    
        row = []
        st = "language 1 "
        
        current_1 = time.change(current_1 ,ch_per_step) [0]
        
        row.append(st)
        

        
        for wd in wds :
            row.append (current_1.voc[wd].ipa)
        
        invent_sim , diff = mother.inventory_comparison(current_1)
        phon_sim = mother.phoneme_comparison(current_1)
        feat_sim = mother.feature_comparison(current_1)
        lev = mother.Levensthein(current_1)
        
        row.append(invent_sim)
        row.append(phon_sim)
        row.append(feat_sim)
        row.append(lev)
        rows.append(row)
        
        row = []
        st = "language 2 "
        
        current_2 = time.change(current_2 ,ch_per_step)[0]
        
        row.append(st)
        

        
        for wd in wds :
            row.append (current_2.voc[wd].ipa)
        
        invent_sim , diff = mother.inventory_comparison(current_2)
        phon_sim = mother.phoneme_comparison(current_2)
        feat_sim = mother.feature_comparison(current_2)
        lev = mother.Levensthein(current_2)
        
        row.append(invent_sim)
        row.append(phon_sim)
        row.append(feat_sim)
        row.append(lev)
        rows.append(row)

        row = []
        row.append("Comparison between the two languages")
        for wd in wds :
            row.append ("       ")
        
        invent_sim , diff = current_1.inventory_comparison(current_2)
        phon_sim = current_1.phoneme_comparison(current_2)
        feat_sim = current_1.feature_comparison(current_2)
        lev = current_1.Levensthein(current_2)
        
        row.append(invent_sim)
        row.append(phon_sim)
        row.append(feat_sim)
        row.append(lev)
        rows.append(row)

 
filename = "second_phonetic_experiment.csv"
    
# writing to csv file 
with open(filename, 'w', encoding = 'utf8') as csvfile: 
    # creating a csv writer object 
    csvwriter = csv.writer(csvfile) 
        
    # writing the fields 
    csvwriter.writerow(fields) 
        
    # writing the data rows 
    csvwriter.writerows(rows)



