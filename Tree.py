# -*- coding: utf-8 -*-
"""
Created on Wed May 18 17:00:17 2022

@author: 3b13j
"""

import os
import random
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
    a special kind of phylogentic tree stocking our languages
    as defined, the structure should be names "forward tree" since the change is unidirectionnal
    
    """
    def __init__(self,  language, root = None ): 
        self.parent = root 
        if self.parent != None : self.parent.nodes.append(self)
        
        self.nodes = [] 
        self.language  = language
        if self.parent == None : self.adress = 'R'
        else : self.adress = self.parent.adress + '.'+ str(self.parent.nodes.index(self)   )
        self.weight = 1
        self.depth = 0
        
        if self.parent != None : self.depth = self.parent.depth +1
        self.change = None
        
        
        
    
        
    def __str__(self):
        if self.parent == None : return "The Root" 
        
        s= self.adress + "   parent " + self.parent.adress + "    nodes  : "
        for n in self.nodes : s+= n.adress + "   "
        return s
        
    def get_depth(self, dic = {}):
        
        dic[self.adress] = self.depth
        for tree in self.nodes :
            tree.get_depth(dic)
        return dic
        
    def get_languages(self, liste = []):
        
        liste.append([self.adress, self.language, self.change])
        for tree in self.nodes :
            tree.get_languages(liste)
        return liste
   
    def get_all_nodes(self,liste=[], scores =[]) :
        
        liste.append(self.adress)
        scores.append(self.weight)
        for tree in self.nodes :
            tree.get_all_nodes(liste, scores)
            
        return liste, scores
    
    
    
    
    
    
    def get_nodes (self, liste=[]) :
        liste.append(self)
        for tree in self.nodes :
            tree.get_nodes(liste)
        return liste
        
    
    
    
    
    
    def get_ad_2_tree(self, dic = {} ):
        dic[self.adress] = self
        for tree in self.nodes :
            tree.get_ad_2_tree(dic)
        return dic
    
    def get_tree_2_add(self, dic = {} ):
        dic[self] = self.adress
        for tree in self.nodes :
            tree.get_tree_2_add(dic)
        return dic
    
    def pick_a_node(self)  :
       
        liste, scores = self.get_all_nodes()
        
        return random.choices(liste, weights=scores, k=1)[0]
    
    
    
    
    def get_leaves(self, liste =[]) :
        
        if len(self.nodes) == 0 :
            liste.append(self)
        else :
            for node in self.nodes :
                node.get_leaves(liste)
        return liste
    
    def get_path_to_root(self) :
        
        liste = []
        parent = self.parent 
        while self.parent != None :
            liste.append(parent)
            parent = parent.parent
        return liste
    
    
    
    
    def get_history_word(self, word , liste = [] ):
        liste.append([self.adress, self.language.voc[word]])
        for st in self.nodes :
            self.get_history_word(word, liste)
        return liste
        
    
    
    
    def print_history_to_graph(self, word ) :

        
      
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
        
        print("execution commande")
        commande = "dot -Tpng  graphe.dot  >  graphe.png"
        
        os.system(commande) #os.system(cmd) exécute cmd
        
        from PIL import Image
        im = Image.open("graphe.png")
        im.show()   
        
        
    
    def elaborate_history_graph (self, word) :
        
        nodes = self.get_nodes()
        
        splits = [n for n in nodes if len(n.nodes)>1] + [self]
        
        leaves = self.get_leaves()
        
        keep = []
        edges = []
        
        
        
        
        for a in splits + leaves :
            
            last = a
            if a not in keep  : keep.append(a)
            b = a.parent
            while b not in splits and b != None and last != None :
                 
                 if b.language.voc[word] != last.language.voc[word] :
                    
                    if b not in keep : 
                        keep.append(b)
                        if [last, b] not in edges :  edges.append([last, b])
                    
                    last = b
                 b = b.parent
                 
            if b != None and last != None : edges.append([last, b])
            
            
        return list(tuple(keep)), list(tuple( edges))
        
      
        
    
    def history_to_graph(self, word) :
        
        
        keep, edges =  self.elaborate_history_graph(word) 
        
 
        
        if None in keep  : keep.remove(None)
    
        f = open ( 'graphe.dot','w', encoding = "utf8") 
        f.write("digraph \" " + "We display the history of a word" + "\" {\n")
        
        f.write(" label = \"" + word+ "\" \n")
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
            
        numeric_edges = []
        
        for edge in edges :
            
                num = [str(keep.index(edge[0])), str(keep.index(edge[1]))]
                
                
                if num not in numeric_edges :
                    
                    s = ""
                    s += num[0]
                    s += " -> "
                    s += num[1]
                    s+=";\n"
                    f.write(s)
                    
                    numeric_edges.append(num)
                    
        print(numeric_edges)         
        f.write("}")
        f.close()
        
        print("execution commande")
        commande = "dot -Tpng  graphe.dot  >  graphe.png"
        
        os.system(commande) #os.system(cmd) exécute cmd
        
        from PIL import Image
        im = Image.open("graphe.png")
        im.show()   
        
        
    """
    def print_history_to_graph_reduced(self, word ) :

        
      
        f = open ( 'graphe.dot','w', encoding = "utf8") 
        f.write("digraph \" " + "We display the history of a word" + "\" {\n")
        
        f.write(" label = \"" + word+ "\" \n")
        f.write("graph[rankdir=\"LR\"];\n")
        
        
        f.write("node [style=\"filled\", fillcolor = \"white\"];\n")
        f.write("edge [style=\"solid\", color=\"purple\"];\n")
        
        liste = self.get_nodes()
        
       
        s = ""
        s += str(self.adress)
        s += " [label=\""
        s += self.language.voc[word].ipa
        s += "\", fillcolor= white, color=\"purple\",  fontcolor=\"red\"];\n"
        
        
        
        words = []
        
        words.append(self.language.voc[word])
        
    
        for tree in liste :
            for subtree in tree.nodes :
                if tree.language.voc[word] != subtree.language.voc[word] :
                    words.append(subtree.language.voc[word])
                   
                    s = ""
                    s += str(words.index(subtree.language.voc[word]))
                    s += " [label=\""
                    s += subtree.language.voc[word].ipa
                    s += "\", fillcolor= white, color=\"purple\",  fontcolor=\"red\"];\n"

                    f.write(s)
                    
        # TODO idée générale à revoir 
        for tree in liste :
            for subtree in tree.nodes :
                if tree.language.voc[word].phonemes != subtree.language.voc[word].phonemes :
                    s = ""
                    
                    
                    s += str(words.index(tree.language.voc[word]))
                    s += " -> "
                    s += str(words.index(subtree.language.voc[word]))
                   
                    
                    s+=";\n"
                    f.write(s)
        f.write("}")
        f.close()
        
        print("execution commande")
        commande = "dot -Tpng  graphe.dot  >  graphe.png"
        
        os.system(commande) #os.system(cmd) exécute cmd
        
        from PIL import Image
        im = Image.open("graphe.png")
        im.show()   
        
        
        
        """
    
    
   
        
        
        
        
    
    