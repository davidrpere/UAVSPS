import numpy as np
import matplotlib.pyplot as plt
import os, utils
from sklearn.neighbors import NearestNeighbors
from datetime import datetime


class AlgoritmoMTSP():
    def __init__(self, nodos, drones):
        '''
        nodos : list
            Lista con el formato: [[id, [pos_x, pos_y]], [id, [pos_x, pos_y]], ...]
        drones : list
            Lista con objetos de la clase UAV.
        '''
        self.INDEX_CROMOSOMA = 0
        self.INDEX_FITNESS = 1

        self.nodos = nodos
        self.drones = drones

        self.nbrs = NearestNeighbors(n_neighbors=len(self.nodos), algorithm='auto').fit(list(self.nodos.values()))

    def inicializarPoblacion(self, n_nearest_rr, n_nearest, n_random):
        self.poblacion = [self.getCromosomaRandom() for i in range(n_random)]
        self.poblacion += [self.getCromosomaNearestNeighbourRR() for i in range(n_nearest_rr)]
        self.poblacion += [self.getCromosomaNearestNeighbour() for i in range(n_nearest)]
        self.poblacion = np.array(self.poblacion)

        np.random.shuffle(self.poblacion)

    def getFitnessCromosoma(self, cromosoma):
        '''
        El tiempo que tardan en recorrer todos los nodos del grafo es el maximo de los tiempos que tardan los drones en hacer su ruta.
        Asumiendo que todos los drones van a la misma velocidad, se calcula el fitness como el maximo de las distancias recorridas por cada UAV.
        Para este problema: Mayor fitness -> Peor cromosoma.
        '''
        ciudades_dron = []
        last_index = 0
        for n_ciudades_dron in cromosoma[-len(self.drones):]:
            ciudades_dron.append(cromosoma[last_index:last_index + n_ciudades_dron])
            last_index += n_ciudades_dron

        distancias_recorridas_drones = []
        if self.contar_pos_inicial_en_fitness:
            for i, posicion_actual_dron in enumerate([dron.posicion_actual for dron in self.drones]):
                distancia_recorrida_dron = 0
                for ciudad in ciudades_dron[i]:
                    distancia_recorrida_dron += utils.distancia(posicion_actual_dron, self.nodos[ciudad])
                    posicion_actual_dron = self.nodos[ciudad]
                distancias_recorridas_drones.append(distancia_recorrida_dron)
        else:
            for i in range(len(self.drones)):
                posicion_actual_dron = self.nodos[ciudades_dron[i][0]]  # Posicion inicial primer nodo del grafo
                distancia_recorrida_dron = 0
                for ciudad in ciudades_dron[i]:
                    distancia_recorrida_dron += utils.distancia(posicion_actual_dron, self.nodos[ciudad])
                    posicion_actual_dron = self.nodos[ciudad]
                distancias_recorridas_drones.append(distancia_recorrida_dron)

        return np.max(distancias_recorridas_drones) + np.sum(distancias_recorridas_drones)

    def getCromosomaNearestNeighbourRR(self):
        '''

        '''
        np.random.shuffle(self.drones)

        ciudades_dron = {}
        cromosoma = []
        ciudades_visitadas = []
        posiciones_actuales = {}
        for dron in self.drones:
            posiciones_actuales[dron.id] = dron.posicion_actual
            ciudades_dron[dron.id] = []

        while len(ciudades_visitadas) < len(self.nodos):
            for dron in self.drones:
                _, indices = self.nbrs.kneighbors([posiciones_actuales[dron.id]])

                for indice in indices[0]:
                    if indice not in ciudades_visitadas:
                        ciudades_dron[dron.id].append(indice)
                        posiciones_actuales[dron.id] = self.nodos[indice]
                        ciudades_visitadas.append(indice)
                        break

        num_ciudades_dron = []
        for ciudades in ciudades_dron.items():
            for ciudad in ciudades[1]:
                cromosoma.append(ciudad)
            num_ciudades_dron.append(len(ciudades[1]))

        for n_ciudades in num_ciudades_dron:
            cromosoma.append(n_ciudades)

        return cromosoma, self.getFitnessCromosoma(cromosoma)

    def getCromosomaNearestNeighbour(self):
        '''

        '''
        np.random.shuffle([dron.id for dron in self.drones])
        ciudades_ya_asignadas = []
        ciudades_dron = [[] for i in range(len(self.drones))]

        n_vecinos = len(self.nodos) // len(self.drones)
        for dron in self.drones:
            posicion_actual = dron.posicion_actual

            while len(ciudades_dron[dron.id]) < n_vecinos and len(ciudades_ya_asignadas) < len(self.nodos):
                _, indices = self.nbrs.kneighbors([posicion_actual])
                for indice in indices[0]:
                    if indice not in ciudades_ya_asignadas:
                        ciudades_ya_asignadas.append(indice)
                        ciudades_dron[dron.id].append(indice)
                        posicion_actual = self.nodos[indice]
                        break

        cromosoma = []
        for ciudades in ciudades_dron:
            for ciudad in ciudades:
                cromosoma.append(ciudad)

        for ciudades in ciudades_dron:
            cromosoma.append(len(ciudades))

        return cromosoma, self.getFitnessCromosoma(cromosoma)

    def getCromosomaRandom(self):
        '''

        '''
        cromosoma = list(self.nodos.keys())
        np.random.shuffle(cromosoma)  # Orden de ciudades aleatorio

        ciudades = [0]
        while 0 in ciudades or sum(ciudades) != len(
                self.nodos):  # Asegurar que a todos los UAVs se le asigna al menos a un nodo y que se repartan todas las ciudades
            ciudades = np.round(np.random.dirichlet(np.ones(len(self.drones)), size=1) * len(self.nodos)).astype(int)[0]

        for ciudad in ciudades:
            cromosoma.append(ciudad)

        return cromosoma, self.getFitnessCromosoma(cromosoma)

    def getCromosomaNearestNeighbourMinsRR(nodos, drones, nbrs):  # TODO -> como asignarPosicionInicialGrafo
        '''

        '''
        pass

    def selectionRouletteWheel(self):
        '''
        Roulette-wheel selection
        Devuelve los indices de los cromosomas seleccionados.
        '''
        fitness = self.poblacion[:, self.INDEX_FITNESS]

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

    def selectionRankRouletteWheel(self):
        '''
        Rank-based roulette-wheel selection
        # https://stackoverflow.com/questions/20290831/how-to-perform-rank-based-selection-in-a-genetic-algorithm
        '''

        fitness = self.poblacion[:, self.INDEX_FITNESS]

        n = len(fitness)
        sum_rank = n * (
                n + 1) / 2  # Formula de Gauss para obtener la suma de todos los rankings (suma de enteros de 1 a N):

        probs_ruleta = [-1 for _ in range(len(fitness))]
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

    def crossoverTCX(self, madre, padre):
        '''
        Madre/padre: [ciudad_1, ciudad_2, ..., ciudad_n, ciudades_dron_1, ..., ciudades_dron_m]
        Ciudades asignadas: [ciudades_dron_1, ..., ciudades_dron_m]
        Segmento: [ciudad_1, ciudad_2, ciudad_3] para ciudades_dron_1 = 3
        Gen: ciudad_i
        '''
        n_drones = len(self.drones)

        new_cromosoma = []
        genes_guardados = []

        segmento = madre[-n_drones:]
        ciudades_drones = [[] for i in range(n_drones)]

        # Seleccion aleatoria de un sub-segmento para cada dron:
        pos_inicio_segmento_actual = 0
        for m in range(-n_drones,
                       0):  # Recorremos de -n_drones a -1 -> acceder a las posiciones de numero de ciudades del cromosoma por orden
            # Tamanho sub-segmento = numero aleatorio entre 1 y el numero de ciudades asignadas para el dron m:
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
        for m in range(-n_drones,
                       0):  # Recorremos de -n_drones a -1 -> acceder a las posiciones de numero de ciudades del cromosoma por orden
            if m != -1:  # Si no es el ultimo dron
                n_genes_dron_m = np.random.randint(0, n_genes_sin_guardar)
            else:
                n_genes_dron_m = n_genes_sin_guardar

            # Anhadir genes sin guardar:
            for i in range(n_genes_dron_m):
                ciudades_drones[m].append(genes_sin_guardar[indice_genes_sin_guardar + i])

            indice_genes_sin_guardar += n_genes_dron_m
            segmento[m] += n_genes_dron_m
            n_genes_sin_guardar -= n_genes_dron_m

        # Construir el hijo: 
        hijo = np.concatenate([np.concatenate(ciudades_drones).ravel().tolist(),
                               segmento]).ravel().tolist()  # TODO: return np.concatenate(....
        return hijo

    def mutationSwap(self, cromosoma):
        '''
        Cambia las posiciones de dos genes seleccionados aleatoriamente en ambas partes del cromosoma (por separado).
        '''
        n_drones = len(self.drones)

        # Swap de dos posiciones aleatorias de la primera parte del cromosoma (lista de ciudades):
        pos_ciudades_1 = pos_ciudades_2 = np.random.randint(0, len(cromosoma[:-n_drones]))
        while pos_ciudades_2 == pos_ciudades_1:
            pos_ciudades_2 = np.random.randint(0, len(cromosoma[:-n_drones]))

        ciudad_1 = cromosoma[pos_ciudades_1]
        ciudad_2 = cromosoma[pos_ciudades_2]

        cromosoma[pos_ciudades_1] = ciudad_2
        cromosoma[pos_ciudades_2] = ciudad_1

        # Swap de dos posiciones aleatorias de la segunda parte del cromosoma (num de ciudades asignadas):
        if (n_drones > 1):
            pos_segmento_1 = pos_segmento_2 = np.random.randint(len(cromosoma[:-n_drones]), len(cromosoma))
            while pos_segmento_2 == pos_segmento_1:
                pos_segmento_2 = np.random.randint(len(cromosoma[:-n_drones]), len(cromosoma))

            segmento_1 = cromosoma[pos_segmento_1]
            segmento_2 = cromosoma[pos_segmento_2]

            cromosoma[pos_segmento_1] = segmento_2
            cromosoma[pos_segmento_2] = segmento_1

        return cromosoma

    def replacementSteadyState(self, parent_1, parent_2, child_1, child_2):
        '''
        Se seleccionan los 2 cromosomas con mayor fitness de entre los padres e hijos.
        '''
        posicion_actual_drones = [dron.posicion_actual for dron in self.drones]
        poblacion_cromosomas = np.array([parent_1, parent_2,
                                         np.array([child_1, self.getFitnessCromosoma(child_1)]),
                                         np.array([child_2, self.getFitnessCromosoma(child_2)])
                                         ])
        fitness_poblacion = poblacion_cromosomas[:, self.INDEX_FITNESS]
        indices_mejor_a_peor = np.argsort(fitness_poblacion)

        # Se devuelven los mejores, si alguno de los padres esta entre los mejores se devuelve en la posicion correcta (0 para parent_1 y 1 para parent_2):
        resultado = []
        mejores = indices_mejor_a_peor[:2]

        if 0 in mejores:
            resultado.append(parent_1)

        for indice in mejores:
            if indice != 1 and indice != 0:
                resultado.append(poblacion_cromosomas[indice])

        if 1 in mejores:
            resultado.append(parent_2)

        return resultado

    def getBestCromosoma(self):  # TODO: buscar forma mejor
        '''
        Devuelve el cromosoma con fitness minimo en la poblacion.
        '''
        return self.poblacion[
            list(self.poblacion[:, self.INDEX_FITNESS]).index(min(self.poblacion[:, self.INDEX_FITNESS]))]

    def getRutasSubOptimas(self, n_generaciones=5000, n_nearest_rr=5, n_nearest=5, n_random=1000,
                           prob_crossover=0.95, prob_mutation=0.01, limite_generaciones_sin_cambio=1000,
                           contar_pos_inicial_en_fitness=True, ruta_logs=None):
        '''
        Devuelve el mejor cromosoma con su fitness tras acabar de iterar todas las generaciones o se cumple el
        limite de generaciones sin cambio.

        n_generaciones : int
            Numero de veces que se iterara en el algoritmo.
        n_nearest_rr : int
            Numero de cromosomas nearest neighbour con round robin.
        n_nearest : int
            Numero de cromosomas nearest neighbour.
        n_random : int
            Numero de cromosomas random.
        prob_crossover : float
            Probabilidad de realizar crossover.
        prob_mutacion : float
            Probabilidad de realizar mutacion despues del crossover.
        limite_generaciones_sin_cambio : int
            Numero de generaciones seguidas sin que haya cambios en el fitness 
            medio tras el que se para la ejecucion del algoritmo.
        contar_pos_inicial_en_fitness : bool
            Si True se tiene en cuenta la distancia de la posicion inicial de 
            los UAVs para el calculo del fitness.
        ruta_logs : str
            Ruta donde guardar imagenes con los mejores cromosomas. 
            Si es None no se guardaran imagenes.
        '''
        best_cromosoma = None
        fitness_medio = 0
        generaciones_sin_cambio = 0

        self.contar_pos_inicial_en_fitness = contar_pos_inicial_en_fitness

        # Poblacion inicial:
        self.inicializarPoblacion(n_nearest_rr, n_nearest, n_random)

        # Iterar generaciones:
        for generacion in range(n_generaciones):
            if generaciones_sin_cambio >= limite_generaciones_sin_cambio:
                print(limite_generaciones_sin_cambio, ' generaciones sin cambio -> fin')
                return best_cromosoma[self.INDEX_CROMOSOMA], best_cromosoma[self.INDEX_FITNESS]

            if prob_crossover >= np.random.random():
                # Selection:
                index_madre, index_padre = self.selectionRankRouletteWheel()

                # Crossover:
                cromosoma_hijo_1 = self.crossoverTCX(self.poblacion[index_madre][self.INDEX_CROMOSOMA],
                                                     self.poblacion[index_padre][self.INDEX_CROMOSOMA])
                cromosoma_hijo_2 = self.crossoverTCX(self.poblacion[index_padre][self.INDEX_CROMOSOMA],
                                                     self.poblacion[index_madre][self.INDEX_CROMOSOMA])

                # Mutation:
                if prob_mutation >= np.random.random():
                    cromosoma_hijo_1 = self.mutationSwap(cromosoma_hijo_1)
                    cromosoma_hijo_2 = self.mutationSwap(cromosoma_hijo_2)

                # Replacement:
                madre, padre = self.replacementSteadyState(self.poblacion[index_madre], self.poblacion[index_padre],
                                                           cromosoma_hijo_1, cromosoma_hijo_2)
                self.poblacion[index_padre] = padre

            # Ver evolucion mejor cromosoma:
            new_best_cromosoma = self.getBestCromosoma()
            if best_cromosoma is None or not np.array_equal(best_cromosoma, new_best_cromosoma):
                if ruta_logs is not None:
                    self.dibujarRutasFitnessCromosoma(new_best_cromosoma[self.INDEX_CROMOSOMA],
                                                      new_best_cromosoma[self.INDEX_FITNESS], show=False,
                                                      ruta_guardar='{}cromosoma_ganador_{}.png'.format(ruta_logs,
                                                                                                       generacion))
                best_cromosoma = new_best_cromosoma
                print('new_best_cromosoma:', new_best_cromosoma[self.INDEX_CROMOSOMA], 'fitness:',
                      new_best_cromosoma[self.INDEX_FITNESS])

            # Ver evolucion fitness medio:
            new_fitness_medio = self.poblacion[:, self.INDEX_FITNESS].mean()
            if new_fitness_medio != fitness_medio:
                print('[{}] - Fitness medio: {}'.format(generacion, new_fitness_medio))
                fitness_medio = new_fitness_medio
                generaciones_sin_cambio = 0
            else:
                generaciones_sin_cambio += 1

        return new_best_cromosoma[self.INDEX_CROMOSOMA], new_best_cromosoma[self.INDEX_FITNESS]


    def dibujarRutasFitnessCromosoma(self, cromosoma, fitness_cromosoma, show=True, ruta_guardar=None):
        '''
        Dibuja las rutas del cromosoma en el grafo.
        '''
        # Dibujar nodos:
        grid = utils.dibujarNodos(self.nodos, aspect=max(np.array(list(self.nodos.values()))[:, 0]) / max(
            np.array(list(self.nodos.values()))[:, 1]))

        # Escribir cromosoma y fitness:
        font = {'family': 'serif',
                'color': 'darkred',
                'weight': 'normal',
                'size': 16,
                }
        plt.text(-5, -5, 'fitness: {}'.format(fitness_cromosoma), fontdict=font)
        font['size'] = 9
        plt.text(-12, -12, '{}'.format(str(cromosoma)), fontdict=font)

        # Dibujar trayectorias:
        n_drones = len(self.drones)
        ultimo_indice = 0
        for i, dron in enumerate(self.drones):

            n_ciudades = cromosoma[-(n_drones - i)]
            ciudades = cromosoma[ultimo_indice:ultimo_indice + n_ciudades]

            origen = dron.posicion_lanzamiento
            # origen = dron.posicion_actual
            for ciudad in ciudades:
                destino = self.nodos[ciudad]
                grid.axes[0][0].plot((origen[0], destino[0]), (origen[1], destino[1]),
                                     '{}{}'.format(dron.color, dron.style))
                origen = destino

            ultimo_indice += n_ciudades

        # Mostrar/Guardar:
        if ruta_guardar is not None:
            plt.savefig(ruta_guardar)
        if show:
            plt.show()
        plt.clf()
        plt.close('all')
