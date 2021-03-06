""""
Created on 31-07-2019

@author: FJSB

Opciones de ejecución del script en base a los parámetros de la línea de comandos sys.argv

    - 2 parámetros: (ejecuta sobre un único fichero SIN información en el nombre)
        # FICHERO         sys.argv[1]:    "D:\ruta\nombre.txt"
        # ID-ASIGNATURA   sys.argv[2]:    "71901037"

    - 1 parámetro: (ejecuta sobre un único fichero CON información aparte del nombre con guiones bajos cuádruples '___')
        # FICHERO         sys.argv[1]:    "D:\ruta\nombre____ABRV____ID____AÑO.txt"
            - ABRV : nombre corto de la asignatura
            - ID   : identificador UNED de la asignatura
            - ANO  : curso (2017, 2018, 1029, ...)

    - 1 parámetro: (se ejecuta sobre todos los ficheros del directorio con el formato "nombre____ABRV____ID____AÑO.txt")
        # DIRECTORIO      sys.argv[1]:    "D:\ruta\"

"""

import os


def filtrar_parametros(parametros):

    ficheros = []
    id_asignatura = ''
    ruta = ''
    rutaynombre = ''
    rutaynombreyextension = ''

    # N.º de parámetros
    n = len(parametros)

    # Ruta de origen
    # Quita Barra final del directorio
    #   (si existe \" en el parámetro ruta)
    #   (si no existe no hace mucho)
    ruta = os.path.normpath(parametros[1].split('"')[0])
    # Si es una ruta con fichero.TXT
    if '.txt' in ruta.split(os.sep)[len(ruta.split(os.sep)) - 1]:
        ruta = ruta.split(ruta.split(os.sep)[len(ruta.split(os.sep)) - 1])[0]
    else:
        ruta = ruta + os.sep

    # 2 parámetros
    if n == 3:
        print('2 Parámetros: Ruta Fichero + ID')

        # 2 Argumentos por línea de comandos:
        #               FICHERO         sys.argv[1]:    "D:\ruta\nombre.txt"
        #               ID-ASIGNATURA   sys.argv[2]:    "71901037"
        #   "D:\ruta\Python\ParserForos\ParserForos\foros\nombre.txt" "71901037"

        # # FICHERO # #
        # Argumento -1: nombre + extensión
        nombreyextension = os.path.splitext(parametros[1].split(os.sep)[len(parametros[1].split(os.sep))-1])[0]
        # # .EXT # #
        extension = nombreyextension.split('.')[1]
        # Argumento 0: ruta + nombre
        rutaynombre = os.path.splitext(parametros[1])[0]
        # Argumento 1: ruta + nombre + extensión
        rutaynombreyextension = parametros[1]
        # Argumento 2: ID asignatura
        id_asignatura = parametros[2]

        return [{'tipo': n, 'ruta': ruta, 'rutaynombre': rutaynombre, 'rutaynombreyextension': rutaynombreyextension,
                 'nombreyextension': nombreyextension, 'extension': extension,
                 'id_asignatura': id_asignatura, 'abreviatura': None, 'ano': '1900'}]

    # 1 parámetro
    elif n == 2:
        print('1 Parámetro: ruta Directorio')

        # # DIR # #
        # Argumento 0: ruta + nombre
        rutaynombre = os.path.splitext(parametros[1])[0]
        # Argumento 1: ruta + nombre + extensión
        rutaynombreyextension = parametros[1]

        # Argumento 1:
        #   FICHERO     : NOMBRE____ABRV____ID____CURSO
        # Argumento 1:
        #   DIRECTORIO  : D:\ruta\
        nombre = rutaynombre.split('____')

        # FICHERO       : NOMBRE____ABRV____ID____CURSO
        if len(nombre) > 1:
            abrv = nombre[1]
            id_asig = nombre[2]
            if len(nombre) > 3:
                curso = nombre[3]
            else:
                curso = '1900'

            #print(nombre, abrv, id_asig, curso)
            ficheros.append({'tipo': n, 'ruta': ruta, 'rutaynombre': rutaynombre,
                             'rutaynombreyextension': rutaynombreyextension, 
                             'nombreyextension': None, 'extension': None,
                             'id_asignatura': id_asig, 'abreviatura': abrv, 'ano': curso})

        # FICHERO       : D:\ruta\
        else:
            from os import walk
            from os.path import isfile, join

            # Quita Barra final del directorio
            #   (si existe \" en el parámetro ruta)
            #   (si no existe no hace mucho)
            if not os.path.exists(parametros[1]):
                parametros[1] = parametros[1].split('"')[0]

            # print(nombre, abrv, id_asig, curso, extension)
            lista_ficheros = []
            for (dirpath, dirnames, filenames) in walk(parametros[1]):
                lista_ficheros.extend(filenames)
                break

            #print(lista_ficheros)

            # PARA CADA FICHERO #
            for index, fichero in enumerate(lista_ficheros):

                # # .EXT # #
                extension = os.path.splitext(os.path.realpath(join(parametros[1], fichero)))[1]
                # Argumento -1: nombre + extensión
                nombreyextension = fichero
                # Argumento 0: ruta + nombre
                rutaynombre = os.path.splitext(os.path.realpath(join(parametros[1], fichero)))[0]
                # Argumento 1: ruta + nombre + extensión
                rutaynombreyextension = os.path.realpath(join(parametros[1], fichero))

                # with open(join(nombre[0], fichero), 'r', encoding='utf8') as fich:

                # Argumento 1:
                #   FICHERO     : NOMBRE____ABRV____ID____CURSO
                nombre = rutaynombre.split('____')
                #   Fichero utf8.txt
                fichero_utf8 = fichero.split('utf8.tx')

                # FICHERO       : NOMBRE____ABRV____ID____CURSO
                if len(nombre) > 1 and extension == '.txt' and len(fichero_utf8) == 1:
                    abrv = nombre[1]
                    id_asig = nombre[2]
                    if len(nombre) > 3:
                        curso = nombre[3]
                    else:
                        curso = '1900'

                    ficheros.append({'tipo': n, 'ruta': ruta, 'rutaynombre': rutaynombre,
                                     'rutaynombreyextension': rutaynombreyextension,
                                     'nombreyextension': nombreyextension, 'extension': extension,
                                     'id_asignatura': id_asig, 'abreviatura': abrv, 'ano': curso})
                else:
                    ficheros.append({'tipo': n, 'ruta': ruta, 'rutaynombre': rutaynombre,
                                     'rutaynombreyextension': rutaynombreyextension,
                                     'nombreyextension': nombreyextension, 'extension': extension,
                                     'id_asignatura': id_asignatura, 'abreviatura': None, 'ano': '1900'})

            print(ficheros)

        return ficheros
