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

class client_waypoints_fotos {

public:

    client_waypoints_fotos(std::string identity, std::string ip_gcs)
            : identity(identity),
              ip_gcs(ip_gcs),
              context(1),
              subscriber(this->context,ZMQ_SUB)
            {
                std::cout << "Constructor client waypoints fotos" << std::endl;
                //me conecto al ip+puerto del gcs porque es donde va a publicar
                //todos los waypoints
                this->subscriber.connect("tcp://192.168.0.10:5558");

                //filtro por mi "identidad" para coger sólo los que me tocan
                const char *filter = identity.c_str();
                this->subscriber.setsockopt(ZMQ_SUBSCRIBE,filter,strlen(filter));

                std::cout << "Conectado receiver al socket con filtro" << std::endl;
            }

    void receive(); //método que escuche a la estación base y reciba waypoints

    bool validar_waypoints(std::istringstream waypoints_ss);

    //bool waypoints_listos

    std::vector<std::tuple<float,float>> get_waypoints();

private:

    std::string identity; //nuestra identidad
    std::string ip_gcs; //IP:puerto

    std::vector<std::tuple<float,float>> waypoints;
    bool waypoints_recibidos = false;

    zmq::context_t context;
    zmq::socket_t subscriber;


};
