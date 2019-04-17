'''
Código que busca expresar y mostrar la posible correlacion de terminos
Va a pintar un conjunto de divs

AAFR, alffore@gmail.com
2019-04-16
'''

import psycopg2
import psycopg2.extras
import math

conn_dic = psycopg2.connect('dbname=DICSR host=127.0.0.1 port=5432 user=userrenic')


def procesaentrada(ad):
    sid = 'i' + str(ad[0])
    alfa = math.pi / 4
    r = round(255 * (1 + math.sin(ad[1])) / 2)
    g = round(255 * (1 + math.sin(ad[1] + alfa)) / 2)
    b = round(255 * (1 + math.sin(ad[1] + 3 * alfa)) / 2)

    color = 'rgb(' + str(r) + ',' + str(g) + ',' + str(b) + ');'
    return '<div class="c" id="' + sid + '" style="background-color:' + color + '">'


def imprimeHeader():
    buff = '<html><head><style>  * {padding: 0px; margin: 0px;} .contendor{display: flex; width: 100%; height: ' \
           '1200px; flex-wrap: wrap;} .c{width: 2px; height: 2px;}</style></head><body><div class="contenedor">'
    return buff


def imprimeFooter():
    return '</div></body></html>'


print(imprimeHeader())

query = "SELECT tablatfr_id,peso FROM tablatfr WHERE trim(cadena) !~*'^$'"
try:
    cursor = conn_dic.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(query)

    for res in cursor:
        # print(res)
        print(procesaentrada(res))

    cursor.close()

except (Exception, psycopg2.DatabaseError) as error:
    print(error)

conn_dic.close()

print(imprimeFooter())
