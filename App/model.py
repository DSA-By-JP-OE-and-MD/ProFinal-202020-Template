"""
 * Copyright 2020, Departamento de sistemas y Computación
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
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * Contribución de:
 *
 * Dario Correal
 *
 """
import config
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import list as lt
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import orderedmapstructure as oms
from DISClib.DataStructures import listiterator as it
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Algorithms.Sorting import mergesort as mrg
from DISClib.Utils import error as error
assert config
import datetime

"""
En este archivo definimos los TADs que vamos a usar y las operaciones
de creacion y consulta sobre las estructuras de datos.
"""

# -----------------------------------------------------
#                       API
def analyzer():
    analyzer = {"Grafo por ID":None,
                "Grafo por CA":None,
                "indice":None,
                "tripList":None}
    analyzer["indice"] = m.newMap(numelements=1000, 
                                     maptype="PROBING",
                                     loadfactor=0.5, 
                                     comparefunction=comparerMap)
    analyzer["Grafo por ID"] = gr.newGraph(datastructure='ADJ_LIST',
                                        directed=True,
                                        size=1000,
                                        comparefunction=comparer)
    analyzer["Grafo por CA"] = gr.newGraph(datastructure='ADJ_LIST',
                                        directed=True,
                                        size=1000,
                                        comparefunction=comparer)
    analyzer["tripList"] = lt.newList(datastructure="SINGLE_LINKED")
    return analyzer
# -----------------------------------------------------

def SR(analyzer):
    taxis=om.keySet(analyzer["indice"])
    taxis=set(taxis)
    return (lt.size(taxis))

def C(analyzer):
    resto=om.valueSet(analyzer["indice"])
    compañias=lt.newList()
    for pedaso in resto:
        lt.addLast(compañias,pedaso["company"])
    return (int(lt.size(compañias))+1)

def TM(analyzer,M):
    rank=oms.newMap('BST',comparefunction=comparerMap)
    rankp=oms.newMap('BST',comparefunction=comparerMap)
    sancocho=om.valueSet(analyzer["indice"])
    for papa in sancocho:
        if oms.contains(rank,papa["company"])==True:
            new=oms.get(rank,papa["company"])
            nueva=lt.newList(new.values())
            lt.addLast(nueva,papa["taxi_id"])
            oms.put(rank,str(new.keys()),nueva)
            if papa["company"]=="" and oms.contains(rank,"Independent Owner")==True:
                news=oms.get(rank,"Independent Owner")
                nuevas=lt.newList(news.values())
                lt.addLast(nuevas,papa["taxi_id"])
                oms.put(rank,str(news.keys()),nuevas)
        else:
            if papa["company"]=="":
                oms.put(rank,"Independent Owner",1)
            oms.put(rank,papa["company"],1)

    for com in list(rank):
        oms.put(rankp,lt.size(set(list(com.values()))),str(com.keys()))

    ranki=lt.newList()
    for puesto in range(M):
        p=oms.maxKey(rankp)
        lt.addLast(ranki,dict(om.keySet(rank)[om.valueSet(rank).index(p)],p))
        oms.deleteMax(rankp)
    return ranki

def TN(analyzer,N):
    rank=oms.newMap('BST',comparefunction=comparerMap)
    rankp=oms.newMap('BST',comparefunction=comparerMap)
    sancocho=om.valueSet(analyzer["indice"])
    for papa in sancocho:
        if oms.contains(rank,papa["company"])==True:
            new=oms.get(rank,papa["company"])
            nueva=int(new.values())+1
            oms.put(rank,str(new.keys()),nueva)
            if papa["company"]=="" and oms.contains(rank,"Independent Owner")==True:
                news=oms.get(rank,"Independent Owner")
                nuevas=int(news.values())+1
                oms.put(rank,str(news.keys()),nuevas)
        else:
            if papa["company"]=="":
                oms.put(rank,"Independent Owner",1)
            oms.put(rank,papa["company"],1)

    for com in list(rank):
        oms.put(rankp,int(com.values()),str(com.keys()))

    rankesito=lt.newList()
    for puesto in range(N):
        p=oms.maxKey(rankp)
        lt.addLast(rankesito,dict(list(rank.keys())[list(rank.values()).index(p)],p))
        oms.deleteMax(rankp)
    return rankesito

# Funciones para agregar informacion al grafo
def añadirIDalIndice(analyzer, archivo):
    m.put(analyzer["indice"], archivo["taxi_id"], archivo)
