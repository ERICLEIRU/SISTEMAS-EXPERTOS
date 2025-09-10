# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 10:45:00 2025

@author: uriel
"""

# imprimir en consola
print("hola mundo")
#numeros 
a = 5 #tipo int por ser python 3 no es necesario long
b = 5.0 #float
c = 8
realexp = 0.56e5 #exponencial en base 10
#suma
print(a + b)
#resta
print(a-c)
#multiplicacion
print (a*a)
#exponente
print(b**2)
#division
print(c/a)
#modulo
print(a%c)
#comillas simples
cads = 'Texto \n comillas simples'
print(type(cads))
print (cads)
#comillas dobles
cadd = "Texto  \n\t comillas dobles"
print(type(cadd))
print (cadd)
#comillas triples dobles
cadc = """ Texto linea 1
linea 2
linea 3
..linea n """
print(type(cadc))
print (cadc)
#repeticion y concatenacion de cadenas
cad = "cadena"*3 # cadenacadenacadena
print (cad)
print (cad + cad) #concatenar cadena

#booleanos y operadores logicos
Bt = True
Bf = False
BAnd = True and True
Bor = True or False
Bnot = not False

#listas son como los arreglos pero de todos los tipos se inicia en 0
l = [2,"tres", True, [10,"uno"], "final"]
print ( l[0])
print (l[3][1])
#copiar partes de una lista
l1 = l[0]
l2 = l[0:3] #del 0 al tres sin tomar en cuanta el tres
l3 = l[0:3:2] #del 0 al tres cada segundo valor despues de tomar el dato
l4 = l[0::2] #todos los valores brincando uno
l[0:2] = [4,5] #cambiar una parte de la lista
lf = l[-1] #acceder al ultimo valor
print (l[0:2])

#tuplas no pueden agregar elementos ni modificar sus elementos
t = (3, "hola", False)
t1 = 3, "hola", True
print( t[0]) #se acceden igual que las listas
#Diccionarios se pueden modivicar los valores mas no las claves y no se puede 
#hacer slicing d[0:2]
d = {"clave1":[1,2,3],
     4 : True,
     "clave3":[2,"tres"]}
d1 = d["clave1"]

#operadores racionales
y = 10
x = 10

z = x == y #tambien valido para cadenas, listas, tuplas y diccionarios
z = x != y #tambien valido para cadenas ... ...
z = x > y  #tambien valido para cadenas pero volatil
z = x <= y
# #encoding: utf-8 para poder usar la ñ
#SENTENCIAS CONDICIONALES
if x > y:
    print("x mayor a y")
elif x == y:
    print("x es igual a y")
else:
    print("y es mayor a x")
    
#bucles

while x < 20:
    print("hola")
    x = x + 1
    if x == 15:
        continue #continua al siguiente ciclo
    if x < 10:
        break #se sale del while
     
elementos = [1,2,3,4]
for elem in elementos:
    print(elem)

# Funciones *algomas para datos extras en touplas **algomas para diccionarios

def mi_funcion (x =0,y = 5):
    print(x + y)
    return x + y
    
mi_funcion(x, y)
mi_funcion(0,)
mi_funcion(x)
mi_funcion()
# mi_funcion(x,y, cadena = "hola") cadena se vuelve la llave
# mi_funcion(x,y,"hola", "adios" , "loco" ) hola, adios, loco se guardan en toupla

#Clases
class Humano:
    def __init__(self,edad = 18):
        self.edad = edad
        self.trabajo = "ingeniero"
        print ("soy un nuevo objeto")
        
    def hablar(self,mensaje):
        print(mensaje)
        print("mi edad es", self.edad)
        
pedro = Humano(25)
raul = Humano()
#usar el metodo
pedro.hablar("hola")
#usar atributo
print(pedro.edad, pedro.trabajo, raul.edad)

#Herencia
class IngSistemas(Humano):
    def programar(self):
        print("voy a programar en python")
        
class LicDerecho (Humano):
    def __init__(self,edad = 18):
        self.edad = edad
        self.trabajo = "ingeniero"
        print ("soy un abogado")
    
        
manuel = IngSistemas()
manuel.programar()
marcus = LicDerecho()
#herencia multiple, el orden importa para tomar el primer metodo repetido

class Estudioso(IngSistemas, LicDerecho):
    pass

#cadenas y metodos

s = "Holao Mundo"
print(len(s)) 
print(s.count("o"))
print(s.count("o",0,4))
print(s.count("o",4))
print(s.lower())
print(s.upper())
print(s)
print(s.replace("o", "x"))
print(s)
print(s.replace("o", "x",1))
print (s.split("o"))
print (s.split("o",2))
print(s)
print(s.find("Mun"))
print(s.rfind("o"))
t = ("H","o","l","a")
p = ";"

print(p.join(t)) #regresa una cadena

#Metodos de las listas
lista = [1, "dos", 3]

if 1 in lista:
    print(lista.index(3,0,len(lista)))

else:
    print("no esta en la lista")
    
lista.append("cuatro")
print(lista)
print(lista.count(3))
lista.insert(3,4)
print(lista)
cadena = "cadena" 
lista.extend(cadena)  
print(lista) 
print(lista.pop(4))
print(lista)
lista.remove(3)
print(lista)
lista.reverse()
print(lista)

#metodos de diccionarios
print("clave1" in d)
print(list(d))
#print(sorted(d))
print(d.keys())
print(d.values())
print(d.items()) #lista de touplas
print(d.pop(4))
print(d.pop(4,-4))
del d["clave1"]
print(d)
d.clear()
print(d)
d["nuevo elem"]="nuevo elemento"
print(d)
d2 = d.copy()
print(d2)

#encapsulamiento __ al principio para que sea metodo publico
#y tampoco terminar en __ (dos guiones bajos)

class Prueba:
    def __init__(self):
        self.__privado = "soy privado"
        self.publico = "soy publico"
        
    def __metodoPrivado(self):
        print("soy privado")
        return "soy privado"
    def metodoPublico(self):
        print("soy publico")
        
    def getPrivado(self):
        return self.__privado
    def setPrivado(self,valor):
        self.__privado = valor
        self.publico = self.__metodoPrivado() #modifica el publico
        
#funciones de orden superior, si no se ponen los () se puede mandar toda la funcion

#funcion map
a = [1, 2, 3, 4]

# Using custom function in "function" parameter

def double(val):
  return val*2

res = list(map(double, a))
print(res)

words = ['apple', 'banana', 'cherry']
res = map(lambda s: s[0], words)
print(list(res))

celsius = [0, 20, 37, 100]
fahrenheit = map(lambda c: (c * 9/5) + 32, celsius)
print(list(fahrenheit))
a = [1, 2, 3]
b = [4, 5, 6]
res = map(lambda x, y: x + y, a, b)
print(list(res))
fruits = ['apple', 'banana', 'cherry']
res = map(str.upper, fruits)
print(list(res))

#filter
# Function to check if a number is even
def even(n):
    return n % 2 == 0

t = [1, 2, 3, 4, 5, 6]
u = filter(even, t)

# Convert filter object to a list
print(list(u)) 

a = [1, 2, 3, 4, 5, 6]
b = filter(lambda x: x % 2 == 0, a)

print(list(b))

#REDUCE
from functools import reduce
# Function to add two numbers
def add(x, y):
    return x + y

a = [1, 2, 3, 4, 5]
res = reduce(add, a)

print(res) 
res = reduce(lambda x, y: x + y, a)

print(res)

#COMPRESION DE LISTAS
l = [1,2,3,-1,4]
s = ["h","o","l","a"]

l2 =[c*num for c in s
             for num in l
                 if num > 0]
print(l2)
#GENERADORES

l5 = (c*num for c in s
             for num in l
                 if num > 0)

for letra in l5:
    print(letra)
for leter in l2:
    print(leter)
    
def factorial(n):
    i = 1
    while n > 0:
        i=n*i
        yield i
        n -= 1 

l8 = factorial(5) #regresa un objeto iterable

print(l8)
for e in factorial(5):
    print(e)
    
#ENTRADAS Y SALIDAD DE TECLADO
#valor = input()
valor = input("Introduce un numero: ")
print(valor)

""" modulos
import m      #importa todas las funciones y clases en m, misma carpeta

e = m.ejemplo() #crea objeto de m
m.fejemplo() # ejecuta la funcion fejemplo de m
from m import Ejemplo #importa solo la clase o funcion ejemplo
from m import *    #importa todas las clases y funciones    

 """
        