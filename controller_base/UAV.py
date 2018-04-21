from time import sleep
import numpy as np


class UAV():

    def __init__(self, id, caracteristicas_sensor, posicion_lanzamiento, color='k', style='--'):
        self.id = id
        self.caracteristicas_sensor = caracteristicas_sensor
        self.posicion_lanzamiento = posicion_lanzamiento
        self.posicion_actual = posicion_lanzamiento
        self.enmovimiento = False

        if color == 'k':
            self.color = ['m', 'g', 'b', 'y'][id]

        self.style = style

    def goToDummy(self, posicion, metros_por_segundo=2, segundos_entre_actualizacion=1, grid=None, count=0):
        '''
        Parametros
        ----------
        posicion : list
            Posicion [x,y] a la que se quiere que viaje el UAV.

        metros por segundo : float
            Metros recorridos cada segundos_entre_actualizacion

        segundos_entre_actualizacion : float
            Segundos que tarda en recorrer metros_por_segundo
        '''
        if posicion[0] == self.posicion_actual[0] and posicion[1] == self.posicion_actual[1]:
            print('[UAV {}] - YA ESTOY EN EL DESTINO.'.format(self.id))
            return

        print('\n\n\n[UAV {}] - INICIANDO DESPLAZAMIENTO DESDE {} HASTA {}'.format(self.id, self.posicion_actual,
                                                                                   posicion))

        # Calcular desplazamiento en cada eje:
        distancia_recorrer = np.sqrt(np.sum(np.power((np.array(posicion) - np.array(self.posicion_actual)), 2)))

        sentido_x = ((-1) * (self.posicion_actual[0] > posicion[0]) + 1 * (self.posicion_actual[0] < posicion[0])) * (
                self.posicion_actual[0] != posicion[0])
        sentido_y = ((-1) * (self.posicion_actual[1] > posicion[1]) + 1 * (self.posicion_actual[1] < posicion[1])) * (
                self.posicion_actual[1] != posicion[1])

        if sentido_x != 0 and sentido_y != 0:
            alpha = np.arctan(abs(self.posicion_actual[0] - posicion[0]) / abs(self.posicion_actual[1] - posicion[1]))

            if sentido_x == sentido_y:
                desplazamiento_x = sentido_x * np.cos(alpha) * metros_por_segundo
                desplazamiento_y = sentido_y * np.sin(alpha) * metros_por_segundo
            else:
                desplazamiento_x = sentido_x * np.sin(alpha) * metros_por_segundo
                desplazamiento_y = sentido_y * np.cos(alpha) * metros_por_segundo
        else:
            desplazamiento_x = sentido_x * metros_por_segundo
            desplazamiento_y = sentido_y * metros_por_segundo

        # Movimiento:
        self.enmovimiento = True
        while distancia_recorrer > 0:

            distancia_recorrer -= metros_por_segundo * segundos_entre_actualizacion

            ultima_posicion = self.posicion_actual.copy()

            if distancia_recorrer > metros_por_segundo * segundos_entre_actualizacion:
                self.posicion_actual[0] += desplazamiento_x
                self.posicion_actual[1] += desplazamiento_y
                print('[UAV {}] - VIAJANDO A DESTINO - Posicion actual: {}'.format(self.id, self.posicion_actual))
            else:
                self.posicion_actual = posicion

            if grid is not None:
                grid.axes[0][0].plot((ultima_posicion[0], self.posicion_actual[0]),
                                     (ultima_posicion[1], self.posicion_actual[1]),
                                     '{}{}'.format(self.color, self.style))
                grid.savefig('./animacion/animacion_{}.png'.format(count))
                count += 1

            sleep(segundos_entre_actualizacion)

        self.enmovimiento = False
        print('[UAV {}] - DESTINO ALCANZADO - Posicion actual: {}'.format(self.id, self.posicion_actual))
        return count
