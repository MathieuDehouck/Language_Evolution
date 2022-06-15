# -*- coding: utf-8 -*-
"""
Created on Thu May  5 15:09:17 2022

@author: 3b13j


Contains the condition class and some methodes that could be applied to them.
A condition is associated to a change object and states whether a change can be applied or not. 

"""

maxC = [11, 1, 1, 1, 1, 2, 1, 1 , 1 , 1]
maxV = [2, 6, 1 , 1 , 1]


import Sampling
from utilitaries import get_random_pattern, mask_match, feature_indices, printl
import random
from encoder_decoder import encode_f, decode_f

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


    def test(self, word, rank) :
        NotImplemented
    
    
    def encode_condition(self):
        if type(self) == P_condition :
            return self.encode_P_cond()
        else  : return self.encode_S_cond()
        
    """
    def decode_condition(string) : 
        if type() == P_condition :
            return self.encode_P_cond()
        else  : return self.encode_S_cond()
    """
    
    
    def decode_condition(string) :
        if string[0] == "P" : return P_condition.decode_P_cond(string)
        if string[0] == "S" : return P_condition.decode_S_cond(string)



class Cond_OR(Condition):
    """
    OR for conditions logic.
    """

    def __init__(self, conditions):
        self.conditions = conditions


    def test(self, word, rank, verbose=False):
        for cond in self.conditions:
            if cond.test(word, rank, verbose):
                return True
        return False



class Cond_AND(Condition):
    """
    AND for conditions logic.
    """

    def __init__(self, conditions):
        self.conditions = conditions


    def test(self, word, rank, verbose=False):
        for cond in self.conditions:
            if not cond.test(word, rank, verbose):
                return False
        return True



class Cond_NOT(Condition):
    """
    NOT for conditions logic.
    """

    def __init__(self, condition):
        self.condition = condition


    def test(self, word, rank, verbose=False):
        return not self.condition(word, rank, verbose)


        
    
    
class P_condition(Condition) :
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
    
    def __init__(self, feature_template,  rel_pos = 0 , absol_pos = 42, continu = False):
        
        self.template = feature_template 
        self.rel_pos = rel_pos
        self.absol_pos = absol_pos
        self.continu = continu
        self.concerns_V = (len(feature_template[1]) == 2)
    
    
    def __eq__(self, other) :
        if other == None or self == None : return False
        return self.template == other.template and self.rel_pos == other.rel_pos and self.absol_pos == other.absol_pos and self.continu == self.continu     
        
        
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
        
        """
        if phon.isV != self.concerns_V:
            if verbose : print("not applicable on the target")
            return False 
        """
        # does the condition have an absolute position to be checked on ?
        #TODO in the implementation,  a condition is either absolute or relative.
        if self.absol_pos  != 42 :
            
            #small words do resist.
            
            if abs(self.absol_pos) >= len(word.phonemes) : return False
            
            
            if verbose : 
                print(word)
                print(self.absol_pos)
                printl(word.phonemes)
            phon_to_test = word.phonemes[self.absol_pos]
            if verbose : print("absolute position requirement tested on "+ phon_to_test.ipa)
            answ =  mask_match(self.template, phon_to_test.features,self.concerns_V)
        
            if verbose : 
                print (self.template )
                print (phon_to_test.features)
                print ("MATCH : ", answ)
            return answ
        
        # we check if the relative positions match 
        index = rank + self.rel_pos 
        #TODO
        if rank not in range (len(word.phonemes)) :
            if verbose : print('conditioning phoneme not in range')
            return False
        if verbose :
            print("we need to satisfy the following pattern")
            print("Template :" , self.template )
            print( "Phoneme :" , word.phonemes[index].ipa, "    " , word.phonemes[index])
            
        if not self.continu :
            if index not in range (len(word.phonemes)) : bol = False
            else : bol = mask_match ( self.template , word.phonemes[index].features , self.concerns_V )
            if verbose :
                if bol :print("CONDITION SATISFIED") 
                else : print ("CONDITION NOT SATISFIED")
            
            return bol
        
        
        for j in range (min(index, rank) ,max(index, rank) ) :
                val = mask_match( self.template , word.phonemes[j].features , self.concerns_V  )
                if verbose :
                    print("we test ",j)
                    print(val)
                    print()
                if val : 
                    if verbose : 
                        print("CONDITION SATISFIED") 
                    return True
                
        if verbose: print ("CONDITION NOT SATISFIED")
        return False
    
    
    
    
    
         
    def __str__(self) :
    
        return "C:   Rel pos :  " + str(self.rel_pos) + "    Abs_pos : "+ str(self.absol_pos) +  "         Continu : "+ str(self.continu) +  "\nTemplate :" + str(self.template)
          
    
    
    
    
    def encode_P_cond(self) :
        
        s= "PCond:"
        s+= "T:" +encode_f(self.template)
        s+= " | " + "Rel:"+str(self.rel_pos)
        s+= " | " + "Abs:"+str(self.absol_pos)
        s+= " | " + "Cont:" + str(self.continu)
        
        return s
    
    
    
    
    
    def decode_P_cond(string) :
        
        string = string [8:]
        string = string.split(" | ")
        
        
        template = decode_f(string[0])
        rel_pos = int(string[1][4:])
        abs_pos = int(string[2][4:])
        b = ((string[3][5:])) == 'True'
    
        return P_condition(template, rel_pos, abs_pos, b)
        
    
