from time import sleep
import numpy as np
import zmq
import json
import base64
from geopy import distance


class UAV ():

    def __init__(self, id, caracteristicas_sensor, posicion_lanzamiento, altura, raspberry = False, puerto_posiciones = "5557",puerto_angulo = "5560", puerto_waypoints = "5558", puerto_foto = "8081",  color='k', style='--'):
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
        self.fin_mision = True

    def startBucleMision(self, metros_por_desplazamiento = 0.00007, segundos_entre_actualizacion = 0.5):

        context = zmq.Context()

        self.socket_camara = context.socket(zmq.REQ)
        #self.socket_camara.bind("tcp://{}:{}".format(self.ip, self.puerto_foto)) # TODO: corregir!
        self.socket_camara.bind("tcp://127.0.0.1:{}".format(self.ip, self.puerto_foto)) # TODO: corregir!

        self.socket_posiciones = context.socket(zmq.PUB)
        self.socket_posiciones.bind("tcp://{}:{}".format(self.ip, self.puerto_posiciones))

        socket_waypoints = context.socket(zmq.REP)
        socket_waypoints.bind("tcp://{}:{}".format(self.ip, self.puerto_waypoints))

        self.socket_angulo = context.socket(zmq.PUB)
        self.socket_angulo.bind("tcp://{}:{}".format(self.ip, self.puerto_angulo))

        while True:
            self.fin_mision = False

            print("Esperando por waypoints...")
            mensaje = socket_waypoints.recv()  # "lat1,lng1 lat2,lng2"
            socket_waypoints.send("waypoints recibidos por dron " + str(self.id))

            if mensaje.split(" ")[0] == "m":
                print('Waypoints:')
                waypoints = []
                for w in mensaje.split(" ")[1:]:
                    lat, long = w.split(',')
                    waypoints.append([long, lat])
                    print([long, lat])

                primer_waypoint = [float(waypoints[0][0]), float(waypoints[0][1])]
                self.posicion_actual = primer_waypoint

                self.initMissionDummy(waypoints, metros_por_desplazamiento, segundos_entre_actualizacion)
                self.goToDummy(primer_waypoint, metros_por_desplazamiento, segundos_entre_actualizacion)
            else:
                self.angulo = self.SUR
                centro = (mensaje.split(" ")[1]).split(',')
                radio = mensaje.split(" ")[2]
                print("centro: ", str(centro), ", radio: ", str(radio))

                radio = int(radio) / 100000.  # (Km)
                lat = float(centro[0]) + radio / 111
                lon = float(centro[1])

                self.initBuitre(lat, lon, radio)
                self.goToDummy([lon, lat], metros_por_desplazamiento, segundos_entre_actualizacion)



    def initMissionDummy(self, waypoints, metros_por_desplazamiento, segundos_entre_actualizacion):

        # Si la distancia del ultimo waypoint con el primero es menor que el
        # doble de la distancia con el d_ultimo_penultimo vuelve al primer waypoints
        d_primero_ultimo = distance.vincenty(waypoints[0], waypoints[-1]).meters
        d_ultimo_penultimo = distance.vincenty(waypoints[-1], waypoints[-2]).meters
        do_reverse = True
        if d_primero_ultimo < 2 * d_ultimo_penultimo:
            do_reverse = False

        self.socket_posiciones.send_string("{} {} {}".format(self.posicion_actual[1], self.posicion_actual[0], self.altura))

        while True:
            for waypoint in waypoints:
                print(5*'\n')
                print("Viajando a ", waypoint)
                if self.fin_mision:
                    return

                self.goToDummy(waypoint, metros_por_desplazamiento, segundos_entre_actualizacion)

                #self.sendPhotoDummy()
                print("Ha llegado a ", waypoint)

            if do_reverse:
                for waypoint in reversed(waypoints):
                    if self.fin_mision:
                        return

                    print(5*'\n')
                    print("Viajando a ", waypoint)
                    self.goToDummy(waypoint, metros_por_desplazamiento, segundos_entre_actualizacion)

                    #self.sendPhotoDummy()

                    print("Ha llegado a ", waypoint)


    def cambiarOrientacion (self, angulo_final, segundos_entre_actualizacion, angulos_desplazamiento):

        # TODO -> VER SENTIDO GIRO OPTIMO
        print('Angulo final:', angulo_final)

        vueltas_horarias = angulo_final / angulos_desplazamiento
        vueltas_antihorarias = (360 - angulo_final) / angulos_desplazamiento

        if vueltas_horarias >= vueltas_antihorarias:
            pass

        diferencia_angulos = abs(angulo_final - self.angulo)
        sentido = (-1) * (angulo_final < self.angulo) + (1) * (angulo_final > self.angulo)

        while diferencia_angulos > 0:
            diferencia_angulos -= angulos_desplazamiento
            self.angulo += sentido * angulos_desplazamiento

            if diferencia_angulos < 0:
                self.angulo = angulo_final

            sleep(segundos_entre_actualizacion/10)
            if self.angulo != self.angulo_anterior:
                self.socket_angulo.send_string(str(int(self.angulo)))
                self.socket_posiciones.send_string("{} {} {}".format(self.posicion_actual[1], self.posicion_actual[0], self.altura))
                self.angulo_anterior = self.angulo
                print("Orientandome hacia: ", self.angulo)


    def getOrientacionFinal(self, sentido_x, sentido_y, alpha):
        # Por el error del ultimo valor del float:
        if np.round(alpha) == self.SUR:
            return self.SUR
        if np.round(alpha) == self.OESTE:
            return self.OESTE
        if np.round(alpha) == self.ESTE:
            return self.ESTE

        if sentido_x == 0:
            return (self.NORTE) * (sentido_y > 0) + (self.SUR) * (sentido_y < 0)
        if sentido_y == 0:
            return (self.ESTE) * (sentido_x > 0) + (self.OESTE) * (sentido_x < 0)

        if sentido_x > 0 and sentido_y > 0:
            return self.ESTE - alpha
        if sentido_x > 0 and sentido_y < 0:
            return self.ESTE + alpha
        if sentido_x < 0 and sentido_y > 0:
            return self.OESTE + alpha
        if sentido_x < 0 and sentido_y < 0:
            return self.OESTE - alpha


    def goToDummy (self, pos_str, metros_por_desplazamiento, segundos_entre_actualizacion, angulos_desplazamiento = 5):
        posicion = [float(pos_str[0]), float(pos_str[1])]

        print("Estoy en:", self.posicion_actual)
        print("Viajando a ", posicion)

        if posicion[0] == self.posicion_actual[0] and posicion[1] == self.posicion_actual[1]:
            return

        distancia_recorrer = np.sqrt(np.sum(np.power((np.array(posicion) - np.array(self.posicion_actual)), 2)))

        sentido_x = ((-1) * (self.posicion_actual[0] > posicion[0]) + 1 * (self.posicion_actual[0] < posicion[0])) * (str(self.posicion_actual[0]) != pos_str[0])
        sentido_y = ((-1) * (self.posicion_actual[1] > posicion[1]) + 1 * (self.posicion_actual[1] < posicion[1]))  * (str(self.posicion_actual[1]) != pos_str[1])

        print('sentido_x:', sentido_x)
        print('sentido_y:', sentido_y)

        if sentido_x != 0 and sentido_y != 0:
            y_delta = abs(self.posicion_actual[1] - posicion[1])
            x_delta = abs(self.posicion_actual[0] - posicion[0])

            if x_delta != 0 and y_delta != 0:
                if sentido_y < 0:
                    alpha = np.arctan( x_delta / y_delta )
                    if sentido_x < 0:
                        alpha = (90 - ( alpha * 180 / self.pi)) * self.pi / 180
                else:
                    alpha = np.arctan( y_delta / x_delta )
                    if sentido_x < 0:
                        alpha = (90 - ( alpha * 180 / self.pi)) * self.pi / 180
            else:
                alpha = 0

            if sentido_x == sentido_y:
                desplazamiento_x = sentido_x * np.cos(alpha) * metros_por_desplazamiento
                desplazamiento_y = sentido_y * np.sin(alpha) * metros_por_desplazamiento
            else:
                desplazamiento_x = sentido_x * np.sin(alpha) * metros_por_desplazamiento
                desplazamiento_y = sentido_y * np.cos(alpha) * metros_por_desplazamiento

            alpha = alpha * 180 / self.pi
        else:
            alpha = 0
            desplazamiento_x = sentido_x * metros_por_desplazamiento
            desplazamiento_y = sentido_y * metros_por_desplazamiento

        print('Alpha: ', alpha)
        angulo_final = self.getOrientacionFinal(sentido_x, sentido_y, alpha)
        self.cambiarOrientacion(angulo_final, segundos_entre_actualizacion, angulos_desplazamiento)
        print("Nueva orientacion: ", self.angulo)

        self.enmovimiento = True
        while distancia_recorrer > 0:
            distancia_recorrer -= metros_por_desplazamiento
            ultima_posicion = self.posicion_actual

            if distancia_recorrer > metros_por_desplazamiento:
                print("distancia_recorrer: ", distancia_recorrer)
                self.posicion_actual[0] += desplazamiento_x
                self.posicion_actual[1] += desplazamiento_y
            else:
                self.posicion_actual = posicion

            sleep(segundos_entre_actualizacion)

            print("{} {} {}".format(self.posicion_actual[1], self.posicion_actual[0], self.altura))
            self.socket_posiciones.send_string("{} {} {}".format(self.posicion_actual[1], self.posicion_actual[0], self.altura))

        self.enmovimiento = False

    def to_rad(self, grados):
        return (grados * self.pi) / 180

    def initBuitre(self, lat, lon, radio):
        while True:
            #radio = radio / 100000.  # (Km)
            #lat = latitud + radio / 111

            for i in range(0, 360):
                if self.fin_mision:
                    return
                if i % 2 == 0:
                    x = lon + (radio / 111) * np.sin(self.to_rad(i))
                    y = lat - (radio / 111.) * (1 - np.cos(self.to_rad(i)))

                    self.posicion_actual = [x,y]

                    print("i: ", i, "x: ", x, ", y: ", y, ", angulo: ", self.angulo, ", bad bunny: ", self.to_rad(i))

                    self.socket_angulo.send_string(str(int(self.angulo)))
                    self.socket_posiciones.send_string("{} {} {}".format(y, x, self.altura))
                    sleep(0.25)

                self.angulo += 1

                if self.angulo == 360:
                    self.angulo = self.NORTE


    def sendPhotoDummy (self):
        self.socket_camara.send_string("{} {} {} {}".format(self.id, self.posicion_actual[1], self.posicion_actual[0], self.altura))

