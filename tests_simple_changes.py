# -*- coding: utf-8 -*-
"""
Created on Tue May 17 10:44:07 2022

@author: 3b13j
"""

import unittest 
from global_script import latin
from usual_changes import *
import copy

class Change_test(unittest.TestCase):
    
     
    def setUp(self ) :
        self.wd = latin.voc["virdia"]
        
    def test_nasalisation_abs(self) :
        change = copy.deepcopy(nasalisation)
        
        out = change.apply_word(self.wd)
        self.assertEqual ( out.ipa,  "mmmnmm" , 'incorrect change application')
    
    def test_nasalisation_cs(self) :
        
        change = copy.deepcopy(nasalisation)
        c = class_conditions["consonnes"]
        change.add_condition(c)
        out = change.apply_word(self.wd)
        self.assertEqual ( out.ipa,  "wimnia" , 'incorrect change application')
        
    def test_nasalisation_plosives(self) :
        
        change = copy.deepcopy(nasalisation)
        c = class_conditions["plosives"]
        change.add_condition(c)
        out = change.apply_word(self.wd)
        self.assertEqual ( out.ipa,  "wirnia" , 'incorrect change application')
        



test = Change_test()
test.setUp()
unittest.main() 


for i in range (100) :
    feature =feature_random_generator()   
    res = []
    
    res = latin.belong_language(feature)
    if len(res) != 0 :
        
        print(feature)
        printl(res)
        print("")
    
    print

print(test.wd)