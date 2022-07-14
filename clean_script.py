# -*- coding: utf-8 -*-
"""


@author: 3b13j
"""

from sys import platform
from pathlib import Path
import os
import random
import argparse 



from Wiki_utilities import get_language
from P_change_generator import Baby_P_change_generator
from log_utilities import change2log, langcomp2log, evolution_2_log, samples2log, extract_changed_words, purge_log, changes2machinelog
from rd_changer import Tree_changer




parser = argparse.ArgumentParser(description='Make a language evolve')

parser.add_argument('Language', type=str,
                    help= 'select the language you want to play with')
parser.add_argument('depth', 
                    help='depth of the generated tree')
parser.add_argument('branches',  default=1,
                    help='Number of branches in the tree')
parser.add_argument('--logs',  default=False,
                    help='store data into logs ?')
parser.add_argument('--display',  default=False,
                    help='display a graph at the end of the derivation ?')

args = parser.parse_args()



path = args.Language + ".txt"
depth = int(args.depth)
nbranches = int(args.branches)
lang = get_language(path, "origin")


bb = Baby_P_change_generator()
time = Tree_changer(lang, bb) 
ml = time.make_evolution( lang , nbranches, depth) 


if args.logs :    
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
    langcomp2log (lang, new_language, path + "_dic.txt")
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




if  args.display :
    wds = random.choices(list(lang.voc.keys()) ,k=5)
    time.tree.history_to_graph(wds)
