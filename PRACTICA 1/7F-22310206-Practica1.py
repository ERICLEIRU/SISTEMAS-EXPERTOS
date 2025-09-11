# -*- coding: utf-8 -*-
"""
Created on Thu Sep 11 08:53:22 2025
PRACTICA 1: APLICACION EN LA VIDA DIARIA

@author: uriel
"""

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# -----------------------------
#Datos de las materias por nombre, tipo (investigacion o problemas) y las horas que han requerido
# -----------------------------
data = {
    "Materia": [
        "Amplificadores","Amplificadores","Amplificadores","Amplificadores",
        "SI","SI","SI",
        "Calidad","Calidad","Calidad",
        "Control","Control","Control",
        "MicroRobotica","MicroRobotica","MicroRobotica","MicroRobotica",
        "Proyecto","Proyecto","Proyecto","Proyecto"
    ],
    "Tipo": [0,1,0,0,
             0,1,1,
             1,1,1,
             0,0,0,
             1,0,0,0,
             0,0,0,1],  # 0 = problemas, 1 = investigación
    "TiempoFinal": [2,3.2,2.5,2.3,
                    1.5,1.7,1.6,
                    2,2.7,2.4,
                    5.0,5.0,6.2,
                    3.0,1,1.2,0.9,
                    3.1,2.6,2.9,6.2]
}

df = pd.DataFrame(data)

# Variables de entrada y salida
X = df[["Materia", "Tipo"]]
y = df["TiempoFinal"]

# -----------------------------
# 2. Crear el preprocesador
# -----------------------------
preprocessor = ColumnTransformer(
    transformers=[
        ("materia", OneHotEncoder(), ["Materia"])
    ],
    remainder="passthrough"
)

# -----------------------------
# 3. Crear el pipeline
# -----------------------------
pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("regressor", LinearRegression())
])

# Entrenar el modelo
pipeline.fit(X, y)

# -----------------------------
# 4. Hacer predicciones
# -----------------------------
nuevas_tareas = pd.DataFrame({
    "Materia": ["Control", "Proyecto", "SI"],
    "Tipo": [0, 1, 0]
})

predicciones = pipeline.predict(nuevas_tareas)

print("Predicciones de tiempo (en horas):")
for tarea, tiempo in zip(nuevas_tareas.to_dict(orient="records"), predicciones):
    print(f"{tarea} → {tiempo:.2f} horas")