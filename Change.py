# -*- coding: utf-8 -*-
"""
Created on Thu May  5 10:22:10 2022

@author: 3b13j
"""
from utilitaries import feature_match,  tpl2candidates, mask_match
from Phoneme import Phoneme, Vowel , Consonant, list_2_tuple
from Syllable import Syllable
from Word import Word
from Language import Language
from Condition import P_condition

from regularizations import regularize_stress, regularize_structure
from IPA import IPA


import random
import copy



# TODO gérer l'interaction entre V et C 
influence_V_on_C = {}
influence_C_on_C = {}




class Change :
    """
    An abstract class representing a phonetic change.
    They can be of three kinds : 
        * Phonetics (P_)
        * Syllabic (I_)
        * Wordzddzqd (?_)

    ...

    Attributes
    ----------
    conditions : list
        list of conditions required for the change to be applied
    imacted_phonems : dic
        dictionnary stocking the phonemes that have been impacted by a change during its application
        #TODO check it works
    target : condition
        a special kind of condition that contraint the category of the phoneme that undergo the change
    
    Methods
    -------
    __init__() constructor taking all these information as input
    
    add_condition
    set_target
    check : checks if all the conditions are satisfied before the application of the change
    """
    def __init__(self) :
        self.conditions = []
        self.impacted_phonemes ={}
        self.target = None
        
        
        
    def add_condition(self, condition) :
        """ used to add a condition to an already built change """
        self.conditions.append(condition)
    
    
    
    def set_target(self, cond) :
        self.target = cond
        
    
    
    def check(self,  phon, index , word, verbose = False):
        """
        check if a Change can be applied or not

        Parameters
        ----------
        phon : Phoneme
            phoneme we want to apply a change on
        index :int.
        word : Word
            Context
        verbose : TYPE, optional
            DESCRIPTION. The default is False.

        Returns
        -------
        apply : bool 
            whether the change can be applied or not

        """
        if len(self.conditions ) == 0  : return True 
        
        for condition in self.conditions :
            if verbose : 
                print("we test the following condition  ")
                print(condition)
            res = condition.test(word, index, verbose)
            # this structure of the loop allow to print all the unsatisied conditions, not just the one making the program crash
            if res == False :
                return False
                if verbose :
                    print ("following condition not satisfied : ")
                    print(condition)
        return True
    
    
    
    

