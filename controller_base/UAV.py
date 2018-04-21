from time import sleep
import numpy as np


class UAV ():

    def __init__(self, id, caracteristicas_sensor, posicion_lanzamiento, altura, raspberry = False, color='k', style='--'):
        self.id = id
        self.caracteristicas_sensor = caracteristicas_sensor
        self.posicion_lanzamiento = posicion_lanzamiento
        self.posicion_actual = posicion_lanzamiento
        self.enmovimiento = False
        self.color = color
        self.style = style

        self.altura = altura
        self.raspberry = raspberry

        self.ESTE = 0
        self.NORTE = 90
        self.OESTE = 180
        self.SUR = 270

        self.angulo = self.NORTE


    def startBucleMision(self, waypoints_str, metros_por_segundo = 2, segundos_entre_actualizacion = 1):
        context = zmq.Context()

        self.socket_camara = context.socket(zmq.PUB) 
        self.socket_camara.bind("tcp://*:8999")

        self.socket_posiciones = context.socket(zmq.PUB) 
        self.socket_posiciones.bind("tcp://*:8") # TODO -> Completar

        self.socket_angulo = context.socket(zmq.PUB) 
        self.socket_angulo.bind("tcp://*:88") # TODO -> Completar

        if self.raspberry:
            from picamera import PiCamera
            self.camera = PiCamera()
            self.stream = io.BytesIO()

        while True:
            # wait esperar recibir
            self.initMissionDummy() # TODO -> implementar


    def initMissionDummy(self, waypoints_str, metros_por_segundo = 2, segundos_entre_actualizacion = 1):
        '''
        waypoints_str = "lat1,lng1 lat2,lng2"
        '''
        waypoints = []
        for w in waypoints_str.split(" "):
            lat, long = w.split(',')
            waipoints.append([float(long), float(lat)])

        while True: # TODO -> cambio
            for waipoint in waypoints:
                self.goToDummy(waipoint, metros_por_segundo, segundos_entre_actualizacion)
                self.sendPhotoDummy()

            for waipoint in reversed(waypoints):
                self.goToDummy(waipoint, metros_por_segundo, segundos_entre_actualizacion)
                self.sendPhotoDummy()


    def cambiarOrientacion (self, angulo_final, segundos_entre_actualizacion, angulos_segundo):

        # TODO -> VER SENTIDO GIRO OPTIMO

        diferencia_angulos = abs(angulo_final - self.angulo)
        sentido = (-1) * (angulo_final < self.angulo) + (1) * (angulo_final > self.angulo)

        while diferencia_angulos > 0:
            diferencia_angulos -= angulos_segundo
            self.angulo += sentido * angulos_segundo
            
            if diferencia_angulos < 0:
                self.angulo = angulo_final

            sleep(segundos_entre_actualizacion)
            self.socket_angulo.send_string(str(alpha)) # PUB alpha respecto al norte


    def getOrientacionFinal(self, sentido_x, sentido_y, alpha):
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


    def goToDummy (self, posicion, metros_por_segundo = 2, segundos_entre_actualizacion = 1, angulos_segundo = 20):
        if posicion[0] == self.posicion_actual[0] and posicion[1] == self.posicion_actual[1]:
            return

        distancia_recorrer = np.sqrt(np.sum(np.power((np.array(posicion) - np.array(self.posicion_actual)), 2)))
        
        sentido_x = ((-1) * (self.posicion_actual[0] > posicion[0]) + 1 * (self.posicion_actual[0] < posicion[0])) * (self.posicion_actual[0] != posicion[0])
        sentido_y = ((-1) * (self.posicion_actual[1] > posicion[1]) + 1 * (self.posicion_actual[1] < posicion[1]))  * (self.posicion_actual[1] != posicion[1])

        if sentido_x != 0 and sentido_y != 0:
            alpha = np.arctan(abs(self.posicion_actual[0] - posicion[0]) / abs(self.posicion_actual[1] - posicion[1]))
            desplazamiento_x = sentido_x * np.cos(alpha) * metros_por_segundo
            desplazamiento_y = sentido_y * np.sin(alpha) * metros_por_segundo
        else:
            alpha = None
            desplazamiento_x = sentido_x * metros_por_segundo
            desplazamiento_y = sentido_y * metros_por_segundo

        angulo_final = self.getOrientacionFinal(sentido_x, sentido_y, alpha)
        self.cambiarOrientacion(angulo_final, segundos_entre_actualizacion, angulos_segundo)

        self.enmovimiento = True
        while distancia_recorrer > 0:
            distancia_recorrer -= metros_por_segundo * segundos_entre_actualizacion
            ultima_posicion = self.posicion_actual.copy()

            if distancia_recorrer > metros_por_segundo * segundos_entre_actualizacion: 
                self.posicion_actual[0] += desplazamiento_x
                self.posicion_actual[1] += desplazamiento_y
            else:
                self.posicion_actual = posicion

            sleep(segundos_entre_actualizacion)
            
            self.socket_posiciones.send_string("{} {} {}".format(posicion_actual[0], posicion_actual[1], self.altura))
            self.socket_angulo.send_string(str(self.angulo)) # PUB alpha respecto al norte

        self.enmovimiento = False
            

    def sendPhotoDummy (self, ruta_img = None):
        if self.raspberry:
            self.camera.capture(self.stream, 'jpeg')
            imagen = base64.b64encode((self.stream.getvalue()))
        else:
            with open(ruta_img, 'rb') as f:
                imagen = base64.b64encode(f.read())        

        info_json = json.dumps({"id_dron": self.id, "lat": self.posicion_actual[0], 
                                "lng": self.posicion_actual[1], "alt": self.altura, 
                                "imagen": imagen })
        self.socket_camara.send_string(info_json)


    def goToDummyDraw (self, posicion, metros_por_segundo = 2, segundos_entre_actualizacion = 1, grid = None, count = 0):
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

        print('\n\n\n[UAV {}] - INICIANDO DESPLAZAMIENTO DESDE {} HASTA {}'.format(self.id, self.posicion_actual, posicion))

        # Calcular desplazamiento en cada eje:
        distancia_recorrer = np.sqrt(np.sum(np.power((np.array(posicion) - np.array(self.posicion_actual)), 2)))

        sentido_x = ((-1) * (self.posicion_actual[0] > posicion[0]) + 1 * (self.posicion_actual[0] < posicion[0])) * (self.posicion_actual[0] != posicion[0])
        sentido_y = ((-1) * (self.posicion_actual[1] > posicion[1]) + 1 * (self.posicion_actual[1] < posicion[1]))  * (self.posicion_actual[1] != posicion[1])

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
                grid.axes[0][0].plot((ultima_posicion[0], self.posicion_actual[0]), (ultima_posicion[1], self.posicion_actual[1]), '{}{}'.format(self.color, self.style))
                grid.savefig('./animacion/animacion_{}.png'.format(count))
                count += 1

            sleep(segundos_entre_actualizacion)

        self.enmovimiento = False
        print('[UAV {}] - DESTINO ALCANZADO - Posicion actual: {}'.format(self.id, self.posicion_actual))
        return count