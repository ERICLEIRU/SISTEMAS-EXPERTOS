# -*- coding: utf-8 -*-
"""
Created on Fri May 16 21:11:38 2025
simulacion de compuerta XOR
@author: uriel
"""

import matplotlib.pyplot as plt
import numpy as np


X2 = np.array([0 , 0 , 1, 1])
X1 = np.array([0 , 1 , 0, 1])
X0 = np.array([1 , 1 , 1, 1])
X = np.column_stack((X0, X1))
X = np.column_stack((X, X2))
y = np.array([[0], [1], [1], [0]])  # Salida esperada


alpha = 0.5  # Tasa de aprendizaje

tamaño = X.size
largo = len(X)
entradas = int (tamaño/largo)


# Pesos para dos capas 
W1 = np.random.randn(entradas, 3)  
W2 = np.random.randn(3, 1)


def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivada(x):
    return  sigmoid(x) / (1 + sigmoid(x))

ErroresMedios =[ np.float64("inf")]
Epoca = 0;
while (True):
# Entrenamiento del perceptrón
#for Epocas in range(50000):
   
    Z1 = np.dot(X, W1)  
    A1 = sigmoid(Z1)  
    Z2 = np.dot(A1, W2) 
    A2 = sigmoid(Z2)  

    # Cálculo del error
    error = y - A2
    dA2 = error * sigmoid_derivada(A2)  # Gradiente de salida
    dW2 = np.dot(A1.T, dA2)  # Ajuste de pesos capa de salida

    dA1 = np.dot(dA2, W2.T) * sigmoid_derivada(A1)  # Gradiente de capa oculta
    dW1 = np.dot(X.T, dA1)  # Ajuste de pesos capa oculta

    # Actualización de pesos
    W1 += alpha * dW1
    W2 += alpha * dW2
    
    if Epoca == 0:
        ErroresMedios[0] =np.mean(error)

         
    else:
        ErroresMedios.append(np.mean(error))
    
    ErrorSum = np.sum(error)

    Epoca += 1
    
    if ( abs(ErrorSum) < 0.0000001 or Epoca > 50000):
        break
    

# Prueba del modelo
for i in range(len(X)):
    Z1 = np.dot(X[i], W1)
    A1 = sigmoid(Z1)
    Z2 = np.dot(A1, W2)
    A2 = sigmoid(Z2)
    print(f"Entrada: {X[i]} -> Salida predicha: {round(A2[0])}")
    
Error_cuadratico = np.power(ErroresMedios,2)
plt.plot(Error_cuadratico)

# Añadir título y etiquetas a los ejes
plt.title("Gráfico Erroes cuadraticos medios de epoca ")
plt.xlabel("Epocas")
plt.ylabel("Error")

