import numpy as np
import matplotlib.pyplot as plt
from geopy import distance
import seaborn as sns # https://github.com/mwaskom/seaborn/issues/1307
import pandas as pd
from UAV import UAV
import threading
from time import sleep
from sklearn.neighbors import NearestNeighbors


altura_vuelo_uav = 20
fraccion_solape = 0.4
caracteristicas_sensor = {'ancho_sensor':1, 'distancia_focal':0.5, 'angulo_inclinacion':90}

#Valores recibidos de NodeJS.
northWest = [42.17226800508796, -8.679393394103954] #(latitud, longitud)
northEast = [42.17226800508796, -8.678347434154489] #(latitud, longitud)
southWest = [42.17112037162631, -8.679393394103954] #(latitud, longitud)
southEast = [42.17112037162631, -8.678347434154489] #(latitud, longitud)



posicion_base = [0,0] # TODO: obtener



'''
SUPOSICIONES:
- Las cámaras de los drones tienen las mismas características y están posicionadas con el mismo ángulo de inclinación.
- Los drones vuelan a la misma altura y velocidad.
- Todos los drones que participan en la misión son lanzados desde la base.


VERSION 0:
- A mayores, para una primera versión no se va a considerar la orientación del dron para tomar las imagenes porque se 
    supone que van a estar orientadas hacia el suelo.
- Por como están diseñadas las conexiones del grafo los movimientos de un nodo a otro son solo en un eje (x ò y).
'''

def getMeters(geoCoordA, geoCoordB):
    '''    
    Calcula la distancia en metros entre dos coordenadas geográficas.

    Entradas:
        geoCoordA: (lat, long).
        geoCoordB: (lat, long).

    Salida:
        distance: (float), distancia en metros entre coordeadas geográficas.
    '''
    return distance.vincenty(geoCoordA,geoCoordB).meters


def cartToGeoCoord(x_meters, y_meters, origenCoordGeo):
    '''
    Convierte coordenadas cartesianas a coordenadas geométricas

    Entradas
        x_meters: (float), indica cuántos metros en el eje x nos desplazamos con respecto al origen de 
        coordenadas.
        y_meters: (float), indica cuántos metros en el eje y nos desplazamos con respecto al origen de 
        coordenadas.
        origenCoordGeo: (lat,long), indica cual es el punto de origen de coordenadas, el cuál sirve para 
        relaccionar la posición real de la zona a cubrir con la distancia en metros teórica hasta el 
        siguiente destino.

    Salidas
        latitud: (float), latitud real del punto desplazado los metros desados en el eje x
        longitud: (float), longitud real del punto desplazado los metros desados en el eje 
    '''
    geoCoord = distance.vincenty(meters=x_meters).destination(origenCoordGeo, 90)
    geoCoord = distance.vincenty(meters=y_meters).destination(geoCoord, 0)
    
    return geoCoord.latitude, geoCoord.longitude


def calcularFootprint (altura_vuelo_uav, ancho_sensor, distancia_focal, angulo_inclinacion):
    '''
    Calcula el número de metros que recoge la cámara del UAV.

    Parámetros
    ------------
    altura_vuelo_uav : float
        Distancia en metros del dron al suelo del área que se quiere cubrir.
    ancho_sensor : float
        Ancho del sensor de imagen en milimetros.
    distancia_focal : float
        Distancia focal de la cámara en milimetros.
    angulo_inclinacion : float
        Ángulo de inclinación de la cámara respecto al UAV en posición horizontal.

    Returns
    ---------
    float
        Número de metros capturados por la cámara del UAV.
    '''
    # TODO: calcular para angulo de inclinación distinto de 90º
    return altura_vuelo_uav * (ancho_sensor / distancia_focal)


def calcularNodosGrafo (divisiones_x, divisiones_y):
    '''
    Devuelve una lista con las coordenadas de cada nodo del grafo.
    '''
    #return [(pos_x, pos_y) for pos_x in divisiones_x for pos_y in divisiones_y]
    nodos = []
    id = 0
    for pos_x in divisiones_x:
        fila_nodos = []
        for pos_y in divisiones_y:
            fila_nodos.append([id, [pos_x, pos_y]])
            id += 1
        nodos.append(fila_nodos)
    return nodos


