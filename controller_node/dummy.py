from UAV import UAV
import threading
import zmq

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:8888")
socket.setsockopt(zmq.SUBSCRIBE, '')

def finMision(dron1):
    while True:
        socket.recv_json()
        print("cancelamos mision")
        dron1.setFinMision()


try:
    dron1 = UAV(1, "", [0,0], 5)
    t = threading.Thread(target=finMision, args=(dron1,))
    t.start()

    dron1.startBucleMision()
finally:
    t.do_run = False
    t.join()
