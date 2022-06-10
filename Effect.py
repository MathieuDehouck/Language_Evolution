# -*- coding: utf-8 -*-
"""
Created on Wed Jun  1 09:55:33 2022

@author: 3b13j
"""



from encoder_decoder import letter_2_manner, manner_2_letter




class Effect (object) :
    """
    A class representing the effect of a change
    
    The effect is encoded as a dictionnary, taking as key the index of the feature to be modified, and
    as value a couple [initial value, new value]
    This representation will allow to modelize cyclic change. 
    
    An effect could be built using a target
    
    ...

    Attributes
    ----------
    target  : (optionnal ) tuple
        a feature pattern representing the phonemes the change can be applied to
    
    Methods
    -------
    __init__() constructor taking all these information as input
    

    random_effect 
    
    """
#TODO éliminer add effect et gérer ailleurs (dans le générateur) 
    def __init__(self, domain, effect)  :
      
       # self.isV = (len(self.idx) == 5)
        self.domain = domain
        self.effect = effect
        

    def __str__(self) : 
        s =  " index of the modified feature :" + str(self.domain) + " old  value : " + str(list(self.effect.keys()))+ "new value : "+  str( list(self.effect.values()))
        return s
    
        
    def __eq__(self, other) :
        return self.domain == other.domain and self.effect == other.effect
    

    def affect(self, phoneme):
        key = [phoneme.features[x][y] for (x,y) in self.domain]
        values = self.effect[key]
        kvs = {k:v for (k, v) in zip((self.domain, values))}

        fts = []
        for x, fs in enumerate(phoneme.features):
            fts.append([])
            for y, v in enumerate(fs):
                if (x,y) in kvs:
                    fts[-1].append(kvs[x, y])
                else:
                    fts[-1].append(v)
            fts[-1] = tuple(fts[-1])

        return tuple(fts)


    
    def encode_e(self):
        
        
        #TODO histoire des manners
   
        s = ""
        for key, value in self.effect.items() :
            s += str(self.domain)
            s+= ":"
            if type(key) == tuple  :
                s+= manner_2_letter[key]
            else  : s += str(key)
            
            s += ">"   
            
            if  type(value) == tuple:
                s+=   manner_2_letter[value]
            else :  s+= str(value)
            s += " | "
        
        return s
    
            
    def decode_e(string) :
        
        effect ={}
        
        string = string.split(":")
        
        st =  [int(string[0][1]) ] +[int(string[0][4])]
        domain = tuple(st)
        
        string = string[1].split(" | ")
        for sub in string :
            if len(sub)>0 :
                sub = sub.split(">")
                if sub[0].isnumeric() : sub[0] = int(sub[0])
                else : sub[0] = letter_2_manner[sub[0]]
                if sub[1].isnumeric() : sub[1] = int(sub[1])
                else : sub[1] = letter_2_manner[sub[1]]
                effect[sub[0]] = sub[1]
            
        
            
        return Effect(domain, effect)

