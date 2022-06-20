# -*- coding: utf-8 -*-
"""
Created on Thu May  5 09:28:54 2022

@author: 3b13j

Contains the Languge class
"""
from utilitaries import printl, feature_indices





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
    
    def __init__(self, dic, name = "unnamed") :
        """
        take as input the name of the language and a dictionnary of words. it is going to create a Language 
        object automatically from this object

        Parameters
        ----------
        
        dic : dic
            voc of the language
        name : str (optional)
            name of the language.

        Returns
        -------
        Self

        """
                
        self.voc = dic 
        self.name = name
        self.phonemes = None
        
        
    


    def set_phonetic_inventory(self) :
        """
        Gives a lot of information about rhe phonetic inventory of a language.
        Extracted from the __init__ lethod in hope for computation time gain
        """
        
        
        phonemes = []
        features = []
        dic_phonemes = {}
        # get an overview of the phonetic inventory of a language
        for word in self.voc.values() :
            for syl in word.syllables :
                for feat in syl.phonemes :
                    if feat.features not in features :
                        features.append(feat.features)
                        phonemes.append(feat)
                        
        self.phonemes   = list(tuple(phonemes)) # we eliminate doubles
        self.features = features
        #TODO is the following dic necessary? 
        for phoneme in phonemes :
            dic_phonemes[phoneme.ipa] = phoneme        
        self.dic_phonemes = dic_phonemes






    def __str__(self) :
        return self.name + str(self.phonemes)

    
    
    
    
    def print_phonetic_inventory(self) :
        """
        Prints a simple version of the inventory of the language's phonemes.

        """
        print()
        print("PHONOLOGICAL INVENTORY OF",self.name)
        print()
        for phon in sorted(self.phonemes) : 
            print(phon.ipa, "   ", phon.description)
    
    
    
    
    
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
            
            if  not w1 == w2 :
                differents.append([self.voc[word],language.voc[word] ])
        
        if verbose :
            print (len(differents), " different words")
            print (len(self.voc) - len(differents), " unchanged words")
        if  verbose and len(differents) != 0 :
                print("change happened")
                printl(differents)
            
        return differents
    
    
    

    def print_both (self,lang) :
        """
        print all words of a language close to each other
        """
        for word in self.voc :
            print(self.voc[word].ipa, "  vs  ", lang.voc[word].ipa)



    

    def inventory_comparison(self, other) :
        """
        Compare the phonetic inventory of two language

        Parameters
        ----------
        other :Language
        """
        
        if self.phonemes == None : self.set_phonetic_inventory()
        if other.phonemes == None : other.set_phonetic_inventory()
        
        printl(self.phonemes)
        print()
        print()
        printl(other.phonemes)
        
        tot = [x for x in self.phonemes if x not in other.phonemes] + [x for x in other.phonemes if x not in self.phonemes]
        match = len( [x for x in self.phonemes if x in other.phonemes ] )
        total = len(tot)
        diff = []  
        ina = [x .ipa for x in self.phonemes if x not in other.phonemes ]
        for p in ina : diff.append([p, "only in "+str(self.name)])
        inb = [x.ipa for x in other.phonemes if x not in self.phonemes ]
        for p in inb : diff.append([p, "only in "+str(other.name)])
        
        return (match)/ total , diff
        




    def phoneme_comparison(self, other) :
        """
        Compare the phonmes

        Parameters
        ----------
        other :Language
        """
        
        match = 0
        total = 0
        
        for key, wd in self.voc.items() :
            
            for i , pho in enumerate(wd.phonemes) :
                total += 1 
                if pho == other.voc[key].phonemes[i] : match += 1 
        
        return match /total 
                
    
    
    
    
    def feature_comparison(self, other) :
        """
        Compare the feature inventory of two languages

        Parameters
        ----------
        other :Language
        """
        
        match = 0
        total = 0
        
        for key, wd in self.voc.items() :
            
            for i , pho in enumerate(wd.phonemes) :      
                other_pho  =  other.voc[key].phonemes[i]                      
                idx = feature_indices(pho.features)
                for j, ids in enumerate(idx) :
                    total += 1
                    if pho.features[ids[0]][ids[1]] == other_pho.features[ids[0]][ids[1]] : match += 1
    
        return match /total 
        
        
        
        
        
    def evaluate_proximity(self, other ) :
        """
        Compare two languages using various metrics. 

        Parameters
        ----------
        other :Language
        """
        
        
        invent_sim , diff = self.inventory_comparison(other)
        phon_sim = self.phoneme_comparison(other)
        feat_sim = self.feature_comparison(other)
    
    
        print("Phonetic inventory similarity ", invent_sim, "%")
        print()
        print("Phoneme match similarity ", phon_sim, "%")
        print()
        print("Feature match similarity", feat_sim, "%")
    
        print("different phonemes :")
        printl(diff)
        
    
    
    

class State():
    """
    
    A condensed representation of a language for faster interaction and change generation

    ...

    Attributes
    ----------    
    phonemes : dict
        list of all the phonemes belonging to the language
    syllables : dict
        a dict of syllables

    Methods
    -------
    __init__() the constructor
    
    
    """

    def __init__(self, language):
        self.phonems = {}
        self.syllables = {}

        for form, word in language.voc.items():
            for syl in word.syllables:
                try:
                    self.syllables[syl].append(word)
                except:
                    self.syllables[syl] = []
                    self.syllables[syl].append(word)

        #for syl, words in sorted(self.syllables.items()):
        #    print(syl.ipa, words)
