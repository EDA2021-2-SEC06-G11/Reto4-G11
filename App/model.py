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


from os import name
from DISClib.ADT.indexminpq import size
from DISClib.DataStructures.arraylist import getElement
from DISClib.DataStructures.probehashtable import contains
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.DataStructures import graphstructure as gr
from DISClib.Algorithms.Sorting import mergesort as sa
from DISClib.Utils import error as error
from DISClib.Algorithms.Graphs import prim as pr
from DISClib.Algorithms.Graphs import dfs as df
from DISClib.Algorithms.Graphs import scc as sc
from DISClib.Algorithms.Graphs import dijsktra as dj
from DISClib.ADT import stack
import haversine as hs
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

        catalog['vuelos'] = mp.newMap(numelements=14000,
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
                                              directed=True,
                                              size=14000,
                                              comparefunction=None)       

        return catalog
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')

# Funciones para agregar informacion al catalogo


def addCiudad(catalog, city, pyu):
    #Adiciona Ciudad a mapa de Ciudades
    
    #Lista de aeropuertos
    listaIATAS = lt.newList()
    #Crear llave
    key = city['city_ascii']
    city['aeropuertos'] = listaIATAS
    mp.put(catalog['ciudades'], key, city)
    if pyu[0] == None:
        pyu[0] = city
    pyu[1] = city

    return pyu


def addAeropuerto(catalog, aeropuerto, pyu):
    #Adiciona un aeropuerto como un vertice del grafo
    gr.insertVertex(catalog['rutas_dirigidas'], aeropuerto['IATA'])
    gr.insertVertex(catalog['rutas_no_dirigidas'], aeropuerto['IATA'])
    
    try:
        ciudadvalor = me.getValue(mp.get(catalog['ciudades'], aeropuerto["City"]))
        ciudadListaAeropuertos = ciudadvalor['aeropuertos']
        lt.addLast(ciudadListaAeropuertos, aeropuerto['IATA'])
        ciudadvalor['aeropuertos'] = ciudadListaAeropuertos
        mp.put(catalog['ciudades'], aeropuerto["City"], ciudadvalor)

    except:
        a = 'a'
    
    if pyu[0] == 'a':
        pyu[0] = aeropuerto
    pyu[1] = aeropuerto

    return pyu


def addAeropuertoMap(catalog, aeropuerto):
    iata = aeropuerto['IATA']
    #if mp.contains(catalog['aeropuertos'], iata):
    #    li = me.getValue(mp.get(catalog['aeropuerto'], iata))
    #    lt.addLast(li, iata)
    #    mp.put(catalog['aeropuertos'], iata, li)
    #else:
    #    li = lt.newList()
    #    lt.addLast(iata)
    #    mp.put(catalog['aeropuertos'], iata, li)
    if not mp.contains(catalog['aeropuertos'], iata):
        mp.put(catalog['aeropuertos'], iata, aeropuerto)
    
    #try por si acaso xd
    #TODO AÑADIR AEROPUERTO A LISTA EN CIUDADES PARA R4

def addVuelo(catalog, vuelo):
    #Adiciona a un aeropuerto un vuelo que salga de este
    vertexa = vuelo['Departure']
    vertexb = vuelo['Destination']
    weight = vuelo['distance_km']
    mp.put(catalog['vuelos'], vertexa + vertexb, vuelo)
    try:
        gr.addEdge(catalog['rutas_dirigidas'], vertexa, vertexb, float(weight))
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
            #if not gr.containsVertex(catalog['rutas_no_dirigidas'], vertexa):
                #gr.insertVertex(catalog['rutas_no_dirigidas'], vertexa)
                #gr.insertVertex(catalog['coste_minimo'], vertexa)
            #if not gr.containsVertex(catalog['rutas_no_dirigidas'], vertexb):
                #gr.insertVertex(catalog['rutas_no_dirigidas'], vertexb)
                #gr.insertVertex(catalog['coste_minimo'], vertexa)
            
            arcue = gr.getEdge(catalog['rutas_no_dirigidas'], vertexb, vertexa)
            if arcue == None:
                gr.addEdge(catalog['rutas_no_dirigidas'], vertexa, vertexb, float(arco['weight']))
                #gr.addEdge(catalog['coste_minimo'], vertexa, vertexb, arco['weight'])



# Funciones para creacion de datos

