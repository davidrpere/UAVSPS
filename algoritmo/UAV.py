from time import sleep
import numpy as np


class UAV ():

    def __init__(self, id, caracteristicas_sensor, posicion_lanzamiento, color='k', style='--'):
        self.id = id
        self.caracteristicas_sensor = caracteristicas_sensor
        self.posicion_actual = posicion_lanzamiento
        self.enmovimiento = False
        self.color = color
        self.style = style


    def goToDummy (self, posicion):
        frecuencia_actualizacion = 1
        metros_por_segundo = 2
        distancia_recorrer = np.sqrt(np.sum(np.power((np.array(posicion) - np.array(self.posicion_actual)), 2)))

        if posicion[0] == self.posicion_actual[0] and posicion[1] == self.posicion_actual[1]:
            print('[UAV {}] - YA ESTOY EN EL DESTINO.'.format(self.id))
            return

        if posicion[0] != self.posicion_actual[0] and posicion[1] != self.posicion_actual[1]:
            # TODO -> programar movimiento
            print('[UAV {}] - ERROR - DESTINO INALCANZABLE DESDE LA POSICION ACTUAL.'.format(self.id))
            return

        self.enmovimiento = True

        print('[UAV {}] - INICIANDO DESPLAZAMIENTO DESDE {} HASTA {}'.format(self.id, self.posicion_actual, posicion))
        if posicion[0] != self.posicion_actual[0]:
            sentido = (-1) * (self.posicion_actual[0] > posicion[0]) + 1 * (self.posicion_actual[0] < posicion[0])
            while True:
                self.posicion_actual[0] += sentido * metros_por_segundo
                distancia_recorrer -= metros_por_segundo

                if distancia_recorrer <= 0:
                    self.posicion_actual[0] = posicion[0]
                    #self.posicion_actual[0] -= distancia_recorrer
                    sleep(-distancia_recorrer/metros_por_segundo)
                    print('[UAV {}] - DESTINO ALCANZADO - Posicion actual: {}'.format(self.id, self.posicion_actual))
                    break;

                sleep(1);
                print('[UAV {}] - VIAJANDO A DESTINO - Posicion actual: {}'.format(self.id, self.posicion_actual))
            self.enmovimiento = False
            return

        if posicion[1] != self.posicion_actual[1]:
            sentido = (-1) * (self.posicion_actual[1] > posicion[1]) + 1 * (self.posicion_actual[1] < posicion[1])
            while True:
                self.posicion_actual[1] += sentido * metros_por_segundo
                distancia_recorrer -= metros_por_segundo

                if distancia_recorrer <= 0:

                    self.posicion_actual[1] = posicion[1]
                    #self.posicion_actual[1] -= distancia_recorrer
                    sleep(-distancia_recorrer/metros_por_segundo)
                    print('[UAV {}] - DESTINO ALCANZADO - Posicion actual: {}'.format(self.id, self.posicion_actual))
                    break;

                sleep(1);
                print('[UAV {}] - VIAJANDO A DESTINO - Posicion actual: {}'.format(self.id, self.posicion_actual))

            self.enmovimiento = False
            return

        
