# -*- coding: utf-8 -*-
"""
Created on Tue May 17 13:04:22 2022

@author: 3b13j
"""

from Change  import P_change
from Tree import Root, L_tree, L_node
from encoder_decoder import decode_change
import copy



class Changer () :
    
   def  __init__(self) :
        return 
    
   def change_u (self, lang) :
       
       
       
       lang = copy.deepcopy(lang)
       change = P_change.rd_change(lang, False)
       while change.applicable(lang) != True :
           change = None
           change = P_change.rd_change(lang, False)
       
           
       
       nl = change.apply_language(lang)
       
      
       #change = None 
       dif = nl.compare(lang)
       if len(dif) == 0 :
           nl, change = self.change_u( lang)
           return nl, change
       else :
           return nl, change
    
   def change(self,lang, n, verbose = False) :
       
       changes = []
       lang = copy.deepcopy(lang)
       # we program n aleatory changes
       for i in range(n):
           if verbose : print("currently generatin chane", i)
           lang , change  = self.change_u ( lang)
           changes.append(change) 
           
    
       return lang, changes
       
class Tree_changer(Changer) :
    
    def __init__(self, lang) :
        super
        rt = Root(lang)
        tree = L_tree(rt)
        self.tree = tree
        
    
    def change_u (self, lang) :
        
        
        
        lang = copy.deepcopy(lang)
        change = P_change.rd_change(lang, False)
        while change.applicable(lang) != True :
            change = None
            change = P_change.rd_change(lang, False)
            
            
        
        nl = change.apply_language(lang)
        
       
        #change = None 
        dif = nl.compare(lang)
        if len(dif) == 0 :
            nl, change = self.change_u( lang)
        node = L_node(self.tree.last, nl)
        self.tree.graft(self.tree.last, node)
            
        return nl, change
      
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
        nl = change.apply_language(lang)
        return nl, change
    
    def change(self,lang, n, verbose = False) :
        lang = copy.deepcopy(lang)
        changes = []
        i = 0 
        for i in range(n):
            if verbose : print(" Retro engeneering change ", i)
            lang , change  = self.change_u ( lang, i)
            changes.append(change) 
            i+=1
        return lang, changes
        