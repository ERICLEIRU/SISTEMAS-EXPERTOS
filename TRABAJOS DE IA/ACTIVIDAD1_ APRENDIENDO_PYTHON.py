# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 07:16:36 2025

@author: uriel
"""
""" PARTE 1 ESTRUCTURA DE DATOS """
""" 1 LISTAS """

libros_fav = []

libros_fav.append("La fundacion")
libros_fav.append("Yo robot")
libros_fav.append("IT")
libros_fav.append("El resplandor")
libros_fav.append("Un mundo feliz")

#funcion para inprimir los libros de la lista
def print_titulos (libros):
    print("Los libros son:")
    for titulos in libros:
        print(titulos)
#funcion para agregar libro a la lista 
def add_libro (libros):
    titulo = input("Nuevo libro: ")
    libros.append(titulo)
        
#agregar nuevo libro
add_libro(libros_fav)
#impresion de los libros en la lista
print_titulos(libros_fav)

""" 2 DICCIONARIOS """

amigos = {}
amigos["Alejandra"]=34
amigos["Edmundo"]=20
amigos["Guadalupe"]=30

#funcion para imprimir la lista de amigos
def print_amigos( dic_amigos):
    print("Lista de amigos")
    for x in dic_amigos:
        print(x , " edad: ",  dic_amigos[x])
        
#funcion para actualizar edad de un amigo en la lista, si este existe
def actua_edad (dic_amigos):

    print_amigos(dic_amigos)
    
    nombre = input ("Escriba el nombre del amigo a cambiar edad : ")
    new_edad = int(input("escriba la nueva edad: "))
    
    if nombre in dic_amigos:
        dic_amigos[nombre] = new_edad
        print(" se ha actualizado la edad")
        
    else:
        print("El nombre no se reconoce por lo que no se actualiza la edad")
        
    print_amigos(dic_amigos)
      
print_amigos(amigos)
actua_edad(amigos)

""" 3 TUPLAS """

paises_por_visitar = ("Alemania", "Japon", "Canada")

#funcion para imprimir paises 
def print_paises ( paises):
    print("Los paises a visitar son:")
    for p in paises:
        print(p)
        
#funcion para verificar paises
def verificar_pais (paises):
    pais = input("Que pais desea verificar: ")
    if pais in paises:
        print("El pais se encuentra en la tupla")
    else:
        print("El pais no se encuentra en la tupla")
        
print_paises(paises_por_visitar)
verificar_pais(paises_por_visitar)

""" PARTE 2 OBJETOS"""

#deficion de la clase cliente
class Cliente ():
    #iniciacion, con los parametros privados
    def __init__(self, nombre, saldo):
        self.__nombre = nombre
        self.__saldo = saldo
        
        
    def get_balance(self):
        print("el saldo es: ", self.__saldo)
        return self.__saldo
    def deposit(self,deposito):
        self.__saldo += deposito
        return self.__saldo
        
    def withdraw(self,valor):
        if valor <= self.__saldo:
            self.__saldo -= valor
        else:
            print("no hay suficiente saldo")
            
        print("saldo remanente: ", self.__saldo)
        
        
#creacion de objeto cliente
cliente1 = Cliente("Eric", 100 )

#Pruebas de los metodos

cliente1.get_balance() #muestra en consola y regresa el saldo
cliente1.deposit(500) #aumenta la cantida de saldo en 500
cliente1.get_balance()
cliente1.withdraw(300) #resta en 300 la cantidad de saldo
cliente1.withdraw(500) #no permite la resta de la cantida ya que es mayor al saldo