# -*- coding: utf-8 -*-
"""
Created on Tue May 17 16:02:54 2022

@author: 3b13j
"""
from utilitaries import feature_match
from IPA import IPA
from encoder_decoder import encode_f
from pathlib import Path


ipa = IPA()
ift = ipa.features
ccl = ipa.classes

def tpl2phons(tpl, alph = ipa.phonemes) :
    phons = []
    for phon in ipa.phonemes : 
        if feature_match(tpl, phon.features) : phons.append(phon)
    return phons




        

def target2str (feat):
    s = "Target : "
    s+= encode_f(feat)
    return s 

def create_breviary() :
    folder = Path("phonetic/")
    
    f = open (folder /"breviary.txt", "w", encoding = "utf8")
    f.write ("BREVIARY") 
    f.write("\n")
    f.write("\n")
    f.write("\n")
    f.write("\n")
    f.write ("PHONEMES") 
    f.write("\n")
    f.write("\n")
    for phoneme in ipa.phonemes :
        f.write(str(phoneme))
        f.write("\n")
        f.write(encode_f(phoneme.features))
        f.write("\n")
        f.write("\n")
    f.write("\n")
    f.write("\n")
    f.write ("NATURAL CLASSES") 
    f.write("\n")
    f.write("\n")
    for cl in ipa.dic_class.values() :
        f.write(str(cl))
        f.write("\n")
        f.write(encode_f(cl.template))
        f.write("\n")
        f.write("\n")
        
def effect2str(ci, cf) :
    s = "Effect : " 
    ci = ci.state
    cf = cf.state
    for i in range(len(ci)) :
        
        if ci[i] != -1  :
            if s != "Effect : " : s+= "  &  "
            
            s+= str ( ift[i]) + " : " 
            if cf[i]>ci[i] : s += "+1"
            else : s += "-1" 
    return s
            
            
def cond2str(cond) :
    s = "cond : "
    
    #TODOmake a difference between c cond and p cond. 
    
    
    s+= encode_f(cond.template)
     
    return s

def change2str(change) : 
    print(change)
    s = "Change :  \n "
    # avant target.template
    s+= target2str(change.target) +" " +effect2str(change.config_initiale, change.config_finale) 
    if len(change.conditions)>1 :
        for j in range (1, len(change.conditions))  :
            s+= cond2str (change.conditions[j])
    return s






# functions directly writing in log files




def write_in_log(path, string):
    """ Takes as input the name of a log file and the sentence that it sould add in it"""
    
    folder = Path("logs/")
    path = folder / path
    f = open(path, 'a',  encoding='utf8')
    f.write(string)
    f.write("\n")



def phon2log (phon, path) :
    """
    writes a phoneme in the log format we defined

    Parameters
    ----------
    phon : phoneme to write in the script
        DESCRIPTION.
    path : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    
    folder = Path("logs/")
    path = folder / path
    
    
    f = open (path, "a",encoding='utf8')
    f.write (str(phon.ipa))
    
    f.write("   :  ")
    f.write( phon.description )
    



def change2log (change, path,lang,  print_phons = False) :
    
    
    folder = Path("logs/")
    path = folder / path
    
    
    
    f = open (path, "a",encoding='utf8')
    
    f.write("A change has occured ")
    f.write("\n")
    f.write("\n")
    f.write("\n")
    
    
    for i in range (len (change.config_initiale.state )) :
        value = change.config_initiale.state [i]
        if value != -1 :
            f.write ( "The feature ")
            f.write ( ipa.features[i]) 
            f.write (' switched values from ')
            f.write (str(change.config_initiale.state [i] ))
            f.write (' to ')
            f.write (str(change.config_finale.state [i]))
            f.write("\n")
            f.write("\n")
    f.write("following phonemes were transformed :")
    f.write("\n")
    f.write(change2str(change))
    
    #TODO this version of impacted phonem selects the impacted phonems an und für sich , not the imacted phonems i nthe language
    # we need to access the language and create functions to update it.
    
    if print_phons :
        f.write("\n")
        
        
        phons = set( tpl2phons(change.target, lang.phonemes))
        
        
        cphons = set(tpl2phons(change.target , lang.phonemes) )
        phons = phons & cphons
        
        """
        
        TODO we need to eliminate phonems regarding the condition. 
        simple and lazy solution : only considering the conditions and the target 
        for condition in change.conditions :
            cphons = set(tpl2phons(condition.template , lang.phonemes) )
            phons = phons & cphons
        """    
        f.write('Impacted phonems :')
        for phon in phons :
            f.write(phon.ipa)
            f.write("  ")
        
        
            
            
    f.write("\n")
    f.write("\n")
    
    """
    for phon in change.impacted_phonemes :
        
        f.write (str(phon.ipa))
        
        f.write("   :  ")
        f.write( phon.description )
        
        
        f.write( "   ->   ")
        
        
        
        phon = change.impacted_phonemes[phon]
        
        f.write (str(phon.ipa))
        
        f.write("   :  ")
        f.write( phon.description )
        
        
        
        f.write("\n")
    """
    f.write("\n")
    f.write("\n")
    f.close()
    
    return 
   
def langcomp2log (l1, l2, path) :
    
    folder = Path("logs/")
    path = folder / path
    
   
    f = open (path, "a",encoding='utf8')
    
    f.write("We are going to solemnly compare the evolution between ")
    f.write (l1.name)
    f.write (" and ")
    f.write (l2.name)
    f.write("\n")
    f.write("\n")
    
    for word in l1.voc :
        f.write(l1.voc[word].ipa) 
        f.write ('   ->    ')
        f.write(l2.voc[word].ipa) 
        f.write("\n")
    f.close()
        
    
def lgs2log(liste) :
    
    
    for i in range (len(liste) -1) :
        langcomp2log (liste[0], liste[i+1], "comp_lat_rom.txt")
        langcomp2log (liste[0], liste[i+1], "comp_rom_rom.txt")
        
    
    
    
    
    