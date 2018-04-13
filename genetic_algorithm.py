import time
import zmq
import json

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
    #  Wait for next request from client
    message = socket.recv_json()

    print "\n\n*************************************************************"
    print "Nombre de la mision: " , message['nombre_mision']
    print "Tipo de mision: " , message['tipo_mision']
    print "Altitud de vuelo: " , message['altura_vuelo']
    print "Numero de drones: " , message['numero_drones']
    print "Solapamiento entre imagenes: " , message['solapamiento']
    print "NE: " , message['norte_este']
    print "NO: " , message['norte_oeste']
    print "SE: " , message['sur_este']
    print "SO: " , message['sur_oeste']
    print "*************************************************************"

    #  Do some 'work'
    time.sleep(1)

    #  Send reply back to client
    socket.send(b"The genetic algorithm is over.")
