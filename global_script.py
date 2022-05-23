# -*- coding: utf-8 -*-
"""
Created on Wed May  4 11:09:46 2022

@author: 3b13j
"""
from wiki_utilities import get_language
from log_utilities import change2log, langcomp2log, lgs2log
from rd_changer import Tree_changer, Log_changer
from encoder_decoder import encoded_changes2log, decode_change, encode_p_change, encode_f , decode_log
import argparse



#we parse the arguments
print("Classical latin is our default language. To try to play with vulgar latin, please type 'vulgar'")
parser = argparse.ArgumentParser(description='Make a language evolve', prog = 'global_script.py')
parser.add_argument('--vulgar', help='do you want vulgar or not')
parser.add_argument('nb_change', type=int, help = 'The number of changes you want to simulate')
parser.add_argument('output_file', help = 'Path / name of the output logs')
parser.add_argument('--verbose', help = 'outputs the language at the end in the command line. Default value = False')
args = parser.parse_args()
latin = get_language('latin_classique.txt', "latin")
if args.vulgar : 
    latin =  get_language('latin_vulgar.txt', "latin")
    print("You had the choice and chose 'vulgar'.")
nc = args.nb_change
path = args.output_file



# We create an instance of a tree changer that's going to store the changes it applies to the language
time = Tree_changer(latin) 
nlp , changes = time.change(latin, nc ,True)
latin.compare(nlp)
# The changes are printed in a readable fashion on a document.
for ch in changes  :
    change2log(ch, path+"_changes.txt" ,nlp,  True)
langcomp2log (latin, nlp, path + "_dic.txt")
evolution = time.tree.languages
lgs2log(evolution)
if args.verbose : latin.print_both(nlp)



# We encode the changes in our not so readable format. 

encoded_changes2log(changes, path)
decode_log (path, True)

# We lastly apply the changes coded in the log to the origin language (and hope to get the same)
Suzanne =  Log_changer(latin,path+ "_encoded.txt" )
neo_lat, chaa = Suzanne.change(latin, nc, True)
if args.verbose : nlp.print_both(neo_lat)
if args.verbose :latin.print_both(neo_lat)