class P_change(Change) :
    
    
    """
    subclass of change 
    A class modelling a phonological change .
    
    ...

    Attributes
    ----------
    conditiosn : list
        list of the conditions that need to be satisfied for the change to be applied
    config_initiale : configuration
        template of the configuration selecting the feature(s) to be modified
    config_finale : configuration
        template with the modification applied
    
    
    Methods
    -------
    __init__() constructor taking all these information as input
    
    apply_phon :
        input : a phoneme (among other onformations)
        outputs a phoneme with the change umpload
    
    variants :
        
    apply_word
    apply_syl
    apply_language
    
    
    add_condition :
        input : a condition
        adds it to the condition list.
    
    rd_change ; creates a random change
    
    
    
    """
    
    
    
    
    def __init__(self, effect, phon) :
        """ 
        a Phonetic change deals with the modification of a phonem, therefore the object P_change need
        information about the phoneme to modify. The two configurations object encode these informations,
        while the impacted_phonemes dictionnary stores the phonem of the language that underwent the change
        during the process of its application
        """
        super().__init__()
        
        
        self.target = phon.features
        self.is_Vowel = phon.is_Vowel()
        self.effect = effect
        self.impacted_phonemes ={}
        
        
        
        #TODO : rustine un bu fait que qd on crée plusieurs changements à la suite du même nom (dans une boucle par ex)
        # la liste des changements n'est pas remise à 0
        
        
        
    def applicable (self, language) :
        """
        checks if a change would modufy a language given as input. 
        if that s not the case, it is not usefull to apply it.

        Parameters
        ----------
        language : Language
            the language we would like to apply the change on

        Returns
        -------
        bool
            DESCRIPTION.

        """
        for phoneme in language.phonemes :
            if mask_match(self.target, phoneme.features, self.is_Vowel) :
                print("winner)")
                print(phoneme)
                return True
        return False
        
        
        
    def compensate(self, phon) :
        
        #TODO
        return phon
        
    
    
        
        
    def apply_phon (self,  phon, index , word, verbose = False):
        """
        Applies the change on a phoneme

        Parameters
        ----------
        phon : phoneme
            phone
        index : int 
            rank of the phoneme in the overall word
        word : word 
            wird that encompass the phoneme we are studying, plays the role of a contest
        verbose : bool, optional
            Enable or disable the verbose mode . The default is True.

        Returns
        -------
        index
            the updated index at the end of the process
        phon 
            the new phoneme obtained after the applciation of the change

        """
        
        if verbose :
            print ()
            print("we study the phoneme : ", index , phon.ipa)
            print()
        applicable = self.check (phon, index , word, verbose = False)
        
        if not applicable or not mask_match(self.target, phon.features, self.is_Vowel):
            if verbose : print("the condition is not respected, nothing is changed", phon.ipa)
            return phon, index+1
        
        
        if phon.isV != self.effect.isV : 
            if verbose : print ("wrong side")
            
            return phon, index+1
        
        
        if not phon.isV : ft = [[0, 0, 0],[0,0,0]]
        
        else : ft =  [[ 0, 0 , 0],[0,0]]
        
        for ind in self.effect.idx : 
            
            if ind in self.effect.effect : 
                ft[ind[0]][ind[1]] = self.effect.effect[ind]
            else :
                ft[ind[0]][ind[1]] = phon.features[ind[0]][ind[1]]

        
        ft = list_2_tuple(ft)
        
        if phon.isV : new_phon = Vowel(ft, phon.syl, phon.speller)
        else : new_phon = Consonant(ft, phon.syl, phon.speller)
        
        """
        if verbose  :
            if modif : print("conditions satisfied, a new phonem is born ", new_phon.ipa)
            else : print("no change")
            """
        return new_phon, index+1

    
    
    def apply_word(self, wd , verbose = False) :
        """
        Apply the change to a word

        Parameters
        ----------
        wd : word

        Returns
        -------
        word : a new word with the change applied

        """
        
        syls = []
        index = 0 #used to parse the whole structure of the word
        

        for syl in wd.syllables :
            syl, index  = self.apply_syl(syl, index, wd, verbose)
            syls.append(syl)
        return Word(syls)
         
    
    
    def apply_syl(self,syl, index, wd, verbose = False):
        """
        Apply the change to a Syllable

        Parameters
        ----------
        syl : syllable
            the syllable we are going to apply the change to
        index : int
            index encoding the phoneme that will undergo the change
        wd : TYPE
            word of origin of the syllable, plays the role of the context

        Returns
        -------
        syl : 
            the updated syllable
        
        index : int
            the index updated

        """
        
        phonemes = []
        for phon in syl.phonemes :
            phon2 , index = self.apply_phon( phon, index , wd , verbose)
            phonemes. append(phon2)
        return Syllable(phonemes, syl.stress, syl.length), index
    
    
                
    def apply_language(self, lang, verbose = False):
        """
        Apply the change on every word in the langugage

        Parameters
        ----------
        lang : language

        Returns
        -------
        a new language with the change applied on every of its word

        """
        changed_words = []
        
        dic = {}
        for wd in lang.voc :
            word  = lang.voc[wd]
            save = copy.deepcopy(word)
            word = self.apply_word(word)
            if verbose : print(word)
            dic[wd] = word
            if not save == word : changed_words.append([ lang.voc[wd].ipa, word.ipa])
            
        return Language(lang.name+"*", dic), changed_words
        #TODO ; the name of the new language could be parametrizable maybe
    
    
    
    def __str__(self) :
        s = "Target :   \n"
        s += str(self.target) + " \n"
        s+= "Effects : \n"
        s+= str(self.effect) + "\n"
        #TODO améliorer
        
        s+= "Conditions : \n"
        for i, condition in enumerate(self.conditions) :
            s+= str(i) + "  " +str(condition) + " \n"
        return s
    
    
    """
    def rd_change (lang, verbose = False ):
            #""
        generates a randomly parametrized change that can be applied and will surely modify the 
        Language given in input.
    
        Parameters
        ----------
        lang : Language
            the language for which we want to create an applicable change.
            We ignore changes that coulnd t be applied
        verbose : TYPE, optional
            DESCRIPTION. The default is False.

        Returns
        -------
        ch : TYPE
            DESCRIPTION.

            #""
            if verbose : print("we create a rd change")
            li = lang.phonemes
            
        # this block list the phonemes creates a condition on the target and checks that this target can
        # be affected by the change. if that s not the case, we find another target       
            trg = P_condition. rd_p_condition()
            tpl = trg.template
            candidates2 = tpl2candidates(li, tpl, verbose)
            i = 0
            while len(candidates2 ) == 0 :
                trg = P_condition.rd_p_condition()
                tpl = trg.template
                candidates2 = tpl2candidates(li, tpl, verbose)
                if verbose : print("fail bis ", i)
                
                if i> 100 :  # trick to avoid the program never terminating in difficult configurations
                    break
                i+=1
                
        # this block of code fixes the nature of the change we generate
            conf_i = Configuration()
            conf_f = conf_i.get_output()
            candidates = []
            i=0
            while len(candidates) == 0 :
                candidates = tpl2candidates(candidates2, conf_i.state, verbose)
                conf_i = Configuration()
                conf_f = conf_i.get_output()
                if verbose : print("fail", i)
                i+=1
                # if the program is not able to find a change to apply to the phoneme , we generate another target
                if i> 100 :
                    trg = P_condition. rd_p_condition()
                    tpl = trg.template
                    candidates2 = tpl2candidates(li, tpl, verbose)
            
            
           ## in this third block, we add new p_conditions on our change.
           # we still want this condition to be applicable.
           
           # first we choose if the assimilation / dissimilation is progressive or not.
           
           
            #TODO refactor cette partie en une sous fonction callable
            direction= random.randint(0,1) 
            if direction == 0 : direction = -1 
            cond = P_condition.constrained_rd_condition( conf_i , direction)
            candidates3 = []
            j = 0
            while len(candidates3 ) == 0 :
                candidates3 = tpl2candidates(candidates, cond.template, verbose)
                cond = P_condition.constrained_rd_condition( conf_i , direction)
                if verbose : print("F A I L", j)
                j += 1
            
            #second condition ?
            sc = random.randint(0,1) 
            if sc :
                direction = -direction  # on conditionne le changement de l'autre côté
                cond2 = P_condition.constrained_rd_condition( conf_i , direction)
                candidates3 = []
                j = 0
                while len(candidates3 ) == 0 and j<100:
                    candidates3 = tpl2candidates(candidates, cond.template, verbose)
                    cond2 = P_condition.constrained_rd_condition( conf_i , direction)
                    if verbose : print("F A I L", j)
                    j += 1  
                
                
                
                
                
                
                
                
                
            
            
            # Those ligns create the P_change with the elements obtained at each step
            ch = P_change(conf_i, conf_f)
            ch.set_target(trg)
            #ch.add_condition(trg)
            ch.add_condition(cond)
            if sc : ch.add_condition(cond2)
            return ch 
                
        """        
      
    
    
