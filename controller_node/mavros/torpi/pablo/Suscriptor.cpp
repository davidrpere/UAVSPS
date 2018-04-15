#include <zmq.hpp>
#include <iostream>
#include <sstream>
int main () {
    	zmq::context_t context (1);
    	std::cout << "Collecting updates from WEB server...\n" << std::endl;
    	zmq::socket_t subscriber (context, ZMQ_SUB);
    	subscriber.connect("tcp://127.0.0.1:8080");
    	const char *filter = "1";
    	subscriber.setsockopt(ZMQ_SUBSCRIBE, filter, strlen (filter));
    	zmq::message_t update;
    	int id;
	double latitud, longitud,altitud;

	subscriber.recv(&update);
        std::istringstream iss(static_cast<char*>(update.data()));

	std::cout << std::string(static_cast<char*>(update.data()), update.size()) << std::endl;

	std::cout << "HOLA" << std::endl;

	char image [update.size()];
	std::cout << "HOLA2" << std::endl;

	iss >> id >> image;

	std::cout << "HOLA3" << std::endl;

        std:: cout << "\nel ID del dron es: " <<id << std::endl;
	std:: cout << "\nla image es: " << image << std::endl;



	for(int i = 0 ; i < update.size() ; i ++ ){
      		std::cout << image[i] ;
	}
	std:: cout << "\nel Longitud es: " <<longitud << std::endl;
	std:: cout <<"\n la Altitud es: " <<altitud <<std::endl;

	return 0;
}
