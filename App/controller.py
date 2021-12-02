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

    for city in ciudades:
        try:
            model.addCiudad(catalog, city)
        except:
            a = 'a'

    #Cargar primer grafo
    
    for aeropuerto in aeropuertos:
        try:
            model.addAeropuertoMap(catalog, aeropuerto)
        except:
            a = 'a'


        model.addAeropuerto(catalog, aeropuerto)

        

    for ruta in rutas:
        model.addVuelo(catalog, ruta)

    #Cargar segundo grafo
    model.cargarDigrafo(catalog)

    #Recorrer primer grafo
    #Por cada aeropuerto, revisas sus destinos
    #En cada destino revisar si se contiene el aeropuerto, si es bilateral (usar contains en lista de conexiones)
    #Si existe la conextion, añadir el vertice con su conexiones





# Funciones de ordenamiento

def planMillas(catalog, cidad, millas):
    model.planMillas(catalog, cidad, millas,)

# Funciones de consulta sobre el catálogo


def totalAeropuertos(catalog):
    return model.totalAeropuertos(catalog)

def totalRutasAereas(catalog):
    return model.totalRutasAereas(catalog)

def totalCiudades(catalog):
    return model.totalCiudades(catalog)

def primerAeropuerto(catalog):
    return model.primerAeropuerto(catalog)

def ultimaciudad(catalog):
    return model.ultimaciudad(catalog)