# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 16:25:07 2022
Parse. script used to parse another Conllu file once the classifier is trained
@author: 3b13j
"""
from conllu_converter import  extract_conllu

import shared
import argparse



def parse_conllu_file(path, output_path) :
    
    sentences = extract_conllu(path)
    parser = shared.parser 
    parser.Parsing_to_log(sentences, output_path)
    

arguments = argparse.ArgumentParser(description='Parsing d un autre fichier', prog = 'parse_file.py')
arguments.add_argument('input_file',type = str, help='fichier à parser')
arguments.add_argument('output_file',type = str, help='adresse du log qui testera le parser')

arguments = arguments.parse_args()



