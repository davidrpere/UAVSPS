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

    publisher_gps_fotos(std::string identity, std::string ip_gcs, int contexto)
            : identity(identity),
              ip_gcs(ip_gcs),
              context(contexto),
              publisher(this->context,ZMQ_PUB),
              publisher_fotos(this->context, ZMQ_REQ)
    {
        std::cout << "Constructor server gps fotos" << std::endl;
        this->publisher.bind(ip_gcs.c_str());
        this->publisher_fotos.connect("tcp://127.0.0.1:8081");
        std::cout << "Conectado publisher al socket" << std::endl;
    }

    void publish(double latitud, double longitud, double altitud);

    void publish(double latitud, double longitud, double altitud, int heading);

    void publish(int heading);

    //void publish(blabla imagen);

    void publish_foto(int id, double lat, double lon, double alt);

private:

    std::string identity; //nuestra identidad
    std::string ip_gcs; //IP:puerto

    bool photo = false;
    //imagenrpi *imagen;

    zmq::context_t context;
    zmq::socket_t publisher;
    zmq::socket_t publisher_fotos;

};
