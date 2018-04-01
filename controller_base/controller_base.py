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

ruta_logs = './logs/prueba/'

INDEX_CROMOSOMA = 0
INDEX_FITNESS = 1


'''
SUPOSICIONES:
- Las cámaras de los drones tienen las mismas características y están posicionadas con el mismo ángulo de inclinación.
- Los drones vuelan a la misma altura y velocidad.

VERSION 0:
- A mayores, para una primera versión no se va a considerar la orientación del dron para tomar las imagenes porque se 
    supone que van a estar orientadas hacia el suelo.
- Todos los drones que participan en la misión son lanzados desde la base.
- Por como están diseñadas las conexiones del grafo los movimientos de un nodo a otro son solo en un eje (x ò y).

VERSION 1:
- Las camaras tienen un grado de inclinación, es necesario orientar al dron para sacar la foto.
- La posición inicial de los drones no tiene porque ser la base.
- El movimiento de los drones no está limitado a un eje.
'''

def getMeters (geoCoordA, geoCoordB):
    '''    
    Calcula la distancia en metros entre dos coordenadas geográficas.

    Entradas:
        geoCoordA: (lat, long).
        geoCoordB: (lat, long).

    Salida:
        distance: (float), distancia en metros entre coordeadas geográficas.
    '''
    return distance.vincenty(geoCoordA,geoCoordB).meters


def cartToGeoCoord (x_meters, y_meters, origenCoordGeo):
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


def calcularDivisiones (lado, footprint, fraccion_solape):
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

    np.random.shuffle(drones)

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

    return cromosoma, getFitnessCromosoma(cromosoma, [dron.posicion_actual for dron in drones], nodos)


def getCromosomaNearestNeighbour (nodos, drones, nbrs):

    np.random.shuffle(drones)

    cromosoma, ciudades_dron = [], []
    n_vecinos = len(nodos) // len(drones)
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

    return cromosoma, getFitnessCromosoma(cromosoma, [dron.posicion_actual for dron in drones], nodos)


def getCromosomaRandom (nodos, drones):
    cromosoma = list(nodos.keys())
    np.random.shuffle(cromosoma) # Orden de ciudades aleatorio
    
    ciudades = [0]
    while 0 in ciudades or sum(ciudades) != len(nodos): # Asegurar que a todos los UAVs se le asigna al menos a un nodo y que se repartan todas las ciudades
        ciudades = np.round(np.random.dirichlet(np.ones(len(drones)),size=1)*len(nodos)).astype(int)[0]

    for ciudad in ciudades:
        cromosoma.append(ciudad)

    return cromosoma, getFitnessCromosoma(cromosoma, [dron.posicion_actual for dron in drones], nodos)


def getDistanciaRecorridaCromosoma (cromosoma, posicion_inicial_drones, nodos):
    '''
    posicion_inicial_drones = [dron.posicion_actual for dron in drones]
    '''
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


def getFitnessCromosoma (cromosoma, posicion_inicial_drones, nodos):
    '''
    El tiempo que tardan en recorrer todos los nodos del grafo es el máximo de los tiempos que tardan los drones en hacer su ruta.
    Asumiendo que todos los drones van a la misma velocidad, se calcula el fitness como el máximo de las distancias recorridas por cada UAV.
    Para este problema: Mayor fitness -> Peor cromosoma.
    '''
    ciudades_dron = []
    last_index = 0
    for n_ciudades_dron in cromosoma[-len(posicion_inicial_drones):]:
        ciudades_dron.append(cromosoma[last_index:last_index + n_ciudades_dron])
        last_index += n_ciudades_dron

    distancias_recorridas_drones = []
    for i, posicion_actual_dron in enumerate(posicion_inicial_drones):
        distancia_recorrida_dron = 0
        for ciudad in ciudades_dron[i]:
            distancia_recorrida_dron += distancia(posicion_actual_dron, nodos[ciudad])
            posicion_actual_dron = nodos[ciudad]
        distancias_recorridas_drones.append(distancia_recorrida_dron)

    return 2* max(distancias_recorridas_drones) + np.mean(distancias_recorridas_drones) #+ max(distancias_recorridas_drones) / np.mean(distancias_recorridas_drones) # Se suma fator para tener en cuenta también los recorridos de los otros drones


