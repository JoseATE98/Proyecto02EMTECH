# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 01:13:20 2021

@author: josea
"""
#importar modulos
import csv
from tabulate import tabulate
registros = []
#extraer los datos del arhivo
with open("synergy_logistics_database.csv") as archivo:
    #Leerlos en forma de diccionario
    contenido = csv.DictReader(archivo)
    for linea in contenido:
        registros.append(linea)

def obtenerRutas(rutasI = True, orden = 'valor', limit = 10, tipo = 'all'):
    """
    obtenerRutas
    ------------
    Obtiene las rutas que mas valor tengan o recorridos hechos
    
    Parametros
    ----------
    rutasI : TIPO, Bool
        DESCRIPCION. Indica si el orden de las rutas importa a-b = b-a
    orden : TIPO, String debe ser valor o conteo
        DESCRIPCION. Indica por que valor ordenar, el numero de veces o el valor comercial
    limit : TIPO, int
        DESCRIPCION. Indica cuantos registros se regresan
    tipo : TIPO, String debe ser all, Exports o Imports
        DESCRIPCION. Decide si se filtra por exportaciones, importaciones o se cuantan ambos

    Returns
    -------
    rutasF : TIPO, list
        DESCRIPCION. Regresa lista con valores de rutas ordenados

    """
    rutas = {}
    rutasF = []
    #Recorrer los registros
    for linea in registros:
        if linea["direction"] == tipo or tipo == 'all': #comprobar si se hacen todos los movimientos o uno en especial
            if rutasI: #Ver si importa el orden
                nameR = min(linea["origin"], linea["destination"]) + '-' + max(linea["origin"], linea["destination"])
            else:
                nameR = linea["origin"] + '-' + linea["destination"]
            
            if nameR in rutas: #Comporbar si esta guardado
                rutas[nameR]["conteo"] += 1 
                rutas[nameR]["valor"] += int(linea["total_value"])
            else:
                rutas[nameR] = {'conteo': 1, "valor":int(linea["total_value"])}
    #Converir a lista            
    for key, value in rutas.items():
        rutasF.append([key, value])
    #Ordenar la lista
    rutasF.sort(reverse = True, key = lambda x:x[1][orden])
    #Limitar la lista
    rutasF = rutasF[0:limit]
    #Acomodar los datos para regresarlos
    rutasF = [[x[0],x[1][orden]] for x in rutasF]
    return rutasF

def obtenerVehiculos(orden = 'valor', tipo = 'all'):
    """
    obtenerVehiculos
    ------------
    Obtiene transportes utilizados 
    
    Parametros
    ----------
    orden : TIPO, String debe ser valor o conteo
        DESCRIPCION. Indica por que valor ordenar, el numero de veces o el valor comercial
    tipo : TIPO, String debe ser all, Exports o Imports
        DESCRIPCION. Decide si se filtra por exportaciones, importaciones o se cuantan ambos

    Returns
    -------
    vehiculosF : TIPO, list
        DESCRIPCION. Regresa lista con valores de los transportes ordenados

    """
    vehiculos = {}
    vehiculosF = []
    #Recorrer los registros
    for linea in registros:
        if linea["direction"] == tipo or tipo == 'all': #Comprobar si se toma encuenta la direccion
            transp = linea["transport_mode"]
            if transp in vehiculos: #Comprobar si ya se guardo
                vehiculos[transp]["conteo"] += 1
                vehiculos[transp]["valor"] += int(linea["total_value"])
            else:
                vehiculos[transp] = {'conteo': 1, "valor":int(linea["total_value"])}
    #Convertir a lista
    for key, value in vehiculos.items():
        vehiculosF.append([key, value])
    #Ordenar
    vehiculosF.sort(reverse = True, key = lambda x:x[1][orden])
    return vehiculosF

def obtenerPaises(tipo = 'all', orden = 'valor'):
    """
    obtenerPaises
    ------------
    Obtiene los paises que mas valor tengan o transacciones
    
    Parametros
    ----------
    orden : TIPO, String debe ser valor o conteo
        DESCRIPCION. Indica por que valor ordenar, el numero de veces o el valor comercial
    tipo : TIPO, String debe ser all, Exports o Imports
        DESCRIPCION. Decide si se filtra por exportaciones, importaciones o se cuantan ambos

    Returns
    -------
    paisesF : TIPO, list
        DESCRIPCION. Regresa lista con valores de rutas ordenados

    """
    paises = {}
    paisesF = []
    for linea in registros:
        if linea["direction"] == tipo or tipo == 'all':
            nameR = linea["origin"]
            
            if nameR in paises:
                paises[nameR]["conteo"] += 1
                paises[nameR]["valor"] += int(linea["total_value"])
            else:
                paises[nameR] = {'conteo': 1, "valor":int(linea["total_value"])}
    for key, value in paises.items():
        paisesF.append([key, value])
    paisesF.sort(reverse = True, key = lambda x:x[1][orden])
    paisesF = [[x[0],x[1][orden]] for x in paisesF]
    return paisesF


def obtenerListaPorcentaje(paisesF, prc = 80):
    """
    obtenerListaPorcentaje
    ------------
    Obtiene los paises que sumen el porcentaje de ventas requerido
    
    Parametros
    ----------
    paisesF : TIPO, List, debe contener la lista de los paises y el valor a comparar
        DESCRIPCION. Lista que contiene los paises a comparar
    prc : TIPO, Int 
        DESCRIPCION. Indica hasta que porcentaje se tienen que mostrar

    Returns
    -------
    listF : TIPO, list
        DESCRIPCION. Regresa lista con paises que acumulen el porcentaje deseado

    """
    tot = sum([x[1] for x in paisesF])
    acum = 0
    listF = []
    for pais in paisesF:
        prcI = (pais[1]/tot)*100
        listF.append([pais[0], pais[1], round(prcI,2)])
        acum += prcI
        if acum > prc:
            break
            
    return listF
print("Rutas tomando en cuenta el valor obtenido Importaciones y Exportaciones")
res = obtenerRutas()
encabezado = ['Ruta','Valor']
print(tabulate(res, headers=encabezado))
print("\nRutas tomando en cuenta el flujo obtenido Importaciones y Exportaciones")
res = obtenerRutas(orden = 'conteo')
encabezado = ['Ruta','Valor']
print(tabulate(res, headers=encabezado))

print("\nRutas tomando en cuenta el valor obtenido Importaciones")
res = obtenerRutas(tipo = 'Imports')
encabezado = ['Ruta','Valor']
print(tabulate(res, headers=encabezado))
print("\nRutas tomando en cuenta el flujo obtenido Importaciones")
res = obtenerRutas(orden = 'conteo', tipo = 'Imports')
encabezado = ['Ruta','Valor']
print(tabulate(res, headers=encabezado))

print("\nRutas tomando en cuenta el valor obtenido Exportaciones")
res = obtenerRutas(tipo = 'Exports')
encabezado = ['Ruta','Valor']
print(tabulate(res, headers=encabezado))
print("\nRutas tomando en cuenta el flujo obtenido Exportaciones")
res = obtenerRutas(orden = 'conteo', tipo = 'Exports')
encabezado = ['Ruta','Valor']
print(tabulate(res, headers=encabezado))


print("\nVehiculos usados en la compañia")
res = [[x[0], x[1]["conteo"], x[1]["valor"]] for x in obtenerVehiculos()]
encabezado = ['Transporte','Conteo','Valor']
print(tabulate(res, headers=encabezado))

print("\nPaises que aportan el 80% de valor total")
res = obtenerListaPorcentaje(obtenerPaises())
encabezado = ['Pais','Valor','Porcentaje']
print(tabulate(res, headers=encabezado))
print("\nPaises que aportan el 80% de valor Importes")
res = obtenerListaPorcentaje(obtenerPaises('Imports'))
encabezado = ['Pais','Valor','Porcentaje']
print(tabulate(res, headers=encabezado))
print("\nPaises que aportan el 80% de valor Exportaciones")
res = obtenerListaPorcentaje(obtenerPaises('Exports'))
encabezado = ['Pais','Valor','Porcentaje']
print(tabulate(res, headers=encabezado))

print("\nPaises que aportan el 80% de flujo total")
res = obtenerListaPorcentaje(obtenerPaises(orden = 'conteo'))
encabezado = ['Pais','Transacciones','Porcentaje']
print(tabulate(res, headers=encabezado))
print("\nPaises que aportan el 80% de flujo Importes")
res = obtenerListaPorcentaje(obtenerPaises('Imports', 'conteo'))
encabezado = ['Pais','Transacciones','Porcentaje']
print(tabulate(res, headers=encabezado))
print("\nPaises que aportan el 80% de flujo Exportaciones")
res = obtenerListaPorcentaje(obtenerPaises('Exports', 'conteo'))
encabezado = ['Pais','Transacciones','Porcentaje']
print(tabulate(res, headers=encabezado))


    



