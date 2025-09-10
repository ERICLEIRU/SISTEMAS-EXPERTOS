# -*- coding: utf-8 -*-
"""
Created on Thu Mar 13 19:57:19 2025

@author: uriel
"""

import numpy as np

m1 = np.zeros((3,4))
#[filas][columnas]


def ReinasColumnas (m):
    
    M = m.copy()
    longColumnas = len(m)
    longFilas = int( m.size/longColumnas)


    columna = {}
    columna[1] =0
    k = 1

    while( k >0 and k <= longFilas):
        columna[k] = columna[k]+1
        ciclo = True    
        while ((columna[k] <= longColumnas) and (k > 1) and ciclo ):
            ciclo = False
            #condiciones
            for x in columna:
                dif = k - x
                EvaDiagoInf = False
                EvaDiagoInf = (columna[k-dif] == (columna[k] + dif))
                EvaDiagoSup = False
                EvaDiagoSup = (columna[k-dif] == (columna[k] - dif))
                EvaFila = False
                EvaFila = (columna[x] == columna[k]) 
                
                if ((x < k) and (EvaDiagoInf or EvaDiagoSup or EvaFila)):
                    columna[k] = columna[k] + 1
                    ciclo = True
                    
                
                    
        if columna[k] > longColumnas:
            k = k-1
            
        else:
            k = k+1
            if k <= longFilas:
                columna[k] = 0
                
    if k < 1:
        resultado = (False,columna, m )
        
    else:
        for x in columna:
            M[(columna[x]-1)][x - 1] = 1
        
        resultado = (True,columna, M)
    
    return resultado



reinas = ReinasColumnas(m1)

"""
longColumnas = len(m)
longFilas = int( m.size/longColumnas)


columna = {}
columna[1] =0
k = 1

while( k >0 and k <= longFilas):
    columna[k] = columna[k]+1
    ciclo = True    
    while ((columna[k] <= longColumnas) and (k > 1) and ciclo ):
        ciclo = False
        #condiciones
        for x in columna:
            dif = k - x
            EvaDiagoInf = False
            EvaDiagoInf = (columna[k-dif] == (columna[k] + dif))
            EvaDiagoSup = False
            EvaDiagoSup = (columna[k-dif] == (columna[k] - dif))
            EvaFila = False
            EvaFila = (columna[x] == columna[k]) 
            
            if ((x < k) and (EvaDiagoInf or EvaDiagoSup or EvaFila)):
                columna[k] = columna[k] + 1
                ciclo = True
                
            
                
    if columna[k] > longColumnas:
        k = k-1
        
    else:
        k = k+1
        if k <= longFilas:
            columna[k] = 0
            
if k < 1:
    resultado = (False, m )
    
else:
    for x in columna:
        m[(columna[x]-1)][x - 1] = 1
    
    resultado = (True,m)

"""        
        

           
       
    