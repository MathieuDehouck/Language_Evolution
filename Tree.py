# -*- coding: utf-8 -*-
"""
Created on Wed May 18 17:00:17 2022

@author: 3b13j
"""

class L_node :
    """ 
    a class representing a node containing a language
    """
    
    def __init__(self,father, language) :
        self.father = father
        self.language = language
        self.children = []
        
    def add_child(self, child):
        self.children.append(child)
        
class Root (L_node) :
     def __init__(self, language) :
         super().__init__(self, language)
         
    


class L_tree :
    """ 
    a special kind of phylogentic tree stocking our languages
    as defined, the structure should be names "forward tree" since the change is unidirectionnal
    
    """
    def __init__(self, root): 
        self.root = root 
        self.nodes = [root] 
        self.languages  = [root.language]
        self.last = root
          
        
        
    def graft (self, f , s) :
        f.add_child(s)
        self.nodes.append(s)
        self.languages.append(s.language)
        self.last = s
        
    