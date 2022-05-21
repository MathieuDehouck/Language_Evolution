# -*- coding: utf-8 -*-
"""
Created on Thu May  5 10:29:21 2022

@author: 3b13j
"""

import random



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
    
    def __init__(self, state = None) :
        
        
            if state == None :
                state = Configuration.random_mono()
            self.state = state   
            nn = []
            for index, val in enumerate (self.state) : 
               if val  > -1 :
                    nn.append(index)
            self.nn = nn
            
            
        
    def random_mono() : 
        """
        help to generate a random configuration with a non wildcarded feature

        Returns
        -------
        state : list
            the random built state
        """
        
        state = [-1 ] * 12
        index = random.randint(0, 11)
        maxi = 1
        if index == 2 or index == 3 :
            maxi = 3
        #TODO modify here if we make round a discrete feature too
        val = random.randint(0, maxi)
        state[index] =  val
        return state
    
    
    
    def __str__(self) :
         return str(self.state)

        
    
    def get_output(self) :
        """
        Returns
        -------
        A new Configuration object with just one feature modified

        """

        nstate = self.state.copy()
        if self.nn == 2 or self.nn == 3 :
            # here we modify in one sense or in another the value of the discrete feature to obtain a
            # final config.
            # TODO treat round as a discrete one
            augmenter = random.randint(0, 1)
            if augmenter == 0 : augmenter = False
            else : augmenter == True
        
            if augmenter :
                if  nstate[self.nn] < 3 :  nstate[self.nn] += 1 
            else : 
               if  nstate[self.nn] > 0 :  nstate[self.nn] -= 1 
            
            # for boolean feature we just have to switch the value
        else :
            index = random.randint(0,len(self.nn)-1)
            if nstate[self.nn[index]] == 0 :
                nstate[self.nn[index]] = 1
            else : nstate[self.nn[index]] = 0
        return Configuration(nstate)


        

        
