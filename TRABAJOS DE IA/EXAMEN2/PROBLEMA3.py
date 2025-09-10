# -*- coding: utf-8 -*-
"""
Created on Sat May 17 15:55:14 2025

@author: uriel
"""
import matplotlib.pyplot as plt
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
        if nombre == "Iris-setosa":
            y.append(0)
        else:
            y.append(1)
    return y
    
#extraccion de variables para aprendixaje A y testeo T
archivo = "iris.data"  # 
df=pd.read_csv(archivo)
df = np.array(df)
df = df[0:98,:]

x1 = df[:,0]
x1A1 = x1[0:40]
x1A2 = x1[49:89]
x1A = np.concatenate((x1A1, x1A2))
x1A = x1A.astype(float)

x1T1 = x1[40:49]
x1T2 = x1[89:98]
x1T = np.concatenate((x1T1, x1T2))
x1T = x1T.astype(float)

x2 = df[:,1]
x2A1 = x2[0:40]
x2A2 = x2[49:89]
x2A = np.concatenate((x2A1, x2A2))
x2A = x2A.astype(float)

x2T1 = x2[40:49]
x2T2 = x2[89:98]
x2T = np.concatenate((x2T1, x2T2))
x2T = x2T.astype(float)

x3 = df[:,2]
x3A1 = x3[0:40]
x3A2 = x3[49:89]
x3A = np.concatenate((x3A1, x3A2))
x3A = x3A.astype(float)

x3T1 = x3[40:49]
x3T2 = x3[89:98]
x3T = np.concatenate((x3T1, x3T2))
x3T = x3T.astype(float)

yS = df[:,4]

#Cambio de los nombres por 0 y 1
y = Cambio_string_num (yS)

yA1 = y[0:40]
yA2 = y[49:89]
yA = np.concatenate((yA1, yA2))
yT1 = y[40:49]
yT2 = y[89:98]
yT = np.concatenate((yT1, yT2))



# Inicialización de pesos W y tasa de aprendizaje alpha
w0, w1,w2,w3 = np.random.rand(4)

alpha = 0.5

ErroresMediosCuadraticos =[ np.float64("inf")]
Epoca = 0;

while (True):  # Iteramos para mejorar los pesos
    # Cálculo de la salida
    y_pred = sigmoid(w0 + w1 * x1A + w2 * x2A + w3 * x3A)



    Error = y_pred - yA

    # Cálculo del gradiente
    dw0 = np.mean(Error)
    dw1 = np.mean(Error * sigmoid_derivada( x1A))
    dw2 = np.mean(Error * sigmoid_derivada( x2A))
    dw3 = np.mean(Error * sigmoid_derivada( x3A))


    # Actualización de pesos
    w0 -= alpha * dw0
    w1 -= alpha * dw1
    w2 -= alpha * dw2
    w3 -= alpha * dw3
    
    Error_al_cuadrado = np.power(Error,2)
    if Epoca == 0:
        
        ErroresMediosCuadraticos[0] =np.mean( Error_al_cuadrado)
         
    else:
        ErroresMediosCuadraticos.append(np.mean( Error_al_cuadrado))

    
    Epoca += 1
    if ((dw0< 0.00001 and dw1 <0.00001 and Epoca > 1000) or Epoca > 80000):
        break  
    
#prueba

W=[[w0 , w1, w2, w3]]
y_prueba = sigmoid(w0 + w1 * x1T + w2 * x2T + w3 * x3T)

"""
plt.plot(ErroresMediosCuadraticos)

# Añadir título y etiquetas a los ejes
plt.title("Gráfico Erroes cuadraticos medios de epoca ")
plt.xlabel("Epocas")
plt.ylabel("Error")
"""

# Configuración de barras
x = np.arange(len(yT))
ancho = 0.4

# Crear la gráfica
plt.bar(x - ancho/2, y_prueba, width=ancho, label='COMPROBACION', color='blue')
plt.bar(x + ancho/2, yT, width=ancho, label='REFERENCIA', color='red')

plt.ylabel('Valores')
plt.title('Comparación de SALIDA EN TESTEO')
plt.legend()
plt.show()