class S_change(Change) :
    """
    subclass of change 
    A class modelling a structural change in the syllable .
    
    ...

    Attributes
    ----------
    conditiosn : list
        list of the conditions that need to be satisfied for the change to be applied
    config_initiale :  list
        a list of 3 boleans coding stress , length and tone (None for now)
    config_finale : list
        a list of 3 boleans coding stress ,length (None for now)
    
    
    Methods
    -------
    __init__() constructor taking all these information as input
    
        
    apply_word
    apply_syl
    apply_lang
    
    
    add_condition :
        input : a condition
        adds it to the condition list.
    
    
    
    
    """
    
    def check(self, word, rank) :
        """
        checks if a change would modufy a language given as input. 
        if that s not the case, it is not usefull to apply it.

        Parameters
        ----------
        language : Language
            the language we would like to apply the change on

        Returns
        -------
        bool
            DESCRIPTION.

        """
        for condition in self.conditions :
            if not condition.test(word, rank) : return False
                
        for s in word.syllables :
            if s.stress == self.config_initiale[0] and s.length == self.config_initiale[1] and  s.tone == self.config_initiale[2] :
                    return True
        return False
    
    
    def __init__(self, config_initiale, config_finale, conditions = []) :
        self.conditions = conditions
        self.config_initiale = config_initiale
        self.config_finale = config_finale
        self.reconfig_stress = []
      
    
    
        
    def apply_syl (self, syl, word, index) :
        
        # Un peu brouillon ,  à améliorer 
        #mettre à jour la rpz de l'accent dans l IPA  / structure de syllabe
        applicable = self.check (word, index)
        if not applicable : return syl
        n_syll = Syllable(syl.phonemes, self.config_finale[0],self.config_finale[1],self.config_finale[2] )
        
        if self.config_initiale[0] != self.config_finale[0] and syl.stress == self.config_initiale[0] :
            self.reconfig_stress.append(index)
            
        return n_syll
    
    def apply_word (self, wd) :
        
        syls = []
        for i, s in enumerate( wd.syllables) :
            ns = self.apply_syl ( s, wd, i)
            syls.append(ns)
        w =  Word(syls)
        for ind in self.reconfig_stress :
            regularize_stress(ind, w)
        return w
    
    
    def __str__(self) :
        s= "if following conditions are satisfied : \n"
        for condition in self.conditions :
            s+= str(condition) + "\:n"
        s+= "following effect  :\n "
        s+= str(self.effect) + "\n"
        
        return s
    
    
    
    
class I_change(Change) :
    
    """
    class allowing insertion or deletion of phonemes
    We examine
    
    
    
    """
    
    def __init__(self, deletion = True ) :
        self.delete = deletion
        
        
      
    def apply_word(self,wd) :
        if self.delete : 
            self.deletion(wd)
  
    
    def deletion(self, wd) :
        
        flag_change =  False
        syls = []
        for syl in wd.syllables :
            for phon in syl :
                if phon.features == syl.target :
                    syl = Syllable ( [pho for pho in syl if pho != phon  ], not phon.is_Vow and syl.stress, not phon.is_Vow and syl.length, None)
                    flag_change = False
                syls.append(syl)
        new_wd = Word(syls)
        if flag_change : regularize_structure(new_wd)
    
    
