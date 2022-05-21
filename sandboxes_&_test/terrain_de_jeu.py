# -*- coding: utf-8 -*-
"""
Created on Thu May  5 14:49:40 2022

@author: 3b13j
"""

from usual_changes import *
from global_script import * 
from configuration import *
from change import *

latin = get_language('latin_classique.txt')







dic2 = latin.voc
zu = dic2["virdia"]

"""
print(zu)
printl(zu.syllables[0].phonemes)



print(zu.__dict__)
z = zu.syllables[0] 
print(z.__dict__)





i = latin.dic_phonemes['i']
print(i)




conf = configuration_mono() 
print(conf)
print(conf.nn)
conf2 = conf.get_output() 
print(conf2)
print()

change = phonetic_change (conf, conf2)





rd = configuration_mono( [-1	 ,-1	,-1	,-1	,-1	,0	,-1	,-1, -1	,-1	,-1	,-1	,-1])
print(rd)
rdf = rd.get_output()
print(rdf)


change = phonetic_change (rd, rdf)
print()
print("before : ",i)
i2 = change.apply(i)
print("ci", change.config_initiale.state)
print("cf", change.config_finale.state)
print("before : ",i)
print("after : " ,i2)


print(zu)
zu = change.apply_word(zu)
print(zu)
z = zu.syllables[0] 
print(z)
#printd(latin.voc)
"""
change = aspiration

proto_roman = change.apply_language(latin)


#printl(latin.voc.keys())


#printl(proto_roman.voc.values())
hip  = IPA()
#printl(hip.classes)

a = get_phon("i")
print(a)



a = back.apply(a)
print(a)

i = rounding.apply(a)
print(i)

print(zu)


printd(latin.voc)


from usual_changes import *
from usual_conditions import *


phon = hip.alphabet["f"]
print(phon)

print(trillisation)

#phon2 = trillisation.apply(phon)



phon2 = hip.alphabet["m"]
print(phon)

print(lateralization)

#pho = lateralization.apply(phon)

#print(class_conditions)

#lateralization.add_cond(class_conditions["nasales"])
#Bug possible : que le conditionnement s'applique à tout 

p = lateralization.apply(phon2)
print(p)
#print(lateralization)


#Test de tous les changements possibles sur un mot
path = "exp_zu_with_unconditionned_change.txt"

log = ["EXPERIENCE : EVOLUTION DE VIRDIA ", " "]

print(zu)


for change in cg :
    zu2 = change.apply_word(zu)
    log.append(str(change))
    log.append(str(zu2))
    log.append(" ")

for string in log :
    write_in_log(path, string)


#plus ambitieux :
    
path = "neo_latins.txt"

log = ["EXPERIENCE : EVOLUTION DU GAFFIOT ", " "]
for word in latin.voc.values() :
    for change in cg :
        zu2 = change.apply_word(word)
        log.append(str(change))
        log.append(str(zu2))
        log.append(" ")
    

    

for string in log :
    write_in_log(path, string)

