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
from prettytable import PrettyTable
import time
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

# Variables

archivoDeCarga1 = 'airports-utf8-small.csv'
archivoDeCarga2 = 'routes-utf8-small.csv'
archivoDeCarga3 = 'worldcities-utf8.csv'
catalog = None
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
    pyu = controller.loadData(catalog, archivoDeCarga1, archivoDeCarga2, archivoDeCarga3)
    totalaeropuerto = controller.totalAeropuertos(catalog)
    totalrutas = controller.totalRutasAereas(catalog)
    totalciudades = controller.totalCiudades(catalog)

    print('=== Airports-Routes DiGraph ===')
    print('Nodes: ' + str(totalaeropuerto[0]) + ' loaded airports.')
    print('Edges: ' + str(totalrutas[0]) + ' loaded routes.' )
    print('First & Last Airport loaded in the DiGraph.')

    table1 = PrettyTable(['IATA', 'Name', 'City', 'Country', 'Latitude', 'Longitude'])

    table1.add_row([pyu[1][0]['IATA'], pyu[1][0]['Name'], pyu[1][0]['City'], pyu[1][0]['Country'], pyu[1][0]['Latitude'], pyu[1][0]['Longitude']])
    table1.add_row([pyu[1][1]['IATA'], pyu[1][1]['Name'], pyu[1][1]['City'], pyu[1][1]['Country'], pyu[1][1]['Latitude'], pyu[1][1]['Longitude']])  

    print(table1)

    print('')

    print('=== Airports-Routes Graph ===')
    print('Nodes: ' + str(totalaeropuerto[1]) + ' loaded airports.')
    print('Edges: ' + str(totalrutas[1]) + ' loaded routes.' )
    print('First & Last Airport loaded in the Graph.')

    print(table1)

    print('')

    print('=== City Network ==')
    print('The number of cities are: ' + str(pyu[2]))
    print('First & Last City loaded in data structure.')

    table2 = PrettyTable(['city', 'country', 'lat', 'lng', 'population'])

    table2.add_row([pyu[0][0]['city'], pyu[0][0]['country'], pyu[0][0]['lat'], pyu[0][0]['lng'], pyu[0][0]['population']])
    table2.add_row([pyu[0][1]['city'], pyu[0][1]['country'], pyu[0][1]['lat'], pyu[0][1]['lng'], pyu[0][1]['population']])

    print(table2)

    return catalog


def opcion3(catalog):
    start = time.time()
    totalaeropuerto = controller.totalAeropuertos(catalog)
    respuestas = controller.getAeropuertoMasConectado(catalog)
    end = time.time()


    print('================ Req No. 1 Inputs ================')
    print('most connected airports in network (TOP 5)')
    print('Numbers of airports in networks: ' + str(totalaeropuerto[0]))
    print('')
    print('================ Req No. 2 Answer ================')
    print('Connected airports inside network: ' + str(respuestas[0]))
    print('TOP 5 most connected airpots...')

    table = PrettyTable(['Name', 'City', 'Country', 'IATA', 'connections', 'inbound', 'outbound'])
    ite = lt.iterator(respuestas[1])
    for element in ite:
        table.add_row([element[0], element[1], element[2], element[3], element[4], element[5], element[6]])

    print(table)
    print(end - start)

def opcion4(catalog,aero1,aero2):
    start = time.time()
    respuestas = controller.estanMismoCluster(catalog,aero1,aero2)
    end = time.time()

    print('================ Req No. 2 Inputs ================')
    print('Airport-1 IATA Code: ' + aero1)
    print('Airport-2 IATA Code: ' + aero2)

    print('')

    print('================ Req No. 2 Answer ================')
    print('+++ Airport1 IATA Code: LED +++')

    table1 = PrettyTable(['IATA', 'Name', 'City', 'Country'])

    table1.add_row([respuestas[0]['IATA'], respuestas[0]['Name'], respuestas[0]['City'], respuestas[0]['Country']])
    print(table1)

    print('+++ Airport1 IATA Code: RTP +++')

    table2 = PrettyTable(['IATA', 'Name', 'City', 'Country'])

    table2.add_row([respuestas[1]['IATA'], respuestas[1]['Name'], respuestas[1]['City'], respuestas[1]['Country']])
    print(table2)

    print('- Number of SCC in Airport-Route network: ' + str(respuestas[3]))
    print('- Does the ' + respuestas[0]['Name'] + ' and the ' + respuestas[1]['Name'] + 'belong together?')
    print('- ANS: ' + str(respuestas[2]))

    print(end - start)

