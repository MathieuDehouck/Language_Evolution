# -*- coding: utf-8 -*-
"""
Created on Tue May 17 16:02:54 2022

@author: 3b13j

Contains some side methods to write the state of some objects and describe the execution of the program  in log files
"""

from utilitaries import feature_indices
from encoder_decoder import encode_f
from pathlib import Path
from Effect import Effect
from IPA import IPA
from Change import P_change , S_change, M_change

ipa = IPA.get_IPA()
ift = ipa.cfeatures
#TODO
#ccl = ipa.classes

        



def target2str (feat):
    """
    Encode the target of a change to write it latter in the log

    Parameters
    ----------
    feat : list 
        description of a feature template

    
    -------
    s : qtring describing it 
    
    """
    s = "Target : "
    s+= encode_f(feat)
    return s 





def create_breviary() :
    """
    Creates a user friendly document that describes all the natural classes that exist with regard to the
    IPA we use at the heart of the program""

    """
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
        
        



# functions directly writing in log files





def write_in_log(path, string):
    """ 
    Takes as input the name of a log file and the sentence that it sould add in it
    """    
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
        
    path : str 
        path to the target file

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
    """
    folder = Path("logs/")
    path = folder / path
    f = open (path, "a",encoding='utf8')   
    
    
    if liste != [] :
        f.write("EXAMPLES")
        f.write (" \n  \n")
        for loop in range(min(n, len(liste))) :
            f.write (str(liste[loop][0]) + "  >  "+str( liste[loop][1]) +" \n" )
    else : f.write ("The branch we study is the one that was not impacted by the change")
    
        
        
        
        
def changes2machinelog(path, change)     :
    folder = Path("logs/")
    path = folder / path
    f = open (path, "a",encoding='utf8')   
    f.write(change.encode_change())
    f.write("\n")
    f.close()
        
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
    """
    Writes a description of a change into a log file

    Parameters
    ----------
    change : Change
    path : str
    lang : Language
    print_phons : TYPE, optional
        DESCRIPTION. The default is True.
    i : TYPE, optional
        DESCRIPTION. The default is 0.
    """
    folder = Path("logs/")
    path = folder / path
    f = open (path, "a",encoding='utf8')
    
    if i != 0 : 
        if i != 1 : 
            f.write("\n")
            f.write("\n")
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
    
    if type(change) == P_change : 
        f.write("\n")
        f.write("The phonemes matching the following target were modified  : \n ")
        f.write(str(change.target))
        f.write("\n")
        
        
        
        idx  = feature_indices(change.target)
        target_vow = (len(idx) == 5)
        
        #RUSTINE, a implementer pour M
        if type(change.effect) == Effect : 
          for key, values in change.effect.effect.items() :
            
            if key != values :
            
                if target_vow : feat_semantics = ipa.vfeatures
                else : feat_semantics = ipa.cfeatures
            
                f.write ( "The feature ")
                
                
                f.write ( str(feat_semantics[change.effect.domain[0]][change.effect.domain[1]])) 
                # For the manner of articulation , it is possible that the result is in fact a tuple 
                f.write (' switched values from ')
                f.write (str(key))
                f.write (' to ')
                f.write (str(values))
                f.write("\n")
        
        f.write("\n")
        
        if print_phons :
            f.write("\n")
            f.write('Impacted phonems :')
            
            for phon in change.impacted_phonemes :
                f.write("\n")
                f.write(phon[1]) 
                f.write(" > ")
                f.write(change.impacted_phonemes[phon][1])
            f.write("\n")
    
    elif type(change) == M_change : 
        f.write("\n")
        f.write("The phonemes matching the following target suffered a metathesis  : \n ")
        f.write(str(change.target))
        f.write("\n")
        f.write("switching position with a phoneme displaying a different value for feature ")
        
        idx  = feature_indices(change.target)
        target_vow = (len(idx) == 5)
        if target_vow : feat_semantics = ipa.vfeatures
        else : feat_semantics = ipa.cfeatures
        f.write ( str(feat_semantics[change.effect[0]][change.effect[1]])) 
        f.write("\n")
        f.write("\n")
        
        
        
    elif type(change) == S_change : 
        f.write("\n")
        f.write("The syllables with a configuration   : \n ")
        f.write(str(change.config_initiale))
        f.write("\n")
        f.write("moved to a new configuration  ")
        f.write(str(change.config_finale))
        
    
    f.write("\n")
    f.write("\n")
    f.close()
    

    
   
    
def langcomp2log (l1, l2, path) :
    """
    Comapres the vobulary of two languages and writes the comparison in a log (subfunction used to trace the evolution between two language state)
    BE CAREFUL, we expect the two languages to be related / at least to have the same voc size for this operation to make sense.

    Parameters
    ----------
    l1 : Language
    
    l2 :Language
    
    path : str
        path to destination file
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
    print the evolution of a language step by step. 

    Parameters
    ----------
    liste : list of languages where the i+1 th element is the result of the evolution of the ith
    """
    for i in range (len(liste) -1) :
        langcomp2log (liste[0], liste[i+1], "comp_lat_rom.txt")
        langcomp2log (liste[i], liste[i+1], "comp_rom_rom.txt")
        
    
    
    
    
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


def languages_2_log(language, path, rewind = False) :
    """ store a language in a log file """
    if rewind  : 
        f = open(path, 'w', encoding = 'utf8')
    else : 
        f = open(path, 'a', encoding = 'utf8')
    
    for key, value in language.voc.items() :
        f.write(key)
        f.write("   ")
        f.write(value.ipa)
        f.write("\n")
    
    f.write("\n")
    f.write("\n")

    
    
    
    
def evolution_2_log(changer, path) :
    """ stores all the cognates in a log"""
    
    f = open(path, 'w', encoding = 'utf8')
    
    lvs = changer.tree.get_leaves() 
    
    root  = changer.tree.language
    
    
    for key, value in root.voc.items() :
        f.write("original word : ")
        f.write("\n")
        f.write(str(key))
        f.write("\n")
        f.write(str(value.ipa))
        f.write("\n")
        f.write("\n")
        form_list = []
        for lf in lvs : 
            if lf.language.voc[key].ipa not in form_list :
                form_list.append(lf.language.voc[key].ipa)
        for form in form_list : 
            f.write(str(form))
            f.write("\n")
        f.write("\n")
        f.write("\n")
    
    
    
    