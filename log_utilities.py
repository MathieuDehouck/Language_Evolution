# -*- coding: utf-8 -*-
"""
Created on Tue May 17 16:02:54 2022

@author: 3b13j
"""
from utilitaries import feature_match, feature_indices, tpl_2_candidates
from IPA import IPA
from encoder_decoder import encode_f
from pathlib import Path



ipa = IPA()
ift = ipa.cfeatures
#TODO
#ccl = ipa.classes

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
    
    
    
    

def samples2log(path, liste, n =10 ) : 
    """
    Method that writes down only some of the words modified by a change. 

    Parameters
    ----------
    path : str
        path to the file you want tp write in.
    liste : list of changed words :
    n : int, optional
        number of words that will be printed. The default is 10.

    Returns
    -------
    None.

    """

    
    folder = Path("logs/")
    path = folder / path
    f = open (path, "a",encoding='utf8')   
    f.write("EXAMPLES")
    f.write (" \n  \n")
    for loop in range(min(n, len(liste))) :
        f.write (str(liste[loop][0]) + "  >  "+str( liste[loop][1]) +" \n" )
        
        
        
        
        
        
def purge_log(path) :
    """
    Clears a log file

    Parameters
    ----------
    path : 

    Returns
    -------
    None.

    """
    folder = Path("logs/")
    path = folder / path
    f = open(path, 'w')
    f.close()



def change2log (change, path,lang,  print_phons = True, i = 0 ) :
    
    
    folder = Path("logs/")
    path = folder / path
    
    
    
    f = open (path, "a",encoding='utf8')
    
    if i != 0 : 
        f.write("CHANGE N°")
        f.write(str(i))
    f.write("\n")
    f.write("\n")
    
    if len(change.conditions) != 0 : 
        f.write ( "If the following conditions were satisfied :  ")
        f.write("\n")
        for cond in change.conditions : 
          f.write(str(cond))  
          f.write("\n")
    
    
    f.write("\n")
    f.write("The phonemes matching the followin target were modified  : \n ")
    f.write(str(change.target))
    f.write("\n")
    
    idx  = feature_indices(change.target)
    target_vow = (len(idx) == 5)
    
    for key, values in change.effect.effect.items() :
        
            if target_vow : feat_semantics = ipa.vfeatures
            else : feat_semantics = ipa.cfeatures
        
            f.write ( "The feature ")
            f.write ( str(feat_semantics[key[0]][key[1]])) 
            # For the manner of articulation , it is possible that the result is in fact a tuple 
            f.write (' switched values from ')
            f.write (str(values[0]))
            f.write (' to ')
            f.write (str(values[1]))
            f.write("\n")
    
    #f.write(str(change))
    f.write("\n")
    
    
   
    
    #TODO this version of impacted phonem selects the impacted phonems an und für sich , not the imacted phonems i nthe language
    # we need to access the language and create functions to update it.
    

    
    
    if print_phons :
        f.write("\n")
        phons = tpl_2_candidates(lang, change.target)
        
    
        f.write('Impacted phonems :')
        
        for phon in phons :
            
            new_phon = change.just_transform(phon)
            
            f.write(phon.ipa) 
            f.write(" > ")
            f.write(new_phon.ipa)
            f.write("\n")
        
            
            
    f.write("\n")
    f.write("\n")
    
    f.write("\n")
    f.write("\n")
    f.close()
    
    return 
   
    
   
    
   
    
   
def langcomp2log (l1, l2, path) :
    """
    Comapres the vobulary of two languages and writes it in a log (subfunction used to trace the evolution between two language state)
    

    Parameters
    ----------
    l1 : Language
    
    l2 :Language
    
    path : str
        path to destination file

    Returns
    -------
    None.

    """
    
    
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
    """
    I honestly currently forgot what it did

    Parameters
    ----------
    liste : ?

    Returns
    -------
    None.

    """
    
    
    for i in range (len(liste) -1) :
        langcomp2log (liste[0], liste[i+1], "comp_lat_rom.txt")
        langcomp2log (liste[0], liste[i+1], "comp_rom_rom.txt")
        
    
    
    
    
    
def extract_changed_words(path, write = False) :
    """
    Analyses a dictionnary log and extracts only the words that were changed.
    
    The function the can if the user wants it write the modified words at the end of the same document

    Parameters
    ----------
    path : str
        path to the file
        
    write : bool
        Does the user want to write down the modified words at the end of the document ?

    Returns
    -------
    chg_wds :list 

    """
    
    folder = Path("logs/")
    path = folder / path
    chg_wds = []
    
    f = open(path, 'r', encoding = 'utf8')
    
    for line in f :
        line = line.split() 
        print(line)
        if len(line) == 3 : 
            if line[0] != line[2] : chg_wds .append(line[2])
   
    if write :
        
        f = open(path, 'a', encoding = 'utf8')
        f.write("\n")
        f.write("\n")
        f.write("CHANGED WORDS ; ")
        f.write("\n")
        f.write("\n")
        for wd in chg_wds : 
            
            f.write (wd)
            f.write("  ;  ")
        
    f.close()
    return chg_wds
    
    
    