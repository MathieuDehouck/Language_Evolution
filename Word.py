"""
Created on Wed May  4 14:39:58 2022

@author: 3b13j

Contains the Word class and some methods used specifically to work with it
"""








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
        s = ""
        for x in self.syllables : s += x.ipa
        self.ipa = s
        self.structure = self.get_structure()
        self.stress_pattern = self.get_stess_pattern()
        
        phon = []
        phon2syl = {}
        inds = 0 #index of syllables
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