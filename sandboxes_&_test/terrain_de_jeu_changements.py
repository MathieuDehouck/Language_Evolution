# -*- coding: utf-8 -*-
"""
Created on Mon May 16 11:47:28 2022

@author: 3b13j
"""

from usual_changes import *
from global_script import * 
from configuration import *
from change import *
import copy

latin = get_language('latin_classique.txt')







dic2 = latin.voc
zu = dic2["virdia"]
print(zu)



print(nasalisation)


zu2 = nasalisation.apply_word(zu)
print(zu2)


change = copy.deepcopy(nasalisation)
change2 = copy.deepcopy(nasalisation)

for i in range(len(zu.phonemes)) :
    print(zu.phonemes[i])
    print(zu2.phonemes[i])
    print()
    
print(zu2)


from  usual_conditions import *

c1 = class_conditions["consonnes"]
c2 = class_conditions["plosives"]

change.add_condition(c1)
change2.add_condition(c2)
print(change)

zu3 = change.apply_word(zu)
print(zu3)


zu4 = change2.apply_word(zu)
print(zu4)


change3 = copy.deepcopy(nasalisation)
c3 = class_conditions["sound"]
c3.set_absol_pos(1)
change3.add_condition(c3)
zu5 = change3.apply_word(zu)
print(zu5)

def testeur_abs(wd) :
    for i in range(len(wd.phonemes)) :
        change3 = copy.deepcopy(nasalisation)
        c3 = class_conditions["sound"]
        c3.set_absol_pos(i)
        change3.add_condition(c3)
        zu5 = change3.apply_word(zu)
        print(zu5)
        
testeur_abs(zu)






change4 = copy.deepcopy(nasalisation)
c4 = class_conditions["vowells"]
c4.set_rel_pos(6)
#change4.add_condition(c4)
zu6 = change4.apply_word(zu)
print(zu6)



testeur_rel(zu, nasalisation)



print()
print("zu7")
print()

change5 = copy.deepcopy(nasalisation)
c5 = class_conditions["trill"]
c5.set_rel_pos(-1)
c5.set_continu(True)
change5.add_condition(c5)
zu7 = change5.apply_word(zu)
print(zu7)






change6 = copy.deepcopy(nasalisation)
c6 = s_condition("accent", None, True)
print()
print(c6)
change6.add_condition(c6) 


zu8 = change6.apply_word(zu)
print(zu8)


change7 = s_change( [True, True], [True, True], [])
print(change7)
zu9 = change7.apply_word(zu)
print(zu9)























"""
hip  = IPA()



from usual_changes import *
from usual_conditions import *
"""