def opcion5(catalog):
    print('================ Req No. 3 Inputs ================')
    ciudadOrigen = input('Departure City: ')
    CiudadDestino = input('Arrival City: ')
    print('')


    ## Valores de TEST
    ciudadOrigen = 'St. Petersburg'
    CiudadDestino = 'Lisbon'

    AeropuertoOrigen,AeropuertoDestino,Ruta = controller.encontrarRutaMasCorta(catalog,ciudadOrigen,CiudadDestino)
    print('================ Req No. 3 Answer ================')

    print('')
    aeropuerto1 = controller.getAeropuerto(catalog, AeropuertoOrigen)
    table1 = PrettyTable(['IATA','Name','City', 'Country'])
    table1.add_row([lt.getElement(aeropuerto1,1),lt.getElement(aeropuerto1,2),lt.getElement(aeropuerto1,3),lt.getElement(aeropuerto1,4)])
    print('The departure ariport from ', ciudadOrigen , ' is:')
    print(table1)
    print('')
    aeropuerto2 = controller.getAeropuerto(catalog, AeropuertoDestino)
    table2 = PrettyTable(['IATA','Name','City', 'Country'])
    table2.add_row([lt.getElement(aeropuerto2,1),lt.getElement(aeropuerto2,2),lt.getElement(aeropuerto2,3),lt.getElement(aeropuerto2,4)])
    print('The arrival ariport at ', ciudadOrigen , ' is:')
    print(table2)
    print('')


    print('Djikstra trip Details: ')
    print('')
    table = PrettyTable(['Airline','Departure','Destination','Distance'])
    distTotal = 0
    for trayecto in lt.iterator(Ruta):
        table.add_row([lt.getElement(trayecto,1),lt.getElement(trayecto,2),lt.getElement(trayecto,3),lt.getElement(trayecto,4)])
        distTotal = distTotal + float(lt.getElement(trayecto,4))

    print('Total Distance Traveled: ',distTotal, ' km')
    print('')
    print('Trip Path: ')
    print(table)


def opcion6(catalog,ciudad,millas):
    
    aeropuertos = controller.aeropuertosDeCiudad(catalog, ciudad)
    aer = lt.iterator(aeropuertos)
    for aeropuer in aer:
        print(aeropuer)
    aeropuerto = input('Elija alguno de los aeropuertos de la ciudad: ')
    start = time.time()
    resultados =  controller.planMillas(catalog,aeropuerto,millas)
    end = time.time()
    
    print('================ Req No. 4 Inputs ================')
    print('Departure IATA Code: ' + aeropuerto)
    print('Available Travel Miles: ' + millas)
    print('')
    print('================ Req No. 4 Answer ================')
    print('+++ Departure Airport for IATA code: LIS +++')

    table1 = PrettyTable(['IATA', 'Name', 'City', 'Country'])

    table1.add_row([resultados[0]['IATA'], resultados[0]['Name'], resultados[0]['City'], resultados[0]['Country']])

    print(table1)

    print('')
    print('- Number of possible airports: ' + str(resultados[1]))
    print('- Max traveling distance between airports: ' + str(round(resultados[2],2)) + ' (km)')
    print('- Passenger available traveling miles: ' + str(resultados[3]) + '(km)')
    print('')
    print('+++ Longest possible route with airport ' + aeropuerto + ' +++')
    print('- Longest possible path distance: ' + str(round(resultados[4], 2)) + '(km)')
    print('- Longests possible path distance:')

    table2 = PrettyTable(['Airline', 'Departure', 'Destination', 'distance_km'])

    vuelos = lt.iterator(resultados[5])

    for vuelo in vuelos:
        table2.add_row([vuelo['Airline'], vuelo['Departure'], vuelo['Destination'], vuelo['distance_km']])

    print(table2)
    print('-----')
    print('The passenger needs ' + str(resultados[6]) + ' miles to complete the trip.')
    print('-----')

    print(end - start)

def opcion7(catalog,aeropuerto):
    start = time.time()
    respuesta = controller.aeropuertoFueraFuncionamiento(catalog,aeropuerto)
    end = time.time()

    print('================ Req No. 5 Inputs ================')
    print('Closing the airport with IATA code: ' + aeropuerto)
    print('')
    print('--- Airport-Routes DiGraph ---')
    print('Original number of Airports: ' + str(respuesta[0][0]) + ' and Routes: ' + str(respuesta[0][1]))
    print('--- Airports-Routes Graph ---')
    print('Original number of Airports: ' + str(respuesta[1][0]) + ' and Routes: ' + str(respuesta[1][1]))
    print('')
    print('+++ Removing Airport with IATA: ' + aeropuerto + ' +++')
    print('')
    print('--- Airports-Routes DiGraph ---')
    print('Resulting number of Airports: ' + str(respuesta[2][0]) + ' and Routes: ' + str(respuesta[2][1]))
    print('--- Airports-Routes Graph ---')
    print('Resulting number of Airports: ' + str(respuesta[3][0]) + ' and Routes: ' + str(respuesta[3][1]))
    print('')
    print('================ Req No. 5 Answer ================')
    print('There are ' + str(lt.size(respuesta[4])) + ' Airports affected by the removal of ' + aeropuerto)
    print('The first & last 3 Airports affected are:')

    table = PrettyTable(['IATA', 'Name', 'City', 'Country'])

    tamanio = lt.size(respuesta[4])
    contador = 1
    while contador <= tamanio:
        while contador <= 3 and contador <= tamanio:
            element = lt.getElement(respuesta[4], contador)
            table.add_row([element['IATA'], element['Name'], element['City'], element['Country']])
            contador = contador + 1
        
        while contador <= 6 and contador <= tamanio:
            element = lt.getElement(respuesta[4], tamanio - contador)
            table.add_row([element['IATA'], element['Name'], element['City'], element['Country']])
            contador = contador + 1
        contador = contador  + 1
    
    print(table)

    print(end - start)
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
            opcion5(catalog)

        elif int(inputs[0]) == 6:
            print('Bienvenido al sistema de Millas')
            print('Ingrese su informacion para buscar el viaje con la mayor cantidad de ciudades bajo el presupuesto de millas dado')
            aeropuerto = input('Ingrese ciudad de origen: ')
            millas = input('Cantidad de millas disponibles del viajero: ')
            opcion6(catalog,aeropuerto,millas)

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