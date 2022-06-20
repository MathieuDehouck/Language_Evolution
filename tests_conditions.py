# -*- coding: utf-8 -*-
"""
Created on Thu Jun  2 14:22:59 2022

@author: 3b13j
"""


from utilitaries import *
from IPA import IPA 
from Wiki_utilities import get_language

from P_change_generator import Baby_P_change_generator

from Effect import Effect
from Condition import P_condition
from Change import S_change, P_change, M_change
from Effect import  Effect
from Condition import S_condition

i = IPA.get_IPA()




lang = get_language("latin_classique.txt", "latin")

"""

wd = lang.voc['virdia']

wd2 = lang.voc['tripaliare']

wd3 = lang.voc['sapere']

target = wd2.phonemes[3].features

target_cong =  wd2.phonemes[2].features


cond = P_condition(target_cong, -1, -1)


effect = Effect((0,2 ), {0:1})




print("you the change that I want")
ch = P_change(target, effect)

print(ch)


nw = ch.apply_word(wd2)
print(nw)
nw = ch.apply_word(wd3)
print(nw)




print("we add a condition")
ch.add_condition(cond)

print(ch)

nw = ch.apply_word(wd2)
print(nw)
nw = ch.apply_word(wd3)
print(nw)


l2, chw = ch.apply_language(lang) 
print(chw)


print("we add another condition")

ch = P_change(target, effect)

target_cong =  wd2.phonemes[0].features


cond = P_condition(target_cong, 0, 0)

ch.add_condition(cond)


print("WD2", wd2)
print(ch)

nw = ch.apply_word(wd2)
print(nw)
print()
nw = ch.apply_word(wd3)
print(nw)


print(wd2)
print(wd3)

ch = P_change(target, effect)
cond = S_condition(42, 0, False, True, None)
ch.add_condition(cond)

nw = ch.apply_word(wd2)
print(nw)
print()
nw = ch.apply_word(wd3)
print(nw)



#PB 


wd = lang.voc["deiformis"]


target = ((4, 2, 0), (-1, -1)) 



target_cong = ((7, (0, 1, 0, 0, 0), 1), (0, 0, 0))


cond = P_condition(target_cong, -1, -1)


effect = Effect(target)
effect.add_effect( (0,1) , (2,1))

change = P_change(target, effect)
nwd = change.apply_word(wd)
print(nwd)



change.add_condition(cond)





nwd = change.apply_word(wd)
print(nwd)

condi = change.conditions[0]

condi.test(wd, 1, True)







lang = get_language("latin_classique.txt", "latin")

wd = lang.voc['virdia']

wd2 = lang.voc['tripaliare']

wd3 = lang.voc['sapere']

target = wd2.phonemes[3].features

target_cong =  wd2.phonemes[2].features


cond = P_condition(target_cong, -1, -1)










sop = lang.voc["Sophocle"]
ft = ((-1, -1, -1), (-1, -1, 0))
ch = M_change(ft, (1,2), [])



nlang, cw = ch.apply_language(lang)

print(cw)

print()

s=ch.encode_change()
print(s)


chc = M_change.decode_change(s)
print(chc)
print(ch)







bb = Baby_P_change_generator()





ch3 = bb.generate_M_change(lang)

nl, wc = ch3.apply_language(lang)

print(wc)
"""



ch4 = S_change([True, False, None], [True, True, None] )
#printd(lang.voc)
l2, cw = ch4.apply_language(lang)
#printd(l2.voc)
for wd in cw : 
    print(wd[0], "=>" ,wd[1])
    
s = ch4.encode_change()
c = S_change.decode_change(s)