from UAV import UAV
import os
from datetime import datetime
import utils
from algoritmo import AlgoritmoMTSP

import numpy as np

'''
SUPOSICIONES:
- Las camaras de los drones tienen las mismas caracteristicas y estan posicionadas con el mismo angulo de inclinacion.
- Los drones vuelan a la misma altura y velocidad.
- Las camaras tienen un grado de inclinacion, es necesario orientar al dron para sacar la foto.
- La posicion inicial de los drones no tiene porque ser la base.
- El movimiento de los drones no esta limitado a un eje.
'''

combinaciones_base = [[np.random.randint(-5, 90), np.random.randint(-5, 130)]
    #[0., 0.],
    #[85.,70.],
    #[-10., 70.],
    #[70., 130.]
    ]

combinaciones = [
    #{'n_nearest_rr': 0, 'n_nearest': 0, 'n_random': 1000, 'n_generaciones': 9000000, 'limite_generaciones_sin_cambio':1000, 'contar_pos_inicial_en_fitness':True},\
    #{'n_nearest_rr': 0, 'n_nearest': 0, 'n_random': 1000, 'n_generaciones': 9000000, 'limite_generaciones_sin_cambio':1000, 'contar_pos_inicial_en_fitness':False},\
    #{'n_nearest_rr': 0, 'n_nearest': 0, 'n_random': 5000, 'n_generaciones': 9000000, 'limite_generaciones_sin_cambio':1000, 'contar_pos_inicial_en_fitness':True},\
    #{'n_nearest_rr': 0, 'n_nearest': 0, 'n_random': 5000, 'n_generaciones': 9000000, 'limite_generaciones_sin_cambio':1000, 'contar_pos_inicial_en_fitness':False},\
    #{'n_nearest_rr': 250, 'n_nearest': 250, 'n_random': 250, 'n_generaciones': 90000, 'limite_generaciones_sin_cambio':1000, 'contar_pos_inicial_en_fitness':True},\
    #{'n_nearest_rr': 250, 'n_nearest': 250, 'n_random': 250, 'n_generaciones': 90000, 'limite_generaciones_sin_cambio':1000, 'contar_pos_inicial_en_fitness':False},\
    {'n_nearest_rr': 7, 'n_nearest': 7, 'n_random': 35, 'n_generaciones': 10000, 'limite_generaciones_sin_cambio':1000, 'contar_pos_inicial_en_fitness':True},\
    #{'n_nearest_rr': 30, 'n_nearest': 30, 'n_random': 140, 'n_generaciones': 90000, 'limite_generaciones_sin_cambio':1000, 'contar_pos_inicial_en_fitness':True},\
    #{'n_nearest_rr': 75, 'n_nearest': 75, 'n_random': 350, 'n_generaciones': 90000, 'limite_generaciones_sin_cambio':1000, 'contar_pos_inicial_en_fitness':True},\
    #{'n_nearest_rr': 150, 'n_nearest': 150, 'n_random': 700, 'n_generaciones': 90000, 'limite_generaciones_sin_cambio':1000, 'contar_pos_inicial_en_fitness':True},\
    #{'n_nearest_rr': 300, 'n_nearest': 300, 'n_random': 1400, 'n_generaciones': 90000, 'limite_generaciones_sin_cambio':1000, 'contar_pos_inicial_en_fitness':True},\
    #{'n_nearest_rr': 7, 'n_nearest': 7, 'n_random': 1000, 'n_generaciones': 90000, 'limite_generaciones_sin_cambio':1000, 'contar_pos_inicial_en_fitness':True},\
    #{'n_nearest_rr': 300, 'n_nearest': 300, 'n_random': 300, 'n_generaciones': 90000, 'limite_generaciones_sin_cambio':1000, 'contar_pos_inicial_en_fitness':True},\
    ]


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


def getAreaDeWeb (): # TODO -> implementar
    '''
    Devuelve los valores recibidos de NodeJS.
    '''
    northWest = [42.17226800508796, -8.679393394103954] #(latitud, longitud)
    northEast = [42.17226800508796, -8.678347434154489] #(latitud, longitud)
    southWest = [42.17112037162631, -8.679393394103954] #(latitud, longitud)
    southEast = [42.17112037162631, -8.678347434154489] #(latitud, longitud)

    return northWest, northEast, southWest, southEast


def getPosicionLanzamientoUAVs (): # TODO: implementar
    '''

    '''
    posicion_base = [0,0]
    return posicion_base


