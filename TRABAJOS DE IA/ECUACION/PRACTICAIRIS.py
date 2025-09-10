# -*- coding: utf-8 -*-
"""
Created on Fri May 16 18:30:40 2025
PRUEBA EXAMEN IRIS
@author: uriel
"""

import numpy as np
import pandas as pd

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivada(x):
    return  sigmoid(x) / (1 + sigmoid(x))

#funcion para asignar valor de Setosa com 1 y versicolor como 0
def Cambio_string_num (yS):
    y = []
    for nombre in yS:
        if nombre == "Setosa":
            y.append(0)
        else:
            y.append(1)
    return y
    


archivo = "iris.csv"  # 
df=pd.read_csv(archivo)

#extraccion de variables para aprendixaje A y testeo T
x1 = df["sepal.length"].values
x1A1 = x1[0:40]
x1A2 = x1[50:90]
x1A = np.concatenate((x1A1, x1A2))


x1T1 = x1[40:50]
x1T2 = x1[90:100]
x1T = np.concatenate((x1T1, x1T2))


x2 = df["sepal.width"].values
x2A1 = x2[0:40]
x2A2 = x2[50:90]
x2A = np.concatenate((x2A1, x2A2))


x2T1 = x2[40:50]
x2T2 = x2[90:100]
x2T = np.concatenate((x2T1, x2T2))

yS = df["variety"].values

#Cambio de los nombres por 0 y 1
y = Cambio_string_num (yS)

yA1 = y[0:40]
yA2 = y[50:90]
yA = np.concatenate((yA1, yA2))
yT1 = y[40:50]
yT2 = y[90:100]
yT = np.concatenate((yT1, yT2))



# Inicialización de pesos W y tasa de aprendizaje alpha
w0, w1,w2 = np.random.rand(3)
W=[[w0 , w1, w2]]
alpha = 5

ErroresMedios =[ np.float64("inf")]
Epoca = 0;


while (True):  # Iteramos para mejorar los pesos
    # Cálculo de la salida
    y_pred = sigmoid(w0 + w1 * x1A + w2 * x2A)



    Error = y_pred - yA

    # Cálculo del gradiente
    dw0 = np.mean(Error)
    dw1 = np.mean(Error * sigmoid_derivada( x1A))
    dw2 = np.mean(Error * sigmoid_derivada( x2A))


    # Actualización de pesos
    w0 -= alpha * dw0
    w1 -= alpha * dw1
    w2 -= alpha * dw2
    
    if Epoca == 0:
        ErroresMedios[0] =np.mean(Error)
         
    else:
        ErroresMedios.append(np.mean(Error))
        W.append(np.array([w0 , w1, w2]))
    
    Epoca += 1
    if ((dw0< 0.000001 and dw1 <0.000001 and Epoca > 1000) or Epoca > 45000):
        break  
    
#prueba

y_prueba = sigmoid(w0 + w1 * x1T + w2 * x2T)





