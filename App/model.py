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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.DataStructures import graphstructure as gr
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Utils import error as error
from DISClib.Algorithms.Graphs import prim as pr
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newAnalyzer():
    """ Inicializa el analizador

   stops: Tabla de hash para guardar los vertices del grafo
   connections: Grafo para representar las rutas entre estaciones
   components: Almacena la informacion de los componentes conectados
   paths: Estructura que almancena los caminos de costo minimo desde un
           vertice determinado a todos los otros vértices del grafo
    """
    try:
        catalog = {
                    'ciudades': None,
                    'rutas_dirigidas': None,
                    'rutas_no_dirigidas': None
                    }

        catalog['ciudades'] = mp.newMap(numelements=14000,
                                     maptype='PROBING',
                                     comparefunction=None)

        catalog['aeropuertos'] = mp.newMap(numelements=14000,
                                     maptype='PROBING',
                                     comparefunction=None)

        catalog['rutas_dirigidas'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=14000,
                                              comparefunction=None)

        catalog['rutas_no_dirigidas'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=False,
                                              size=14000,
                                              comparefunction=None)
        catalog['coste_minimo'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=False,
                                              size=14000,
                                              comparefunction=None)       

        return catalog
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')

# Funciones para agregar informacion al catalogo


def addCiudad(catalog, city):
    #Adiciona Ciudad a mapa de Ciudades
    
    #Lista de aeropuertos
    listaIATAS = lt.newList()

    #Crear llave
    key = city['city_ascii']
    city['aeropuertos'] = listaIATAS
    mp.put(catalog['ciudades'], key, city)


def addAeropuerto(catalog, aeropuerto):
    #Adiciona un aeropuerto como un vertice del grafo
    gr.insertVertex(catalog['rutas_dirigidas'], aeropuerto['IATA'])
    try:
        ciudadvalor = me.getValue(mp.get(catalog['ciudades'], aeropuerto["City"]))
        ciudadListaAeropuertos = ciudadvalor['aeropuertos']
        lt.addLast(ciudadListaAeropuertos, aeropuerto['IATA'])
        ciudadvalor['aeropuertos'] = ciudadListaAeropuertos
        mp.put(catalog['ciudades'], aeropuerto["City"], ciudadvalor)
        print(ciudadvalor)
    except:
        a = 'a'
    
    #print(ciudadListaAeropuertos)

def addAeropuertoMap(catalog, aeropuerto):
    mp.put(catalog['aeropuertos'], aeropuerto['IATA'], aeropuerto)
    #try por si acaso xd
    #TODO AÑADIR AEROPUERTO A LISTA EN CIUDADES PARA R4

def addVuelo(catalog, vuelo):
    #Adiciona a un aeropuerto un vuelo que salga de este
    vertexa = vuelo['Departure']
    vertexb = vuelo['Destination']
    weight = vuelo['distance_km']
    try:
        gr.addEdge(catalog['rutas_dirigidas'], vertexa, vertexb, weight)
    except:
        a = 'a'


def cargarDigrafo(catalog):
    listaarcos = gr.edges(catalog['rutas_dirigidas'])
    arcos = lt.iterator(listaarcos)
    for arco in arcos:
        vertexa = arco['vertexA']
        vertexb = arco['vertexB']
        
        arq = gr.getEdge(catalog['rutas_dirigidas'], vertexb, vertexa)
        if arq != None:
            if not gr.containsVertex(catalog['rutas_no_dirigidas'], vertexa):
                gr.insertVertex(catalog['rutas_no_dirigidas'], vertexa)
                gr.insertVertex(catalog['coste_minimo'], vertexa)
            if not gr.containsVertex(catalog['rutas_no_dirigidas'], vertexb):
                gr.insertVertex(catalog['rutas_no_dirigidas'], vertexb)
                gr.insertVertex(catalog['coste_minimo'], vertexa)
            
            arcue = gr.getEdge(catalog['rutas_no_dirigidas'], vertexb, vertexa)
            if arcue == None:
                gr.addEdge(catalog['rutas_no_dirigidas'], vertexa, vertexb, arco['weight'])
                gr.addEdge(catalog['coste_minimo'], vertexa, vertexb, arco['weight'])



# Funciones para creacion de datos

def planMillas(catalog, ciudad, millas):
    ciudad = me.getValue(mp.get(catalog['ciudades'], ciudad))
    aeropuertos = me.getValue(mp.get(ciudad, 'aeropuertos'))
    primervertice = lt.firstElement(aeropuertos)
    #Tonces, creo que esto con
    #Mapa de arcos nuevos
    nuevos_arcos = mp.newMap()

    prim = pr.PrimMST('coste_minimo')
    
    

    #Coger adjacentes

    #Verificar si alguno esta en otra ciudad

    #Si no, tomar el de menor costo




    

    

    
    arcos = gr.edges(catalog["rutas_no_dirigidas"])

# Funciones de consulta

def totalAeropuertos(catalog):
    grafo_dirigido = gr.numVertices(catalog['rutas_dirigidas'])
    grafo_no_dirigido = gr.numVertices(catalog['rutas_no_dirigidas'])
    return grafo_dirigido, grafo_no_dirigido

def totalRutasAereas(catalog):
    grafo_dirigido = gr.numEdges(catalog['rutas_dirigidas'])
    grafo_no_dirigido = gr.numEdges(catalog['rutas_no_dirigidas'])
    return grafo_dirigido, grafo_no_dirigido

def totalCiudades(catalog):
    return mp.size(catalog['ciudades'])

def primerAeropuerto(catalog):
    listavertices1 = gr.vertices(catalog['rutas_dirigidas'])
    listavertices2 = gr.vertices(catalog['rutas_no_dirigidas'])
    primero1 = lt.firstElement(listavertices1)
    primero2 = lt.firstElement(listavertices2)
    respuesta1 = me.getValue(mp.get(catalog['aeropuertos'], primero1))
    respuesta2 = me.getValue(mp.get(catalog['aeropuertos'], primero2))
    return respuesta1, respuesta2

def ultimaciudad(catalog):
    listault = mp.valueSet(catalog['ciudades'])
    ultima = lt.lastElement(listault)
    return ultima

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento


'''
def compararCiudad(ciudad1, ciudad2):
    ciudada = ciudad1['city_ascii']
    ciudadb = ciudad2['city_ascii']

    if ciudada > ciudadb:
        return 1
    elif ciudada < ciudadb:
        return -1
    else:
        return 0

def compararIata(aeropuerto1, aeropuerto2):
    Iata1 = aeropuerto1
    Iata2 = aeropuerto2

    if Iata1 > Iata2:
        return 1
    elif Iata1 < Iata2:
        return -1
    else:
        return 0
'''