def dibujarRutasFitnessCromosoma (nodos, drones, cromosoma, fitness, show = True, ruta_guardar = None):
    '''
    '''

    font =  {'family': 'serif',
        'color':  'darkred',
        'weight': 'normal',
        'size': 16,
        }

    grid = dibujarNodos(nodos, aspect = max(np.array(list(nodos.values()))[:,0]) / max(np.array(list(nodos.values()))[:,1]))

    plt.text(-5,-5, 'fitness: {}'.format(fitness), fontdict=font)

    font['size'] = 9
    plt.text(-12,-12, '{}'.format(str(cromosoma)), fontdict=font)

    n_drones = len(drones)
    ultimo_indice = 0
    for i, dron in enumerate(drones):

        n_ciudades = cromosoma[-(n_drones - i)]
        ciudades =  cromosoma[ultimo_indice:ultimo_indice+n_ciudades]

        origen = dron.posicion_actual
        for ciudad in ciudades:
            destino = nodos[ciudad]
            grid.axes[0][0].plot((origen[0], destino[0]), (origen[1], destino[1]), '{}{}'.format(dron.color, dron.style))
            origen = destino
        
        ultimo_indice += n_ciudades

    if ruta_guardar is not None:
        plt.savefig(ruta_guardar)
    
    if show:
        plt.show()

    plt.clf()
    plt.close('all')


def getFitnessPoblacion (poblacion_inicial, drones, nodos):
    '''
    Mayor fitness -> menor distancia recorrida
    '''
    #return 1 / np.array([getDistanciaRecorridaCromosoma(cromosoma, [dron.posicion_actual for dron in drones], nodos) for cromosoma in poblacion_inicial])
    #return np.array([getFitnessCromosoma(cromosoma, [dron.posicion_actual for dron in drones], nodos) for cromosoma in poblacion_inicial])
    return [getFitnessCromosoma(cromosoma, [dron.posicion_actual for dron in drones], nodos) for cromosoma in poblacion_inicial]


def selectionRouletteWheel (fitness):
    '''
    Roulette-wheel selection

    Devuelve los indices de los cromosomas seleccionados.
    '''
    probs_ruleta = fitness / sum(fitness)
    
    padres = []
    while len(padres) != 2:
        p = np.random.uniform()
        for index, prob in enumerate(probs_ruleta):
            if index in padres:
                continue
            if p <= 0:
                padres.append(index)
                break
            p -= prob

    return padres


def selectionRankRouletteWheel (fitness):
    '''
    Rank-based roulette-wheel selection
    # https://stackoverflow.com/questions/20290831/how-to-perform-rank-based-selection-in-a-genetic-algorithm
    '''
    n = len(fitness)
    sum_rank = n * (n + 1) / 2 # Fórmula de Gauss para obtener la suma de todos los rankings (suma de enteros de 1 a N):

    probs_ruleta = [-1 for _ in range (len(fitness))]
    for ranking, index_ruleta in enumerate(np.argsort(np.array(fitness))):
        probs_ruleta[index_ruleta] = (n - ranking) / sum_rank

    padres = []
    while len(padres) != 2:
        p = np.random.uniform()
        for index, prob in enumerate(probs_ruleta):
            if index in padres:
                continue
            if p <= 0:
                padres.append(index)
                break
            p -= prob

    return padres


def crossoverTCX (madre, padre, n_drones):
    '''
    Madre/padre: [ciudad_1, ciudad_2, ..., ciudad_n, ciudades_dron_1, ..., ciudades_dron_m]
    Ciudades asignadas: [ciudades_dron_1, ..., ciudades_dron_m]
    Segmento: [ciudad_1, ciudad_2, ciudad_3] para ciudades_dron_1 = 3
    Gen: ciudad_i
    '''
    new_cromosoma = []
    genes_guardados = []

    segmento = madre[-n_drones:]
    ciudades_drones = [[] for i in range(n_drones)]

    # Selección aleatoria de un sub-segmento para cada dron:
    pos_inicio_segmento_actual = 0
    for m in range(-n_drones, 0): # Recorremos de -n_drones a -1 -> acceder a las posiciones de número de ciudades del cromosoma por orden
        # Tamaño sub-segmento = número aleatorio entre 1 y el número de ciudades asignadas para el dron m:
        if madre[m] != 1:
            segmento[m] = np.random.randint(1, madre[m]) 

        # Elegir posicion de inicio del sub-segmento:
        pos_incio_segmento = pos_inicio_segmento_actual
        if madre[m] > segmento[m]:
            pos_incio_segmento += np.random.randint(0, madre[m] - segmento[m])

        # Guardar los genes del sub-segmento:
        for k in range(pos_incio_segmento, pos_incio_segmento + segmento[m]):
            genes_guardados.append(madre[k])
            ciudades_drones[m].append(madre[k])

        # Posicion de inicio para el siguiente segmento:
        pos_inicio_segmento_actual += madre[m]

    # Mezclar posiciones de los genes de acuerdo con la primera parte del padre:
    genes_sin_guardar = []
    for gen in padre[:-n_drones]:
        if gen not in genes_guardados:
            genes_sin_guardar.append(gen)

    indice_genes_sin_guardar = 0
    n_genes_sin_guardar = len(genes_sin_guardar)
    for m in range(-n_drones, 0): # Recorremos de -n_drones a -1 -> acceder a las posiciones de número de ciudades del cromosoma por orden
        if m != -1: # Si no es el ultimo dron
            n_genes_dron_m = np.random.randint(0, n_genes_sin_guardar)
        else:
            n_genes_dron_m = n_genes_sin_guardar

        # Añadir genes sin guardar:
        for i in range(n_genes_dron_m):
            ciudades_drones[m].append(genes_sin_guardar[indice_genes_sin_guardar + i])

        indice_genes_sin_guardar += n_genes_dron_m
        segmento[m] += n_genes_dron_m
        n_genes_sin_guardar -= n_genes_dron_m

    # Construir el hijo: 
    hijo = np.concatenate([np.concatenate(ciudades_drones).ravel().tolist(), segmento]).ravel().tolist() # TODO: return np.concatenate(....
    return hijo


