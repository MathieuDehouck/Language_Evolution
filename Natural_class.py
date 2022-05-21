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
    path = folder /  "class.csv"
    dic_class = {}
    dic_class_liste = {}
    classes = []
    data = np.genfromtxt(path, delimiter = ',', dtype = str, encoding = "utf8")
    f = open(folder /"liste_classes.txt", 'w',  encoding = 'utf8')
    f.write ("LIST OF NATURAL CLASSES  \n")
    
    
    
    # we extract the list of classes
    features = data[0][1:]
    f.write(str(features))
    f.write('\n')
    f.write (" \n")
    
    
    
    for sound in data[1:]  :
        n_class  = Natural_class(sound[0])
        fts =  [int(x) for x in sound[1:]]
        phonemes = []
        
        # we check which phonemes of the alphabet belon to the class
        for phon in alphabet :
            features_phon = alphabet[phon]
            features_phon = features_phon.features
            add = True 
            
            
            for i in range(len(fts)) :
                if int(fts[i]) != -1 and int(features_phon[i]) != int( fts[i]) :
                    add = False 
            if add :
                phonemes.append(phon)
                n_class.add_phon(phon)
        
        
        #we write the classes and its members in a text file
        n_class.set_template(fts)
        f.write (sound[0])
        f.write ( '  :   ')
        f.write(str(fts))
        f.write (" \n")
        f.write(" contains following phonems : " )
        f.write(str(phonemes))
        f.write (" \n")
        f.write (" \n")
        dic_class [sound[0] ] = phonemes
        dic_class [sound[0] ] = n_class
        classes.append(n_class)
        
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
    

    
    def __init__(self, name) :
        self.name = name 
        self.members = []
        self.template = [-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1	,-1]
        
        
        
    def add_phon(self, ph) :
        self.members.append(ph)
        
        
        
    def set_template(self, template) :
        self.template = template
        
        
        
    def __str__(self) :
        s = self.name + "\n" + str(self.members)
        return s

    
