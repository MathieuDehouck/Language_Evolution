# -*- coding: utf-8 -*-
"""
Created on Wed May  4 14:25:07 2022

@author: 3b13j

Contains some functions that help handling phonetically transcribed words available on wikipedia

"""


from IPA import IPA, create_classes
from Word import Word
from Phoneme import Phoneme
from Syllable import Syllable
from Language import Language
from pathlib import Path 

ipa = IPA()
alphabet = ipa.alphabet






def wiki_lexicon(path) :
    folder = Path("phonetic/")
    path = folder / path
    """ Extract the data taken from wikipedia (input : path of the file) and returns a dictionnary """
    dico = {}
    with open(path,'r', encoding = 'utf8') as doc :
        for ligne in doc :
            ligne = ligne.split()
            dico[ligne[0]]= ligne[1]
            
            
            
    
    return dico


def segm2syl(dic, alphabet ) :
    """ take as input the dictionnary created out of the wiki data and used the info concerning syllabification
    to create syllables in out IPA format"""
    dic_syl = {}
    for word in dic :
        
        syllables = []
        
        segm = dic[word]
        
        
        """
        copy = ""
        for let in segm :
            if str(let) == "ˈ" and let != segm [0]:
                
                copy+= "."
            copy += let 
        
        """  
        
        segm = segm.split(".")
        
        for syl in segm :
            
            
            
            
            stress = ( syl[0] == "ˈ" )
            
            if stress : 
                syl = syl [1:]
            
            double = False
            if not stress :
                if "ˈ" in syl :
                    
                    bric = syl.split("ˈ")
                    syl = bric[0]
                    double = True
                    syl2 = bric [1]
                    
            
            length =   ("ː" in syl )
            
            
            if length :
                
                
                syl = "".join(i for i in syl if  i != "ː")
                
            # ATTENTION, LABIALISATION A TRAITER PLUS TARD
            
            syl = syl.replace("ʷ", "w")
            
            syl = syl.replace('̯', "")
            
            syl = syl.replace('ʰ', "h")
                
            phonemes = []
            for pho in syl :
                #print(phoneme)
                
                feat = alphabet[pho]
                
                nphon = Phoneme(feat.ipa, list(feat.features))
                phonemes.append(nphon)
            
            syl = Syllable (phonemes, stress, length)
            syllables.append(syl)
            
            if double :
                
                
                length =   ("ː" in syl2 )
                
                
                if length :
                    
                    
                    syl2 = "".join(i for i in syl2 if  i != "ː")
                    
                syl2 = syl2.replace("ʷ", "w")
                
                syl2 = syl2.replace('̯', "")
                
                syl2 = syl2.replace('ʰ', "h")
            
            
                phonemes = []
                for pho in syl2 :
                #print(phoneme)
                
                    feat = alphabet[pho]
                
                    nphon = Phoneme(feat.ipa, list(feat.features))
                    phonemes.append(nphon)
            
                syl2 = Syllable (phonemes, stress, length)
                syllables.append(syl2)
            
            
            
            
    
        dic_syl[word] = syllables
    return dic_syl



def dic2word(dic, alphabet) :
    """ converts a wiki dic into a dic of "word" objects """
    
    dic2syl = segm2syl(dic, alphabet)
    
    dic2word = {}
    for w in dic2syl :
        wor = Word(dic2syl[w])
        dic2word[w] = wor
    return dic2word 
gaffiot = wiki_lexicon('latin_classique.txt')



            

def get_language(path, name) :   
    """
    builds a Language object from data found on wiktionnary

    Parameters
    ----------
    path : str
        path to a file extracted from wiktionnary.

    Returns
    -------
    lg : Language

    """
    # creation of the alphabet
    al = IPA()
    dic_class, classes = create_classes(al.alphabet)
    
    # exctraction of the words from the document
    gaffiot = wiki_lexicon(path)
    dic = dic2word(gaffiot, alphabet) 
    lg = Language(name, dic)
    
    return lg







