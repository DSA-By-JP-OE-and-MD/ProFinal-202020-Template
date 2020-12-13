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
from DISClib.DataStructures import listiterator as it
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
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
                "indice":None}
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
    return analyzer
# -----------------------------------------------------

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