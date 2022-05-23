# -*- coding: utf-8 -*-
"""
Created on Tue May 17 13:04:22 2022

@author: 3b13j
"""

from Change  import P_change
from Tree import Root, L_tree, L_node
from encoder_decoder import decode_change
from Generator import Change_Generator

import copy



class Changer () :
    
   def  __init__(self) :
        self.generator = Change_Generator() 
    
   def change_u (self, lang) :
       
       
       
       lang = copy.deepcopy(lang)
       change = P_change.rd_change(lang, False)
       while change.applicable(lang) != True :
           change = None
           change = P_change.rd_change(lang, False)
       
           
       
       nl , changed_words = change.apply_language(lang)
       
      
       #change = None 
       dif = nl.compare(lang)
       if len(dif) == 0 :
           nl, change = self.change_u( lang)
           return nl, change, changed_words
       else :
           return nl, change, changed_words
    
   def change(self,lang, n, verbose = False) :
       
       
       changes = []
       wc = []
       lang = copy.deepcopy(lang)
       # we program n aleatory changes
       for i in range(n):
           if verbose : print("currently generating change", i)
           lang , change , changed_words = self.change_u ( lang)
           changes.append(change) 
           wc.append(changed_words)
           
    
       return lang, changes, wc
       
class Tree_changer(Changer) :
    
    def __init__(self, lang) :
        super().__init__()
        rt = Root(lang)
        tree = L_tree(rt)
        self.tree = tree
        
    
    def change_u (self, lang) :
        
        
        
        lang = copy.deepcopy(lang)
        change = self.generator.generate_p_change(lang)
        while change.applicable(lang) != True :
            change = None
            change = self.generator.generate_p_change(lang)
            
            
        
        nl, wc = change.apply_language(lang)
        
       
        #change = None 
        dif = nl.compare(lang)
        if len(dif) == 0 :
            nl, change, wc = self.change_u( lang)
        node = L_node(self.tree.last, nl)
        self.tree.graft(self.tree.last, node)
            
        return nl, change, wc
      
class Log_changer(Changer) :
    
    def __init__(self, lang, path) :
        
        super().__init__() 
        
        
        f= open(path, "r", encoding = 'utf8')
        lines = []
        for line in f : lines.append(line)
        
        
        self.file = lines
        
    
    def change_u (self, lang, index ) :
        
        lang = copy.deepcopy(lang)
        change = decode_change(self.file[index])
        print(self.file[index])
        nl, wc  = change.apply_language(lang)
        return nl, change, wc
    
    def change(self,lang, n, verbose = False) :
        lang = copy.deepcopy(lang)
        changes = []
        i = 0 
        for i in range(n):
            if verbose : print(" Retro engeneering change ", i)
            lang , change, wc  = self.change_u ( lang, i)
            changes.append(change) 
            i+=1
        return lang, changes
        