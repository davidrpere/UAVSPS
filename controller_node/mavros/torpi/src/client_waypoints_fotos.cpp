//
// Created by David Rodriguez Pereira on 9/4/18.
//

#include "client_waypoints_fotos.h"


void client_waypoints_fotos::receive() {

    while(!waypoints_recibidos)
    {
        zmq::message_t waypoints_update_from_gcs;

        this->subscriber.recv(&waypoints_update_from_gcs);

        std::istringstream waypoints_ss(static_cast<char *>
                               (waypoints_update_from_gcs.data()));

        //haced lo que queráis con ese istringstream, se convierte
        //a lo que más os guste y se valida
        //if(this->validar_waypoints(waypoints_ss)){
        //    this->waypoints_recibidos = true;
        //}else continue;

        usleep(5000000); //duermo 5 segundos
    }

}

bool client_waypoints_fotos::validar_waypoints(std::istringstream waypoints_ss) {
    //método que valide que hemos recibido unos waypoints válidos

    //uno a uno validamos y si son buenos,
    // std::tuple<float,float> waypoint(lat,long)
    // this->waypoints.push (waypoint)
    return false;
}

std::vector<std::tuple<float,float>> client_waypoints_fotos::get_waypoints(){
    if(this->waypoints_recibidos){
        return this->waypoints;
    } else{
        std::vector<std::tuple<float,float>> vacio;
        return vacio;
    }
};