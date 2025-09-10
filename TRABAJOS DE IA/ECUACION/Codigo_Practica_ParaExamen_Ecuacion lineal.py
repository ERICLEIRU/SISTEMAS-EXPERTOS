# -*- Codigo para estimar ecuaciones lineales de suma,resta,multiplicacion,division, dado un dataset con sus valores -*-
# De la forma x0w0+x1w1+x2w2+...zwn=y donde z=1 y n es el numero de variables independientes
"""
Created on Fri May  2 19:25:40 2025

@author: c23ag
"""
import numpy as np
import pandas as pd

def smart_round_nines(value):
    # Convertimos el número a cadena con precisión alta
    value_str = f"{value:.20f}"  # 20 decimales por seguridad
    integer_part, decimal_part = value_str.split(".")
    
    # Buscar la última aparición de '9999'
    last_pos = decimal_part.rfind('9999')
    
    if last_pos == -1:
        # Si no hay cuatro 9 consecutivos, no hacemos nada
        return value

    # Posición del dígito anterior a los 9999
    round_pos = last_pos

    # Obtener la parte decimal hasta el dígito anterior
    pre_nines = decimal_part[:round_pos]
    
    if not pre_nines:
        # Si los 9999 son los primeros decimales, redondeamos al entero
        return int(integer_part) + 1

    # Redondear el último dígito de pre_nines hacia arriba
    last_digit = int(pre_nines[-1])
    rounded_digit = last_digit + 1

    # Nueva parte decimal redondeada
    new_decimal = pre_nines[:-1] + str(rounded_digit)

    # Eliminar ceros a la derecha, si quieres un formato limpio
    final_str = f"{integer_part}.{new_decimal}".rstrip("0").rstrip(".")

    return float(final_str)
    
def check_four_nines(value):
    # Convertir el número en una cadena, eliminando la parte entera y el punto decimal
    decimal_part = str(value).split('.')[1]
    
    # Verificar si hay cuatro '9' consecutivos en la parte decimal
    if '9999' in decimal_part:
        return True  # Lanza la bandera si se encuentran 4 nueves consecutivos
    else:
        return False  # No se encontró
#===================Generar todas las posibles variables en la ecuacion, dado el dataset=========================================
#======Condiciones iniciales,dataset y Tasa de aprendizaje============
Dataset=pd.read_csv("Dataset_Ecuacion_-9x+7.csv")
Dataset=np.array(Dataset)
TasaDeAprendizaje=0.05
Sumatoria=0
#=====Conteo de variables con posibles coefientes W==============
VariablesEnUso=Dataset.shape
CantidadDeDatos=VariablesEnUso[0]
VariablesEnUso=VariablesEnUso[1]
#======Declaracion de variables Independientes en uso x0w0+x1w1+x2w2+...zwn=y donde z=1=================
Y=Dataset[:,VariablesEnUso-1].copy()
Z=np.ones_like(Dataset[:,0])
Dataset=np.insert(Dataset, VariablesEnUso-1, Z,axis=1)
Variables=Dataset[:,:-1]
#======Declaracion de Coeficientes (W) contemplando un posible termino constante (Z)=======================
"""h(x)=x0w0+x1w1+x2w2+zw3 donde z=1"""
W=np.zeros([VariablesEnUso])
#Busqueda de valores de W======================================================================
"""h(x)=x0w0+x1w1+x2w2+zw3 donde z=1"""
ContadorDeEpocas=0
B=1
while B==1:  
    p=0
    for muestra in Variables:
    #Obtencion de parametros basicos para Machine learning, Ypredecida y error
        y=(Y[p])
        yp=np.dot(W, muestra)
        E=(yp-y)
    #Generamos la sumatoria para despues cuantificar la eficacia del aprfendizaje
        Sumatoria=Sumatoria+E
    #Calculamos el gradiente desendiente para despues actualizar las W o nuestros parametros (Coeficientes)
        G=E*muestra
        W=W-(TasaDeAprendizaje*G)
        p=p+1
    #Calculamos J para conocer la eficacia del aprendizaje
    J=Sumatoria/(2*CantidadDeDatos)
 #Mostramos el final de una epoca
    ContadorDeEpocas=ContadorDeEpocas+1
    print("Epoca:",ContadorDeEpocas)
    print("W:",W)    
    print("J:",J)
    print("G:",G)    
    

#Evaluacion de W Dentro de tolerancia ============================================================================

#Esta tolerancia es; a partir de que todas las W tienen 4 nueves consecutivos
#Por ejemplo: 3.89999 and 5.1259999 = True

#Con un solo valor de W que no tenga los 4 9's, se entra en otra epoca
    B=0   
    for x in W:
        if check_four_nines(x) == False:
            B=1
#Redondeo de valores
p=0
for x in W:
   print(W[p])
   W[p]=smart_round_nines(x)
   print(W[p])
   p=p+1
        
        
    







