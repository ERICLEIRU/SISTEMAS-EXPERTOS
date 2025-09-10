# -*- coding: utf-8 -*-
"""
Created on Fri Mar 21 21:30:14 2025
EXAMEN IA
@author: uriel
"""
import heapq
import math
import numpy as np
import cv2


def a_star(matriz, inicio, objetivo):
    filas, columnas = len(matriz), len(matriz[0])
    
    # Direcciones posibles (arriba, abajo, izquierda, derecha, y diagonales)
    direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1), 
                   (-1, -1), (-1, 1), (1, -1), (1, 1)]  # Movimientos diagonales

    # Heurística: distancia Manhattan entre dos puntos
    def heuristica(a, b):
        return math.sqrt(abs((a[0] - b[0])*(a[0] - b[0])) + abs((a[1] - b[1])*(a[1] - b[1])))

    # Función para verificar si una celda es válida (dentro de los límites y no es un obstáculo)
    def es_valido(x, y):
        return 0 <= x < filas and 0 <= y < columnas and matriz[x][y] != 8

    # Inicialización de las listas abiertas y cerradas
    lista_abierta = []
    lista_cerrada = set()
    
    # El nodo inicial
    inicio_x, inicio_y = inicio
    objetivo_x, objetivo_y = objetivo
    
    # El valor 1.4 es el costo de moverse diagonalmente
    #Empujar el valor item en el heap, manteniendo el montículo invariable.
    heapq.heappush(lista_abierta, (0 + heuristica(inicio, objetivo), 0, inicio))  # (f, g, nodo)
    costos = {inicio: 0}
    padres = {inicio: None}

    while lista_abierta:
        # Sacamos el nodo con menor f (costo total estimado)
        #Desapila o pop y retorna el elemento más pequeño del heap, manteniendo el montículo invariable.
        _, g, nodo_actual = heapq.heappop(lista_abierta)
        x, y = nodo_actual
        
        # Si hemos llegado al objetivo, reconstruimos el camino
        if nodo_actual == objetivo:
            camino = []
            while nodo_actual:
                camino.append(nodo_actual)
                nodo_actual = padres.get(nodo_actual)
            return camino[::-1]  # Regresamos el camino en orden de inicio a objetivo

        lista_cerrada.add(nodo_actual)

        # Comprobamos los vecinos (arriba, abajo, izquierda, derecha y diagonales)
        for dx, dy in direcciones:
            vecino_x, vecino_y = x + dx, y + dy
            vecino = (vecino_x, vecino_y)
            
            if not es_valido(vecino_x, vecino_y) or vecino in lista_cerrada:
                continue

            # Si es un movimiento diagonal, el costo es 1.4, sino es 1
            if dx != 0 and dy != 0:  # Movimiento diagonal
                nuevo_g = g + 1.4
            else:  # Movimiento cardinal
                nuevo_g = g + 1

            if vecino not in costos or nuevo_g < costos[vecino]:
                costos[vecino] = nuevo_g
                f = nuevo_g + heuristica(vecino, objetivo)
                padres[vecino] = nodo_actual
                heapq.heappush(lista_abierta, (f, nuevo_g, vecino))
    
    return None  # Si no hay solución

def dibujar_mapa(matriz, camino, inicio, objetivo):
    filas, columnas = len(matriz), len(matriz[0])
    tamaño_celda = 30
    img = np.ones((filas * tamaño_celda, columnas * tamaño_celda, 3), dtype=np.uint8) * 255  

    for y in range(filas):
        for x in range(columnas):
            color = (255, 255, 255)  # Blanco
            if matriz[y][x] == 8:
                color = (128, 0, 128)  # Morado para obstáculos
            cv2.rectangle(img, (x * tamaño_celda, y * tamaño_celda), 
                          ((x + 1) * tamaño_celda, (y + 1) * tamaño_celda), color, -1)

    if camino:
        for (y, x) in camino:
            cv2.rectangle(img, (x * tamaño_celda, y * tamaño_celda), 
                          ((x + 1) * tamaño_celda, (y + 1) * tamaño_celda), (255, 0, 0), -1)  # Azul camino
    
    cv2.rectangle(img, (inicio[1] * tamaño_celda, inicio[0] * tamaño_celda), 
                  ((inicio[1] + 1) * tamaño_celda, (inicio[0] + 1) * tamaño_celda), (0, 255, 0), -1)  # Verde inicio
    cv2.rectangle(img, (objetivo[1] * tamaño_celda, objetivo[0] * tamaño_celda), 
                  ((objetivo[1] + 1) * tamaño_celda, (objetivo[0] + 1) * tamaño_celda), (0, 0, 255), -1)  # Rojo fin
    
    cv2.imshow("Mapa", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
# Definir la matriz del mapa (0 es camino libre, 255 es obstáculo)
matriz1 = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 8, 8, 0, 0, 0, 0, 0, 0, 0],
    [0, 8, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 8, 8, 8, 0, 0, 0, 0, 0, 0],
    [0, 0, 8, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 8, 0, 0, 0, 0, 0, 0, 0],
    [0, 8, 8, 0, 0, 0, 0, 0, 0, 0],
    [0, 8, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 8, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

# Coordenadas de inicio y objetivo
inicio1 = (0, 0)
objetivo1 = (4, 4)

matriz2 = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 8, 8, 8, 8, 8, 8, 8, 0, 0],
    [0, 8, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 8, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 8, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 8, 0, 0, 0, 8, 8, 8, 0, 0],
    [0, 8, 0, 0, 0, 0, 0, 8, 0, 0],
    [0, 8, 0, 0, 0, 0, 0, 8, 0, 0],
    [0, 8, 8, 8, 8, 8, 8, 8, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

# Coordenadas de inicio y objetivo
inicio2 = (9, 9)
objetivo2 = (0, 0)

matriz3 = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 8, 0, 0, 0, 0, 0, 8, 0, 0],
    [0, 8, 0, 0, 0, 0, 0, 8, 0, 0],
    [0, 8, 0, 0, 0, 0, 0, 8, 0, 0],
    [0, 8, 0, 0, 0, 0, 0, 8, 0, 0],
    [0, 8, 0, 0, 0, 0, 0, 8, 0, 0],
    [0, 8, 0, 0, 0, 0, 0, 8, 0, 0],
    [0, 8, 0, 0, 0, 0, 0, 8, 0, 0],
    [0, 8, 8, 8, 8, 8, 8, 8, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

# Coordenadas de inicio y objetivo
inicio3 = (4, 4)
objetivo3 = (9, 4)

# Ejecutar A*
camino1 = a_star(matriz1, inicio1, objetivo1)
camino2 = a_star(matriz2, inicio2, objetivo2)
camino3 = a_star(matriz3, inicio3, objetivo3)

# Mostrar el resultado
if camino1:
    print("Camino más corto:", camino1)
    dibujar_mapa(np.array(matriz1), camino1, inicio1, objetivo1)
else:
    print("No hay solución.")

if camino2:
    print("Camino más corto:", camino2)
    dibujar_mapa(np.array(matriz2), camino2, inicio2, objetivo2)
else:
    print("No hay solución.")
     
if camino3:
    print("Camino más corto:", camino2)
    dibujar_mapa(np.array(matriz3), camino3, inicio3, objetivo3)
else:
    print("No hay solución.")