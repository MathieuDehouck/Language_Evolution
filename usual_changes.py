# -*- coding: utf-8 -*-
"""
Created on Thu May  5 14:21:16 2022

@author: 3b13j
"""

from Configuration import Configuration
from Change import P_change
from pathlib import Path
from encoder_decoder import decode_f

folder = Path ("phonetic/")
path = folder / "usual_p_changes.csv"
usual_changes = {}
f = open (path, "r", encoding = "utf8")
for line in f :
    
    line = line.split(',') 
    name = line[0]
    ci = Configuration(decode_f(line[1]))
    cf = Configuration(decode_f(line[2]))
    change = P_change(ci, cf)
    usual_changes[name] = change