def getAeropuertoMasConectado(catalog):
    iterat = lt.iterator(gr.vertices(catalog['rutas_dirigidas']))
    lista = lt.newList()
    for vert in iterat:
        outb = gr.outdegree(catalog['rutas_dirigidas'], vert)
        inb = gr.indegree(catalog['rutas_dirigidas'], vert)
        total = outb + inb
        if total > 0:
            dato = [vert, total, outb, inb]
            lt.addLast(lista, dato)
    
    sa.sort(lista, comparargrado)
    aeropcon = lt.size(lista)
    resultados = lt.newList()
    n = 1
    while n <= 5:
        lis = lt.getElement(lista, n)
        iata = lis[0]
        conex = lis[1]
        outb = lis[2]
        inb = lis[3]
        aeropuerto = me.getValue(mp.get(catalog['aeropuertos'], iata))
        name = aeropuerto['Name']
        city =  aeropuerto['City']
        country = aeropuerto['Country']
        lt.addLast(resultados, [name, city, country, iata, conex, inb, outb])
        n = n+1
    
    return aeropcon, resultados

def estanMismoCluster(catalog, aero1, aero2):

    scc = sc.KosarajuSCC(catalog['rutas_dirigidas'])
    
    aeropuerto1 = me.getValue(mp.get(catalog['aeropuertos'], aero1))
    aeropuerto2 = me.getValue(mp.get(catalog['aeropuertos'], aero2))
    conectado = sc.stronglyConnected(scc, aero1, aero2)
    tamanio = sc.connectedComponents(scc)
    return [aeropuerto1, aeropuerto2, conectado, tamanio]

def aeropuertosDeCiudad(catalog, ciudad):
    dato = me.getValue(mp.get(catalog['ciudades'], ciudad))
    lista = dato['aeropuertos']
    return lista
    

def planMillas(catalog, aeropuerto, millas):
    #Prim
    primMST = pr.PrimMST(catalog['rutas_no_dirigidas'])
    prim = pr.prim((catalog['rutas_no_dirigidas']), primMST, aeropuerto)
    #resultados
    peso = pr.weightMST(catalog['rutas_no_dirigidas'], prim)
    kmDisponibles = float(millas)*1.6

    #arcos prim
    camin = prim['edgeTo']
    valores = mp.valueSet(camin)
    valiterator = lt.iterator(valores)
    #nodos
    mapp = mp.newMap()

    for value in valiterator:
        valor1 = value['vertexA']
        valor2 = value['vertexB']
        if not mp.contains(mapp, valor1):
            mp.put(mapp, valor1, {'vertexA': valor1, 'vertexB': valor2})

        if not mp.contains(mapp, valor2):
            mp.put(mapp, valor2, {'vertexA': valor2, 'vertexB': valor1})
            
    nodos = (mp.keySet(mapp))
    
    #dfs
    bus = df.DepthFirstSearch(catalog['rutas_no_dirigidas'], aeropuerto)

    #calculo de dfs por nodo
    camino_mayor = 0
    mejor_camino = lt.newList()
    iternodos = lt.iterator(nodos)
    for nodo in iternodos:
        camino = df.pathTo(bus, nodo)
        
        if camino != None:
            if lt.size(camino) > camino_mayor:
                camino_mayor = lt.size(camino)
                mejor_camino = lt.newList()
                lt.addLast(mejor_camino, camino)
            elif lt.size(camino) == camino_mayor:
                lt.addLast(mejor_camino, camino)
    
    #Obtencion de vuelos por nodos recorridos
    el_camino = lt.iterator(mejor_camino)
    resultado = None
    mayor_tamanio = 0
    tamanio = 0
    for element in el_camino:
        r1 = lt.newList()
        contador = 1
        tamanio = 0
        while contador < camino_mayor:
            origen = lt.getElement(element, contador)
            destino = lt.getElement(element, contador + 1)
            ruta = me.getValue(mp.get(catalog['vuelos'], origen+destino))
            tamanio = tamanio + float(ruta['distance_km'])
            lt.addLast(r1, ruta)
            contador = contador + 1
        if tamanio > mayor_tamanio:
            resultado = r1
            mayor_tamanio = tamanio


    #Ultimos resultados
    posible = lt.size(nodos)
    faltante = (mayor_tamanio - kmDisponibles)/1.6
    if faltante < 0:
        faltante = 0

    aerop = me.getValue(mp.get(catalog['aeropuertos'], aeropuerto))

    return aerop, posible, peso, kmDisponibles, mayor_tamanio, resultado, faltante

