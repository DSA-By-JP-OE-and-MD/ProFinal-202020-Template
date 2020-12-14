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
from DISClib.Utils import error as error
assert config

"""
En este archivo definimos los TADs que vamos a usar y las operaciones
de creacion y consulta sobre las estructuras de datos.
"""

# -----------------------------------------------------
#                       API
def analyzer():
    analyzer = {"Grafo por ID":None, 
                "Indice":None}
    analyzer["indice"] = m.newMap(numelements=1000, 
                                     maptype="PROBING",
                                     loadfactor=0.5, 
                                     comparefunction=comparerMap)
    analyzer["Grafo por ID"] = gr.newGraph(datastructure='ADJ_LIST',
                                        directed=True,
                                        size=1000,
                                        comparefunction=comparer)
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
    for puesto in range(M):
        p=oms.maxKey(rankp)
        lt.addLast(rankesito,dict(list(rank.keys())[list(rank.values()).index(p)],p))
        oms.deleteMax(rankp)
    return rankesito

# Funciones para agregar informacion al grafo
def añadirIDalIndice(analyzer, archivo):
    m.put(analyzer["indice"], archivo["taxi_id"], archivo)




# ==============================
# Funciones de consulta
# ==============================

# ==============================
# Funciones Helper
# ==============================

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