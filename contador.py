# coding=utf-8
''''
Algoritmo que cuenta todas las palabras y hace una estadística en la BD

@TODO: Ver + campos en tablas
'''

import psycopg2
import psycopg2.extras
from typing import Any

conn_dic = psycopg2.connect('dbname=DICSR host=127.0.0.1 port=5432 user=userrenic')
conn_sic = psycopg2.connect('dbname=nuevadbrenic host=127.0.0.1 port=5432 user=userrenic')

cardes = '-.,+*{}[]/()?¡!·#º\|:;><{¨^~'

diccionario = {}


def procesaentrada(ares):
    acad = ares[0].split(' ')
    peso = ares[1]

    for aux in acad:
        aux.translate({ord(i): None for i in cardes})
        cad = aux.strip()

        if len(cad) > 0:

            if len(diccionario) == 0:
                diccionario[cad] = peso
            elif cad in diccionario:
                diccionario[cad] = (diccionario[cad] + peso)
            else:
                diccionario[cad] = peso

    return


def procesaEntradaG(cad):
    cad = cad.strip()

    cad.translate({ord(i): None for i in cardes})

    if cad in diccionario:
        diccionario[cad] = diccionario[cad] + 1
    else:
        diccionario[cad] = 1

    return


def insertadatos():
    cursori = conn_dic.cursor()

    for cad in diccionario:
        if cad is None or len(cad) == 0 or len(cad) > 1024:
            continue
        cursori.execute('INSERT INTO diccon (cadena,peso) VALUES (%s,%s)', (cad, diccionario[cad],))

    conn_dic.commit()
    cursori.close()

    return


'''Se procesa entradas de las busquedas'''
query = "SELECT cadena,peso FROM tablatfr WHERE trim(cadena) !~*'^$'"

try:
    cursor = conn_dic.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(query)

    for res in cursor:
        procesaentrada(res)

    cursor.close()

except (Exception, psycopg2.DatabaseError) as error:
    print(error)

'''Se procesa entradas de la BD del SIC-RENIC'''
aux_campos = ['tabla', 'nombre', 'campo0', 'campo1', 'campo2', 'municipio', 'estado']
apalabras = {}
query = "SELECT tabla,nombre,campo0,campo1,campo2,municipio,estado FROM mvbusquedas"

try:
    cursor_sic = conn_sic.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor_sic.execute(query)

    for res in cursor_sic.fetchall():
        for c in aux_campos:
            if c != 'estado' or c != 'municipio':
                if res[c] is not None:
                    apalabras = res[c].split(' ')
                    for palabra in apalabras:
                        if len(palabra) > 0:
                            procesaEntradaG(palabra)
            else:
                procesaEntradaG(res[c])

    cursor_sic.close()

except (Exception, psycopg2.DatabaseError) as error:
    print(error)

insertadatos()

conn_dic.close()
conn_sic.close()
