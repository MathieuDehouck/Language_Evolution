"""
to fill
"""
import random
from wiki_utilities import get_language 
latin = get_language('latin_classique.txt', "latin")
from utilitaries import printl, feature_match,  tpl2candidates
from Configuration import Configuration
from Condition import P_condition , S_condition 
from Change import P_change

def mod() :
    return random.randint(0,1)

def restrict(phon, sub_classes, classe2 = None) :
    # we extract the sub_classes containing the phoneme
    sub_classes = [ cl  for cl in sub_classes if phon in  cl ]
    rd = random.randint(0, len(sub_classes)-1)
    classe = sub_classes[rd]
    sub_classes.remove(classe)
    if classe2 != None : classe = list ( set(classe ) .intersection( set( classe2)))
    return sub_classes, classe

class Change_Generator():

    

    def __init__(self, verbose = False):
        self.verbose = verbose



    def generate_P_cond(self, lang_state, conf_i, candidates):
        """
        Generates a random P_condition

        Parameters
        ----------
        lang_state : Language
            The Language we are currently studying

        Returns
        -------
        cond : P_condition
        
        """
        
        direction= random.randint(0,1) 
        if direction == 0 : direction = -1 
        rel_pos = random.randint(1, 5)
        continu = random. randint(0,1)
        cond = P_condition.constrained_rd_condition( conf_i , direction*rel_pos, -1, continu)
        candidates2 = tpl2candidates(candidates, cond.template)
        # We want our condition to be compatible with the phonemes belongingto out language
        while len(candidates ) == 0 :
            print("we generate a P_cond")
            candidates2 = tpl2candidates(candidates, cond.template)
            cond = P_condition.constrained_rd_condition( conf_i , direction*rel_pos, -1, continu)
           
        return cond
        
    
    
    def generate_S_cond(self, lang_state) :
        """
        Generates a random S_condition

        Parameters
        ----------
        lang_state : Language
            The Language we are currently studying

        Returns
        -------
        cond : S_condition
        

        """
        length = False 
        stress = False
        if mod() : stress =  bool(random.randint(0,1) )
        if mod() : length = bool(random.randint(0,1) )
        #TODO tone
        
        abs_pos = 42
        if mod() : 
            sign = random.randint(0,1)
            if not sign : sign = -1 
            rang = random.randint(1,2)
            abs_pos = sign*rang 
            
        rel_pos = 0
        if mod() : 
            sign2 = random.randint(0,1)
            if not sign2 : sign2 = -1 
            rang2 = random.randint(0,2)
            
        
        cond = S_condition(abs_pos, rel_pos , length, stress,  ) 
        return cond 


    def generate_condition(self, lang_state, conf_i, candidates, distrib) :
        
        ran = sum(distrib) 
        ind = random.randint(0, ran)
        if ind > distrib[1] :
            return self.generate_P_cond(lang_state, conf_i, candidates) 
        return  self.generate_S_cond( lang_state) 


    def generate_P_change(self, lang_state):
        """
        generates a random P_change

        Parameters
        ----------
        lang_state : language
            The language that will undergo the change

        Returns
        -------
        ch : Change
            DESCRIPTIONthe change we want.

        """
        
        # pick a phonem (target)
        rd = random.randint(0, len(lang_state.phonemes)-1)
        phon = lang_state.phonemes[rd]
        if self.verbose : print(phon)
        
        # generalise, but not always (target-s)
        # TODO Cette généralisation pourra être paramétrisée mieux
        generalize = random.randint(0,1)
        
        if generalize : 
            sub_classes, classe = restrict (phon, lang_state.subclasses[phon])
             
        else : classe = [phon]
        
        
        restrict_generalization = random.randint(0,1)
        
        
        
        # TODO attention à la paramétrisation de ce point
        while len(classe)>13 :
            sub_classes, classe = restrict (phon, sub_classes, classe)
        
        
        if self.verbose : printl(classe)
        target = phon.features.copy()
        for i, ft in enumerate (target ) :
            for phon2 in classe :
                if phon2.features[i] != phon.features[i] :
                    target[i] = -1
        if self.verbose :
            print(target)
            print("survivors")
            print(len(classe))
        
        # we find a change to operate
        conf_i = Configuration()
        conf_f = conf_i.get_output()
        candidates = tpl2candidates(classe, conf_i.state)
        
        while len(candidates) == 0 :
            candidates = tpl2candidates(classe, conf_i.state)
            conf_i = Configuration()
            conf_f = conf_i.get_output()
        
        
        ch = P_change(conf_i, conf_f)
        ch.set_target(target)
        
        
        
        
        
        
        # find a context (conditions)
        
        #TODO parametrize the number and nature of conditions 
        
        c1 = random.randint(0,1)
        c2 = random.randint(0,1)
        c3 = random.randint(0,1) 
        c4 = random.randint(0,1)
        c5 = random.randint(0,1)
        
        nb_cond = c1+c2+c3+c4+c5
        
        for i in range( nb_cond ):
            distrib = [5, 5]
            cond = self.generate_condition(lang_state, conf_i, candidates, distrib)
            ch.add_condition(cond)
        
        
        if self.verbose : print(ch)
        return ch
        
    
        
        
        
        
        
        
        
        
        
        
        