def mutationSwap (cromosoma, n_drones):
    '''
    Cambia las posiciones de dos genes seleccionados aleatoriamente en ambas partes del cromosoma (por separado).
    '''
    # Swap de dos posiciones aleatorias de la primera parte del cromosoma (lista de ciudades):
    pos_ciudades_1 = pos_ciudades_2 = np.random.randint(0, len(cromosoma[:-n_drones]))
    while pos_ciudades_2 == pos_ciudades_1:
        pos_ciudades_2 = np.random.randint(0, len(cromosoma[:-n_drones]))

    ciudad_1 = cromosoma[pos_ciudades_1]
    ciudad_2 = cromosoma[pos_ciudades_2]

    cromosoma[pos_ciudades_1] = ciudad_2
    cromosoma[pos_ciudades_2] = ciudad_1

    # Swap de dos posiciones aleatorias de la segunda parte del cromosoma (num de ciudades asignadas):
    pos_segmento_1 = pos_segmento_2 = np.random.randint(len(cromosoma[:-n_drones]) + 1, len(cromosoma))
    while pos_segmento_2 == pos_segmento_1:
        pos_segmento_2 = np.random.randint(len(cromosoma[:-n_drones]) + 1, len(cromosoma))

    segmento_1 = cromosoma[pos_segmento_1]
    segmento_2 = cromosoma[pos_segmento_2]

    cromosoma[pos_segmento_1] = segmento_2
    cromosoma[pos_segmento_2] = segmento_1

    return cromosoma


def replacementSteadyState (parent_1, parent_2, child_1, child_2, drones, nodos):
    '''
    Se seleccionan los 2 cromosomas con mayor fitness de entre los padres e hijos.
    '''
    posicion_actual_drones = [dron.posicion_actual for dron in drones]
    poblacion_cromosomas = np.array([parent_1, parent_2, 
                                     np.array([child_1, getFitnessCromosoma(child_1, posicion_actual_drones, nodos)]), 
                                     np.array([child_2, getFitnessCromosoma(child_2, posicion_actual_drones, nodos)])
                                   ])
    fitness_poblacion = poblacion_cromosomas[:,INDEX_FITNESS]
    indices_mejor_a_peor = np.argsort(fitness_poblacion)

    # Devolvemos los mejores, si alguno de los padres esta entre los mejores los devolvemos en la posicion correcta (0 para parent_1 y 1 para parent_2):
    resultado = []
    mejores = indices_mejor_a_peor[:2]

    if 0 in mejores:
        resultado.append(parent_1)

    for indice in mejores:
        if indice != 1 and indice != 0:
            resultado.append(poblacion_cromosomas[indice])

    if 1 in mejores:
        resultado.append(parent_2)
    
    #return poblacion_cromosomas[indices_mejor_a_peor[0]], poblacion_cromosomas[indices_mejor_a_peor[1]]
    return resultado


