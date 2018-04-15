//
// Created by David Rodriguez Pereira on 9/4/18.
//

#include "client_waypoints_fotos.h"


void client_waypoints_fotos::receive() {

    while(!waypoints_recibidos)
    {
        zmq::message_t update;
        subscriber.recv(&update);

		std::string strJson =std::string(static_cast<char*>(update.data()), update.size())	;
		Json::Value waypoints_ss; // en waypoints_ss se guardan los Waypoints en formato JSON (no sé bien como se deben validar ni como me los van a mandar)
    	Json::Reader reader;
		reader.parse(strJson.c_str(),waypoints_ss);
    	Json::FastWriter fastwriter;
        if(this->validar_waypoints(waypoints_ss)){
            this->waypoints_recibidos = true;
        }else continue;

        usleep(5000000); //duermo 5 segundos
    }

}

bool client_waypoints_fotos::validar_waypoints(Json::Value waypoints_ss) {
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
