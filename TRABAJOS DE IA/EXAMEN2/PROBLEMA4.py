# -*- coding: utf-8 -*-
"""
Created on Sat May 17 17:31:28 2025

@author: uriel
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

#extraccion de variables para aprendixaje A y testeo T
archivo = "drug_consumption.data"  # 
df1=pd.read_csv(archivo)
df = np.array(df1)
df = df[0:1000,:]

x1 = df[:,1]
x1A1 = x1[0:40]
x1A2 = x1[49:1000]
x1A = np.concatenate((x1A1, x1A2))
x1A = x1A.astype(float)

x1T1 = x1[40:49]
x1T2 = x1[400:460]
x1T = np.concatenate((x1T1, x1T2))
x1T = x1T.astype(float)

x2 = df[:,2]
x2A1 = x2[0:40]
x2A2 = x2[49:1000]
x2A = np.concatenate((x2A1, x2A2))
x2A = x2A.astype(float)

x2T1 = x2[40:49]
x2T2 = x2[400:460]
x2T = np.concatenate((x2T1, x2T2))
x2T = x2T.astype(float)

x3 = df[:,3]
x3A1 = x3[0:40]
x3A2 = x3[49:1000]
x3A = np.concatenate((x3A1, x3A2))
x3A = x3A.astype(float)

x3T1 = x3[40:49]
x3T2 = x3[400:460]
x3T = np.concatenate((x3T1, x3T2))
x3T = x3T.astype(float)

x4 = df[:,4]
x4A1 = x4[0:40]
x4A2 = x4[49:1000]
x4A = np.concatenate((x4A1, x4A2))
x4A = x4A.astype(float)

x4T1 = x4[40:49]
x4T2 = x4[400:460]
x4T = np.concatenate((x3T1, x3T2))
x4T = x4T.astype(float)

y = df[:,12]

yA1 = y[0:40]
yA2 = y[49:1000]
yA = np.concatenate((yA1, yA2))
yT1 = y[40:49]
yT2 = y[400:460]
yT = np.concatenate((yT1, yT2))

w0, w1,w2,w3, w4 = np.random.rand(5)

alpha = 1

ErroresMediosCuadraticos =[ np.float64("inf")]
Epoca = 0;

while (True):  # Iteramos para mejorar los pesos
    # Cálculo de la salida
    y_pred = w0 + w1 * x1A + w2 * x2A + w3 * x3A +w4 * x4A



    Error = y_pred - yA

    # Cálculo del gradiente
    dw0 = np.mean(Error)
    dw1 = np.mean(Error * x1A)
    dw2 = np.mean(Error * x2A)
    dw3 = np.mean(Error * x3A)
    dw4 = np.mean(Error * x4A)


    # Actualización de pesos
    w0 -= alpha * dw0
    w1 -= alpha * dw1
    w2 -= alpha * dw2
    w3 -= alpha * dw3
    w4 -= alpha * dw4
    
    Error_al_cuadrado = np.power(Error,2)
    if Epoca == 0:
        
        ErroresMediosCuadraticos[0] =np.mean( Error_al_cuadrado)
         
    else:
        ErroresMediosCuadraticos.append(np.mean( Error_al_cuadrado))

    
    Epoca += 1
    if ( Epoca > 150000):
        break  
    
#prueba

W=[[w0 , w1, w2, w3, w4]]
y_prueba = w0 + w1 * x1T + w2 * x2T + w3 * x3T + w4 * x4T

x = np.arange(len(yT))
ancho = 0.4

"""
plt.plot(ErroresMediosCuadraticos)
# Añadir título y etiquetas a los ejes
plt.title("Gráfico Erroes cuadraticos medios de epoca ")
plt.xlabel("Epocas")
plt.ylabel("Error")
"""

# Crear la gráfica
plt.bar(x - ancho/2, y_prueba, width=ancho, label='COMPROBACION', color='blue')
plt.bar(x + ancho/2, yT, width=ancho, label='REFERENCIA', color='red')

plt.ylabel('Valores')
plt.title('Comparación de SALIDA EN TESTEO')
plt.legend()
plt.show()
