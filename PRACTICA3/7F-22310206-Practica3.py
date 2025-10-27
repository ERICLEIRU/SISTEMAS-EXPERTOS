# -*- coding: utf-8 -*-
"""
Created on Mon Oct 8 12:00:55 2025

@author: uriel
"""
"""
mi_lista = [4, 2, 7, 2, 5, 4, 1]

# Eliminar duplicados y ordenar
lista_limpia = sorted(set(mi_lista))

print(lista_limpia)  # Resultado: [1, 2, 4, 5, 7]

"""

import json
import os
import tkinter as tk
from tkinter import messagebox


pregunta = None
historial = None
ventana = None


def guardar_respuesta():
    # Obtener texto del Entry
    respuesta = entrada.get().strip().casefold()
    
    # Actualizar la estructura de datos
    global SiCaract, huesos
    SiCaract = sorted(set(SiCaract))
    huesos[respuesta] = SiCaract
    
    # Guardar en archivo JSON
    with open("huesos.json", "w") as f:
        json.dump(huesos, f, indent=4)
    
    # Mostrar mensaje en ventana
    messagebox.showinfo("Aprendizaje", "¡Gracias! He aprendido algo nuevo.")
    ventana.destroy()  # cerrar la ventana después de guardar


def boton_SI():
    global pregunta
    pregunta ='s'
    ventana.destroy()

def boton_NO():
   global pregunta
   pregunta='n'
   ventana.destroy()