def GA (nodos, drones, n_iteraciones = 5000, tam_poblacion = 100, perc_nearest_rr= 0.4, perc_nearest = 0.4, 
        perc_random = 0.2, prob_crossover = 0.85, prob_mutation = 0.01, limite_iteraciones_sin_cambio = 1000):

    dir_logs = '{},{},{},{},{},{},{}'.format(n_iteraciones, tam_poblacion, perc_nearest_rr, perc_nearest, perc_random, prob_crossover, prob_mutation)
    best_cromosoma = None
    iteraciones_sin_cambio = 0

    # Poblacion inicial:
    nbrs = NearestNeighbors(n_neighbors=len(nodos), algorithm='auto').fit(list(nodos.values()))
    poblacion = [getCromosomaRandom(nodos, drones) for i in range(int(tam_poblacion*perc_random))]
    poblacion += [getCromosomaNearestNeighbourRR(nodos, drones, nbrs) for i in range(int(tam_poblacion*perc_nearest_rr))]
    poblacion += [getCromosomaNearestNeighbour(nodos, drones, nbrs) for i in range(int(tam_poblacion*perc_nearest))]
    poblacion = np.array(poblacion)

    np.random.shuffle(poblacion)

    # Iterar:
    for iteracion in range(n_iteraciones):
        if iteraciones_sin_cambio >= limite_iteraciones_sin_cambio:
            print(limite_iteraciones_sin_cambio, ' iteraciones sin cambio -> fin')
            return best_cromosoma[INDEX_CROMOSOMA], best_cromosoma[INDEX_FITNESS]

        # Crossover:
        if prob_crossover >= np.random.random():
            # Selection:
            index_madre, index_padre = selectionRankRouletteWheel (poblacion[:,INDEX_FITNESS])

            # Crossover
            cromosoma_hijo_1 = crossoverTCX (poblacion[index_madre][INDEX_CROMOSOMA], poblacion[index_padre][INDEX_CROMOSOMA], len(drones))
            cromosoma_hijo_2 = crossoverTCX (poblacion[index_padre][INDEX_CROMOSOMA], poblacion[index_madre][INDEX_CROMOSOMA], len(drones))

            # Replacement:
            madre, padre = replacementSteadyState(poblacion[index_madre], poblacion[index_padre], 
                                                  cromosoma_hijo_1, cromosoma_hijo_2, drones, nodos)
            poblacion[index_madre] = madre
            poblacion[index_padre] = padre

        # Mutacion:
        if prob_mutation >= np.random.random():
            # Selection:
            index_madre, index_padre = selectionRankRouletteWheel (poblacion[:,INDEX_FITNESS])

            # Mutacion
            cromosoma_hijo_1 = mutationSwap(poblacion[index_madre][INDEX_CROMOSOMA], len(drones))
            cromosoma_hijo_2 = mutationSwap(poblacion[index_padre][INDEX_CROMOSOMA], len(drones))

            # Replacement:
            madre, padre = replacementSteadyState(poblacion[index_madre], poblacion[index_padre], 
                                                  cromosoma_hijo_1, cromosoma_hijo_2, drones, nodos)
            poblacion[index_madre] = madre
            poblacion[index_padre] = padre

        # Ver evolucion:
        new_best_cromosoma = poblacion[list(poblacion[:,INDEX_FITNESS]).index(min(poblacion[:,INDEX_FITNESS]))] # TODO: buscar forma mejor
        if best_cromosoma is None or not np.array_equal(best_cromosoma, new_best_cromosoma):
            dibujarRutasFitnessCromosoma(nodos, drones, new_best_cromosoma[INDEX_CROMOSOMA], new_best_cromosoma[INDEX_FITNESS], show=False, 
                                         ruta_guardar='{}cromosoma_ganador_{}.png'.format(ruta_logs, iteracion))
            iteraciones_sin_cambio = 0
            print('new_best_cromosoma:', new_best_cromosoma[INDEX_CROMOSOMA], 'fitness:', new_best_cromosoma[INDEX_FITNESS])
        else:
            iteraciones_sin_cambio += 1

        best_cromosoma = new_best_cromosoma

        if iteracion % 10 == 0:
            print('[{}] Media fitness: {}'.format(iteracion, poblacion[:,INDEX_FITNESS].mean()))

    return new_best_cromosoma[INDEX_CROMOSOMA], new_best_cromosoma[INDEX_FITNESS]

    
def main ():
    nodos = getNodosGrafo()

    drones = [UAV (0, caracteristicas_sensor, [0.,0.], color='m', style='--'), 
              UAV (1, caracteristicas_sensor, [0.,0.], color='g', style='--'),
              UAV (2, caracteristicas_sensor, [0.,0.], color='b', style='--'),
              UAV (3, caracteristicas_sensor, [0.,0.], color='y', style='--')]

    cromosoma_ganador, fitness = GA(nodos, drones, tam_poblacion = 40,
                                    perc_nearest_rr = 0.25, perc_nearest = 0.25, perc_random=0.50, 
                                    n_iteraciones = 99999999999,limite_iteraciones_sin_cambio = 99999999999)   
    #cromosoma_ganador = GA(nodos, drones)
    dibujarRutasFitnessCromosoma(nodos, drones, cromosoma_ganador, fitness, show = False, ruta_guardar='{}cromosoma_ganador_final.png'.format(ruta_logs))


if __name__ == '__main__':
    main()
