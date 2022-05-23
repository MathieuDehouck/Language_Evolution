# -*- coding: utf-8 -*-
"""
Created on Thu May  5 09:28:54 2022

@author: 3b13j

Contains the languge class
"""

from utilitaries import printl, feature_match


class Language() :
    """
    
    A class to represent a language, considered as the list of the phonems it possesses.

    ...

    Attributes
    ----------
    name : str
        name of the language
    voc : dic 
        dicitonnary storing all the words of the language
    phonemes : list
        list of all the phonemes belonging to the language
    dic_phonemes : dic
        a dic mapping a character to a phoneme

    Methods
    -------
    __init__() the constructor
    
    
    """
    
    def __init__(self, name,  dic) :
        """
        take as input the name of the language and a dictionnary of words. it is going to create a Language 
        object automatically from this object

        Parameters
        ----------
        name : str
            name of the language.
        dic : dic
            voc of the language

        Returns
        -------
        Self

        """
                
        self.voc = dic 
        self.name = name
        # To simplify we are going to state that phonemes are a list of features
        phonemes = []
        features = []
        dic_phonemes = {}
        
        for word in dic.values() :
            for syl in word.syllables :
                for feat in syl.phonemes :
                    if feat.features not in features :
                        features.append(feat.features)
                        phonemes.append(feat)
                        
        self.phonemes   = list(tuple(phonemes)) # we eliminate doubles
        self.features = features
        for phoneme in phonemes :
            dic_phonemes[phoneme.ipa] = phoneme        
        self.dic_phonemes = dic_phonemes
        self.subclasses = self.get_subclasses()


    def __str__(self) :
        return self.name + str(self.phonemes)
    
    
    
    def get_subclasses(self) :
        
        subclasses = {} 
        for phoneme in self.phonemes :
            subclass = []
            for i, ft in enumerate(phoneme.features) :
                classe = [] 
                for phoneme2 in self.phonemes :
                    if phoneme2.features[i] == ft :
                        classe.append(phoneme2)
                subclass.append(classe)
            subclasses[phoneme] = subclass
        return subclasses
    
    
    
    
    def compare(self, language, verbose = False) :
        """
        

        Parameters
        ----------
        language : another Language object
            DESCRIPTION.

        Returns
        -------
        differents : list 
            the list of word that have been modified in the new language

        """
        
        #TODO check that it actually works
        if verbose :
            print("original language")
            print(self.name)
            print("there are ", len(self.voc), " words ")
            print("target language")
            print("there are ", len(language.voc), " words ")
        differents = []
        
        for word in self.voc.keys() :
            w1 = self.voc[word]
            w2 = language.voc[word]
            bol = w1.equals(w2)
            if  not bol :
                differents.append([self.voc[word],language.voc[word] ])
        
        if verbose :
            print (len(differents), " different words")
            print (len(self.voc) - len(differents), " unchanged words")
        if  verbose and len(differents) != 0 :
                print("change happened")
                printl(differents)
            
        return differents
    
    
    
    
    def belong_language(self,ft)    :
        liste = []
        
        for pho in self.phonemes :
              
              f = pho.features 
              if feature_match (ft, f) : 
                  i = str(pho)
                  liste.append(i)
                  
        return (liste)

    def print_both (self,lang) :
        for word in self.voc :
            print(self.voc[word].ipa, "  vs  ", lang.voc[word].ipa)
