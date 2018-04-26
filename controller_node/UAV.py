from time import sleep
import numpy as np
import zmq
import json
import base64
from geopy import distance


class UAV():
    def __init__(self, id, caracteristicas_sensor, posicion_lanzamiento, altura, raspberry=False,
                 puerto_posiciones="5557", puerto_angulo="5560", puerto_waypoints="5558", puerto_foto="8081", color='k',
                 style='--'):
        self.id = id
        self.caracteristicas_sensor = caracteristicas_sensor
        self.posicion_lanzamiento = posicion_lanzamiento
        self.posicion_actual = posicion_lanzamiento
        self.enmovimiento = False
        self.color = color
        self.style = style

        self.ip = "*"
        self.puerto_posiciones = puerto_posiciones
        self.puerto_angulo = puerto_angulo
        self.puerto_foto = puerto_foto
        self.puerto_waypoints = puerto_waypoints

        self.pi = 3.141592653589793
        self.altura = altura
        self.raspberry = raspberry

        self.ESTE = 90
        self.NORTE = 0
        self.OESTE = 270
        self.SUR = 180

        self.angulo = self.NORTE
        self.angulo_anterior = self.angulo

        self.fin_mision = False

    def setFinMision(self):
        self.fin_mision = bool

    def startBucleMision(self, metros_por_desplazamiento=0.00007, segundos_entre_actualizacion=0.5):
        context = zmq.Context()

        self.socket_camara = context.socket(zmq.REQ)
        # self.socket_camara.bind("tcp://{}:{}".format(self.ip, self.puerto_foto)) # TODO: corregir!
        self.socket_camara.bind("tcp://127.0.0.1:{}".format(self.ip, self.puerto_foto))  # TODO: corregir!

        self.socket_posiciones = context.socket(zmq.PUB)
        self.socket_posiciones.bind("tcp://{}:{}".format(self.ip, self.puerto_posiciones))

        socket_waypoints = context.socket(zmq.REP)
        socket_waypoints.bind("tcp://{}:{}".format(self.ip, self.puerto_waypoints))

        self.socket_angulo = context.socket(zmq.PUB)
        self.socket_angulo.bind("tcp://{}:{}".format(self.ip, self.puerto_angulo))

        while True:
            self.fin_mision = False

            print("Esperando por waypoints...")
            mensaje = socket_waypoints.recv()
            socket_waypoints.send("waypoints recibidos por dron " + str(self.id))
            self.initMissionDummy(mensaje, metros_por_desplazamiento, segundos_entre_actualizacion)



    def initMissionDummy(self, waypoints_str, metros_por_desplazamiento, segundos_entre_actualizacion):
        '''
        waypoints_str = "lat1,lng1 lat2,lng2"
        '''
        print('Waypoints:')
        waypoints = []
        for w in waypoints_str.split(" "):  # [1:]: # TODO: CAMBIO CON NUEVA VERSION
            lat, long = w.split(',')
            # waypoints.append([float(long), float(lat)])
            waypoints.append([long, lat])
            print([long, lat])

        # Si la distancia del ultimo waypoint con el primero es menor que el
        # doble de la distancia con el d_ultimo_penultimo vuelve al primer waypoints
        d_primero_ultimo = distance.vincenty(waypoints[0], waypoints[-1]).meters
        d_ultimo_penultimo = distance.vincenty(waypoints[-1], waypoints[-2]).meters
        do_reverse = True
        if d_primero_ultimo < 2 * d_ultimo_penultimo:
            do_reverse = False

        self.posicion_actual = [float(waypoints[0][0]), float(waypoints[0][1])]
        self.socket_posiciones.send_string(
            "{} {} {}".format(self.posicion_actual[1], self.posicion_actual[0], self.altura))

        while True:
            for waypoint in waypoints:
                if self.fin_mision:
                    print("vamos a finalizar mision")
                    return
                print(5 * '\n')
                print("Viajando a ", waypoint)
                self.goToDummy(waypoint, metros_por_desplazamiento, segundos_entre_actualizacion)

                if not self.raspberry:
                    self.sendPhotoDummyFake('./rojo.png')
                print("Ha llegado a ", waypoint)

            if do_reverse:
                for waypoint in reversed(waypoints):
                    if self.fin_mision:
                        print("vamos a finalizar mision")
                        return
                    print(5 * '\n')
                    print("Viajando a ", waypoint)
                    self.goToDummy(waypoint, metros_por_desplazamiento, segundos_entre_actualizacion)

                    if self.raspberry:
                        self.sendPhotoDummy('./verde.png')
                    print("Ha llegado a ", waypoint)

    def cambiarOrientacion(self, angulo_final, segundos_entre_actualizacion, angulos_segundo):

        # TODO -> VER SENTIDO GIRO OPTIMO

        diferencia_angulos = abs(angulo_final - self.angulo)
        sentido = (-1) * (angulo_final < self.angulo) + (1) * (angulo_final > self.angulo)

        while diferencia_angulos > 0:
            diferencia_angulos -= angulos_segundo
            self.angulo += sentido * angulos_segundo

            if diferencia_angulos < 0:
                self.angulo = angulo_final

            sleep(segundos_entre_actualizacion)
            if self.angulo != self.angulo_anterior:
                self.socket_angulo.send_string(str(int(self.angulo)))
                self.socket_posiciones.send_string(
                    "{} {} {}".format(self.posicion_actual[1], self.posicion_actual[0], self.altura))
                self.angulo_anterior = self.angulo
                print("Nueva orientacion: ", self.angulo)

    def getOrientacionFinal(self, sentido_x, sentido_y, alpha):
        # alpha = alpha * 180 / self.pi
        # print('Alpha:', alpha)
        if sentido_x == 0:
            return (self.NORTE) * (sentido_y > 0) + (self.SUR) * (sentido_y < 0)
        if sentido_y == 0:
            return (self.ESTE) * (sentido_x > 0) + (self.OESTE) * (sentido_x < 0)
        if sentido_x > 0 and sentido_y > 0:
            return self.ESTE + alpha
        if sentido_x > 0 and sentido_y < 0:
            return self.ESTE - alpha
        if sentido_x < 0 and sentido_y > 0:
            return self.OESTE - alpha
        if sentido_x < 0 and sentido_y < 0:
            return self.OESTE + alpha

    def goToDummy(self, pos_str, metros_por_desplazamiento, segundos_entre_actualizacion, angulos_segundo=45):
        posicion = [float(pos_str[0]), float(pos_str[1])]

        print("Estoy en:", self.posicion_actual)
        print("Viajando a ", posicion)

        if posicion[0] == self.posicion_actual[0] and posicion[1] == self.posicion_actual[1]:
            return

        distancia_recorrer = np.sqrt(np.sum(np.power((np.array(posicion) - np.array(self.posicion_actual)), 2)))

        sentido_x = ((-1) * (self.posicion_actual[0] > posicion[0]) + 1 * (self.posicion_actual[0] < posicion[0])) * (
                    str(self.posicion_actual[0]) != pos_str[0])
        sentido_y = ((-1) * (self.posicion_actual[1] > posicion[1]) + 1 * (self.posicion_actual[1] < posicion[1])) * (
                    str(self.posicion_actual[1]) != pos_str[1])

        print(sentido_x)
        print(sentido_y)

        if sentido_x != 0 and sentido_y != 0:
            print('if')
            y_delta = abs(self.posicion_actual[1] - posicion[1])
            x_delta = abs(self.posicion_actual[0] - posicion[0])

            if x_delta != 0:

                if sentido_y < 0:
                    alpha = np.arctan(x_delta / y_delta)
                    # if sentido_x < 0:
                    #    alpha = (-1) * alpha
                else:
                    alpha = np.arctan(y_delta / x_delta)
                    # if sentido_x < 0:
                    #    alpha = (-1) * alpha

                print('Alpha:', alpha * 180 / self.pi)
                # alpha = np.arctan( x_delta / y_delta )
                # alpha = np.arctan( y_delta / x_delta )
                '''
                # Funcionan 6 casos
                if sentido_y < 0:
                    alpha = np.arctan( x_delta / y_delta )
                    if sentido_x < 0:
                        alpha = 90 - alpha
                else:
                    alpha = np.arctan( y_delta / x_delta )
                    if sentido_x < 0:
                        alpha = 45 - alpha
                '''
                # print('alpha:', alpha)

            if sentido_x == sentido_y:
                desplazamiento_x = sentido_x * np.cos(alpha) * metros_por_desplazamiento
                desplazamiento_y = sentido_y * np.sin(alpha) * metros_por_desplazamiento
            else:
                desplazamiento_x = sentido_x * np.sin(alpha) * metros_por_desplazamiento
                desplazamiento_y = sentido_y * np.cos(alpha) * metros_por_desplazamiento

            # desplazamiento_x = sentido_x * np.sin(alpha) * metros_por_desplazamiento
            # desplazamiento_y = sentido_y * np.cos(alpha) * metros_por_desplazamiento

        else:
            print('else')
            alpha = 0
            desplazamiento_x = sentido_x * metros_por_desplazamiento
            desplazamiento_y = sentido_y * metros_por_desplazamiento

        angulo_final = self.getOrientacionFinal(sentido_x, sentido_y, alpha)

        self.cambiarOrientacion(angulo_final, segundos_entre_actualizacion, angulos_segundo)
        print("Nueva orientacion: ", self.angulo)

        print("Desplazamiento x:", desplazamiento_x)
        print("Desplazamiento y:", desplazamiento_y)
        self.enmovimiento = True
        while distancia_recorrer > 0:
            distancia_recorrer -= metros_por_desplazamiento
            # ultima_posicion = self.posicion_actual.copy()
            ultima_posicion = self.posicion_actual

            if distancia_recorrer > metros_por_desplazamiento:
                print("distancia_recorrer: ", distancia_recorrer)
                self.posicion_actual[0] += desplazamiento_x
                self.posicion_actual[1] += desplazamiento_y
            else:
                self.posicion_actual = posicion

            sleep(segundos_entre_actualizacion)

            print("{} {} {}".format(self.posicion_actual[1], self.posicion_actual[0], self.altura))
            self.socket_posiciones.send_string(
                "{} {} {}".format(self.posicion_actual[1], self.posicion_actual[0], self.altura))

        self.enmovimiento = False

    def sendPhotoDummy(self):
        self.socket_camara.send_string(
            "{} {} {} {}".format(self.id, self.posicion_actual[1], self.posicion_actual[0], self.altura))

    def sendPhotoDummy_v0(self, ruta_img=None):
        if self.raspberry:
            self.camera.capture(self.stream, 'jpeg')
            imagen = base64.b64encode((self.stream.getvalue()))
        else:
            with open(ruta_img, 'rb') as f:
                imagen = base64.b64encode(f.read())

        info_json = json.dumps({"id_dron": self.id, "lat": self.posicion_actual[0],
                                "lng": self.posicion_actual[1], "alt": self.altura,
                                "imagen": imagen})
        self.socket_camara.send_string(info_json)

    def sendPhotoDummyFake(self, ruta_img):
        print('fotoFake')
        # with open(ruta_img, 'rb') as f:
        #    imagen = base64.b64encode(f.read())
        # info_json = json.dumps({"id_dron": self.id, "lat": self.posicion_actual[0],
        #                        "lng": self.posicion_actual[1], "alt": self.altura,
        #                        "imagen": imagen })

        # self.socket_camara.send_string(info_json)

        # self.socket_camara.send_string("{} {} {} {} {}".format(self.id, self.posicion_actual[1], self.posicion_actual[0], self.altura, ruta_img))

    def goToDummyDraw(self, posicion, metros_por_desplazamiento=2, segundos_entre_actualizacion=1, grid=None, count=0):
        '''
        Parametros
        ----------
        posicion : list
            Posicion [x,y] a la que se quiere que viaje el UAV.

        metros por segundo : float
            Metros recorridos cada segundos_entre_actualizacion

        segundos_entre_actualizacion : float
            Segundos que tarda en recorrer metros_por_desplazamiento
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
                desplazamiento_x = sentido_x * np.cos(alpha) * metros_por_desplazamiento
                desplazamiento_y = sentido_y * np.sin(alpha) * metros_por_desplazamiento
            else:
                desplazamiento_x = sentido_x * np.sin(alpha) * metros_por_desplazamiento
                desplazamiento_y = sentido_y * np.cos(alpha) * metros_por_desplazamiento
        else:
            desplazamiento_x = sentido_x * metros_por_desplazamiento
            desplazamiento_y = sentido_y * metros_por_desplazamiento

        # Movimiento:
        self.enmovimiento = True
        while distancia_recorrer > 0:

            distancia_recorrer -= metros_por_desplazamiento * segundos_entre_actualizacion

            ultima_posicion = self.posicion_actual.copy()

            if distancia_recorrer > metros_por_desplazamiento * segundos_entre_actualizacion:
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
