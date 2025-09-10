# -*- coding: utf-8 -*-
"""
Created on Thu Mar 13 14:19:23 2025

DIJKSTRA
@author: uriel
"""

GDist = {"a":{"b":2,"f":1},
           "b":{"a":2,"c":2,"d":2,"e":4},
           "c":{"b":2,"e":3,"z":1},
           "d":{"b":2,"f":3,"e":4},
           "e":{"b":4,"c":3,"d":4,"g":7},
           "f":{"a":1,"d":3,"g":5},
           "g":{"f":5,"e":7,"z":6},
           "z":{"c":1,"g":6}}

Start = "a"
End = "z"

def DKSTRA (GraDist,StartPoint,EndPoint):
    #T es el conjunot de todos los vertices que no se han evaluado desde Starpoint
    T = list(GraDist.keys())
    #Creacion de la lista con los infnitos
    L = {}
    for x in T:
        L[x] = float('inf')  
    L[StartPoint]=0
    Ruta = []


    while ( EndPoint in T):
        #Encontrar el vector con el L[v] minimo
        min = float('inf')
        for v in T:
            if min >= L[v]:
                min = L[v]
                Vmin = v
        T.remove(Vmin)        

        #encontrar los abyacentes minimos y sustituir
        for x in GraDist[Vmin]:
            if x in T:
                if L[x] > (L[Vmin]+GraDist[Vmin][x]):
                    L[x]= (L[Vmin]+GraDist[Vmin][x])
        
      #Generar Ruta 
    RetroPoint = EndPoint
    Ruta.append(RetroPoint)
    minRuta = min

    while(RetroPoint != StartPoint):
        for x in GraDist[RetroPoint]:
            if L[x] == (minRuta - GraDist[RetroPoint][x]):

                Ruta.append(x)
                minRuta = (minRuta - GraDist[RetroPoint][x])
                RetroPoint = x
                
                break
            
    Ruta.reverse()
    
    RutaDistmin = (Ruta,min)
    
    return RutaDistmin
   
    
RutaDistmin = DKSTRA(GDist, Start, End)
    


"""
#T es el conjunot de todos los vertices que no se han evaluado desde Starpoint
T = list(GraDist.keys())
#Creacion de la lista con los infnitos
L = {}
for x in T:
    L[x] = float('inf')  
L[StartPoint]=0
Ruta = []


while ( EndPoint in T):
    #Encontrar el vector con el L[v] minimo
    min = float('inf')
    for v in T:
        if min >= L[v]:
            min = L[v]
            Vmin = v
    T.remove(Vmin)        

    #encontrar los abyacentes minimos y sustituir
    for x in GraDist[Vmin]:
        if x in T:
            if L[x] > (L[Vmin]+GraDist[Vmin][x]):
                L[x]= (L[Vmin]+GraDist[Vmin][x])
    
  #Generar Ruta 
RetroPoint = EndPoint
Ruta.append(RetroPoint)   

while(RetroPoint != StartPoint):
    for x in GraDist[RetroPoint]:
        if L[x] == (min - GraDist[RetroPoint][x]):

            Ruta.append(x)
            min = (min - GraDist[RetroPoint][x])
            RetroPoint = x
            
            break
        
Ruta.reverse()
    
"""








   
        
        
        
        
        
    