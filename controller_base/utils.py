import numpy as np
from geopy import distance
import seaborn as sns # https://github.com/mwaskom/seaborn/issues/1307
import pandas as pd
import zmq
import json
import os

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:7777")


def getDatosWeb():
    '''
    Recibe valores de NodeJS.
    '''

    message = socket.recv_json()

    json_norte_este = message['norte_este']
    json_sur_oeste = message['sur_oeste']

    norte_este = [json_norte_este['lat'], json_norte_este['lng']]
    norte_oeste = [json_norte_este['lat'], json_sur_oeste['lng']]
    sur_este = [json_sur_oeste['lat'], json_norte_este['lng']]
    sur_oeste = [json_sur_oeste['lat'], json_sur_oeste['lng']]

    altura_vuelo = float(message['altura_vuelo'])
    fraccion_solape = float(message['fraccion_solape'])

    posiciones_base = message['posiciones_base']

    bases_drones = []
    for base in posiciones_base:
       bases_drones.append(base)


    return bases_drones, altura_vuelo, fraccion_solape, norte_oeste, norte_este, sur_oeste, sur_este


def enviarResultado(cromosoma, nodos_geometricas,drones):
    waypoints_drones_list = []
    waypoints_drones = {}
    last_index = 0
    for id_dron, n_ciudades_dron in enumerate(cromosoma[-len(drones):]):
        waipoints_dron = []
        for ciudad in (cromosoma[last_index:last_index + n_ciudades_dron]):
            waipoints_dron.append({'id_nodo': int(ciudad), 'latitud': float(nodos_geometricas[ciudad][0]),
                                   'longitud': float(nodos_geometricas[ciudad][1])})
        waypoints_drones_list.append({'id_dron': int(id_dron), 'waypoints': waipoints_dron})
        last_index += n_ciudades_dron


    socket.send_string(json.dumps(waypoints_drones_list))

    print("lista enviada")
    return


def getMeters(geoCoordA, geoCoordB):
    '''
    Calcula la distancia en metros entre dos coordenadas geograficas.

    Entradas:
        geoCoordA: (lat, long).
        geoCoordB: (lat, long).

    Salida:
        distance: (float), distancia en metros entre coordeadas geograficas.
    '''
    return distance.vincenty(geoCoordA, geoCoordB).meters


def cartToGeoCoord(x_meters, y_meters, origenCoordGeo):
    '''
    Convierte coordenadas cartesianas a coordenadas geometricas

    Entradas
        x_meters: (float), indica cuantos metros en el eje x nos desplazamos con respecto al origen de
        coordenadas.
        y_meters: (float), indica cuantos metros en el eje y nos desplazamos con respecto al origen de
        coordenadas.
        origenCoordGeo: (lat,long), indica cual es el punto de origen de coordenadas, el cual sirve para
        relaccionar la posicion real de la zona a cubrir con la distancia en metros teorica hasta el
        siguiente destino.

    Salidas
        latitud: (float), latitud real del punto desplazado los metros desados en el eje x
        longitud: (float), longitud real del punto desplazado los metros desados en el eje
    '''
    geoCoord = distance.vincenty(meters=x_meters).destination(origenCoordGeo, 90)
    geoCoord = distance.vincenty(meters=y_meters).destination(geoCoord, 0)

    return geoCoord.latitude, geoCoord.longitude


def coordenadasNodosToGeograficas(nodos):
    pass


def calcularFootprint(altura_vuelo_uav, ancho_sensor, distancia_focal, angulo_inclinacion):
    '''
    Calcula el numero de metros que recoge la camara del UAV.

    Parametros
    ------------
    altura_vuelo_uav : float
        Distancia en metros del dron al suelo del area que se quiere cubrir.
    ancho_sensor : float
        Ancho del sensor de imagen en milimetros.
    distancia_focal : float
        Distancia focal de la camara en milimetros.
    angulo_inclinacion : float
        angulo de inclinacion de la camara respecto al UAV en posicion horizontal.

    Returns
    ---------
    float
        Numero de metros capturados por la camara del UAV.
    '''
    # TODO: calcular para angulo de inclinacion distinto de 90 grados
    return altura_vuelo_uav * (ancho_sensor / distancia_focal)


def calcularNodosGrafo(divisiones_x, divisiones_y):
    '''
    Devuelve una lista con las coordenadas de cada nodo del grafo.
    '''
    # return [(pos_x, pos_y) for pos_x in divisiones_x for pos_y in divisiones_y]
    nodos = []
    id = 0
    for pos_x in divisiones_x:
        fila_nodos = []
        for pos_y in divisiones_y:
            fila_nodos.append([id, [pos_x, pos_y]])
            id += 1
        nodos.append(fila_nodos)
    return nodos


