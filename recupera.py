'''
Código inicial para recuperar información de PostgreSQL a traves de psycopg2 https://pypi.org/project/psycopg2/
Adicionalmente se encuentra en GitHUB: https://github.com/alffore/diccionario

AAFR alffore@gmail.com
2019-04-08
'''


import psycopg2
import psycopg2.extras

conn_dic = psycopg2.connect('dbname=DICSR host=127.0.0.1 port=5432 user=userrenic')


def obtenDatos():

    query="SELECT * FROM tablatfr Limit 1000"
    try:
        cursor = conn_dic.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(query)
        res = cursor.fetchall()
        cursor.close()
        return res
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


# Comienza el codigo

res = obtenDatos()

print(res)

