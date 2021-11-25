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
import threading
from DISClib.ADT import list as lt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

# Variables

archivoDeCarga1 = 'airports_full.csv'
archivoDeCarga2 = 'routes_full.csv'
archivoDeCarga3 = 'worldcities.csv'

#Menu

def printMenu():
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información en el catálogo")
    print("3- Req1 - Consultar Aeropuerto mas interconectado")
    print("4- Req2 - Consultar si dos mismos aeropuertos estan en el mismo cluster")
    print("5- Req3 - Conseguir la ruta mas corta para un aeropuerto de origen y otro de destino")
    print("6- Req4 - Abrir el sistema de millas para encontrar la ruta con mayor numero de ciudades visitadas en el presupuesto dado por las millas")
    print("7- Req5 - Consultar el impacto que tendria si un aeropuerto dado estuviera fuera de servicio en las rutas")


# Nota: Los prints se hacen aqui y no en el menu
def opcion2(catalog):
    print('\nCargando informacion de aeropuertos y sus vuelos')
    controller.loadData(catalog, archivoDeCarga1, archivoDeCarga2, archivoDeCarga3)
    totalaeropuerto = controller.totalAeropuertos(catalog)
    print(totalaeropuerto)
    totalrutas = controller.totalRutasAereas(catalog)
    print(totalrutas)
    totalciudades = controller.totalCiudades(catalog)
    print(totalciudades)
    primerosaeropuertos = controller.primerAeropuerto(catalog)
    print(primerosaeropuertos)
    ultimaciudad = controller.ultimaciudad(catalog)
    print(ultimaciudad)
    print('Numero total de aeropuertos del grafo direccional:' + str(totalaeropuerto[0]))
    print('Numero total de aeropuertos del grafo no direccional:' + str(totalaeropuerto[1]))
    print('Numero total de rutas aéreas del grafo direccional: ' + str(totalrutas[0]))
    print('Numero total de rutas aéreas del grafo no direccional: ' + str(totalrutas[1]))
    print('Numero total de ciudades: ' + str(totalciudades))
    print('El primer aeropuerto del grafo direccional:' , primerosaeropuertos[0])
    print('El primer aeropuerto del grafo no direccional:' , primerosaeropuertos[1])
    print('La ultima ciudad cargada fue:', ultimaciudad)
    print('Que pena no sabemos si el numero total de aeropuertos es el adecuado, y creemos que es por un problema de limite de memoria, ya tenemos cita para averiguar este problema, muchas gracias :)')


def opcion3(catalog):
    return controller.getAeropuertoMasConectado(catalog)

def opcion4(catalog,aero1,aero2):
    return controller.estanMismoCluster(catalog,aero1,aero2)

def opcion5(catalog,origen,destino):
    return controller.rutaMasCorta(catalog,origen,destino)

def opcion6(catalog,ciudad,millas):
    return controller.planMillas(catalog,ciudad,millas)

def opcion7(catalog,aeropuerto):
    return controller.aeropuertoFueraFuncionamiento(catalog,aeropuerto)
"""
Menu principal
"""
def thread_cycle():
    while True:
        printMenu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs[0]) == 1:
            print("\nInicializando....")
            catalog = controller.init()

        elif int(inputs[0]) == 2:
            print("Cargando información de los archivos ....")
            catalog = opcion2(catalog)

        elif int(inputs[0]) == 3:
            print('Calculando los aeropuertos con mas Conexiones en rutas')
            opcion3(catalog)

        elif int(inputs[0]) == 4:
            print('Ingrese la informacion de los dos aeropuertos que quiere conocer si estane en el mismo cluster')
            aero1 = input('Código IATA del aeropuerto 1:')
            aero2 = input('Código IATA del aeropuerto 2:')
            opcion4(catalog,aero1,aero2)

        elif int(inputs[0]) == 5:
            print('Ingrese la informacion para encontrar la ruta mas corta entre dos ciudades')
            origen  = input('Ingrese ciudad de origen')
            destino = input('Ingrese ciudad de destino')
            opcion5(catalog,origen,destino)

        elif int(inputs[0]) == 6:
            print('Bienvenido al sistema de Millas')
            print('Ingrese su informacion para buscar el viaje con la mayor cantidad de ciudades bajo el presupuesto de millas dado')
            ciudad = input('Ingrese Ciudad de origen:')
            millas = input('Cantidad de millasdisponibles del viajero.')
            opcion6(catalog,ciudad,millas)

        elif int(inputs[0]) == 7:
            aeropuerto = input('Código IATA del aeropuerto fuera de funcionamiento:')
            opcion7(catalog,aeropuerto)
            
        else:
            sys.exit(0)
    sys.exit(0)


if __name__ == "__main__":
    threading.stack_size(67108864)  # 64MB stack
    sys.setrecursionlimit(2 ** 20)
    thread = threading.Thread(target=thread_cycle)
    thread.start()