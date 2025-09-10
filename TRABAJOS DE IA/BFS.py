# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 19:44:16 2025

BUSQUEDA A LO ANCHO

@author: 22310206
"""

G = {"a":["b","c","g"],"b":["a","d","g"],"c":["a","e","d"],"d":["b","f","c"],
     "e":["c","f","g"],"f":["e","d","h"],"g":["a","e","b"],"h":["f"]}

V1 = "a"
Vp = [V1]
Ep = []
S = [V1]
Sd = []
V = list(G.keys())
Vd = V.copy()
Vd.remove(V1)

for x in V: 
    for y in Vd:
        if y in G[x]: 
            if y in Vd:    
                Ep.append((x,y))
                Vp.append(y)
                Sd.append(y)  
        
    S = Sd.copy()
    Sd = []
    for i in range(len(S)):
        Vd.remove(S[i])  
     
T = (Vp,Ep)