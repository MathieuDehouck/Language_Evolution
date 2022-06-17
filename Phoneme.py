# -*- coding: utf-8 -*-
"""
Created on Tue May  3 00:08:43 2022

@author: 3b13j
"""

from ipapy import UNICODE_TO_IPA



class Phoneme(object) :
    """
    A class representing a phoneme
    
    ...

    Attributes
    ----------
    ipa : str
        the ipa representation of a phoneme
    features : list
        a list representing the features associated to the phonem
    description : str
        the verbose descritption of the phoneme
    voice : bool 
        states if the phoneme is voiced or not
    syl : bool 
        states if the phoneme is center of a syllable
    
    
    Methods
    -------
    __init__() constructor taking all these information as input
    

    update_IPA  : finds the closest ipa character to represent a new phoneme
    
    lot of setters, most of which will be useful in I / D change when the position of a phoneme in the word structure might change. 
    
    """
    def __init__(self, features, syllabic, speller=None): 
        """
        a gentle Phoneme constructor
        """
        self.speller = speller
        self.syl = syllabic
        self.word_rank = None
        self.features = features
        self.ipa = speller.get_char(self)
        try:
            self.description = UNICODE_TO_IPA[str(self.ipa)]._IPAChar__canonical_string
        except:
            self.description = 'No description'
       
        
       
        
        
    def __str__(self):
        return str(self.ipa )+  " : " + str(self.description ) + "\n" + str(self.features)




#TODO : still useful ?  What for ?
    def to_int(self):
        h = int('1010'+str(self.features).replace(' ','').replace('(','').replace(')','').replace(',',''))

        h *= 4
        if self.is_Vowel():
            h += 1
        if self.syl:
            h += 2
        return h





    def set_word_rank(self, rk) :
        self.word_rank = rk 

    def set_rank_in_wd(self, rk) :
        self.set_word_rank(rk)
    
    def set_in_syl(self, i) : 
        self.in_syl = i

    def is_Consonant(self) :
        return type(self) == Consonant

    def is_Vowel(self) :
        return type(self) == Vowel

    def __eq__(self, other):
        return self.features == other.features





    def update_IPA(self, config, verbose = False) :
        """
        updates the ipa field of the Phoneme it is applied to. 

        Parameters
        ----------
        config : list
            A list representingthe feature we want 
        verbose : bool, optional
            As usual. Verbose with me means verry verbose. The default is False.

        Returns 
        -------
        None.

        """
        self.ipa = self.speller.get_char(self)


    


"""
def get_phon(string) :
"""
    #transform a string (we excpect the user to enter an ipa character) into the Phoneme object representing this character
"""
    if string not in ipa.alphabet.keys() :
        return
    return Phoneme(string, list(ipa.alphabet[string].features))

"""




class Vowel(Phoneme) : 
    
    """
    A class representing a Vowel
    
    Semantic of a feature ;
    
    syl : field of the Phoneme
    voice : filed of the Phoneme
    
    Features :
        First tuple :
             
            "fronting" : int  btw 0 and 2
            "height", int btw 0 and 6
                
        Second tuple :
            
            "round" : bool
            "nasal" : bool
    
    ...

    Attributes
    ----------
    ipa : str
        the ipa representation of a phoneme
    features : list
        a list representing the features associated to the phonem
    description : str
        the verbose descritption of the phoneme
    syl : bool 
        states if the phoneme is center of a syllable
    
    Methods
    -------
    __init__() constructor taking all these information as input
    
    update_IPA  : finds the closest ipa character to represent a new phoneme
    
    get_height
    get_front

    is_round
    is_nasal
    is_palatal
    is_voiced

    
    """
    
    def __init__(self, features, syllabic, speller):
        super().__init__(features, syllabic, speller)
        self.isV = True
        self.semantics =  ( 'Height','Backness', 'Round'), ('Voiced', 'Nasal')
        
        
        
        
        
    def get_height(self) :
        return self.features[0][0]

    def get_front(self) :
        return self.features[0][1]

    def is_round (self) :
        return self.features[0][3]

    def is_nasal(self) :
        return self.features[1][1] == 1

    def is_voiced(self):
        return self.features[1][0] == 1
    
    def is_palatal(self, threshold):
        return self.features[0][1] > threshold

    def __lt__(self, other):
        if other.is_Consonant():
            return True
        return self.features < other.features
    




class Consonant(Phoneme) : 
    """
    A class representing a Consonant
    
    Semantic of a feature ;
    
    syl : field of the Phoneme
    voice : filed of the Phoneme
    
    Features :
        First tuple :
            0 : 
            "place of articulation" : int 
            1 : list of 5 manner of articulation , each coded by a boolean
                "plosive"
                "fricative"
                "nasal"
                "trill"
                "lateral"
                
        Second tuple :
            
            "secondary place of articulation"  int (3 or 4 possibilities, same semantics as in place of articulation)
            "pren_nasal"  bool
            "aspiration" bool 
            
    
    ...

    Attributes
    ----------
    ipa : str
        the ipa representation of a phoneme
    features : list
        a list representing the features associated to the phonem
    description : str
        the verbose descritption of the phoneme
    voice : bool 
        states if the phoneme is voiced or not

    Methods
    -------
    __init__() constructor taking all these information as input
    
    update_IPA  : finds the closest ipa character to represent a new phoneme
    
    is_round
    is_nasal
    is_palatal
    
    get_place
    get_manner
    
    linearize : get the representation of the phoneme as a list of integers
    
    """
    
    
    
    def __init__(self, features, syllabic, speller):
        super().__init__(features, syllabic, speller)
        self.isV = False
        self.semantics = ('place of articulation', 'manner of articulation', 'Voiced'), ('secondary place of articulation', 'nasal' , 'aspiration')
        
    

    def is_round (self) :
        return self.features[0][0] == 11
    
    def is_labialised (self) :
        return self.features[1][0] == 11

    def is_palatal (self) :
        return self.features[0][0] == 3

    def is_uvular (self) :
        return self.features[0][0] == 1

    def is_nasal (self) :
        return self.features[0][1] == (1, 0, 0, 0, 0) or self.features[1][1] == 1

    def is_pre_nasalised(self):
        return self.features[1][1] == 1

    def is_aspirated (self) :
        return self.features[1][2] == 1
    
    def is_sonorant(self) :
        return self.features[0][1][0] == 0 and  self.features[0][1][0] == 1
 
    def has_sec_articulation (self) :
        return self.features[1][2]

    def __lt__(self, other):
        if other.is_Vowel():
            return False
        return self.features < other.features