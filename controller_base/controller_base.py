from UAV import UAV
import utils
import time
from AlgoritmoMTSP import AlgoritmoMTSP

combinacion = {'n_nearest_rr': 100,
               'n_nearest': 1,
               'n_random': 1000,
               'n_generaciones': 100,
               'limite_generaciones_sin_cambio': 1000,
               'contar_pos_inicial_en_fitness': False}

caracteristicas_sensor = {'ancho_sensor': 1,
                          'distancia_focal': 0.5,
                          'angulo_inclinacion': 90}


def main():
    posiciones_base, altura_vuelo, fraccion_solape, norte_oeste, norte_este, sur_oeste, sur_este = utils.getDatosWeb()
    drones = [UAV(i, caracteristicas_sensor, posicion_base) for i, posicion_base in enumerate(posiciones_base)]
    nodos, nodos_geometricas = utils.getNodosGrafo(norte_oeste, norte_este, sur_oeste, sur_este, altura_vuelo,
                                                   fraccion_solape, caracteristicas_sensor)
    ga = AlgoritmoMTSP(nodos, drones)
    cromosoma_ganador, fitness = ga.getRutasSubOptimas(n_nearest_rr=combinacion['n_nearest_rr'],
                                                       n_nearest=combinacion['n_nearest'],
                                                       n_random=combinacion['n_random'],
                                                       n_generaciones=combinacion['n_generaciones'],
                                                       limite_generaciones_sin_cambio=combinacion[
                                                           'limite_generaciones_sin_cambio'],
                                                       contar_pos_inicial_en_fitness=combinacion[
                                                           'contar_pos_inicial_en_fitness'],
                                                       ruta_logs=utils.getRutaLogs(combinacion))
    	
    #time.sleep(10)
    utils.enviarResultado(cromosoma_ganador, nodos_geometricas, drones)


if __name__ == '__main__':
    while True:
        main()