def añadirAreaAlGrafo(analyzer, archivo):
    origen = archivo["pickup_community_area"]
    destino = archivo["dropoff_community_area"]
    horainicio = time_converter(archivo["trip_start_timestamp"])
    horafin = time_converter(archivo["trip_end_timestamp"])
    if archivo["trip_seconds"] == "":
        archivo["trip_seconds"] = 0
    duracion = float(archivo["trip_seconds"])
    if origen == destino or (destino == "" or origen == ""):
        None
    else:
        if gr.containsVertex(analyzer["Grafo por CA"], origen+"-"+horainicio) and gr.containsVertex(analyzer["Grafo por CA"],destino+"-"+horafin):
            gr.addEdge(analyzer["Grafo por CA"], (origen+"-"+horainicio), (destino+"-"+horafin), duracion)
        elif (not gr.containsVertex(analyzer["Grafo por CA"], origen+"-"+horainicio)) and gr.containsVertex(analyzer["Grafo por CA"], destino+"-"+horafin):
            gr.insertVertex(analyzer["Grafo por CA"], origen+"-"+horainicio)
            gr.addEdge(analyzer["Grafo por CA"], (origen+"-"+horainicio), (destino+"-"+horafin), duracion)
        elif gr.containsVertex(analyzer["Grafo por CA"], origen+"-"+horainicio) and (not gr.containsVertex(analyzer["Grafo por CA"], destino+"-"+horafin)):
            gr.insertVertex(analyzer["Grafo por CA"], destino+"-"+horafin)
            gr.addEdge(analyzer["Grafo por CA"], (origen+"-"+horainicio), (destino+"-"+horafin), duracion)
        else:
            gr.insertVertex(analyzer["Grafo por CA"], origen+"-"+horainicio)
            gr.insertVertex(analyzer["Grafo por CA"], destino+"-"+horafin)
            gr.addEdge(analyzer["Grafo por CA"], (origen+"-"+horainicio), (destino+"-"+horafin), duracion)

def añadirViajealaLista(analyzer, archivo):
    lt.addLast(analyzer["tripList"], archivo)
    
# ==============================
# Funciones de consulta
# ==============================
def RutaMasRapida(analyzer, rangoA, rangoB, origen, destino):
    origen = origen+".0"
    destino = destino+".0"
    Lista = gr.vertices(analyzer["Grafo por CA"])
    ite = it.newIterator(Lista)
    while it.hasNext(ite):
        A = it.next(ite)
        B = A.split("-")
        if B[0] == origen and RangodeHorayMinuto(rangoA, rangoB, B[1]):
            N = djk.Dijkstra(analyzer["Grafo por CA"], A)
            ite2 = it.newIterator(Lista)
            while it.hasNext(ite2):
                C = it.next(ite2)
                D = C.split("-")
                if D[0] == destino and djk.hasPathTo(N, C):
                    return [djk.pathTo(N, C), djk.distTo(N, C)]
                    
    

    
                    

    

# ==============================
# Funciones Helper
# ==============================
def time_converter(time):
    if time != '':
        cuttime = datetime.datetime.strptime(time, '%Y-%m-%dT%H:%M:%S.%f')
        hora = cuttime.time()
        A = hora.strftime('%H:%M')
    else:
        A = "0"
    return A    
def RangodeHorayMinuto(rangoA, rangoB, hora):
    time = datetime.datetime.strptime(hora, '%H:%M').time()
    timeA = datetime.datetime.strptime(rangoA, '%H:%M').time()
    timeB = datetime.datetime.strptime(rangoB, '%H:%M').time()
    if timeA <= time and timeB >= time:
        return True
    else:
        return False
"""    ranA = rangoA.split(":")
    horaA = int(ranA[0])
    minutoA = int(ranA[1])
    ranB = rangoB.split(":")
    horaB = int(ranB[0])
    minutoB = int(ranB[1])
    h = hora.split(":")
    horah = int(h[0])
    minutoh = int(h[1])
    if horah > horaB or horah < horaA:
        return False
    else:
        if horaA == horaB:
            elif (minutoh => minutoA) and (minuto <= minutoB):
                return True
        elif horaA < horaB:
            if minutoA <= minutoB:
                if minutoh <= minutoB and minutoh >= minutoA:
                    return True
            elif minutoA >= minutoB:
                if """

