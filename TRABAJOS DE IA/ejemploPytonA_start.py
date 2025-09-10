# -*- coding: utf-8 -*-
"""
Created on Fri Mar 21 20:43:47 2025

@author: uriel
"""

import heapq

def a_star(matriz, inicio, objetivo):
    filas, columnas = len(matriz), len(matriz[0])
    
    # Direcciones posibles (arriba, abajo, izquierda, derecha)
    direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Heurística: distancia Manhattan entre dos puntos
    def heuristica(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    # Función para verificar si una celda es válida (dentro de los límites y no es un obstáculo)
    def es_valido(x, y):
        return 0 <= x < filas and 0 <= y < columnas and matriz[x][y] != 8

    # Inicialización de las listas abiertas y cerradas
    lista_abierta = []
    lista_cerrada = set()
    
    # El nodo inicial
    inicio_x, inicio_y = inicio
    objetivo_x, objetivo_y = objetivo
    
    heapq.heappush(lista_abierta, (0 + heuristica(inicio, objetivo), 0, inicio))  # (f, g, nodo)
    costos = {inicio: 0}
    padres = {inicio: None}

    while lista_abierta:
        # Sacamos el nodo con menor f (costo total estimado)
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

        # Comprobamos los vecinos (arriba, abajo, izquierda, derecha)
        for dx, dy in direcciones:
            vecino_x, vecino_y = x + dx, y + dy
            vecino = (vecino_x, vecino_y)
            
            if not es_valido(vecino_x, vecino_y) or vecino in lista_cerrada:
                continue

            # Calculamos el costo g para este vecino
            nuevo_g = g + 1  # El costo es 1 por cada paso
            if vecino not in costos or nuevo_g < costos[vecino]:
                costos[vecino] = nuevo_g
                f = nuevo_g + heuristica(vecino, objetivo)
                padres[vecino] = nodo_actual
                heapq.heappush(lista_abierta, (f, nuevo_g, vecino))
    
    return None  # Si no hay solución

# Definir la matriz del mapa (0 es camino libre, 255 es obstáculo)
matriz = [
    [0, 0, 0, 0, 0],
    [0, 8, 8, 8, 8],
    [0, 8, 0, 0, 0],
    [0, 8, 0, 8, 0],
    [0, 0, 0, 0, 0]
]

# Coordenadas de inicio y objetivo
inicio = (0, 0)
objetivo = (3, 4)

# Ejecutar A*
camino = a_star(matriz, inicio, objetivo)

# Mostrar el resultado
if camino:
    print("Camino más corto:", camino)
else:
    print("No hay solución.")