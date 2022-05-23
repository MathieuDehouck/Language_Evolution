"""
to fill
"""
import random
from wiki_utilities import get_language 
latin = get_language('latin_classique.txt', "latin")
from utilitaries import printl, feature_match,  tpl2candidates
from Configuration import Configuration
from Condition import P_condition 
from Change import P_change


        


class Change_Generator():


    def __init__(self, verbose = False):
        self.verbose = verbose

    def generate_cond(self, lang_state, conf_i, candidates):
        direction= random.randint(0,1) 
        if direction == 0 : direction = -1 
        
        rel_pos = random.randint(1, 5)
        
        continu = random. randint(0,1)
        
        cond = P_condition.constrained_rd_condition( conf_i , direction*rel_pos, -1, continu)
        
        candidates2 = tpl2candidates(candidates, cond.template)
        
        while len(candidates ) == 0 :
            candidates2 = tpl2candidates(candidates, cond.template)
            cond = P_condition.constrained_rd_condition( conf_i , direction*rel_pos, -1, continu)
           
        return cond
        
        
        

    def generate_p_change(self, lang_state):
        
        # pick a phonem (target)
        rd = random.randint(0, len(lang_state.phonemes)-1)
        phon = lang_state.phonemes[rd]
        if self.verbose : print(phon)
        
        # generalise, but not always (target-s)
        # TODO Cette généralisation pourra être paramétrisée mieux
        generalize = random.randint(0,1)
        if generalize : 
            sub_classes = lang_state.subclasses[phon]
            rd = random.randint(0, len(sub_classes)-1)
            classe = sub_classes[rd]
        else : classe = [phon]
         
        
        restrict_generalization = random.randint(0,2) 
        if generalize and  not restrict_generalization :
            if self.verbose : print ("restriction")
            rd = random.randint(0, len(sub_classes)-1)
            classe2 = sub_classes[rd]
            classe = list ( set(classe ) .intersection( set( classe2)))
        
        if self.verbose : printl(classe)
        target = phon.features.copy()
        for i, ft in enumerate (target ) :
            for phon2 in classe :
                if phon2.features[i] != phon.features[i] :
                    target[i] = -1
        if self.verbose : print(target)
        
        
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
            cond = self.generate_cond(lang_state, conf_i, candidates)
            ch.add_condition(cond)
        
        
        if self.verbose : print(ch)
        return ch
        
        # find a plausible resolution (result)
        ()
        
        
        
        
        
        
        
        
        

cg = Change_Generator() 
cg.generate_p_change(latin)