def distancia (pos1, pos2):
    '''
    Devuelve la distancia entre dos vectores
    '''
    # TODO: solucion temporal -> buscar forma de calculo mas rapida
    return np.sqrt(np.sum(np.power((np.array(pos1)-np.array(pos2)),2)))


def calcularGrafo (nodos):
    '''
    Construye el grafo.

    Parámetros
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
        for n_columna in range (n_columnas):

            grafo[nodos[n_fila][n_columna][0]] = nodos[n_fila][n_columna][1]

            for i, j in [[n_fila + 1, n_columna], [n_fila - 1, n_columna], [n_fila, n_columna + 1], [n_fila, n_columna - 1]]:
                if i < 0 or j < 0 or i >= n_filas or j >= n_columnas: # No existe el nodo
                    continue
                pos_extremo1 = nodos[n_fila][n_columna][1]
                pos_extremo2 = nodos[i][j][1]
                list_edges.append([pos_extremo1, pos_extremo2, distancia(pos_extremo1, pos_extremo2)])

    return grafo, np.array(list_edges)


def dibujarNodos (grafo, aspect, size = 9):
    df_nodos_grafo = pd.DataFrame(grafo, ['x', 'y']).transpose()
    grid = sns.lmplot('x', 'y', data=df_nodos_grafo, fit_reg=False, scatter_kws={"s": 100}, aspect = aspect, size = size)

    for nodo in grafo.items():
        grid.axes[0][0].text(nodo[1][0] + 1, nodo[1][1] + 1, str(nodo[0]), fontsize=14, fontweight='bold')

    return grid


def dibujarEdges (grid, color='k', style = '--'):
    for edge in edges:
        grid.axes[0][0].plot((edge[0][0], edge[1][0]), (edge[0][1], edge[1][1]), color+style)

        pto_medio = (np.array(edge[0]) + np.array(edge[1]))/2 + np.array([1,1])
        grid.axes[0][0].text(pto_medio[0], pto_medio[1], str(int(edge[2])), transform=grid.axes[0][0].transData)

    return grid


def dibujarGrafo (grafo, edges, aspect, size = 9):
    grid = dibujarNodos(grafo, aspect, size)
    dibujarEdges(grid)
    
    return grid


def escalar (valor, old_min, old_max, new_min, new_max):
    '''
    '''
    return ((new_max - new_min) * (valor - old_min) / (old_max - old_min)) + new_min    


def dibujarNodosEnImagen (grafo, x, y, ruta_img = './area.png', size = 9):
    img = plt.imread(ruta_img)
    new_y, new_x, _ = img.shape

    old_min = np.array([0,0])
    new_min = np.array([0,0])

    old_max = np.array([x,y])
    new_max = np.array([new_x, new_y])

    new_grafo = {}
    for item in grafo.items():
        new_grafo[item[0]] = escalar(item[1], old_min, old_max, new_min, new_max)


    print(pd.DataFrame(grafo, ['x', 'y']).transpose())

    print('\n\n')
    print(pd.DataFrame(new_grafo, ['x', 'y']).transpose())


    grid = dibujarNodos(new_grafo, x/y)
    plt.imshow(img, origin='lower')

    return grid, old_min, old_max, new_min, new_max


def calcularDivisiones(lado, footprint, fraccion_solape):
    '''
    '''
     
    num_filas = int(np.ceil(lado / (footprint * (1 - fraccion_solape))))
    distancia = lado/num_filas

    return [i * distancia - (distancia / 2) for i in range (1, num_filas + 1)]


def getNodosGrafo (): # def calcularGrafo (x, y, altura_vuelo_uav, caracteristicas_sensor):
    x = getMeters(southWest,southEast)
    y = getMeters(southWest,northWest)

    footprint = calcularFootprint (altura_vuelo_uav, caracteristicas_sensor['ancho_sensor'], 
                                   caracteristicas_sensor['distancia_focal'], caracteristicas_sensor['angulo_inclinacion'])

    divisiones_x = calcularDivisiones (x, footprint, fraccion_solape)
    divisiones_y = calcularDivisiones (y, footprint, fraccion_solape)

    nodos = calcularNodosGrafo (divisiones_x, divisiones_y)
    grafo, edges = calcularGrafo(nodos)
    
    return grafo


def getCromosomaNearestNeighbourRR (nodos, drones, nbrs):
    ciudades_dron = {}
    cromosoma = []
    ciudades_visitadas = []

    posiciones_actuales = {}
    for dron in drones:
        posiciones_actuales[dron.id] = dron.posicion_actual
        ciudades_dron[dron.id] = []

    while len(ciudades_visitadas) < len(nodos):
        for dron in drones:
            _, indices = nbrs.kneighbors([posiciones_actuales[dron.id]])

            for indice in indices[0]:
                if indice not in ciudades_visitadas:
                    ciudades_dron[dron.id].append(indice)
                    posiciones_actuales[dron.id] = nodos[indice]
                    ciudades_visitadas.append(indice)
                    break

    num_ciudades_dron = []
    for ciudades in ciudades_dron.items():
        for ciudad in ciudades[1]:
            cromosoma.append(ciudad)
        num_ciudades_dron.append(len(ciudades[1]))

    for n_ciudades in num_ciudades_dron:
        cromosoma.append(n_ciudades)

    return cromosoma


def getPoblacionNearestNeighbour (nodos, drones, nbrs):
    cromosoma, ciudades_dron = [], []
    for dron in drones:
        posicion_actual = dron.posicion_actual
        vecinos_dron = 0
        while vecinos_dron < n_vecinos and len(cromosoma) < len(nodos):
            _, indices = nbrs.kneighbors([posicion_actual])
            for indice in indices[0]:
                if indice not in cromosoma:
                    cromosoma.append(indice)
                    posicion_actual = nodos[indice]
                    vecinos_dron += 1
                    break

        ciudades_dron.append(vecinos_dron)

    for n_ciudades in ciudades_dron:
        cromosoma.append(n_ciudades)

    return cromosoma


def getCromosomaRandom (nodos, drones):
    cromosoma = list(nodos.keys())
    np.random.shuffle(cromosoma)
    
    ciudades = [0]
    while 0 in ciudades: # Asegurar que todos los UAVs van al menos a un nodo
        ciudades = np.round(np.random.dirichlet(np.ones(len(drones)),size=1)*len(nodos)).astype(int)

    for ciudad in ciudades[0]:
        cromosoma.append(ciudad)

    return cromosoma


def getFitnessCromosoma (cromosoma, posicion_inicial_drones, nodos):
    ciudades_dron = []
    last_index = 0
    for n_ciudades_dron in cromosoma[-len(posicion_inicial_drones):]:
        ciudades_dron.append(cromosoma[last_index:last_index + n_ciudades_dron])
        last_index += n_ciudades_dron

    fitness = 0
    for i, posicion_actual_dron in enumerate(posicion_inicial_drones):
        
        distancia_recorrida_dron = 0
        for ciudad in ciudades_dron[i]:
            distancia_recorrida_dron += distancia(posicion_actual_dron, nodos[ciudad])
            posicion_actual_dron = nodos[ciudad]

        fitness += distancia_recorrida_dron

    return fitness


def main ():
    nodos = getNodosGrafo()

    drones = [UAV (0, caracteristicas_sensor, nodos[0], color='m', style='--'), 
              UAV (1, caracteristicas_sensor, nodos[21], color='g', style='--'),
              UAV (2, caracteristicas_sensor, nodos[2], color='b', style='--'),
              UAV (3, caracteristicas_sensor, [0.,0.], color='y', style='--')]
    
    for dron in drones:
        print("Dron", dron.id, "- posicion inicial ", dron.posicion_actual)

    n_vecinos = len(nodos) // len(drones)
    nbrs = NearestNeighbors(n_neighbors=len(nodos), algorithm='auto').fit(list(nodos.values()))

    cromosoma = getCromosomaRandom(nodos, drones)
    print(cromosoma)

    posiciones_actuales = []
    for dron in drones:
        posiciones_actuales.append(dron.posicion_actual)

    print("Fitness:", getFitnessCromosoma(cromosoma, posiciones_actuales, nodos))

    dibujarNodos(nodos,1)
    plt.show()



if __name__ == '__main__':
    main()