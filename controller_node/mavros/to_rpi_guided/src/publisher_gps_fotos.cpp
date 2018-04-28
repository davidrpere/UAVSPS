//
// Created by David Rodriguez Pereira on 9/4/18.
//

#include "publisher_gps_fotos.h"

void publisher_gps_fotos::publish(double latitud, double longitud, double altitud) {
    int size = sizeof(latitud)+ sizeof(longitud)+ sizeof(altitud)+2;
    zmq::message_t message(size);
    snprintf((char *) message.data(), size ,
             "%f %f %f", latitud, longitud, altitud);
    this->publisher.send(message);

}

void publisher_gps_fotos::publish(double latitud, double longitud, double altitud, int heading) {
    int size = sizeof(latitud)+sizeof(longitud)+sizeof(altitud)+sizeof(heading)+3;
    zmq::message_t message(size);
    snprintf((char *) message.data(), size ,
             "%f %f %f %i", latitud, longitud, altitud, heading);
    this->publisher.send(message);

}

void publisher_gps_fotos::publish(int heading) {
    //Publicamos nuestras cosas
    int size = sizeof(heading)+1;
    zmq::message_t message(size);
    snprintf((char *) message.data(), size ,
             "%i ", heading);
    this->publisher.send(message);

}

void publisher_gps_fotos::publish_foto(int id, double lat, double lon, double alt){
    int size=0;
    zmq::message_t reply;
    size=sizeof(id)+sizeof(lat)+sizeof(lon)+sizeof(alt)+1;
    zmq::message_t message(size);
    snprintf((char *) message.data(), size ,
             "%i %f %f %f",id, lat, lon, alt);
    publisher_fotos.send(message);
    printf("Peticion: ");
    std::cout << std::string(static_cast<char*>(message.data()), message.size()) << std::endl;

    publisher_fotos.recv (&reply);
    printf("Respuesta: ");
    std::cout << std::string(static_cast<char*>(reply.data()), reply.size()) << std::endl;
}