def Ventana_pregunta(CARACTERISTICA_pregunta):
    # Crear ventana
    global ventana
    global historial
    ventana = tk.Tk()
    ventana.title("Ejemplo con historial en ventana")
    ancho = len(CARACTERISTICA_pregunta) * 8
    alto = 150
    
    # Obtener dimensiones de la pantalla
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    
    # Calcular coordenadas para centrar
    x = (pantalla_ancho // 2) - (ancho // 2)
    y = (pantalla_alto // 2) - (alto // 2)
    
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

    
    # Variable de texto que se actualizará
    historial = tk.StringVar()
    historial.set(CARACTERISTICA_pregunta)
    
    # Etiqueta que muestra el historial
    label = tk.Label(ventana, textvariable=historial, justify="left", anchor="w")
    label.pack(pady=10)
    
    # Botones
    btn1 = tk.Button(ventana, text="SI", command=boton_SI)
    btn1.pack(pady=5)
    
    btn2 = tk.Button(ventana, text="NO", command=boton_NO)
    btn2.pack(pady=5)
    
    # Inicia el loop de eventos
    ventana.mainloop()
    

while(True):
        
    #lista de caracteristicas deseada, no deseadas y opciones
    SiCaract=[]
    NoCaract=[]
    NoseCarct=[]
    opciones=[]
    
    
    
    # Cargar base de conocimiento y caracteristicas
    if os.path.exists("huesos.json"):
        with open("huesos.json", "r") as f:
            huesos = json.load(f)
    else:
        huesos = {}
    # Cargar base de conocimiento y caracteristicas
    if os.path.exists("caracteristicas.json"):
        with open("caracteristicas.json", "r") as f:
            caracteristicas = json.load(f)
    else:
        caracteristicas = {}
    
    #evaluacion y seleccion de pregunta inicial
    mitadHuesos = int( len(huesos)/2)
    
    cantCaract = [0]*(len(caracteristicas)+1)
    
    for clave in huesos:
        for caract in huesos[clave]:
            cantCaract[caract]= cantCaract[caract]+1
    
    P=1
    diffMenor = float('inf')
    ValorDiffMenor = P
    
    while(P<=len(caracteristicas)):
        
        cantCaract[P]=abs( cantCaract[P]-mitadHuesos)
        if cantCaract[P]==0:
            break
        if cantCaract[P]<diffMenor:
            diffMenor=cantCaract[P]
            ValorDiffMenor = P
            
        P= P+1
        
    PCarat = str(ValorDiffMenor)
    #pregunta inicial
    pregunta = 'x'
    Ventana_pregunta("Tu hueso " + caracteristicas[PCarat] + "?") 
    if pregunta == 'x':
        break
    """
    print("¿Tu hueso ", caracteristicas[PCarat],'?')
        
    pregunta = input("S para si o N para no: ")
    pregunta = pregunta.strip().casefold()
    """
    
    if pregunta== 's':
        SiCaract.append(ValorDiffMenor)
     
    else:
        NoCaract.append(ValorDiffMenor)
        
    X=True
    #sigue verificar que huesos cumplen con las especificaciones, comenzando desde el inicio
    #en cuanto detecte detecte 2 se hace la pregunta, se tiene que verificar el largo
    for clave in huesos:
        
        
        #Valora que el hueso tenga la caracteristicas deseadas
        TieneCaracDeseadas = all(elem in huesos[clave]  for elem in SiCaract )
        #Valora que el hueso no tenga caracteristicas indeseadas
        if len(NoCaract)>0:
            TieneIndeseadas = any(elem in huesos[clave]  for elem in NoCaract )
        else:
            TieneIndeseadas = False
        
        #incorporacion de posibles respuestas
        if TieneCaracDeseadas and not(TieneIndeseadas):
            opciones.append(clave)
          
        #eliminar opciones antes de continuar evaluando los siguientes casos   
        while len(opciones)>1 and X:
    
            #Se obtiene una lista de todas las caracteristicas en opciones
            CaracteEnOpcio=[]
            CaracDiffSime = []
            for opc in opciones:
                CaracteEnOpcio=list((set(CaracteEnOpcio) | set(huesos[opc]))  )
                CaracDiffSime = list(set(CaracDiffSime) ^ set(huesos[opc]))

                
            #Se obtienen las caracteristicas que no se han valorado
            CaractNoValoradas = list(set(CaracteEnOpcio) - (set(SiCaract) | set(NoCaract)))
            CaracDiffSime = resultado = list(set(CaracDiffSime) & set(CaractNoValoradas))
            if len(CaracDiffSime) > 0:
                CaractNoValoradas=list(CaracDiffSime)

            #Si hay caracteristicas por valorar se valora la primera disponible
            if len(CaractNoValoradas)>0:
                PCarat = str(CaractNoValoradas[0])
                pregunta ='x'
                Ventana_pregunta("Tu hueso " + caracteristicas[PCarat] + "?") 
                if pregunta == 'x':
                    break
    
                if pregunta== 's':
                    SiCaract.append(CaractNoValoradas[0])
                 
                else:
                    NoCaract.append(CaractNoValoradas[0])
                  
                #Valorar si en las opciones cumple con las nuevas caracteristicas
                opcionesCopia = list(opciones)
                for opcCopia in opcionesCopia:
                    #Valorar que el hueso tenta las nuevas caracteristicas
                    TieneCaracDeseadas = all(elem in huesos[opcCopia] for elem in SiCaract)
                    #Valora que el hueso no tenga las nuevas caracteristicas indeseadas
                    if len(NoCaract)>0:
                       TieneIndeseadas = any(elem in huesos[opcCopia]  for elem in NoCaract )
                    else:
                        TieneIndeseadas = False
                    
                        #eliminar hueso de opciones 
                    if TieneIndeseadas or  not(TieneCaracDeseadas) :
                        opciones.remove(opcCopia)
    
                
            else:
               X = False
#Mostrar respuesta             
            
    if len(opciones)==1:
        pregunta='x'
        print(opciones)
        Ventana_pregunta("Tu hueso es: " + opciones[0] + "\n ¿Es correcto?") 
        if pregunta == 'x':
            break

#solicitar respuesta si es que no se encontro o no fue correcta 
    if len(opciones)<1 or pregunta == 'n':
    
            ventana = tk.Tk()
            ventana.title("Nueva respuesta")
            if not (pregunta == 'n'):
                tk.Label(ventana, text="¿Cuál es la respuesta?:").pack(pady=10)
                print("no se la respuesta")
            else:
                tk.Label(ventana, text="No encontre la respuesta \n ¿Cuál es la respuesta?:").pack(pady=10)
                
            
 #Guardar respuesta           
            entrada = tk.Entry(ventana, width=40)
            entrada.pack(pady=5)
            
            tk.Button(ventana, text="Guardar", command=guardar_respuesta).pack(pady=10)
            
            ventana.mainloop()
    """
            respuesta = input("¿Cual es la respuesta?: ")
            respuesta= respuesta.strip().casefold()
            SiCaract = sorted(set(SiCaract))
            huesos[respuesta] = SiCaract
            with open("huesos.json", "w") as f:
                json.dump(huesos, f)
            print("¡Gracias! He aprendido algo nuevo.")
     """   
#volver a jugar     
    if len(opciones)>1:
        txtRepetir = "Lo siento se tiene mas de una respuesta,\n Quieres volver a intentar"
    else:
        txtRepetir = "¿Quiere volver a intentar?"
    pregunta = 'x'
    Ventana_pregunta(txtRepetir) 
    if pregunta == 'x' or pregunta =='n':
        break
        