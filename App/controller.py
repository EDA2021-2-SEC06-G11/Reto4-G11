"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
import model
import csv

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros

def init():
    # Inicializacion del modelo
    intermediario = model.newAnalyzer() 
    return intermediario


# Funciones para la carga de datos

def loadData(catalog, airportfile, routefile, cityfile):
    #Arreglar los tres archivos
    citylista = cf.data_dir + cityfile
    ciudades = csv.DictReader(open(citylista, encoding="utf-8"),
                                delimiter=",") #GUARDAR LISTA IATAS
    
    airportlista = cf.data_dir + airportfile
    aeropuertos = csv.DictReader(open(airportlista, encoding="utf-8"),
                                delimiter=",")


    rutalista = cf.data_dir + routefile
    rutas = csv.DictReader(open(rutalista, encoding="utf-8"),
                                delimiter=",")
    #ciudades es lista iterable de python

    #Cargar informacion de las ciudades
    pyuc = [None, None]
    tciud = 0
    for city in ciudades:
        tciud = tciud + 1
        pyuc = model.addCiudad(catalog, city, pyuc)

    #Cargar primer grafo
    
    pyua = ['a', None]
    for aeropuerto in aeropuertos:
        try:
            model.addAeropuertoMap(catalog, aeropuerto)
        except:
            a = 'a'
        pyua = model.addAeropuerto(catalog, aeropuerto, pyua)


    for ruta in rutas:
        model.addVuelo(catalog, ruta)

    #Cargar segundo grafo
    model.cargarDigrafo(catalog)


    return [pyuc, pyua, tciud]
    #Recorrer primer grafo
    #Por cada aeropuerto, revisas sus destinos
    #En cada destino revisar si se contiene el aeropuerto, si es bilateral (usar contains en lista de conexiones)






# Funciones de ordenamiento\

def getAeropuertoMasConectado(catalog):
    return model.getAeropuertoMasConectado(catalog)

def estanMismoCluster(catalog, ciudad1, ciudad2):
    return model.estanMismoCluster(catalog, ciudad1, ciudad2)

def planMillas(catalog, cidad, millas):
    return model.planMillas(catalog, cidad, millas,)

def aeropuertoFueraFuncionamiento(catalog, iata):
    return model.aeropuertoFueraFuncionamiento(catalog, iata)

def encontrarRutaMasCorta(catalog,ciudadOrigen,CiudadDestino):
    """
    Funcion para encontrar el camino mas corto entre dos ciudades:
    Returns:
        1. Aeropuerto Origen(String)
        2. Aeropuerto Destino(String)
        3. Ruta (lt que tiene [trayecto(string),distancia(double en km)])
        4. Distancia Total de la Ruta
    """

    AeropuertoOrigen = model.getAeropuertoMasCerca(catalog,ciudadOrigen)
    AeropuertoDestino = model.getAeropuertoMasCerca(catalog,CiudadDestino)

    Ruta = model.getRutaMasCorta(catalog,AeropuertoOrigen,AeropuertoDestino)


    return AeropuertoOrigen, AeropuertoDestino, Ruta


# Funciones de consulta sobre el catálogo

def getAeropuerto(catalog, IATA):
    """
    Deberia retornar una lista de 4 elementos de esta forma:[Iata,Name,City,Country]
    """
    return model.getAeropuerto(catalog, IATA)

def totalAeropuertos(catalog):
    return model.totalAeropuertos(catalog)

def totalRutasAereas(catalog):
    return model.totalRutasAereas(catalog)

def totalCiudades(catalog):
    return model.totalCiudades(catalog)

def aeropuertosDeCiudad(catalog, ciudad):
    return model.aeropuertosDeCiudad(catalog, ciudad)
