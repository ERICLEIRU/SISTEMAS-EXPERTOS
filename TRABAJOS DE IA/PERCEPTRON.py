# -*- coding: utf-8 -*-
"""
Created on Fri Apr  4 19:26:42 2025

PERCEPTRON
COMPOSICION DE FUNCIONES

recordar agregar error para monitorear
@author: uriel
"""

import numpy as np

X0 = np.array([1 , 1 , 1, 1])
X1 = np.array([-1 , 1 , -1, 1])
X2 = np.array([1 , -1 , -1, 1])

Y = np.array([-1 , -1 , -1, 1])

W = np.array([1,1,1])
A = 0.5 # taza de aprendizaje 
Eold = np.float64("inf")
while(True):
    age = 1
    for n in range(len(X0)):
        X =np.array([X0[n],X1[n],X2[n]])
        YE = np.sign(np.dot(W,X))
        Enew = Y[n] - YE
        W = W+((A)*(Enew)*X)
        
    age +=1
    
    if Enew == 0:
        print("Se logro")
        break
    elif(Enew == Eold):
        print("no se logro, error no cambio")
        break
    print(Enew ," " ,Eold)   
    Eold = Enew
    
#Prueba
print("X0 X1  X2  Y  YE  Prueba")
for n in range(len(X0)):
    X =np.array([X0[n],X1[n],X2[n]])
    YE = np.sign(np.dot(W,X))
    YE = int(YE)
    P = Y[n] == YE
    print(X0[n],X1[n],X2[n],Y[n],YE,P)
    


