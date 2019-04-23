# coding=utf-8
'''
Este código muestra todos los campos y valores implicados en la busqueda y los terminos empleados (solo para registros
públicos)

@author AAFR <alffore@gmail.com>
'''

import psycopg2
import psycopg2.extras

conn_dic = psycopg2.connect('dbname=DICSR host=127.0.0.1 port=5432 user=userrenic')
conn_sic = psycopg2.connect('dbname=nuevadbrenic host=127.0.0.1 port=5432 user=userrenic')


def recuperaCadenas(tabla, id):
    cadesal = ' '
    query_cad = "SELECT cadena FROM tablatfr WHERE trim(cadena) !~*'^$' AND tabla='" + tabla + "' AND tabla_id=" + \
                str(id) + " ORDER BY peso"
    try:
        cursor_dic2 = conn_dic.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor_dic2.execute(query_cad)

        for res2 in cursor_dic2.fetchall():
            cadesal = cadesal.join([res2['cadena']])

        cursor_dic2.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return ''
    return cadesal


def recuperaDSIC(tabla, id):
    query_sic = "SELECT nombre,campo0,campo1,campo2,municipio,estado FROM mvbusquedas WHERE tabla='" + tabla + \
                "' AND id=" + str(id)
    try:
        cursor_sic = conn_sic.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor_sic.execute(query_sic)
        ren = cursor_sic.fetchone()
        cursor_sic.close()
        return ren
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return {}


def procesaentrada(res):
    ren = recuperaDSIC(res['tabla'], res['tabla_id'])

    if ren is not None:
        d = dict(res.items(), ren.items())
    else:
        d = res

    buff = '<tr>'
    for c in ['tabla_id', 'tabla', 'peso', 'cadena', 'nombre', 'campo0', 'campo1', 'campo2', 'municipio', 'estado']:
        if c == 'cadena':
            buff += '<td>' + recuperaCadenas(res['tabla'], res['tabla_id']) + '</td>'
        else:
            buff += '<td>' + str(d[c]) + '</td>'
    buff += '</tr>'
    return buff


def imprimeHeader():
    buff = '<html><head><style> *{font-family: Arial; font-size: 10px;} .contenedor{} </style></head>' \
           '<body><table class="contenedor">'
    buff =buff + '<tr><th>tabla_id</th><th>tabla</th><th>peso</th><th>cadenas</th><th>nombre</th><th>campo0</th><th>campo1' \
            '</th><th>campo2</th><th>municipio</th><th>estado</th></tr>'
    return buff


def imprimeFooter():
    return '</table></body></html>'


imprimeHeader()

query = "SELECT tablatfr_id,tabla,tabla_id,peso FROM tablatfr WHERE trim(cadena) !~*'^$' ORDER BY peso DESC, tablatfr_id Limit 10"
try:
    cursor_dic = conn_dic.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor_dic.execute(query)

    for res in cursor_dic.fetchall():
      #  print(res)    
       print(procesaentrada(res))

    cursor_dic.close()

except (Exception, psycopg2.DatabaseError) as error:
    print(error)

conn_dic.close()
conn_sic.close()

imprimeFooter()
