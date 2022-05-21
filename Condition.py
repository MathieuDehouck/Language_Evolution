# -*- coding: utf-8 -*-
"""
Created on Thu May  5 15:09:17 2022

@author: 3b13j


Contains the condition class and some methodes that could be applied to them.
A condition is associated to a change object and states whether a change can be applied or not. 

"""

import utilitaries
import random

class Condition():
    
    """
    MOTHER CLASS
    
    
    A class to represent a condition.
    This is an abstract class.
    
    In our implementation of phonetic change, we distinguished 3 different subclasses of conditions :
        
        * phonemic condition
        
        * stress and syllable weight condition
        
        * metathesis and mechanical conditions
    
    """
    
    def __str__(self) :
        return "condition :"
    
    
    
class P_condition (Condition) :
    """
    A class to represent a condition regarding the nature of the phoneme that undergoes a change 
    and its neighbours.

    ...

    Attributes
    ----------
    template : list
        the feature template that need to be satisfied (-1 means  wildcard) for the condition to be satisfied
    name : str (optionnal)
        used to name usual changes
    absol_pos : int
        absolute offset, checks the position of the phoneme inside the word.
        -1 means wildcard
    rel_pos : int
        defines the position of the phoneme conditionning the change regarding the phoneme undergoing it
        0 means the condition applies to the phonemes that changes itself
    continu : bool
        states if the condition needs to be satisfied by at least one of the phoneme in the range of rel_pos or 
            if just the phoneme at "rel pos " is concerned. 
    
    
    Methods
    -------
    __init__() constructor taking all these information as input
    
    test :
        input : a word and an index.
        checks whether the condition is satisfied.
    """
    
    def __init__(self, feature_template,absol_pos = -1,  rel_pos = 0 , continu = False):
        
        self.template = feature_template 
        self.rel_pos = rel_pos
        self.absol_pos = absol_pos
        self.continu = continu
    
    
    
    def set_absol_pos(self, value) :
        """
        set the condition's absol pos with a new value'

        Parameters
        ----------
        value : int

        Returns
        -------
        None.

        """
        self.absol_pos = value 
        
        
        
    def set_rel_pos(self, value) :
        """
        set the condition's relative pos with a new value'

        Parameters
        ----------
        value : int

        Returns
        -------
        None.

        """
        self.rel_pos = value 
    
    
    
    def set_ft(self, index, value) :
        self.template[index] = value 
       
        
       
    def set_continu(self, value) :
        self.continu = value
    
    
    
    def test(self, word, rank, verbose = False) :
        """
        Checks if a condition is satisfied on a given word.
        Key method of the Condition class

        Parameters
        ----------
        word : word
            word on which we check the condition
        rank : int
            rank of the word we examine the condition on
        verbose : TYPE, optional
            as usual. The default is False.

        Returns
        -------
        a boolean
        """
        
        if verbose :
            print("word on which the condition is being tested ")
            print(word)
            print("we test the condition on the ", rank,"th phonem")
            print(word.phonemes[rank])
            print()
            
        phon = word.phonemes[rank]
        
        # does the condition have an absolute position to be checked on ?
        if self.absol_pos  != - 1 :
            if  self.absol_pos != rank :
                if verbose : print("The condition is not applied on the phoneme "+ phon.ipa)
                return  False
        
        # we check if the relative posotions match 
        index = rank + self.rel_pos 
        if index not in range (len(word.phonemes)) :
            return False
        if verbose :
            print("we need to satisfy the following pattern")
            print("Template :" , self.template )
            print( "Phoneme :" , word.phonemes[index].ipa, "    " , word.phonemes[index])
            
        if not self.continu :
            bol = utilitaries.feature_match ( self.template , word.phonemes[index].features)
            return bol
        
        
        for j in range (min(index, rank) ,max(index, rank) ) :
                val = utilitaries.feature_match ( self.template , word.phonemes[j].features    )
                if verbose :
                    print("on teste ",j)
                    print(val)
                    print()
                if val : return True   
        return False
    
    
         
    def __str__(self) :
        return "C:   rel pos : " + str(self.rel_pos) + "\n    template :" + str(self.template)
          
    
    
    #TODO raffiner la gestion des conditions contraintes 
    def constrained_rd_condition( config , rel_pos = 0, abs_pos = -1, continu = False):
        """
        Creates a random condition constrained by a configuration 
        """
        modifs = [] # the non wildcarded features
        tpl = config.state
        for i in range (len(tpl)) :
            if tpl[i] != -1 :
                modifs.append(i) 
                   
        cond = P_condition.rd_p_condition(  rel_pos , abs_pos  , continu ) 
        
        #these lines of code add a constrained condition on a phoneme directly following the target phoneme
        for ind in modifs :
            if ind >1 :
                if cond.template == -1 : 
                    val = random.randint (0,1)
                    cond.set_ft(ind, val)
                    
        return cond
        
        
    
    def rd_p_condition( rel_pos = 0, abs_pos = -1, continu = False):
        """
        generates a random s_condition

        Parameters
        ----------
        rel_pos : int, optional
            indicates the relative position of the condition
        abs_pos : TYPE, int
             cf condition class
        continu : TYPE, optional
            cf condition class

        Returns
        -------
        None.

        """
         
        # the main goal of this function to generate a condition is to generate the feature_template.
        ft = [-1] * 12
        sy = random.randint (0,1)
        vo = random.randint (0,1)
        while sy == 1 and vo == 1 :
            sy = random.randint (0,1)
            vo = random.randint (0,1)
        ft[0] = sy
        ft[1] = vo
        
        
        #TODO crucial pt in the parameters we would like a distribution over proba here
        #TODO we decided to just condition up to two parameters. this value could / shuld change
        #we want to condition one to three other features :
        fts = random.randint (0,4)
        
        for i in range(fts) :
            index = random.randint (2,11)
            
            # we adapt the rank to the feature
            ran = 1
            if index == 1 or index == 2 :
                ran = 3
                if sy == 1 and index == 1 :  ran = 2
                if sy == 0 and index == 2 : ran =2
            
            #TODO roundness
            
            value = random.randint(0, ran)
            ft[index] = value
        
        cond = P_condition(ft,  abs_pos, rel_pos, continu)
        
        return cond
    
            
            
            
           
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
# premier essai d'implémentation, en lien étroit avec la façon donc on a implémenté la structure dans la classe mot
class s_condition (Condition) : 
    
    def __init__(self, name,length = None, stress = None  , abs_position = -1 , rel_pos=0):
        
        
        self.name = name
        self.stress = stress
        self.length = length
        self.abs_position = abs_position
        self.rel_pos = rel_pos
        
    def test(self, word, rank, verbose = False) :
        """
        Test if the change can be applied on the word regarding the syllabic configuration

        Parameters
        ----------
        word : word
            the word that undergoes the change
        rank : int
            rank of the syllable that is being examined
        verbose : bool, optional
            enable the verbose mode. The default is False.

        Returns
        -------
        bool
            boolean, if the change has to be applied

        """
        
        
        index_syl = word.phon2syl[rank]
        index = index_syl + self.rel_pos 
        
        print("on teste pour la syl ", index_syl)
        
        
        if index not in range (len(word.phonemes)) :
            print("index out of range")
            return False
        syl = word.syllables[index]
        print("length", self.length,syl.length )
        print("stress", self.stress, syl.stress )
        
        if self.length != None :
            if self.length != syl.length :
                return False
        if self.stress != None :
            if self.stress != syl.stress :
                return False
                
        return True
        
         
    def __str__(self) :
        
        return "condition :" + self.name + "\n" + str(self.length) + "stress : " +str(self.stress)
        
