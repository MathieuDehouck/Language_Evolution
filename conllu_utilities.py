# -*- coding: utf-8 -*-
"""
Created on Mon May  2 16:34:02 2022

@author: 3b13j

contains usefull functions to extract data from conllu files
"""
import os 
import re



def extract_conllu(path) :
    """
    Extracts data from a conllu file

    Parameters
    ----------
    path : str
        a path to the origin file

    Returns
    -------
    res : a list 
        the result of a successful extraction

    """
    
    absolute_path = os.path.abspath(__file__)
    pre_processed_data = []
    with open(path,'r') as conllu :
        for ligne in conllu :
            donnee  =  [str(d) for d in ligne.split()]
            pre_processed_data .append(donnee)
    
    dic = []
    sentence = []
    res = []
    for ligne in pre_processed_data :
        if len(ligne) > 2 :
            if ligne[0] == '1':
                dic.append(sentence)
                sentence = []
            if ligne[0] != '#' and  "-" not in ligne[0]  :
                sentence.append(ligne)
            
    # to delete problematic characters
    
    for sentence in dic :
        if len(sentence) == 1  :
            dic.remove(sentence)
   
    for sentence in dic :
        for ligne in sentence :
            lemma = ligne[2].lower()
            if lemma not in res :
                if lemma[0].isalpha ()    :
                    res.append(lemma)
    res.sort()
    return res



def GetKey(val, dic):
    """
    to get the key giving as input the value and a dictionnary
    """
    
    for key, value in dic.items():
        if val == value:
            return key
    return "key doesn't exist"



def word_2_phoneme_lat(string, alph) :
    """
    A useless thing that treats latin
    """
    features = []
    index = 0
    while index != len(string)  :
        
        if string[index] == "q" :
            string = re.sub(string[index+1], "",string)
            string = string.replace('q','k')
                   
        if string[index] == "c" :
            string = string.replace('c','k')
            
    
        if string[index] in alph :
            features.append(alph[string[index]])
        index +=1
    return features
   

    
def dic_w2f(liste, alph) :
    w2f = {}
    for word in liste :
        feats = word_2_phoneme_lat(word, alph)
        w2f[word] = feats
    return w2f
        




