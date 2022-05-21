# -*- coding: utf-8 -*-
"""
Created on Thu May  5 15:24:11 2022

@author: 3b13j
"""
from utilitaries import *
from IPA import IPA
from Natural_class import list2class
from Condition import P_condition

hip = IPA()

ph = hip.alphabet
cl = hip.dic_class


# On génère automatiquement un dictionnaire à partir des phonèmes uniques 
phon_conditions = {}
for key in ph.keys():
    locals()[str(key)] = ph[key].features
    
    cond = P_condition (key, ph[key])
    phon_conditions[key] = cond

# On génère automatiquement un dictionnaire à partir des classes naturelles



class_conditions = {}
for key in cl.keys():
    locals()[str(key)] = cl[key]
    
    cond = P_condition (key, cl[key].template)
    class_conditions[key] = cond
    



approximant = list2class ("approximant", lateral.members  + nasales.members + trill.members)
class_conditions["approximant"] = approximant


ds = {}
ds["consonne"] = "C"
ds["voyelle"] = "V"
ds["edge"] = "#"
ds["stress"] = "v"

structure_conditions = {}
for key in ds.keys():
    locals()[str(key)] = ds[key]
    
    cond = P_condition (key, ds[key])
    structure_conditions[key] = cond


"""
printl(class_conditions.values())
printl(phon_conditions.values())
printl(structure_conditions.values())
"""






# functions allowing to test phonetic change


#TODO make the condition a parameter of the following functions to make them reusable

def testeur_abs(wd, change) :
    for i in range(len(wd.phonemes)) :
        change3 = copy.deepcopy(change)
        c3 = class_conditions["sound"]
        c3.set_absol_pos(i)
        change3.add_condition(c3)
        nw = change3.apply_word(wd)
        print(nw)
        return nw
        
        
        
def testeur_rel(wd, chang) :
    for i in range(-len(wd.phonemes),len(wd.phonemes) ) :
        change = copy.deepcopy(chang)
        c = class_conditions["vowells"]
        c.set_rel_pos(i)
        change.add_condition(c)
        nw = change.apply_word(wd)
        print()
        print("relative value : ", i)
        print(nw)
        return nw


