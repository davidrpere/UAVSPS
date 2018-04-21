import zmq
import random
import time

port = "5550"


context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:%s" % port)

while True:
    messagedata = random.randrange(1,215) - 80

    socket.send(messagedata)
    time.sleep(1)