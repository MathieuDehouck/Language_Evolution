# -*- coding: utf-8 -*-
"""
Created on Tue May  3 12:20:06 2022

@author: 3b13j
"""
from __future__ import unicode_literals
import numpy as np
import os
import locale
from pathlib import Path


def create_classes(alphabet) :
    """
    creates the natural classes from an ipa alphabet
    definded outside the class to be used once and for all 

    Parameters
    ----------
    alphabet : an ipa alphabet

    Returns
    -------
    dic_class : dic
        dictionnary mapping the name of a natural class to the class object 
    classes : list
        list of the natural classes we want to work with

    """
    
    
    # we open the source csv.file
    folder = Path("phonetic/")
    path = folder /  "natural_class.csv"
    dic_class = {}
    dic_class_liste = {}
    classes = []
    data = np.genfromtxt(path, delimiter = ',', dtype = str, encoding = "utf8")
    f = open(folder /"liste_classes.txt", 'w',  encoding = 'utf8')
    f.write ("LIST OF NATURAL CLASSES  \n")

    # we extract the list of classes
    features = data[0][1:]
    
    f.write('\n')
    f.write (" \n")
    
    
    for classe in data[1:][1:] :
        
        name = classe[0]
        isV = classe[1]
        
        fts  = "" 
        if not isV :
            
            voiced = classe[2]
            place = classe[3]
            manner = (classe[4] , classe[5], classe[6], classe[7], classe[8])
            
            tpl1 = (place, manner, voiced)
            tpl2 = (classe[9], classe[10], classe[11])
            fts = (tpl1, tpl2)
        
        
        else :
            voiced = classe[2]
            front = classe[3]
            heigth = classe [4]
        
            tpl1 = (front, heigth, voiced)
            tpl2 = (classe[5], classe[6])
            fts = (tpl1, tpl2)
            
        
        
        classe = [truc for truc in classe[1:] if truc != ""]
        
        classe = Natural_class(name, fts, isV, classe[1:])
        classes.append(classe)
        dic_class[name] = classe
         
        
        
        # we check which phonemes of the alphabet belon to the class
    for classe in classes :
        for phon in alphabet.phonemes :
            
            fts  = phon.lin
            add = False
            if len(fts) ==  len(classe.lin): 
                
                add = True
                for i , ft in enumerate (fts) :
            
                  if int(ft) != -1 and int(classe.lin[i]) != int( ft) :
                       add = False 
            print()
            print(fts)
            print("vs")
            print(classe.lin)
            
            if add :
                
               classe.add_phon(phon)
    
        
    #TODO cafouillage dand l ordre des features
    return dic_class, classes


def list2class(name, clas) :
    """
    Creates a Natural_class with the name given as input and add all the phonemes givent in the second input (list)
    """

    res = Natural_class(name)
    for phon in clas :
        res.add_phon(phon)
    return res



class Natural_class :
    """
    An object representing a natural class
    
    ...

    Attributes
    ----------
    name : str 
        The name of a class
    members : list
        list of the phonemes belonging to a class 
    template : list
        list of the feature template representing the class. initiated with full wildcards
        
    
    
    Methods
    -------
    __init__() constructor taking all these information as input
    
    add_phon
    set_template
    
    """
    

    
    def __init__(self, name, feat, vow , lin) :
        self.name = name 
        self.members = []
        self.template = feat
        self.isV = vow
        self.lin = lin
        
        
    def add_phon(self, ph) :
        self.members.append(ph)
        
    def set_lin(self, lin) :
        self.lin = lin
        
    def set_template(self, template) :
        self.template = template
        
        
        
    def __str__(self) :
        s = self.name + "\n" + str(self.template) + "\n" + str(self.lin )+ "\n" + str(self.members)
        return s

    
