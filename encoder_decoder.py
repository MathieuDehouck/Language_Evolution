# -*- coding: utf-8 -*-
"""
Created on Fri May 20 11:15:50 2022

@author: 3b13j
"""

from IPA import IPA
from Condition import P_condition
from Change import P_change

ipa = IPA()
ift = ipa.cfeatures
#TODO 


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
    
    
    if len(feat[1]) == 2  :
        s = "V: "
        semantics =  ( 'Height','Backness', 'Round'), ('Voiced', 'Nasal')
        
    else : 
        s = "C: "
        semantics = ('place of articulation', 'manner of articulation', 'Voiced'), ('secondary place of articulation', 'nasal' , 'aspiration')
        
        
    for i , tp in enumerate (feat) :
        for j, el  in enumerate(tp) :
            #TODO faire plus rafiné pour manner
            if type(el)== int :
                if el == -1 : 
                    s+= "*"
                    break
            s+= semantics[i][j][0].upper()
            s+= str(el) + " "
        
    return s





def decode_f (string) :
    """
    Decode a string we encoded earlier

    Parameters
    ----------
    string : to be decoded


    """
    string = string.split(":") 
    if string[0] == "V" : decoder  =  ( 'Height','Backness', 'Round'), ('Voiced', 'Nasal')
    else : decoder = ('place of articulation', 'manner of articulation', 'Voiced'), ('secondary place of articulation', 'nasal' , 'aspiration')
    
    string = string[1]
    
    string =  string.replace(' ','')
    
    
    dic = {}
    for i, letter in enumerate (string) :
        if i == len(string)-1 : break
        if string[i+1] == '(' :
            for j, let in enumerate (string) : 
                if string[j]== ')'  : 
                    break
            
            
            tupl = tuple [int(i+1) : int(j+1)]
            #tupl = tuple (el for el in tupl)
            dic[letter] = tupl
            #for h in range (i, j-1) :
              #  string = string.replace(string[i], "")
            
        else :
            chiffre = ""
            for  k in range (i+1, len(string)-1) :
                if string[k].isdigit() : 
                    chiffre += string[k]
                
                else : 
                    print("oops", k, string[k])
                    break
                if chiffre != "" : dic[letter] =  chiffre
            
    # check if str is int to end encoding. *
    return dic
    """
    feature = tuple() 
    for i,  tpl in enumerate(decoder) :
        part = tuple()
        for j, ft in enumerate(tpl) :
            lettre = j[0].upper() 
            if lettre in non_wild :
                for sub in string : 
                    if sub[0] == lettre : part += sub[1:]
            else : 
                part += -1
        feature += part
    return feature
            
    
    """
    
    
def encode_p_change(change) :
    s = ""
    s+= "Target:" + encode_f(change.target) +" "
    s+= "Effect:" + encode_f(change.config_initiale.state)+">"+encode_f(change.config_finale.state) + " "
    for condition in change.conditions :
        s+= "Condition:"+"rp"+str(condition)
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
        
    change = P_change()
    
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
    
    