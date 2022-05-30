"""
Created on Wed May  4 14:39:58 2022

@author: 3b13j

Contains the word class and some methods used specifically to work with it
"""

def get_structure(syllabes):
    """ transform a list of syllables into a string representing its structure (in the CVC format)"""
    s = '#'
    for syl in syllabes :
        for phon in syl.phonemes :
            if phon.isV :
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
        self.structure = get_structure(self.syllables)
        
        phon = []
        phon2syl = {}
        inds = 0 #index of syllables
        indp = 0 # index of phonemes
        for syl in syls :
            syl.set_rank_in_wd(inds)
            for po in syl.phonemes :
                phon.append(po)
                phon2syl[indp] = inds
                po.set_rank_in_wd(indp)
                indp += 1
            
            inds += 1
        self.phonemes = phon
        self.phon2syl = phon2syl
        
        
        
    def equals(self,word, verbose = False) :
        if verbose :
            print(self.ipa)
            print(word.ipa)
        bol = self.ipa == word.ipa 
        return bol
        
        
        
    def __str__(self)  :
        print()
        s =self.ipa + "\n"    +'syllabation : '
        for x in self.syllables : s += x.ipa + "/"
        if s[-1] =="\"" :
            s = s [:-2]
        s += "\n"    + "structure : "+ str(self.structure)
        
        return s
    
    
    
    def get_stess_patter(self) :
        """
        Returns a string representing the stress pattern of the word

        Returns
        -------
        s : str.

        """
        s = ""
        for syllable in self.syllables :
            if syllable.stress : s += "S/"
            else : s += "_/"
        s = s[:-1]
        return s
