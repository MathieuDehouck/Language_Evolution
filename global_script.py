# -*- coding: utf-8 -*-
"""
Created on Wed May  4 11:09:46 2022

@author: 3b13j
"""
from utilitaries import printl, printd
from wiki_utilities import get_language
from log_utilities import change2log, langcomp2log, lgs2log
from rd_changer import Tree_changer, Log_changer
from encoder_decoder import encoded_changes2log, decode_change, encode_p_change, encode_f
import argparse



#we parse the arguments
print("Classical latin is our default language. To try to play with vulgar latin, please type 'vulgar'")
parser = argparse.ArgumentParser(description='Make a language evolve', prog = 'global_script.py')
parser.add_argument('--vulgar', help='do you want vulgar or not')
parser.add_argument('nb_change', type=int, help = 'The number of changes you want to simulate')
parser.add_argument('output_file', help = 'Path / name of the output logs')
args = parser.parse_args()
latin = get_language('latin_classique.txt', "latin")
if args.vulgar : 
    latin =  get_language('latin_vulgar.txt', "latin")
    print("yYu had the choice and chose 'vulgar'.")
nc = args.nb_change
path = args.output_file



# We create an instance of the programm
time = Tree_changer(latin) 
nlp , changes = time.change(latin, nc ,True)
latin.compare(nlp)


f = open (path + ".txt", "a")
for ch in changes  :
    change2log(ch, path+".txt" ,nlp,  True)
langcomp2log (latin, nlp, path + "_dic.txt")


evolution = time.tree.languages
lgs2log(evolution)

#latin.print_both(nl)

"""
f = open("log_changes.txt", "w", encoding = "utf8") 
f.close () 

encoded_changes2log(changes)

copych = []
f = open("log_changes.txt", "r", encoding = "utf8") 
j= 0
for line in f : 
    print(j)
    j = j+1
    chan =  decode_change(line)
    copych.append(chan)
f.close()
f2 = open("log_changes_encoded_decoded.txt", "w", encoding = "utf8")

for chain in copych :
    string = encode_p_change(chain) 
    f2.write(string)
    
    f2.write("\n")
f2.close()

   
Suzanne =  Log_changer(latin,"log_changes.txt" )

neo_lat, chaa = Suzanne.change(latin, nc, True)
nlp.print_both(neo_lat)

latin.print_both(neo_lat)

"""