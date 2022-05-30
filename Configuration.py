# -*- coding: utf-8 -*-
"""
Created on Thu May  5 10:29:21 2022

@author: 3b13j
"""

import random

maxC = [11, 1, 1, 1, 1, 2, 1, 1 , 1 , 1]
maxV = [2, 6, 1 , 1 , 1]

class Configuration (object) :
    """
    A class to represent an abstract configuration of features

    ...

    Attributes
    ----------
    state : list
        representation of the features involved 
    nn : list
        list on non wildcards indexes

    Methods
    -------
    
    __init__() : classical constructor
       
    """
    
    def __init__(self, target , random = True) :
        
            
           
            if random : state = Configuration.random_mono(target )

            
            else : state = target
            self.state = state   
            nn = []
            for index, val in enumerate (self.state) : 
               if val  > -1 :
                    nn.append(index)
            self.nn = nn
            self.isV = (len (self.state)   < 7   )
            
        
    def random_mono(target) : 
        """
        help to generate a random configuration with a non wildcarded feature

        Returns
        -------
        state : list
            the random built state
        """
        
        
        if len(target)  == 5 :
            
            state = [-1 ] * 5
            index = random.randint(0, 4)
            
        
        else :  
            
            state = [-1 ] * 10
            index = random.randint(0, 9)
    
        
       
        state[index] =  target[index]
        return state
    
    
    
    
    
    def __str__(self) :
         return str(self.state)

        


    
    def get_output(self) :
        """
        Returns
        -------
        A new Configuration object with just one feature modified

        """
        print("STATE")
        state_fin = self.state.copy()
        #TODO peut être paramétré
        
            
        if self.isV : m = maxV 
        else : m = maxC
            
        for i , el in  enumerate(state_fin ): 
        
         el = int(el)
         
         if el != -1 :
            
            if m[i] == 1 :
                
                if state_fin[i] == 1 : state_fin[i] = 0 
                else : state_fin[i] = 1
            
            else :
                augmenter = bool (random.randint(0,1))
                
                if augmenter and  state_fin[i] < m[i] : state_fin[i] += 1
                elif state_fin[i]>0 : state_fin[i] -= 1 
        
        return Configuration(state_fin, False)
                    
                

        

        
