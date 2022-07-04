# -*- coding: utf-8 -*-
"""
Created on Tue May 17 13:04:22 2022

@author: 3b13j

Class representing a changer that applies the linguistic change. It automatically generates changes using the change generator it has been given, and apply them to a given language.
"""

from Change  import Change, P_change, I_change, M_change, S_change
from Tree import  L_tree
from tqdm import tqdm, trange
from Generator import Change_Generator

import random
import Sampling
import copy




class Changer () :
    
    """
    Class representing a changer that applies the linguistic change. It automatically generates changes using the change generator it has been given, and apply them to a given language.
    
    The Changer just deterministically applies a set of changes it recieves. Therefore, several different subclasses of changer can be created, depending on the way changes are generated :
    
    Two particulats Changers have been implemented :
        * a first one that uses a random Change_generator  to predict the next change it is going to apply
        
        * a Log changer that reads the changes from logs (now, changes that have been recorded from a previous random generation, but we wish to elaborate a system that would allow the user to write 
         changes in an easy manner
    
    ...

    Attributes
    ----------
    
    #TODO : the generator only concerns the Tree Generator, and could be excluded from the field of the abstract class
    gen : a Change_generator
    
    Methods
    -------
    __init__() constructor taking all these information as input
    
    change_u  : applies a unitary change
    
    change : applies n changes
    """

    



    def  __init__(self, gen = Change_Generator()) :
        #TODO modified for the new micro script
        self.generator = gen
     
        
     
        
     
    def change_u (self, lang) :
         """
         applies a unitary change
         """
         NotImplemented




         
    def change(self, lang, n, verbose=False) :
        """
        Apply n changes
        """
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
    """
    A Class applying randomly generated changes and storing each and every change and language state in a tree structure
    
    We generate the change in a very precise way :  we generate a first row of changes leading from the origin to the wanted depth.
    Then the correct number of branches is grafted.
    """
    

    def __init__(self, lang, gen=None) :
        super().__init__(gen)
        self.tree = L_tree(lang)
        self.current_tree = self.tree





    def change_u (self, lang, verbose = False) :
        
        type_of_change = random.choices(Sampling.change_types, Sampling.weights_change_type )[0]
        
        
        if type_of_change == "M" : 
            change = self.generator.generate_M_change(lang)
            if verbose : print("M_generated")
        elif type_of_change == "S" : 
            change = self.generator.generate_S_change(lang)
            if verbose : print("S_generated")
        elif  type_of_change == "P" : 
            change = self.generator.generate_P_change(lang)
            if verbose : print("P_generated")

        
        nl, wc = change.apply_language(lang)
        # TODO modify the way the branch is grafted
        self.current_tree.change = change
        self.current_tree.changed_words = wc
        new_tree = L_tree(nl, self.current_tree)
        self.current_tree = new_tree
         
        
        return nl, change, wc
     
     
     
     
     
    def change(self, lang, n, verbose=False) :
        """
        Apply n changes
        """
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
            lf = copy.copy(self.current_tree)
            
        return lang, changes, wc, lf
     
     
     
    def pursue_evolution(self, wanted_depth , node = None, verbose = False) :
        """
        

        Parameters
        ----------
        wanted_depth : int
            final number of changes we want in every branch
        node : TYPE, optional
            if we want to select by force a given node to expand
        -------
       
        """
        
        dic = self.tree.get_ad_2_tree()
        if node == None : node = self.tree.pick_a_node()
        
        expanded_tree = dic[node]
        
        for nch in trange((wanted_depth - expanded_tree.depth), desc="generating " +str(wanted_depth -expanded_tree.depth)+"changes") :
            
            type_of_change = random.choices(Sampling.change_types, Sampling.weights_change_type )[0]
            
            
            if type_of_change == "M" : 
                change = self.generator.generate_M_change(expanded_tree.language)
                if verbose : print("M_generated")
            elif type_of_change == "S" : 
                change = self.generator.generate_S_change(expanded_tree.language)
                if verbose : print("S_generated")
            elif type_of_change == "P" :
                change = self.generator.generate_P_change(expanded_tree.language)
                if verbose : print("P_generated")
    
            nl, wc = change.apply_language(expanded_tree.language)
            expanded_tree.change = change
            expanded_tree.changed_words = wc
            new_tree = L_tree(nl, expanded_tree)
            expanded_tree = new_tree

        # The method moodify the state of the tree itself, so it do not return any value.





    def octopus(self, nb_branches, depth):
        """
        graft nb_branches -1 branches to the first evolution path

        Parameters
        ----------
        nb_branches : TYPE
            DESCRIPTION.
        depth : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
          
        for i in range(nb_branches - 1) :
            print("grafting branch ",i+1)
            self.pursue_evolution(depth)
     
        
     
        
     
    def make_evolution(self, lang , nb_branches, depth) :
         """ 
         from a untouched language, derives the given number of branches, and pushes forward until the trees all have the same depth
         
         """
         lang, changes, wc, main_leaf = self.change( lang, depth)
         self.octopus(nb_branches, depth)
         return main_leaf
         
         
         
         
    def show_of_the_evolution(self, nb_wd) :
        """
        Gives a nice overview of the changes generated by the programm by picking random words and displaying their evolution on a beautiful and coloured graph. 
        
        Parameters
        ----------
        nb_wd : Number of word we want to display in our graph

        """
        origin = self.tree.language
        
        wds = []
        for i in range(nb_wd) :
            w = random.choice ( list(origin.voc.keys()))
            wds.append(w)
        self.tree.history_to_graph(wds)
     
        
     
     
        
class Log_changer(Changer) :
    # TODO precise logs and test them with other kind of changes
     """
     A class of changer that reads changes from a log file, in the format we created at different steps of the programm,
     and applying them back.
     
     """
     
     def __init__(self, lang, path) :
          
          super().__init__()     
          f= open(path, "r", encoding = 'utf8')
          lines = []
          for line in f : lines.append(line)
          self.file = lines
          
          
          
          
     
     def change_u (self, lang, index ) :
          change = Change.decode_change(self.file[index])
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