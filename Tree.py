# -*- coding: utf-8 -*-
"""
Created on Wed May 18 17:00:17 2022

@author: 3b13j
"""

import os
import random
from sys import platform
from PIL import Image

"""
class L_node :
   
    
    def __init__(self,father, language) :
        self.father = father
        self.language = language
        self.children = []
        
    def add_child(self, child):
        self.children.append(child)
        
class Root (L_node) :
     def __init__(self, language) :
         super().__init__(self, language)
         
""" 


class L_tree :
    """ 
    a special kind of phylogentic tree storing our languages
    as defined, the structure should be names "forward tree" since the change is unidirectionnal
    
    """
    def __init__(self, language, parent=None): 
        self.parent = parent
        if self.parent != None:
            self.parent.nodes.append(self)
        
        self.nodes = [] 
        self.language = language
        
        if self.parent == None:
            self.adress = 'R'
        else:
            self.adress = self.parent.adress + '.'+ str(self.parent.nodes.index(self))

        self.weight = 1
        self.depth = 0
        
        if self.parent != None :
            self.depth = self.parent.depth +1
        self.change = None
        
        
    def __str__(self):
        if self.parent == None:
            return "The Root" 
        
        s = self.adress + "   parent " + self.parent.adress + "    nodes  : "
        for n in self.nodes:
            s += n.adress + "   "
        return s
        
    
    def get_depth(self, dic = {}):
        """
        return a dictionarry mapping the address of a tree to its depth
        """
        
        dic[self.adress] = self.depth
        for tree in self.nodes :
            tree.get_depth(dic)
        return dic
    
    
    def get_languages(self, liste = {}):
        """
        Returns a dictionnary mapping the adress of a tree to the language it stores

        """
        
        liste[self.adress] = [ self.language, self.change]
        for tree in self.nodes :
            tree.get_languages(liste)
        return liste
   

    def get_all_nodes(self,liste=[], scores =[]) :
        
        liste.append(self.adress)
        scores.append(self.weight)
        for tree in self.nodes :
            tree.get_all_nodes(liste, scores)
            
        return liste, scores

    
    
    def get_nodes (self, liste=None):
        """
        returns a list containing all the tree object that are nodes in the mother tree

        """
        if liste == None:
            liste = []
        liste.append(self)
        for tree in self.nodes:
            tree.get_nodes(liste)
        return liste
        
    
    def get_ad_2_tree(self, dic = {} ):
        """ 
        returns a dictionnary mapping an adress to the tree object
        """
        dic[self.adress] = self
        for tree in self.nodes :
            tree.get_ad_2_tree(dic)
        return dic
    
    
    def get_tree_2_add(self, dic = {} ):
        dic[self] = self.adress
        for tree in self.nodes :
            tree.get_tree_2_add(dic)
        return dic
        
    def get_scores(self,liste=[], scores =[]) :
        """ 
        Get a mapping between change objects and the chance they have to appear
        """
        #TODO ; paramétriser le fait que les embranchements ne se fassent pas forcément à trop peu de distance
        liste.append(self.adress)
        scores.append(self.weight)
        for tree in self.nodes :
            tree.get_scores(liste, scores)
            
        return liste, scores
    
    
    def pick_a_node(self):
        """
        Pick a random node from a tree

        """
        liste, scores = self.get_scores()
        
        return random.choices(liste, weights=scores, k=1)[0]
    

    def get_leaves(self, liste=None) :
        """ 
        Get the list of the leaves of a language
        """
        if liste == None:
            liste = []
        if len(self.nodes) == 0 :
            liste.append(self)
        else :
            for node in self.nodes :
                node.get_leaves(liste)
        return liste
    
    
    def get_final_state_of_the_evolution(self): 
        """
        Returns the languages at the end of our evolution tree
        """
        
        leaves = self.get_leaves()
        return [leaf.language for leaf in leaves]


    def get_path_to_root(self) :
        """ 
        Returns the list of all the nodes leading from the target node to the root of the tree
        """
        liste = []
        parent = self.parent 
        while self.parent != None :
            liste.append(parent)
            parent = parent.parent
        return liste
    
    
    
    
    def get_history_word(self, word , liste = [] ):
        """
        Stores the state of the word in the histtory of all the generated languages

        """
        liste.append([self.adress, self.language.voc[word]])
        for st in self.nodes :
            self.get_history_word(word, liste)
        return liste
        
    
    
    
    def print_history_to_graph(self, word ) :
        """
        Display a graph in which the nodes represent a word at a certain langugage state, and the edges the link between two languages

        """ 
        
        f = open ( 'graphe.dot','w', encoding = "utf8") 
        f.write("digraph \" " + "We display the history of a word" + "\" {\n")       
        f.write(" label = \"" + word+ "\" \n")
        f.write("graph[rankdir=\"LR\"];\n")     
        f.write("node [style=\"filled\", fillcolor = \"white\"];\n")
        f.write("edge [style=\"solid\", color=\"purple\"];\n")
        
        liste = self.get_nodes()
        
        dic = {}
        for i,  el in enumerate(liste) : dic[el] = i
        print(liste)
        t2a = self.get_tree_2_add()
        print(t2a)
        
        for tree in liste :
            
            s = ""
            s += str(dic[tree])
            s += " [label=\""
            s += tree.language.voc[word].ipa
            s += "\", fillcolor= white, color=\"purple\",  fontcolor=\"red\"];\n"
            f.write(s)
            
        for tree in liste :
            for subtree in tree.nodes :
                
                s = ""
                s += str(dic[tree])
                s += " -> "
                s += str(dic[subtree])        
                s+=";\n"
                f.write(s)
                
        f.write("}")
        f.close()
        
        print("order executed")
        commande = "dot -Tpng  graphe.dot  >  graphe.png"
        os.system(commande) #os.system(cmd) exécute cmd
        
        if platform != 'linux':
            im = Image.open("graphe.png")
            im.show()   
        
        
    
    
    
    def elaborate_history_graph(self, word) :
        """
        Extracts a subgraph representing the history of the evolution of a particular word in all the languages we generated 
        """
        
        nodes = self.get_nodes()

        splits = [n for n in nodes if len(n.nodes) > 1]
        if self not in splits:
            splits.append(self)

        leaves = self.get_leaves()
        keep = set()
        edges = []

        print(keep)
        print(edges)

        for a in splits + leaves:
            print(a)
            last = a
            keep.add(a)

            b = a.parent
            while b not in splits and b != None and last != None :     
                if b.language.voc[word] != last.language.voc[word] :
                    keep.add(b)
                    edges.append([last, b])
                    last = b
                b = b.parent
                 
            if b != None and last != None :
                edges.append([last, b])

        print(len(edges))
            
        return list(keep), list(edges)
        
      
        
      
    
    def history_to_graph(self, word) :
        """
        print a graph only displaying the informations on the evolution of a single word
        """
        keep, edges = self.elaborate_history_graph(word) 
        

        if None in keep  : keep.remove(None)
    
        f = open ('graphe.dot','w', encoding = "utf8") 
        f.write("digraph \" " + "We display the history of a word" + "\" {\n")    
        f.write("label = \"" + word+ "\" \n")

        f.write("graph[rankdir=\"LR\"];\n")   
        f.write("node [style=\"filled\", fillcolor = \"white\"];\n")
        f.write("edge [style=\"solid\", color=\"purple\"];\n")
        

        for tree in keep :
            s = ""
            s += str(keep.index(tree))
            s += " [label=\""
            s += tree.language.voc[word].ipa
            s += "\", fillcolor= white, color=\"purple\",  fontcolor=\"red\"];\n"
            f.write(s)

            
        for edge in edges :
            num = [str(keep.index(edge[0])), str(keep.index(edge[1]))]
            change = edge[0].language.voc[word] != edge[1].language.voc[word]

            s = num[1] + " -> " + num[0]
            if change:
                s += '[style=\"solid\", color=\"green\"]'
            s += ";\n"
            f.write(s)

        f.write("}")
        f.close()
        
        print("execution commande")
        commande = "dot -Tpng  graphe.dot  >  graphe.png"
        
        os.system(commande) #os.system(cmd) exécute cmd

        if platform != 'linux':
            im = Image.open("graphe.png")
            im.show()   
        
        
