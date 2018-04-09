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
    print "Nombre de la mision: " , message['mission_name']
    print "Tipo de mision: " , message['mission_type']
    print "Altitud de vuelo: " , message['altitude_fly']
    print "Numero de drones: " , message['number_drones']
    print "Solapamiento entre imagenes: " , message['overlap']
    print "NE: " , message['north_east']
    print "NO: " , message['north_west']
    print "SE: " , message['south_east']
    print "SO: " , message['south_west']
    print "*************************************************************"

    #  Do some 'work'
    time.sleep(1)

    #  Send reply back to client
    socket.send(b"The genetic algorithm is over.")
