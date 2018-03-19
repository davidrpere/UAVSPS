from wifi import Cell, Scheme
from time import clock
import zmq
import time
import sys
a = 0
port = "5556"
if len(sys.argv) > 1:
    port =  sys.argv[1]
    int(port)

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect ("tcp://localhost:%s" % port)

print "Sending request "
while True:
	cell = Cell.all('wlp5s0');
	var=0;
	b = clock()
	if b - a > 2:
		while (var!=len(cell)):
			socket.send_string (cell[var].ssid,cell[var].signal)
			print "Nombre de la red:",cell[var].signal,"y",cell[var].ssid,"dbm"
			var=var+1
		a=b



