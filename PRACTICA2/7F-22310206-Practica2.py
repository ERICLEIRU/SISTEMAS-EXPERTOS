# -*- coding: utf-8 -*-
"""
Created on Thu Sep 11 12:01:36 2025
Practica 2: chatbot sencillo con modulo de adquisicion de conocimiento
@author: uriel
"""

import json
import os

# Cargar base de conocimiento
if os.path.exists("conocimiento.json"):
    with open("conocimiento.json", "r") as f:
        conocimiento = json.load(f)
else:
    conocimiento = {}

# Chat loop

salir = False        
print("Hola, para terminer el programa escribe salir.")
    
while not salir:
    pregunta = input("Tú: ")
    pregunta = pregunta.strip().casefold()

    if pregunta == "salir" or pregunta == "adios":
        salir = True
    if pregunta in conocimiento:
        print("Bot:", conocimiento[pregunta])
    else:
        print("Bot: No sé la respuesta. ¿Me la enseñas?")
        respuesta = input("Tú (respuesta): ")
        conocimiento[pregunta] = respuesta
        with open("conocimiento.json", "w") as f:
            json.dump(conocimiento, f)
        print("Bot: ¡Gracias! He aprendido algo nuevo.")
