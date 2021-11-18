"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- ")

catalog = None
# Nota: Los prints se hacen aqui y no en el menu
def opcion1():
    return controller.loadData()

def opcion2(catalog):
    return controller.getAeropuertoMasConectado(catalog)

def opcion3(catalog,aero1,aero2):
    return controller.estanMismoCluster(catalog,aero1,aero2)

def opcion4(catalog,origen,destino):
    return controller.rutaMasCorta(catalog,origen,destino)

def opcion5(catalog,ciudad,millas):
    return controller.planMillas(catalog,ciudad,millas)

def opcion6(catalog,aeropuerto):
    return controller.aeropuertoFueraFuncionamiento(catalog,aeropuerto)
"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        catalog = opcion1()

    elif int(inputs[0]) == 2:
        print('Calculando los aeropuertos con mas Conexiones en rutas')
        opcion2(catalog)

    elif int(inputs[0]) == 3:
        print('Ingrese la informacion de los dos aeropuertos que quiere conocer si estane en el mismo cluster')
        aero1 = input('Código IATA del aeropuerto 1:')
        aero2 = input('Código IATA del aeropuerto 2:')
        opcion3(catalog,aero1,aero2)

    elif int(inputs[0]) == 4:
        print('Ingrese la informacion para encontrar la ruta mas corta entre dos ciudades')
        origen  = input('Ingrese ciudad de origen')
        destino = input('Ingrese ciudad de destino')
        opcion4(catalog,origen,destino)

    elif int(inputs[0]) == 5:
        print('Bienvenido al sistema de Millas')
        print('Ingrese su informacion para buscar el viaje con la mayor cantidad de ciudades bajo el presupuesto de millas dado')
        ciudad = input('Ingrese Ciudad de origen:')
        millas = input('Cantidad de millasdisponibles del viajero.')
        opcion5(catalog,ciudad,millas)

    elif int(inputs[0]) == 6:
        aeropuerto = input('Código IATA del aeropuerto fuera de funcionamiento:')
        opcion6(catalog,aeropuerto)
        
    else:
        sys.exit(0)
sys.exit(0)
