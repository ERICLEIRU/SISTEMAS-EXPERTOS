# -*- coding: utf-8 -*-
"""
Created on Sat May 17 20:06:51 2025
PROBLEMA4 con la libreria sklearn
@author: uriel
"""
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Cargar el archivo
df = pd.read_csv("drug_consumption.data")  # O pd.read_excel("datos.xlsx")

# Selección de características
X = df.iloc[:, 1:5]  # Todas las columnas menos la última
y = df.iloc[:, 12]   # Última columna como salida

# División en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.01, random_state=42)

# Inicialización del modelo
modelo = LinearRegression()

# Simulación de entrenamiento por épocas
epochs = 10000
errors = []

for epoch in range(epochs):
    modelo.fit(X_train, y_train)  # Entrenamiento en cada época
    y_pred = modelo.predict(X_test)
    error = mean_squared_error(y_test, y_pred)
    errors.append(error)
    print(f"Época {epoch + 1}: Error cuadrático medio = {error:.4f}")

# Gráfica del error por épocas
plt.plot(range(1, epochs + 1), errors, marker='o', linestyle='-', color='blue')
plt.xlabel("Época")
plt.ylabel("Error cuadrático medio (MSE)")
plt.title("Evolución del error cuadrático medio por épocas")
plt.show()

# Gráfica de comparación entre valores reales y predichos
x = np.arange(len(y_test))
ancho = 0.4
plt.bar(x - ancho/2, y_pred, width=ancho, label='COMPROBACION', color='blue')
plt.bar(x + ancho/2, y_test, width=ancho, label='REFERENCIA', color='red')
plt.ylabel('Valores')
plt.title('Comparación de SALIDA EN TESTEO')
plt.legend()
plt.show()