def rd_p_condition( language, rel_pos = 0, abs_pos = -1, continu = False):
        """
        generates a random P_condition

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
         
        
        sign = random.randint(0, 1) 
        if sign == 0 : sign = -1
        
        pattern = get_random_pattern(language)
        cond = P_condition(pattern, sign)
         
        return cond
    
    
    
    
    
    

    
    
    
    
# premier essai d'implémentation, en lien étroit avec la façon donc on a implémenté la structure dans la classe mot
class S_condition (Condition) : 
    """
    A class to represent a condition regarding the Syllabic structure of the word

    ...

    Attributes
    ----------
    absol_pos : int
        absolute offset, checks the position of the syllable  inside the word.
        -1 means wildcard
    rel_pos : int
        defines the position of the phoneme conditionning the change regarding the syllable undergoing it
        0 means the condition applies to the phonemes that changes itself
    stress : bool 
        Checks a condition on the stress 
    length : bool 
        Checks a condition on the length 
    tone : bool 
        Checks a condition on the tone
        
    
    Methods
    -------
    __init__() constructor taking all these information as input
    
    test :
        input : a word and an index.
        checks whether the condition is satisfied.
    """
    
    #TODO implement tones 
    
    def __init__(self, abs_position = 42 , rel_pos=0, length = None, stress = None  ,tone = None, ):
        
        self.stress = stress
        self.length = length
        self.tone = tone
        self.abs_position = abs_position
        self.rel_pos = rel_pos
        
    def __eq__(self, other ) :
        return self.stress == other.stress and self.length == other.length and self.tone == other.tone and self.abs_position == other.abs_position and self.rel_pos == other.rel_pos 
        
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
        
        
        
        nb_syl = len(word.syllables)
        
        # we test the condition on absolute positions.
        # in the semantic of our programm -1 means the last , -2 the penultian and so on
        
        
        # index of the syllable we need to study
        index  = rank + self.rel_pos
        
        if index not in range(nb_syl) : return False  
        #TODO modif
        if abs(self.abs_position) not in range (nb_syl) : return False
        
        #test of absolute position : 
        if self.abs_position != 42 :
            if word.syllables[self.abs_position] != word.syllables[index] : return False 
            #else : print ( word.syllables[rank] .ipa , " vs ", word.syllables[index] )
        
        
        return  self.length == word.syllables[index].length and self.stress == word.syllables[index].stress and self.tone == word.syllables[index].tone
        
        
      
            
            
            
            
         
    def __str__(self) :
        
        return "C Syl :" + "\nabsolute position : " + str(self.abs_position) + "         relative position : " +str(self.rel_pos) + "\nlength : " + str(self.length) + "         stress : " +str(self.stress)
        
    
    
    def encode_S_cond(self) :
        
        s= "SCond:"
        s+= "Str:" + str(self.stress)
        s+= "|" + "Len:"+str(self.length)
        s+= "|" + "Ton:"+str(self.tone)
        s+= "|" + "Rel:"+str(self.rel_pos)
        s+= "|" + "Abs:"+str(self.abs_position)
        
        return s
    
    
    
    
    
    def decode_S_cond(string) :
        
        string = string [8:]
        string = string.split("|")
        
        stress = ((string[0][5:])) == 'True'
        length =  ((string[1][5:])) == 'True'
        
        tone = (string[2][5:]) == 'True'
        if  (string[2][5:]) == "None" : tone = None
        rel_pos = int(string[3][4:])
        abs_pos = int(string[4][4:])
        
    
        return S_condition(abs_pos, rel_pos, stress, length, tone)
