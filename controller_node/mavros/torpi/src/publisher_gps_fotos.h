//
// Created by David Rodriguez Pereira on 9/4/18.
//

#include <string>

#include <vector>
#include <thread>
#include <memory>
#include <functional>

#include <zmq.hpp>
#include "zhelpers.hpp"

class publisher_gps_fotos {

public:

    publisher_gps_fotos(std::string identity, std::string ip_gcs)
            : identity(identity),
              ip_gcs(ip_gcs),
              context(1),
              publisher(this->context,ZMQ_PUB)
    {
        std::cout << "Constructor server gps fotos" << std::endl;
        this->context = zmq::context_t(1);
        this->publisher = zmq::socket_t(this->context, ZMQ_PUB);
        this->publisher.bind(ip_gcs.c_str());
        std::cout << "Conectado publisher al socket" << std::endl;

        //pthread create (thread-parameters, blabla, this->run(), blabla)
    }

    void publish(int id,double latitud, double longitud, double altitud);

    void publish();

    //void publish(blabla imagen);

    void run();
    //Hay que lanzarlo en un hilo
    //Tiene que poder acceder a las variables privadas de la clase

private:

    std::string identity; //nuestra identidad
    std::string ip_gcs; //IP:puerto

    bool photo = false;
    //imagenrpi *imagen;

    zmq::context_t context;
    zmq::socket_t publisher;


};
