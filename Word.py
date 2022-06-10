"""
Created on Wed May  4 14:39:58 2022

@author: 3b13j

Contains the Word class and some methods used specifically to work with it
"""

from IPA import IPA
ipa = IPA.get_IPA()


class Word :
    """
    A class to represent a word.

    ...

    Attributes
    ----------
    ipa : str
        phonological transcription of the word using the IPA
    structure : str 
        structure of the word (using a CVC format)
    syllables : list
        list of the syllable object the word contains
    phonemes : list
        list of the phonemes the word contains
    phon2syl : dic
        dictionnary mapping the index of a phoneme to the index of the syllable it is in

    Methods
    -------
    info(additional=""):
        Prints the person's name and age.
    """
    def __init__(self, syls):
        
        self.syllables = syls 
        #s = ""
        #for x in self.syllables : s += x.ipa
        self.ipa = '.'.join([syl.ipa for syl in self.syllables])
        self.structure = self.get_structure()
        self.stress_pattern = self.get_stess_pattern()
        
        phon = []
        phon2syl = {}
        inds = 0 # index of syllables
        indp = 0 # index of phonemes
        for j , syl in enumerate(syls) :
            syl.set_rank_in_wd(inds)
            for po in syl.phonemes :
                po.set_in_syl(j)
                phon.append(po)
                phon2syl[indp] = inds
                po.set_rank_in_wd(indp)
                indp += 1
            
            inds += 1
        self.phonemes = phon
        self.phon2syl = phon2syl
        

    def __eq__(self, other) :
        
        for i, phon in enumerate ( self.phonemes ) :
            if phon.features != other.phonemes[i].features :
                return False
        return True

        
    def __str__(self)  :
        
        s =self.ipa + "\n"    +'syllabation : '
        for x in self.syllables : s += x.ipa + "/"
        if s[-1] =="\"" :
            s = s [:-2]
        s += "\n"    + "structure : "+ str(self.structure)
        s += "\n"    + "stress pattern : "+ str(self.stress_pattern)
        return s
    
    
    def get_structure(self):
        """ transform a list of syllables into a string representing its structure (in the CVC format)"""
        s = '#'
        for syl in self.syllables :
            for phon in syl.phonemes :
                if phon.is_Vowel() :
                    if syl.stress :
                        s+= "v"
                    else :
                        s+= "V"
                    if syl.length :
                        s+= ":"
                else :
                    s +="C"
            s += "/"
        s = s[:-1]
        s+="#"
        return s    
    
    
    def get_stess_pattern(self) :
        """
        Returns a string representing the stress pattern of the word
        """
        s = ""
        for syllable in self.syllables :
            if syllable.stress : s += "S/"
            else : s += "_/"
        s = s[:-1]
        return s




class Syllable(object) :
    """
    A class to represent a syllable.

    ...

    Attributes
    ----------
    phonemes : list
        list of the phonemes composing the syllable
    stress : bool 
        indicate whether the syllable bears stress or not
    length : bool 
        indicate if the vowell in the syllable have more than 2 mora.
    i_center : int
        index of the phoneme which is at the heart of the syllable
    center: phoneme : 
        phoneme which is at the heart of the syllable

    Methods
    -------
    init__()__
        constructor that takes as input the list of phonemes in the syllable
        
    set_stress(bool) :
        allow the programm to change the stress of a syllable
        
    set_length(bool) : 
        allow the programm to change thelength of a syllable
    
    """
    
    
    
    def __init__(self, phonemes, stress=False, length=False, tone=None) :
        self.phonemes = phonemes
        self.stress = stress 
        self.length = length
        self.tone = tone
    
        # way to know which of the syllable's phoneme bears the accent / tone 
        syl = [phon.syl for phon in self.phonemes]
        print(syl)
        if True in syl:
            id_center = syl.index(True)
        else:
            vow = [phon.is_Vowel() for phon in self.phonemes]
            id_center = vow.index(True)

        self.center = self.phonemes[id_center]

        if self.stress:
            s = "'"
        else:
            s = ''
        for i, phoneme in enumerate(self.phonemes):
            phoneme.ipa = ipa.get_char(phoneme)
            s += phoneme.ipa
            if i == id_center and self.length:
                s += ':'

        self.ipa = s
        self.rank_in_wd = None
       
        
        
        
        
    def __str__(self) :
        return self.ipa  + "\nstress : "+str(self.stress)+"    length : "+ str(self.length)
    
    
    def set_rank_in_wd(self, rk) :
        """ small setter for the rank in word if it changes durong an I change) """
        self.rank_in_wd = rk
        
        
    def set_stress(self, stress) :
        """
        Allow the program to change the stress of a syllable

        Parameters
        ----------
        stress : bool
            The new value 

        Returns
        -------
        None.

        """
        
        self.stress = stress
        
        
        
    def set_length(self, length) :
        """
        Allow the program to change the stress of a syllable

        Parameters
        ----------
        stress : bool
            The new value 

        Returns
        -------
        None.

        """
        
        self.length =  length
        
    
    def __eq__(self, other ) :
            """ a syllable is equal to antoher syllable if it contains the same phonemes ,and have same stress, length and tone
            
            """
            for i, phon in enumerate ( self.phonemes ) :
                
                if phon.features != other.phonemes[i].features :
                    
                    return False
        
            if self.length != other.length : return False
            if self.stress != other.stress : return False 
            if self.tone != other.tone : return False
                
            return True
