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

from time import process_time
import sys
import config
from App import controller
from DISClib.ADT import stack
from DISClib.DataStructures import listiterator as it
import timeit
assert config

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Variables
size = None
file = "taxi-trips-wrvz-psew-subset-"+str(size)+".csv"
ciclo = True
analyzer = None
# ___________________________________________________

def printReqB(resp, numero):
    print("\n")
    print("TOP "+ numero +" TAXIS CON MÁS PUNTOS")
    itresp = it.newIterator(resp)
    while it.hasNext(itresp):
        M = it.next(itresp)
        print("- "+M)

# ___________________________________________________
#  Menu principal
# ___________________________________________________

"""
Menu principal
"""
def menu():
    print("\n")
    print("Bienvenido al menu principal")
    print("-----------------------------------------")
    print("1) Inicializar catalogo")
    print("2) Cargar archivos")
    print("A) Generar reporte")
    print("B) Puntos asignados")
    print("C) Buscar la mejor ruta")
    print("0) Cerrar programa")
    print("-----------------------------------------")

while ciclo == True:
    menu()
    opcion = str(input("Eliga una opción: "))
    if opcion == "1":
        analyzer = controller.InitCatalog()
        print("Catalogo inicializado con exito")
    elif opcion == "2":
        size = input("Eliga el tamaño del archivo (large, medium, small): ")
        file = "taxi-trips-wrvz-psew-subset-"+size+".csv"
        time1 = float(process_time())
        controller.loadFile(analyzer, file)
        time2 = float(process_time())
        print("Se cargo el archivo exitosamente")
        print("Tiempo de carga: "+str(time2-time1))
    elif opcion == "A":
      M=input("Cuantas compañias con mayores taxis afiliados desea ver? ?\n")
      N=input("Cuantas compañias con mayores servicios prestados desea ver?\n")
        print("Cargando informe...")
        timeA1=process_time
        SR=controller.SR(analyzer)
        C=controller.C()
        TopM=controller.TM(M)
        TopN=controller.TN(N)
        timeA2=process_time
        print("Informe cargado, tiempo en carga: "+str(timeA1-timeA2))
        print(SR)
        print(C)
        print(TopM)
        print(TopN)
    elif opcion == "B":
        print("\n")
        print("1) Top de taxis en una fecha")
        print("2) Top de taxis entre dos fechas")
        print("\n")
        N = input("Elija una opción: ")
        if N == "1":
            print("\n")
            fecha = input("Ingrese una fecha (YYYY-MM-DD): ")
            numero = input("¿Cuantas posiciones desea que tenga el top de taxis?: ")
            time1 = float(process_time())
            H = controller.TaxisConPuntosEnFecha(analyzer, fecha, int(numero))
            time2 = float(process_time())
        else:
            print("\n")
            fecha1 = input("Ingrese la fecha inicial (YYYY-MM-DD): ")
            fecha2 = input("Ingrese la fecha final (YYYY-MM-DD): ")
            numero = input("¿Cuantas posiciones desea que tenga el top de taxis?: ")
            time1 = float(process_time())
            H = controller.TaxisConPuntosEntreFechas(analyzer, fecha1, fecha2, int(numero))
            time2 = float(process_time())
        printReqB(H, numero)
        print("Tiempo de carga: "+str(time2-time1))
    elif opcion == "C":
        origen = input("Escriba el area de inicio: ")
        destino = input("Escriba el area de llegada: ")
        rangoA = input("Escriba el rango de hora inicial(formato HH:MM): ")
        rangoB = input("Escriba el rango de hora final(formato HH:MM): ")
        time1 = float(process_time())
        controller.BuscarRutaMasCorta(analyzer, rangoA, rangoB, origen, destino)
        time2 = float(process_time())
        print("Tiempo de carga: "+str(time2-time1))
    elif opcion == "0":
        ciclo = False