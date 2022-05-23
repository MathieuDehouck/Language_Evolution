# -*- coding: utf-8 -*-
"""
Created on Fri May 20 11:15:50 2022

@author: 3b13j
"""

from IPA import IPA
from Condition import P_condition
from Configuration import Configuration
from Change import P_change

ipa = IPA()
ift = ipa.features


def encode_f (feat) :
    """
    encode a feature into the format we chose

    Parameters
    ----------
    feat : list
        the feature rpz of a template

    Returns
    -------
    s : str

    """
    
    
    s = ""
    for i in range (len(feat)) :
        if feat[i] == 0 :
            s+= ift[i][0].lower() 
        elif feat[i] >= 1 :
            s+= ift[i][0].upper()
            if feat[i] > 1  : s+= str(feat[i])
            
        elif feat[i] == -1 :
            s+= "?"
        
                   
    return s

def decode_f (string) :
    
    
    decoder = ift
    feature = [-1] *12
    
    for j, char in enumerate(string) : 
        
        for ind, nam in enumerate(decoder) :
            
            if char == nam[0].lower() :
                feature[ind] = 0
                
            elif char == nam[0].upper() : 
                feature[ind] = 1
                
                if j + 1 in range(len(string)) :
                    
                    if string[j+1].isdigit() : feature[ind] = int(string[j+1])
    return feature
            
            
    
def encode_p_change(change) :
    s = ""
    s+= "Target:" + encode_f(change.target) +" "
    s+= "Effect:" + encode_f(change.config_initiale.state)+">"+encode_f(change.config_finale.state) + " "
    for condition in change.conditions :
        s+= "Condition:"+"rp"+str(condition.rel_pos) +encode_f(condition.template) + " "
    return s

def encoded_changes2log(changes, path, rewind = False ):
    rew = "a"
    if rewind: rew = "w"
    f = open(path + "_encoded.txt", rew, encoding = "utf8")
    for change in changes :
        f.write(encode_p_change(change))
        f.write("\n")
    f.close()
    
def decode_log(path, copy_back = False) :
    
    f = open(path + "_encoded.txt", "r", encoding = "utf8") 
    
    copych = []
    j= 0
    for line in f : 
        print(line)
        print(j)
        j = j+1
        chan =  decode_change(line)
        copych.append(chan)
    f.close()
    if copy_back : return 
    
    f2 = open(path + "_encoded_decoded.txt", "w", encoding = "utf8")

    for chain in copych :
        string = encode_p_change(chain) 
        f2.write(string)
        f2.write("\n")
    f2.close()

def decode_change(string) :
    string = string.split()
    
    #target
    str_trg = string[0] 
    if str_trg[0 : 7] != "Target:" :
        print("wrong formed string")
        print(str_trg[0 : 7])
        return
    else :
        trg = P_condition(decode_f(str_trg[7:]))
    
    #effect
    str_eff = string[1] 
    if str_eff[0 : 7] != "Effect:" :
        print("wrong formed string")
        return
    else :
        str_eff = str_eff[7:].split(">")
        ci = Configuration(decode_f(str_eff[0]))
        cf = Configuration(decode_f(str_eff[1]))
    
    change = P_change(ci, cf)
    
    change.set_target(trg)
    print("reste à traiter")
    print(string[2:])
    # conditions
    for cond in string[2:] :
        if cond[0 : 10] != "Condition:" :
            print("wrong formed string")
            print(cond[0 : 10])
            
        else :
            str_cond = cond[10:]
            rp = 0
            #TODO we suppose the max range is 9 and is only one digit
            if str_cond[0:2] == "rp" :
                
                if str_cond[2].isdigit() : 
                    rp = int(str_cond[2])
                    str_cond = str_cond [2:]
                elif str_cond[2] == "-" :
                    rp = int(str_cond[3])
                    str_cond = str_cond [3:]
            
            nc = P_condition(decode_f(str_cond), -1,  rp)    
            
            
            change.add_condition(nc)

            #print(change.conditions[0])
      
            return change
        
    return change
    
    