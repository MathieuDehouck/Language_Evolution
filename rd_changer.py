# -*- coding: utf-8 -*-
"""
Created on Tue May 17 13:04:22 2022

@author: 3b13j
"""

from Change  import P_change
from Tree import  L_tree

from Generator import Change_Generator

import copy



class Changer () :
    
   def  __init__(self, gen = None) :
       #TODO modified for the new micro script
        if gen == None : self.generator = Change_Generator() 
        else : self.generator = gen
    
    
   def change_u (self, lang) :
       
      NotImplemented
    
   def change(self,lang, n, verbose = False) :
       
       
       changes = []
       wc = []
       lang = copy.deepcopy(lang)
       # we program n aleatory changes
       for i in range(n):
           
           if verbose : 
               print()
               print("Currently generating change", i+1)
               print()
           lang , change , changed_words = self.change_u ( lang)
           
           
           changes.append(change) 
           
           
           wc.append(changed_words)
           
           if verbose : print("Change ", i+1, " created")
    
       return lang, changes, wc
       
class Tree_changer(Changer) :
    
    def __init__(self, lang, gen = None) :
        super().__init__(gen)
        
        tree = L_tree(lang)
        self.tree = tree
        self.current_tree = self.tree
        
    
    def change_u (self, lang, verbose = False) :
        
        
        
        
        change = self.generator.generate_P_change(lang)
        
        """
        while change.applicable(lang) != True :
            change = None
            change = self.generator.generate_P_change(lang)
            
        """    
        
        nl, wc = change.apply_language(lang)
        
       
        """
        
        dif = nl.compare(lang)
        if len(dif) == 0 :
            nl, change, wc = self.change_u( lang)
            
        """
        self.current_tree.change = change
        new_tree = L_tree(nl, self.current_tree)
        self.current_tree = new_tree
        
            
        return nl, change, wc
    
    
    def pursue_evolution(self, wanted_depth , node = None) :
        
       dic = self.tree.get_ad_2_tree()
        
       if node == None : node = self.tree.pick_a_node()
       #node is an adress 
       
       expanded_tree = dic[node]
       
       for nch in range(wanted_depth -expanded_tree.depth) :
           change = self.generator.generate_P_change(expanded_tree.language)
           nl, wc = change.apply_language(expanded_tree.language)
           new_tree = L_tree(nl, expanded_tree)
           expanded_tree = new_tree
    
    def octopus(self, nb_branches, depth) :
        
        
        for i in range(nb_branches -1) :
            print("grafting branch ",i+1)
            self.pursue_evolution(depth)
    
    
    
    
    
      
class Log_changer(Changer) :
    
    def __init__(self, lang, path) :
        
        super().__init__() 
        
        
        f= open(path, "r", encoding = 'utf8')
        lines = []
        for line in f : lines.append(line)
        
        
        self.file = lines
        
    
    def change_u (self, lang, index ) :
      
        
        change = P_change.decode_change(self.file[index])
        print(self.file[index])
        nl, wc  = change.apply_language(lang)
        return nl, change, wc
    
    def change(self,lang, n, verbose = False) :
        
        changes = []
        i = 0 
        for i in range(n):
            if verbose : print(" Retro engeneering change ", i)
            lang , change, wc  = self.change_u ( lang, i)
            changes.append(change) 
            i+=1
        return lang, changes
        
    
    
   
    
    
    
    
    
    
    
    