def distancia(pos1, pos2):
    '''
    Devuelve la distancia entre dos vectores
    '''
    # TODO: solucion temporal -> buscar forma de calculo mas rapida
    return np.sqrt(np.sum(np.power((np.array(pos1) - np.array(pos2)), 2)))


def calcularGrafoEdges(nodos):
    '''
    Construye el grafo.

    Parametros
    ------------
    nodos: list
        Lista de nodos del grafo

    Returns
    --------
    dict
        Diccionario, key = id, value: posicion
    list
        Lista de conexiones entre nodos y el coste del enlace.
    '''
    grafo = {}
    list_edges = []
    n_filas, n_columnas = len(nodos), len(nodos[0])
    for n_fila in range(n_filas):
        for n_columna in range(n_columnas):

            grafo[nodos[n_fila][n_columna][0]] = nodos[n_fila][n_columna][1]

            for i, j in [[n_fila + 1, n_columna], [n_fila - 1, n_columna], [n_fila, n_columna + 1],
                         [n_fila, n_columna - 1]]:
                if i < 0 or j < 0 or i >= n_filas or j >= n_columnas:  # No existe el nodo
                    continue
                pos_extremo1 = nodos[n_fila][n_columna][1]
                pos_extremo2 = nodos[i][j][1]
                list_edges.append([pos_extremo1, pos_extremo2, distancia(pos_extremo1, pos_extremo2)])

    return grafo, np.array(list_edges)


def getNodos(divisiones_x, divisiones_y, origenCoord):
    '''
    Construye el grafo.

    Parametros
    ------------
    divisiones_x: list
        Divisiones eje x
    divisiones_y : list
        Divisiones eje y

    Returns
    --------
    dict
        Diccionario, key = id, value: posicion
    '''
    nodos_cartesianas, nodos_geometricas = {}, {}
    id = 0
    for pos_x in divisiones_x:
        for pos_y in divisiones_y:
            nodos_cartesianas[id] = [pos_x, pos_y]
            nodos_geometricas[id] = cartToGeoCoord(pos_x, pos_y, origenCoord)
            id += 1
    return nodos_cartesianas, nodos_geometricas


def escalar(valor, old_min, old_max, new_min, new_max):
    '''
    '''
    return ((new_max - new_min) * (valor - old_min) / (old_max - old_min)) + new_min


def calcularDivisionesEje(lado, footprint, fraccion_solape):
    '''
    '''

    num_filas = int(np.ceil(lado / (footprint * (1 - fraccion_solape))))
    distancia = lado / num_filas

    return [i * distancia - (distancia / 2) for i in range(1, num_filas + 1)]


def getNodosGrafo(northWest, northEast, southWest, southEast, altura_vuelo_uav, fraccion_solape, caracteristicas_sensor):
    x = getMeters(southWest, southEast)
    y = getMeters(southWest, northWest)

    footprint = calcularFootprint(altura_vuelo_uav, caracteristicas_sensor['ancho_sensor'],
                                  caracteristicas_sensor['distancia_focal'],
                                  caracteristicas_sensor['angulo_inclinacion'])

    divisiones_x = calcularDivisionesEje(x, footprint, fraccion_solape)
    divisiones_y = calcularDivisionesEje(y, footprint, fraccion_solape)

    nodos_cartesianas, nodos_geometricas = getNodos(divisiones_x, divisiones_y, southWest)

    return nodos_cartesianas, nodos_geometricas


def dibujarNodos (grafo, aspect, size = 9):
    df_nodos_grafo = pd.DataFrame(grafo, ['x', 'y']).transpose()
    grid = sns.lmplot('x', 'y', data=df_nodos_grafo, fit_reg=False, scatter_kws={"s": 100}, aspect = aspect, size = size)

    for nodo in grafo.items():
        grid.axes[0][0].text(nodo[1][0] + 1, nodo[1][1] + 1, str(nodo[0]), fontsize=14, fontweight='bold')

    return grid


def getRutaLogs (combinacion):
    '''
    Crea ruta para guardar logs a partir de parametros ajustables del algoritmo.
    '''
    i = 0
    ruta_logs = './'
    while os.path.exists(ruta_logs):
        ruta_logs = './logs/pob{},nnrr{},nn{},r{},gen{},lim{},posinic{}_v{}/'.format(
                    str(combinacion['n_nearest_rr'] + combinacion['n_nearest'] + combinacion['n_random']),
                    str(combinacion['n_nearest_rr']),
                    str(combinacion['n_nearest']),
                    str(combinacion['n_random']),
                    str(combinacion['n_generaciones']),
                    str(combinacion['limite_generaciones_sin_cambio']),
                    str(combinacion['contar_pos_inicial_en_fitness']),
                    i)
        i += 1
    os.makedirs(ruta_logs)
    return ruta_logs
