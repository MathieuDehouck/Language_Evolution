# -*- coding: utf-8 -*-
"""
Created on Fri May 20 11:15:50 2022

@author: 3b13j
"""

from IPA import IPA



ipa = IPA()
ift = ipa.cfeatures
#TODO 

manner_2_letter  =  { (0, 0, 0, 0, 0) : 'a', # approximant
                (1, 0, 0, 0, 0) :  'n' ,  # nasal
                (0, 1, 0, 0, 0) : 'p', # plosive
                (0, 0, 1, 0, 0) : 's', # fricative / sibilant
                (0, 0, 0, 1, 0) : 'f', # flap
                (0, 0, 0, 2, 0) : 't', # trill
                (0, 0, 0, 0, 1) : 'l', # lateral
                (0, 0, 1, 0, 1) : 'F', # lateral fric
                (0, 0, 0, 1, 1) : 'T',# lateral trill
                (0, 1, 1, 0, 0) : 'A' }  #Africates


letter_2_manner = {}
for key, value in manner_2_letter.items() : letter_2_manner[value] = key













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
        s = "V:"
        semantics =  ( 'Height','Backness', 'Round'), ('Voiced', 'Nasal')
        
    else : 
        s = "C:"
        semantics = ('place of articulation', 'manner of articulation', 'Voiced'), ('secondary place of articulation', 'nasal' , 'aspiration')
        
        
    for i , tp in enumerate (feat) :
        for j, el  in enumerate(tp) :
            

            if type(el)== tuple : el = manner_2_letter[el]
            
            if type(el)== int :
                if el == -1 : 
                    el = "*"
                    
            s+= semantics[i][j][0].upper()
            s+= str(el) # +" "
        
    return s



def dt(string, x) :
    # for decoding trick
    if string[x] =='*' : return-1
    if string[x].isnumeric() : return int(string[x])
    

def decode_f (string) :
    """
    Decode a string we encoded earlier

    Parameters
    ----------
    string : to be decoded


    """
   
    
    string = string.split(":") 
    if string[0] == "V" : 
        decoder  =  ( 'Height','Backness', 'Round'), ('Voiced', 'Nasal') 
        string = string[1]
        
        tupl1 = (dt(string, 1), dt(string, 3), dt(string, 5))
        tupl2 = (dt(string, 7), dt(string, 9))
        
    
    
    
    else : 
        decoder = ('place of articulation', 'manner of articulation', 'Voiced'), ('secondary place of articulation', 'nasal' , 'aspiration')
        string = string[1]
       
        dec = 0
        if string[1] == '*' : place = -1
        else :
            if string[2].isnumeric() :
                dec = 1
                place = int(string[1:3])
            else : place = int(string[1])
        print(dec)
        if string[3+dec] == "*" : manner = -1
        else : manner = letter_2_manner[string[3+dec]]
        
        
        if string[7+dec] == '*' : sec_place = -1
        else :
            if string[8+dec].isnumeric() :
                sec_place = int(string[7+dec : 9 +dec])
                dec += 1
            else : sec_place = int(string[7+dec])
        
        
        
        print(string)
        tupl1 = (place, manner, dt(string,5+dec))
        tupl2 = (  dt(string,7+dec),  dt(string,9+dec),  dt(string,11+dec)) 
   
            
    tupl = (tupl1, tupl2)
    return tupl
    
    
    
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

"""    
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
"""
