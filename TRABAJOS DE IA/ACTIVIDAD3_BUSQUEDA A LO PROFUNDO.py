# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 19:17:36 2025

BUSQUEDA A PROFUNDIDAD DFS
@author: uriel
"""

Gra = {"a":["b","c","g"],"b":["a","d","g"],"c":["a","d","e"],"d":["b","c","f"],
     "e":["c","f","g"],"f":["d","e","h"],"g":["a","b","e"],"h":["f"]}

Raiz = "a"




def DFS (G,V1):
    Vp = [V1]
    Ep = []
    w = V1
    inicio = True
    while(inicio):
        
        ciclo = True
        while(ciclo):
            ciclo = False
            for x in G[w]:
                if not x in Vp:
                    Vp.append(x)
                    Ep.append((w,x))
                    w=x
                    ciclo = True  #Se creo un ciclo para T
                    break
                else:
                    continue
         #ciclo para retroceder w  a su padre       
        while(True):
            Ubi = Vp.index(w)
            w = Vp[Ubi - 1]
            """Valoracion de si los datos en VP no estan dentro de G[W]
                para salir del ciclo"""
            if not all (val in Vp for val in G[w]): #
                break
            if w == V1:
                inicio = False
                break

    T = (Vp,Ep)
    
    return T

        
T= DFS(Gra, Raiz)
print(T)    