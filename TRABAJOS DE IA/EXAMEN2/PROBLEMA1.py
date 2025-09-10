# -*- coding: utf-8 -*-
"""
Created on Fri May 16 19:46:57 2025
PROBLEMA 1 Y= 5 + 5X1 + 4X2 + 3X3
@author: uriel
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


"""
Dataset=pd.read_csv("Dataset_Ecuacion_-9x+7X2.csv")
Dataset=np.array(Dataset)
"""
# Cargar datos desde un archivo Excel
#archivo = "LibroPrueba.csv" 
archivo = "PROBLEMA1_5+5X1+4X2+3X3.csv"  # 
df=pd.read_csv(archivo)
dfA = df[0:150]
dfT = df[150:200]
#extraccion de las columnas del excel
"""
x0 = dfA["x0"].values
x1 = dfA["x1"].values
x2 = dfA["x2"].values
x3 = dfA["x3"].values
y = dfA["y"].values
"""
x0 = np.random.randint(0,10,200)
x1 = np.random.randint(0,10,200)
x2 = np.random.randint(0,10,200)
x3 = np.random.randint(0,10,200)

y= (5*x0) + (5*x1) + (4*x2) + (3*x3)


x0T = dfT["x0"].values
x1T = dfT["x1"].values
x2T = dfT["x2"].values
x3T = dfT["x3"].values
yT = dfT["y"].values


# Inicialización de pesos W y tasa de aprendizaje alpha
w0, w1,w2,w3 = np.random.rand(4)

W=[[w0, w1,w2,w3]]
alpha = 0.0051

ErroresMedios =[ np.float64("inf")]
Epoca = 0;
while (True):  # Iteramos para mejorar los pesos
    # Cálculo de la salida
    y_pred = (w0*x0) + (w1*x1) + (w2*x2) + (w3*x3)


    Error = y_pred - y
    if Epoca == 0:
        ErroresMedios[0] =np.mean(Error)

         
    else:
        ErroresMedios.append(np.mean(Error))
        W.append(np.array([w0 , w1]))
    
    # Cálculo del gradiente
    dw0 = np.mean(Error)
    dw1 = np.mean(Error * x1)
    dw2 = np.mean(Error * x2)
    dw3 = np.mean(Error * x3)


    # Actualización de pesos
    w0 -= alpha * dw0
    w1 -= alpha * dw1
    w2 -= alpha * dw2
    w3 -= alpha * dw3
    
    Epoca += 1

    if ((abs(dw0)< 0.00000001 and abs(dw1) <0.00000001 and abs(dw2) <0.00000001 and abs(dw2) <0.00000001 and Epoca > 1000) ):
        break    
    

    y_prueba = (w0*x0T) + (w1*x1T) + (w2*x2T) + (w3*x3T)
    Error_Prueba = y_prueba - yT

# Mostrar pesos finales
print(f"Pesos finales: w0 = {w0:.4f}, w1 = {w1:.4f},w2 = {w2:.4f},w3 = {w3:.4f}")
Error_cuadratico = np.power(ErroresMedios,2)
plt.plot(Error_cuadratico)

# Añadir título y etiquetas a los ejes
plt.title("Gráfico de datos")
plt.xlabel("Índice")
plt.ylabel("Valor")
