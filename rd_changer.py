# -*- coding: utf-8 -*-
"""
Created on Tue May 17 13:04:22 2022

@author: 3b13j
"""

from Change  import P_change, I_change
from Tree import  L_tree
from tqdm import tqdm, trange
from Generator import Change_Generator

import copy




class Changer () :

    def  __init__(self, gen = Change_Generator()) :
        #TODO modified for the new micro script
        self.generator = gen
     
     
    def change_u (self, lang) :
         """
         What that does ?
         """
         NotImplemented

         
    def change(self, lang, n, verbose=False) :
        changes = []
        wc = []
        #lang = copy.deepcopy(lang)
        # we program n random changes
        for i in tqdm (range(n), "generating " + str(n) + " changes"):
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

    def __init__(self, lang, gen=None) :
        super().__init__(gen)

        self.tree = L_tree(lang)
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
        
        """
        print('Just trying an insertion before the rest')
        change = self.generator.generate_P_change(expanded_tree.language)
        
        
        change = I_change(change.target,
                          [change.effect,
                           self.generator.select_effect(expanded_tree.language, change.target, len(change.target[1]) == 2),
                           
                           self.generator.select_effect(expanded_tree.language, change.target, len(change.target[1]) == 2),],
                          change.conditions)
        
        nl, wc = change.apply_language(expanded_tree.language)
        new_tree = L_tree(nl, expanded_tree)
        expanded_tree = new_tree
        """
        for nch in trange((wanted_depth - expanded_tree.depth), desc="generating " +str(wanted_depth -expanded_tree.depth)+"changes") :
            change = self.generator.generate_P_change(expanded_tree.language)
            nl, wc = change.apply_language(expanded_tree.language)
            new_tree = L_tree(nl, expanded_tree)
            expanded_tree = new_tree


    def octopus(self, nb_branches, depth):
          
        for i in range(nb_branches - 1) :
            print("grafting branch ",i+1)
            self.pursue_evolution(depth)
     
     
    def evoluate(self, lang , nb_branches, depth) :
         self.change( lang, depth)
         self.octopus(nb_branches, depth)
     
     
        
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
  