def getCaracteristicasUAVs (): # TODO: implementar 
    '''
    '''
    altura_vuelo_uav = 20
    fraccion_solape = 0.4
    caracteristicas_sensor = {'ancho_sensor':1, 'distancia_focal':0.5, 'angulo_inclinacion':90}

    return altura_vuelo_uav, fraccion_solape, caracteristicas_sensor


def computarAlgoritmoCombinaciones (nodos, drones, combinaciones_base, combinaciones):
    ga = AlgoritmoMTSP(nodos, drones)

    for base in combinaciones_base:
        # Asignar nueva posicion base:
        for i, dron in enumerate(drones):
            dron.posicion_lanzamiento = base
            ga.drones[i] = dron

        #ga.asignarPosicionInicialGrafo () # Asigna como posicion inicial de los drones el nodo mas cercano mediante RoundRobin

        # Ejecutar algoritmo genetico para cada combinacion:
        for combinacion in combinaciones:
            ruta_logs = getRutaLogs(combinacion)
            inicio = datetime.now()

            cromosoma_ganador, fitness = ga.getRutasSubOptimas(n_nearest_rr = combinacion['n_nearest_rr'], 
                                                                n_nearest = combinacion['n_nearest'], 
                                                                n_random=combinacion['n_random'], 
                                                                n_generaciones = combinacion['n_generaciones'], 
                                                                limite_generaciones_sin_cambio = combinacion['limite_generaciones_sin_cambio'],
                                                                contar_pos_inicial_en_fitness = combinacion['contar_pos_inicial_en_fitness'],
                                                                ruta_logs = ruta_logs)

            # Registrar la duracion de ejecucion de la combinacion y los resultados:
            duracion = (datetime.now()  - inicio).total_seconds()
            with open(ruta_logs + 'duracion.txt', 'w') as f:
                f.write('Segundos: {}\n'.format(duracion))
                f.write('Minutos: {}\n'.format(duracion/60))
                f.write('\n\n')
                f.write('Cromosoma ganador:\n\t{}'.format(cromosoma_ganador))
                f.write('Fitness: {}'.format(fitness))


def main ():

    northWest, northEast, southWest, southEast = getAreaDeWeb()

    altura_vuelo_uav, fraccion_solape, caracteristicas_sensor = getCaracteristicasUAVs ()
    posicion_base = getPosicionLanzamientoUAVs()
    # TODO -> construir numero de drones y caracteristicas a partir de info recibida
    #drones = [UAV (0, caracteristicas_sensor, posicion_base, color='m', style='--'), 
    #          UAV (1, caracteristicas_sensor, posicion_base, color='g', style='--'),
    #          UAV (2, caracteristicas_sensor, posicion_base, color='b', style='--'),
    #          UAV (3, caracteristicas_sensor, posicion_base, color='y', style='--')]

    drones = [UAV (0, caracteristicas_sensor, [np.random.randint(-5, 90), np.random.randint(-5, 130)], color='m', style='--'), 
              UAV (1, caracteristicas_sensor, [np.random.randint(-5, 90), np.random.randint(-5, 130)], color='g', style='--'),
              UAV (2, caracteristicas_sensor, [np.random.randint(-5, 90), np.random.randint(-5, 130)], color='b', style='--'),
              UAV (3, caracteristicas_sensor, [np.random.randint(-5, 90), np.random.randint(-5, 130)], color='y', style='--')]

    nodos = utils.getNodosGrafo(northWest, northEast, southWest, southEast, altura_vuelo_uav, fraccion_solape, caracteristicas_sensor)

    
    combinacion = {'n_nearest_rr': 7, 'n_nearest': 7, 'n_random': 35, 'n_generaciones': 10000, 'limite_generaciones_sin_cambio':1000, 'contar_pos_inicial_en_fitness':True}


    ga = AlgoritmoMTSP(nodos, drones)
    cromosoma_ganador, fitness = ga.getRutasSubOptimas(n_nearest_rr = combinacion['n_nearest_rr'], 
                                                                n_nearest = combinacion['n_nearest'], 
                                                                n_random=combinacion['n_random'], 
                                                                n_generaciones = combinacion['n_generaciones'], 
                                                                limite_generaciones_sin_cambio = combinacion['limite_generaciones_sin_cambio'],
                                                                contar_pos_inicial_en_fitness = combinacion['contar_pos_inicial_en_fitness'],
                                                                ruta_logs = './prueba/')
    #computarAlgoritmoCombinaciones(nodos, drones, combinaciones_base, combinaciones)


if __name__ == '__main__':
    main()