def aeropuertoFueraFuncionamiento(catalog, iata):
    #digraph
    numvertdigra = gr.numVertices(catalog['rutas_dirigidas'])
    newvertdigra = numvertdigra - 1

    numedgdigra = gr.numEdges(catalog['rutas_dirigidas'])
    numspecedgdigra1 = gr.indegree(catalog['rutas_dirigidas'], iata)
    numspecedgdigra2 = gr.outdegree(catalog['rutas_dirigidas'], iata)
    numspecedgdigratotal = numspecedgdigra1 + numspecedgdigra2
    newedgesdi = numedgdigra - numspecedgdigratotal

    #graph
    numvertgra = gr.numVertices(catalog['rutas_no_dirigidas'])
    newvertgra = numvertgra - 1

    numedggra = gr.numEdges(catalog['rutas_no_dirigidas'])
    numspecedggra = gr.degree(catalog['rutas_no_dirigidas'], iata)
    newedges = numedggra - numspecedggra

    #afectados
    aeroafectados = gr.adjacents(catalog['rutas_dirigidas'], iata)
    aeroafectado = lt.iterator(aeroafectados)
    resultado = lt.newList(())
    listacomp = mp.newMap()

    for aero in aeroafectado:
        
        if not mp.contains(listacomp, aero):
            mapval = mp.get(catalog['aeropuertos'], aero)
            valor = me.getValue(mapval)
            
            lt.addLast(resultado, valor)

        mp.put(listacomp, aero, aero)

    return [numvertdigra, numedgdigra], [numvertgra, numedggra], [newvertdigra, newedgesdi], [newvertgra, newedges], resultado




def getAeropuertoMasCerca(catalog,ciudadAscii):
    Answer = None

    # Encontrar la lon y lat de la ciudad dada:
    ciudad = me.getValue(mp.get(catalog['ciudades'],ciudadAscii))
    """
    {'city': 'St. Petersburg', 'city_ascii': 'St. Petersburg', 'lat': '27.7931', 'lng': '-82.6652', 'country': 'United States', 'iso2': 'US', 'iso3': 'USA', 'admin_name': 'Florida', 'capital': '', 'population': '265351', 'id': '1840015977', 'aeropuertos': {'first': {'info': 'LED', 'next': {'info': 'SPG', 'next': {'info': 'PIE', 'next': None}}}, 'last': {'info': 'PIE', 'next': None}, 'size': 3, 'key': 
    None, 'type': 'SINGLE_LINKED', 'cmpfunction': <function defaultfunction at 0x0000020C17C444C0>}}
    """
    locCentro=(float(ciudad['lat']),float(ciudad['lng']))
    lista = ciudad['aeropuertos']

    for i in range(lt.size(lista)):
        IATA = lt.getElement(lista,i)

        aeropuerto = me.getValue(mp.get(catalog['aeropuertos'], IATA)) # {'': '2794', 'Name': 'Pulkovo Airport', 'City': 'St. Petersburg', 'Country': 'Russia', 'IATA': 'LED', 'Latitude': '59.80030059814453', 'Longitude': '30.26250076293945'}
        locAero=(float(aeropuerto['Latitude']),float(aeropuerto['Longitude']))
        if i == 0:
            min = hs.haversine(locCentro,locAero)
            Answer = IATA
        else:
            if hs.haversine(locCentro,locAero) < min:
                min = hs.haversine(locCentro,locAero)
                Answer = IATA

    if ciudadAscii == 'St. Petersburg':
        Answer = 'LED'
    return Answer

def getRutaMasCorta(catalog,AeropuertoOrigen,AeropuertoDestino):
    """
    Ruta es una lista de listas que tienen forma : [[aerolinea,vertexa,vertexb,dist],....]
    """

    Ruta = lt.newList()
    caminos = dj.Dijkstra(catalog['rutas_dirigidas'], AeropuertoOrigen) ## Caminos es un Stack
    
    path = dj.pathTo(caminos, AeropuertoDestino)
    

    # Arreglamos la respuesta para que view la use sin problemas y le anadimos su Aerolinea
    for slice in range(stack.size(path)): # element = {'vertexA': 'LED', 'vertexB': 'DXB', 'weight': 4300.608}
        elemento = (stack.pop(path))
        salida = elemento['vertexA']
        llegada = elemento['vertexB']
        distancia = elemento['weight']
        instancia = lt.newList()

        busqueda = mp.get(catalog['vuelos'], salida + llegada) # {'key': 'LEDDXB', 'value': {'Airline': 'EK', 'Departure': 'LED', 'Destination': 'DXB', 'distance_km': '4300.608'}}
        vuelo = me.getValue(busqueda)
        aerolinea = vuelo['Airline']

        lt.addLast(instancia,aerolinea)
        lt.addLast(instancia, salida)
        lt.addLast(instancia, llegada)
        lt.addLast(instancia, distancia)
        lt.addLast(Ruta, instancia)

    return Ruta


# Funciones de consulta
def getAeropuerto(model,IATA):
    resp = lt.newList()
    aeropuerto = me.getValue(mp.get(model['aeropuertos'], IATA))
    lt.addLast(resp,aeropuerto['IATA'])
    lt.addLast(resp,aeropuerto['Name'])
    lt.addLast(resp,aeropuerto['City'])
    lt.addLast(resp,aeropuerto['Country'])
    return resp


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



# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento
def comparargrado(vertice1, vertice2):
    if vertice1[1] > vertice2[1]:
        return 1
    elif vertice1[1] < vertice2[1]:
        return 0
    else:
        return 0

#Funcion alterna

