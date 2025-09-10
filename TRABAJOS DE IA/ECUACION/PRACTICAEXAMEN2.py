# -*- coding: utf-8 -*-
"""
Editor de Spyder
PRACTICA Y = -9X+7
Este es un archivo temporal.
"""

import numpy as np
import pandas as pd


"""
Dataset=pd.read_csv("Dataset_Ecuacion_-9x+7X2.csv")
Dataset=np.array(Dataset)
"""
# Cargar datos desde un archivo Excel
#archivo = "LibroPrueba.csv" 
archivo = "Dataset_Ecuacion_-9x+7X2.csv"  # 
df=pd.read_csv(archivo)

#extraccion de las columnas del excel

x0 = df["x0"].values
#x1 = np.array(x1S,dtype)
#x0 = x0S.astype(float)
x1 = df["x1"].values
x1=np.array(x1)

y = df["y"].values


# Inicialización de pesos W y tasa de aprendizaje alpha
w0, w1 = np.random.rand(2)
W=[[w0 , w1]]
alpha = 0.01

ErroresMedios =[ np.float64("inf")]
Epoca = 0;
while (True):  # Iteramos para mejorar los pesos
    # Cálculo de la salida
    y_pred = w0 * x0 + w1 * x1



    Error = y_pred - y
    if Epoca == 0:
        ErroresMedios[0] =np.mean(Error)

         
    else:
        ErroresMedios.append(np.mean(Error))
        W.append(np.array([w0 , w1]))
    
    # Cálculo del gradiente
    dw0 = np.mean(Error)
    dw1 = np.mean(Error * x1)


    # Actualización de pesos
    w0 -= alpha * dw0
    w1 -= alpha * dw1
    
    Epoca += 1
    if ((dw0< 0.000001 and dw1 <0.000001 and Epoca > 1000) or Epoca > 6000):
        break    
    
    

# Mostrar pesos finales
print(f"Pesos finales: w0 = {w0:.4f}, w1 = {w1:.4f}")

"""
# Función de activación (sigmoide)
def sigmoid(x):
    return 1 / (1 + np.exp(-x))
    y_pred = sigmoid(w1 * x1 + w2 * x2)
    
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

"""
