''''
Algoritmo que cuenta todas las palabras y hace una estadistica en la BD
'''

import psycopg2
import psycopg2.extras

conn_dic = psycopg2.connect('dbname=DICSR host=127.0.0.1 port=5432 user=userrenic')
conn_sic = psycopg2.connect('dbname=nuevadbrenic host=127.0.0.1 port=5432 user=userrenic')

diccionario = {}


def procesaentrada(ares):
    acad = ares[0].split(' ')
    peso = ares[1]

    for aux in acad:
        cad = aux.strip()
        if len(cad) > 0:
            if len(diccionario) == 0:
                diccionario[cad] = peso
            elif cad in diccionario:
                diccionario[cad] = (diccionario[cad] + peso)
            else
                diccionario[cad] = peso

    return

def procesaEntradaG(cad):
    cad=cad.strip()

    if cad in diccionario:
        diccionario[cad] = diccionario[cad]+1
    else
        diccionario[cad] = 1

    return


def insertaDatos():
    for cad in diccionario:
        peso = diccionario[cad]
        query='INSERT INTO diccionario (cadena,peso) VALUES (\''+cad+'\','+str(peso)+');'
        print(query)
    return


'''Método que procesa entradas de las busquedas'''
query = "SELECT cadena,peso FROM tablatfr WHERE trim(cadena) !~*'^$' limit 1000"

try:
    cursor = conn_dic.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(query)

    for res in cursor:
        procesaentrada(res)

    cursor.close()

except (Exception, psycopg2.DatabaseError) as error:
    print(error)


'''Método que procesa entras de la BD del SIC-RENIC'''
aux_campos=['tabla','nombre','campo0','campo1','campo2','municipio','estado']
query = "SELECT tabla,nombre,campo0,campo1,campo2,municipio,estado FROM mvbusquedas limit 10"

try:
    cursor_sic = conn_sic.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor_sic.execute(query)

    for res in  cursor_sic.fetchall():
        for c in aux_campos:
            if c!='estado' or c!='municipio':
                apalabras = res[c].split(' ')
                for palabra in apalabra:
                    if len(palabra) >0:
                        procesaEntradaG(palabra)
            else
                procesaEntradaG(res[c])

except (Exception, psycopg2.DatabaseError) as error:
    print(error)



conn_dic.close()

insertaDatos()