# -*- coding: utf-8 -*-
"""
Created on Sun Jul  3 10:14:01 2022

@author: 3b13j
"""

import matplotlib.pyplot as plt
import numpy as np

f = open("second_phonetic_experiment.csv", "r", encoding = 'utf8')
lines = []
j = 0
for l in f :
    if l.split(",") [0] != "": 
        lines.append(l.replace("\n", "").split(","))

lines = lines [2:]

nb_changes = list(range( 0, 55, 5))


lev1 = [0]
lev2 = [0]
lev3 = [0]
i1 = [1]
i2 = [1]
i3 = [1]
ft1 = [1]
ft2 = [1]
ft3 = [1]

i = 0 

#print(lines)
while 4* i  < len(lines) :
    
    lev1.append(float(lines[4*i+1][9]))
    lev2.append(float(lines[4*i+2][9]))
    lev3.append(float(lines[4*i+3][9]))
    
    
    i1.append(float(lines[4*i+1][6]))
    i2.append(float(lines[4*i+2][6]))
    i3.append(float(lines[4*i+3][6]))
    
    
    ft1.append(float(lines[4*i+1][8]))
    ft2.append(float(lines[4*i+2][8]))
    ft3.append(float(lines[4*i+3][8]))
    i+=1
    
    

plt.figure()
plt.plot(nb_changes, lev1, c='blue', label = "l1 vs mother" , marker = '*')
plt.plot(nb_changes, lev2, c='red', label = "l2 vs mother", marker = '*')
plt.plot(nb_changes, lev3, c='green', label = "l1 vs l2", marker = '*')



plt.title('Edit distance')
plt.xlabel('nb of change')
plt.ylabel('ditance value')
plt.legend()

plt.show()




plt.figure()
plt.plot(nb_changes, ft1, c='blue', label = "l1 vs mother" , marker = '*')
plt.plot(nb_changes, ft2, c='red', label = "l2 vs mother", marker = '*')
plt.plot(nb_changes, ft3, c='green', label = "l1 vs l2", marker = '*')



plt.title('Feature match')
plt.xlabel('nb of change')
plt.ylabel('feature siilarity (%)')
plt.legend()

plt.show()



plt.figure()
plt.plot(nb_changes, i1, c='blue', label = "l1 vs mother" , marker = '*')
plt.plot(nb_changes, i2, c='red', label = "l2 vs mother", marker = '*')
plt.plot(nb_changes, i3, c='green', label = "l1 vs l2", marker = '*')



plt.title('Inventory similarity')
plt.xlabel('nb of change')
plt.ylabel('inventory siilarity (%)')
plt.legend()

plt.show()


