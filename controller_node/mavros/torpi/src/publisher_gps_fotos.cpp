//
// Created by David Rodriguez Pereira on 9/4/18.
//

#include "publisher_gps_fotos.h"

void publisher_gps_fotos::publish(int latitud, int longitud, int altitud) {

    srandom ((unsigned) time (NULL));
    zmq::message_t message(20);

    //Formato al azar, tenemos que ponerlo de forma que quepan
    //nuestros datos
    snprintf((char *) message.data(), 20 ,
        "%d %d %d", latitud, longitud, altitud);

    publisher.send(message);

    std::cout << "Creado objeto mensaje " << std::endl;



    this->publisher.send(message);

}

void publisher_gps_fotos::publish() {
    //Publicamos nuestras cosas
}

void publisher_gps_fotos::run(){
    while(1){

        //obtener posición gps

        //publicar
        this->publish();

        usleep(500000); //dormir 0.5 segundos

        if(photo){
            //this->publish(blabla imagen);
        }

        usleep(500000); //dormir 0.5 segundos

    }
}

