import zmq
import json

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://192.168.43.171:5555")

while True:

    latlong = str(42.1694839) + "," + str(-8.683478499999978) + " " \
              + str(43.1694839) + "," + str(-9.683478499999978) + " " \
              + str(44.1694839) + "," + str(-10.683478499999978)

    print(latlong)
    socket.send_string(latlong)

    #  Get the reply.
    message = socket.recv()
    print(message)