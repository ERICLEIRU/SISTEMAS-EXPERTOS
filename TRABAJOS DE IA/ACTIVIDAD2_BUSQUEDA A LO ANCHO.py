# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 15:36:00 2025
Busqueda a lo ancho, grafos
@author: uriel
"""


Gra = {"a":["b","c","g"],"b":["a","d","g"],"c":["a","e","d"],"d":["b","f","c"],
     "e":["c","f","g"],"f":["e","d","h"],"g":["a","e","b"],"h":["f"]}

Raiz = "h"
#Definiendo BFS como función, recibe G = Grago y V1 raiz 

def BFS (G,V1):
    

    Vp = [V1]
    Ep = []  #lista para nuestras aristas
    S = [V1]
    Sd = []
    V = list(G.keys()) # obteniendo los vertices de nuestro arbol (grafo)
    Vd = V.copy() #copia de nuestras aristas
    Vd.remove(V1) #se remueve nuestra raiz
    Vt=Vd.copy() 
    
    
    while True:
        
        for x in S: 
            for y in Vt:
                if y in G[x]:     
                    Ep.append((x,y)) #almacenaje de las aristas
                    Vp.append(y) # Se agrega el vertice en conexion 
                    Sd.append(y)   
                    Vd.remove(y)
                Vt=Vd.copy() #actualizacion de VT para el ciclo
        if Sd==[]:
            
            break
        S = Sd.copy()
        Sd=[]
        T = (Vp,Ep)
    return T
   
    
   
T= BFS(Gra, Raiz)
print(T)
    