def ViajesUtilesEnUnaFecha(analyzer, fecha):
    listaPuntos = lt.newList(datastructure="SINGLE_LINKED")
    fechain = datetime.datetime.strptime(fecha, "%Y-%m-%d")
    diain = fechain.date()
    ite = it.newIterator(analyzer["tripList"])
    while it.hasNext(ite):
        A = it.next(ite)
        fechaviaje = datetime.datetime.strptime(A["trip_start_timestamp"], '%Y-%m-%dT%H:%M:%S.%f')
        diaviaje = fechaviaje.date()
        if diain == diaviaje and A["trip_total"] != "" and A["trip_miles"] != "":
            if float(A["trip_total"]) > 0.0 and float(A["trip_miles"]) > 0.0:
                lt.addLast(listaPuntos, A)
    return listaPuntos

def ViajesUtilesEntreFechas(analyzer, fecha1, fecha2):
    listaPuntos = lt.newList(datastructure="SINGLE_LINKED")
    fechain1 = datetime.datetime.strptime(fecha1, "%Y-%m-%d")
    diain1 = fechain1.date()
    fechain2 = datetime.datetime.strptime(fecha2, "%Y-%m-%d")
    diain2 = fechain2.date()
    ite = it.newIterator(analyzer["tripList"])
    while it.hasNext(ite):
        A = it.next(ite)
        fechaviaje = datetime.datetime.strptime(A["trip_start_timestamp"], '%Y-%m-%dT%H:%M:%S.%f')
        diaviaje = fechaviaje.date()
        if diain1 <= diaviaje <= diain2 and A["trip_total"] != "" and A["trip_miles"] != "":
            if float(A["trip_total"]) > 0.0 and float(A["trip_miles"]) > 0.0:
                lt.addLast(listaPuntos, A)
    return listaPuntos

def tablaPuntos(lista):
    poinTable = m.newMap(numelements=1000,
                         maptype="PROBING",
                         loadfactor=0.5,
                         comparefunction=comparerMap)
    itelista = it.newIterator(lista)
    while it.hasNext(itelista):
        V = it.next(itelista)
        idtaxi = V["taxi_id"]
        millasV = float(V["trip_miles"])
        costoV = float(V["trip_total"])
        if not m.contains(poinTable, idtaxi):
            m.put(poinTable, idtaxi, {"millas":millasV, "costo":costoV, "servicios":1})
        else:
            A = m.get(poinTable, idtaxi)
            B = me.getValue(A)
            m.put(poinTable, idtaxi, {"millas":B["millas"]+millasV, "costo":B["costo"]+costoV, "servicios":B["servicios"]+1})
    llaves = m.keySet(poinTable)
    puntosTaxi = m.newMap(numelements=1000,
                          maptype="PROBING",
                          loadfactor=0.5,
                          comparefunction=comparerMap)
    itellaves = it.newIterator(llaves)
    while it.hasNext(itellaves):
        C = it.next(itellaves)
        D = m.get(poinTable, C)
        E = me.getValue(D)
        m.put(puntosTaxi, C, (E["millas"]/E["costo"])*E["servicios"])
    return puntosTaxi

def hallarTop(tabla, numero):
    taxis = m.keySet(tabla)
    puntos = m.valueSet(tabla)
    mrg.mergesort(puntos, lessfunction)
    listaOrd = lt.newList(datastructure="ARRAY_LIST")
    i = 0
    while i < numero:
        F = lt.lastElement(puntos)
        lt.addLast(listaOrd, F)
        lt.removeLast(puntos)
        i += 1
    listaTaxis = lt.newList(datastructure="ARRAY_LIST")
    itelistapuntos = it.newIterator(listaOrd)
    while it.hasNext(itelistapuntos):
        G = it.next(itelistapuntos)
        itetop = it.newIterator(taxis)
        while it.hasNext(itetop):
            H = it.next(itetop)
            I = m.get(tabla, H)
            J = me.getValue(I)
            if J == G:
                lt.addLast(listaTaxis, H)
    return listaTaxis

# ==============================
# Funciones de Comparacion
# ==============================
def comparer(stop, keyvaluestop):
    """
    Compara dos estaciones
    """
    stopcode = keyvaluestop['key']
    if (stop == stopcode):
        return 0
    elif (stop > stopcode):
        return 1
    else:
        return -1

def comparerMap(keyname, value):
    entry = me.getKey(value)
    if (keyname == entry):
        return 0
    elif (keyname > entry):
        return 1
    else:
        return -1

def lessfunction(ele1, ele2):
    if ele1 < ele2:
        return True
    return False