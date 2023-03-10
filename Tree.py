# -*- coding: utf-8 -*-
"""
Created on Wed May 18 17:00:17 2022

@author: 3b13j
"""

import os
import random
from sys import platform
from PIL import Image
from Change import M_change, S_change, P_change

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
        self.changed_words = []
        
        
    def __str__(self):
        if self.parent == None:
            return "The Root" 
        
        s = self.adress + "   parent " + self.parent.adress + "    nodes  : "
        for n in self.nodes:
            s += n.adress + "   "
            s += "\n"
            #s += str(self.change)
            #s += str(self.changed_words)
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
        #TODO ; param??triser le fait que les embranchements ne se fassent pas forc??ment ?? trop peu de distance
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
        liste = [self]
        parent = self.parent 
        while parent.parent != None :
            liste.append(parent)
            parent = parent.parent
        #we add the root
        liste.append(parent)
        return liste
    
    
    
    
    
    def get_a_change_path(self, lf = None) :
        """
        gives the list of all the changes and languages from a randomly selected leaf
        """
        lvs =  self.get_leaves()
        if lf == None  : lf = random.choice(lvs)
        ptr = lf.get_path_to_root()
        lgs = []
        chs = []
        wcs = []
        ptr.reverse()
        for tr in ptr[:-1] :
            lgs.append(tr.language)
            chs.append(tr.change)
            wcs.append(tr.changed_words)
        return lgs, chs, wcs
    
    
    
    
    
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
        os.system(commande) #os.system(cmd) ex??cute cmd
        
        if platform != 'linux':
            im = Image.open("graphe.png")
            im.show()   
        
        
    
    
    
    def elaborate_history_graph(self, words):
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


        for a in splits + leaves:
            
            last = a
            keep.add(a)

            b = a.parent
            while b not in splits and b != None and last != None:
                changes = [b.language.voc[w] != last.language.voc[w] for w in words]
                if True in changes:
                    keep.add(b)
                    edges.append([last, b])
                    last = b
                b = b.parent
                 
            if b != None and last != None :
                edges.append([last, b])

       
            
        return list(keep), list(edges)
        
      
        
      
    
    def history_to_graph(self, words) :
        """
        print a graph only displaying the informations on the evolution of a single word
        """
        keep, edges = self.elaborate_history_graph(words)
        
        if None in keep:
            keep.remove(None)
    
        f = open ('graphe.dot','w', encoding = "utf8") 
        f.write("digraph \" " + "We display the history of a word" + "\" {\n")    
        f.write("label = \"" + '\n'.join(words) + "\" \n")

        f.write("graph[rankdir=\"LR\"];\n")   
        f.write("node [style=\"filled\", fillcolor = \"white\"];\n")
        f.write("edge [style=\"solid\", color=\"purple\"];\n")
        
        

        for tree in keep :
            s = ""
            s += str(keep.index(tree))
            s += " [label=\""
            s += '\n'.join([tree.language.voc[w].ipa for w in words])
            s += "\", fillcolor= white, color=\"purple\", "
            if tree.depth == self.depth :  s += "  shape = doubleoctagon, "
            if tree.nodes == [] :  s += "  shape = doublecircle, "
            s+= " fontcolor=\"red\"];\n"
            f.write(s)

            
        for edge in edges :
            x, y = [str(keep.index(edge[0])), str(keep.index(edge[1]))]
            change = True in [edge[0].language.voc[w] != edge[1].language.voc[w] for w in words]



            s = y + " -> " + x
            if change: 
                
                if type(edge[0].change) == M_change :
                    s += '[style=\"solid\", color=\"red\"]'
                    
                elif type(edge[0].change) == P_change :
                    s += '[style=\"solid\", color=\"green\"]'
                
                elif type(edge[0].change) == S_change :
                    s += '[style=\"solid\", color=\"blue\"]'
                   
            s += ";\n"
            f.write(s)

        f.write("}")
        f.close()
        
        print("execution commande")
        commande = "dot -Tpng  graphe.dot  >  graphe.png"
        
        os.system(commande) #os.system(cmd) ex??cute cmd

        if platform != 'linux':
            im = Image.open("graphe.png")
            im.show()   
        
        
