//
// Created by David Rodriguez Pereira on 9/4/18.
//

#include "publisher_gps_fotos.h"

void publisher_gps_fotos::publish(int id, double latitud, double longitud, double altitud) {
    int size=0;
	size=sizeof(id)+sizeof(latitud)+sizeof(longitud)+sizeof(altitud)+3;
	zmq::message_t message(size);
    snprintf((char *) message.data(), size ,
        "%i %f %f %f",id, latitud, longitud, altitud);
    this->publisher.send(message);

}

void publisher_gps_fotos::publish() {
    //Publicamos nuestras cosas

}

Json publisher_gps_fotos::run(){
    while(1){



        //publicar
        this->publish();

        usleep(500000); //dormir 0.5 segundos

        if(photo){
            //this->publish(blabla imagen);
        }

        usleep(500000); //dormir 0.5 segundos

    }
}
