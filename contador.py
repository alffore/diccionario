''''
Algoritmo que cuenta todas las palabras y hace una estadistica en la BD
'''

import psycopg2
import psycopg2.extras

conn_dic = psycopg2.connect('dbname=DICSR host=127.0.0.1 port=5432 user=userrenic')

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


def insertaDatos():
    for cad in diccionario:
        peso = diccionario[cad]
        query='INSERT INTO diccionario (cadena,peso) VALUES (\''+cad+'\','+str(peso)+');'
        print(query)
    return

query = "SELECT cadena,peso FROM tablatfr WHERE trim(cadena) !~*'^$' limit 1000"
try:
    cursor = conn_dic.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(query)

    for res in cursor:
        procesaentrada(res)

    cursor.close()

except (Exception, psycopg2.DatabaseError) as error:
    print(error)

conn_dic.close()

insertaDatos()