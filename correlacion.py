'''
Código que busca expresar y mostrar la posible correlacion de terminos
Va a pintar un conjunto de divs

AAFR, alffore@gmail.com
2019-04-16
'''

import psycopg2
import psycopg2.extras

import math


def procesaentrada(ad):
    sid = 'i' + str(ad[0])
    alfa =math.pi/4
    r=round(255*sin(ad[1])/2)
    g=round(255*sin(ad[1]+alfa)/2)
    b=round(255*sin(ad[1]+2*alfa)/2)
    color = 'rgb('+str(r)+','+str(g)+','+str(b)+')'
    return '<div id="' + sid + '" style="background-color:' + color + '">'


conn_dic = psycopg2.connect('dbname=DICSR host=127.0.0.1 port=5432 user=userrenic')

query = "SELECT tablatfr_id,peso FROM tablatfr WHERE trim(cadena) !~*'^$' LIMIT 10"
try:
    cursor = conn_dic.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(query)

    for res in cursor:
        print(res)
        print(procesaentrada(res))

    cursor.close()

except (Exception, psycopg2.DatabaseError) as error:
    print(error)

conn_dic.close()
