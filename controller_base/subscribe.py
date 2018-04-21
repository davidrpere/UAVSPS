import zmq

context = zmq.Context()
socket = context.socket(zmq.SUB)

socket.connect("tcp://navio.local:5599")
socket.setsockopt(zmq.SUBSCRIBE, '')

while True:
    string = socket.recv()

    print(string["lat"])