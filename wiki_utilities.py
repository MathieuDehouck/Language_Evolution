# -*- coding: utf-8 -*-
"""
Created on Wed May  4 14:25:07 2022

@author: 3b13j

Contains some functions that help handling phonetically transcribed words available on wikipedia

"""
from IPA import IPA
from Word import Word
from Phoneme import Phoneme, Vowel, Consonant
from Syllable import Syllable
from Language import Language
from pathlib import Path
from IPA_utils import diacritics

ipa = IPA.get_IPA()





def wiki_lexicon(path) :
    """
    extracts the information from the iki files

    Parameters
    ----------
    path : str
        path to the file we read

    Returns
    -------
    dico : 
        keys : simple orthograph of the word. 
        values : the IPA and syllabled representation of the word give by the wiktionnary websiote. 

    """
    
    folder = Path("phonetic/")
    path = folder / path
    # Extract the data taken from wikipedia (input : path of the file) and returns a dictionnary """
    dico = {}
    with open(path,'r', encoding = 'utf8') as doc :
        for line in doc:
            line = line.strip()
            line = line.split('\t')
            if line == []:
                continue
            dico[line[0]] = line[1].replace(' ', '.').replace('(','').replace(')','')

    return dico





def treat_syl(syl, stress = False) :
    """
    Converts a syllable in the syllabled jey of the vocabulary into a syllable object. 
    Effectuates the actual encoding of data into the objects used in this program. 

    Parameters
    ----------
    syl : str
    stress : TYPE, optional
        DESCRIPTION. The default is False.

    Returns
    -------
    syl : a Syllable object

    """

    length = 'ː' in syl
    syl = syl.replace('ː', '')
    syl = syl.replace('g', 'ɡ')
    syl = syl.replace('̯', '')
    phones = []
    feats = []
    
    for i, ch in enumerate(syl):
        
        if ch in diacritics:
            feats[-1].append(diacritics[ch])
            continue

        phones.append(ipa.alphabet[ch])
        feats.append([])
    
    phonemes = []
    for i, pho in enumerate(phones):
        phonemes.append(pho.get_one(feats[i], False))

    syl = Syllable(phonemes, stress, length)
    return syl





def segm2syl(dic) :
    """ take as input the dictionnary created out of the wiki data and used the info concerning syllabification
    to create syllables in out IPA format"""
    dic_syl = {}
    for word, segm in dic.items() :
        #print(word, segm)
        syllables = []
        segm = segm.split(".")

        for syl in segm :
            stress = ( syl[0] == "ˈ" )    
            if stress : 
                syl = syl [1:]  
                s = treat_syl(syl, stress)
                syllables.append(s)
                
            double = False
            
            if not stress :
                if "ˈ" in syl :
                    bric = syl.split("ˈ")
                    syl = bric[0]
                    s = treat_syl(syl, stress)
                    syllables.append(s)
                    double = True
                    syl2 = bric [1]
                    s2 = treat_syl(syl2, stress)
                    syllables.append(s2)
                else : 
                    s = treat_syl(syl, stress)
                    syllables.append(s)              
        dic_syl[word] = syllables
           
    return dic_syl





def dic2word(dic) :
    """ converts a wiki dic into a dic of "word" objects
    
    """
    
    dic2syl = segm2syl(dic)
    dic2word = {}
    for w in dic2syl :
        wor = Word(dic2syl[w])
        dic2word[w] = wor
    return dic2word 


            


def get_language(path, name) :   
    """
    builds a Language object from data found on wiktionnary
    Final step of the conversion that reunites all the previous functions.

    Parameters
    ----------
    path : str
        path to a file extracted from wiktionnary.

    Returns
    -------
    lg : Language

    """
    al = IPA()
    gaffiot = wiki_lexicon(path)
    dic = dic2word(gaffiot) 
    lg = Language(name, dic)
    
    return lg