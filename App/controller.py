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

import config as cf
from App import model
import csv
from DISClib.ADT import stack

"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""

# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________
def InitCatalog():
    analyzer = model.analyzer()
    return analyzer

# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________
def loadFile(analyzer, file):
    """
    """
    file = cf.data_dir + file
    input_file = csv.DictReader(open(file, encoding="utf-8"),
                                delimiter=",")
    for a in input_file:
        model.añadirIDalIndice(analyzer, a)
        model.añadirAreaAlGrafo(analyzer, a)
        model.añadirViajealaLista(analyzer, a)
        
        
    return analyzer

# ___________________________________________________
#  Funciones para consultas
def BuscarRutaMasCorta(analyzer, rangoA, rangoB, origen, destino):
    A = model.RutaMasRapida(analyzer, rangoA, rangoB, origen, destino)
    Inicio = stack.pop(A[0])["vertexA"].split("-")
    Duracion = A[1]
    print("Ruta de viaje: ")
    while stack.size(A[0]) > 1:
        B = stack.pop(A[0])["vertexA"].split("-")
        print(B[0])
        print("------")
    n = stack.pop(A[0])["vertexB"].split("-")
    print(n[0])
    print("-----------------------------------------")
    print("Partida del area",Inicio[0],"a la hora",Inicio[1])
    print("Duracion en minutos del viaje",str(float(Duracion)/60))

def TaxisConPuntosEnFecha(analyzer, fecha, numero):
    listaV = model.ViajesUtilesEnUnaFecha(analyzer, fecha)
    tablaV = model.tablaPuntos(listaV)
    B = model.hallarTop(tablaV, numero)
    return B

def TaxisConPuntosEntreFechas(analyzer, fecha1, fecha2, numero):
    listaV = model.ViajesUtilesEntreFechas(analyzer, fecha1, fecha2)
    tablaV = model.tablaPuntos(listaV)
    B = model.hallarTop(tablaV, numero)
    return B