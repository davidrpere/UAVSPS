#include <zmq.hpp>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <iostream>
#include <string>

int main () {
	zmq::context_t context (1);
        zmq::socket_t socket (context, ZMQ_REQ);
	socket.connect ("tcp://127.0.0.1:8081");
	int id=1;
	double latitud= 42.1694839;
	double longitud= -8.683478499999978;
	double altitud= 89.01;
	int size=0;
	zmq::message_t reply;
	while(1){
		size=sizeof(id)+sizeof(latitud)+sizeof(longitud)+sizeof(altitud)+1;
		zmq::message_t message(size);
		snprintf((char *) message.data(), size ,
			"%i %f %f %f",id, latitud, longitud, altitud);
		socket.send(message);
		printf("Peticion:");
		std::cout << std::string(static_cast<char*>(message.data()), message.size()) << std::endl;

		socket.recv (&reply);
		printf("Respuesta:");
		std::cout << std::string(static_cast<char*>(reply.data()), reply.size()) << std::endl;

		return 0;
	}
	return 0;
}
