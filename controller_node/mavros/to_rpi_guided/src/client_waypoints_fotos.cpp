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

std::vector<waypoint_str> client_waypoints_fotos::get_waypoints()
{
    std::cout << "esperando waypoints " << std::endl;
    std::vector<waypoint_str> map;
    zmq::message_t request;
    //  Wait for next request from client
    this->subscriber.recv(&request);

    std::string isss(static_cast<char*>(request.data()));
    double latitude, longitude;
    std::istringstream iss(isss);
    std::vector<std::string> waypoints;
    std::copy(std::istream_iterator<std::string>(iss),
              std::istream_iterator<std::string>(),
              back_inserter(waypoints));        //isss >> latitude >> longitude;

    bool vigilancia = false;
    bool monitor = false;
    int radio = 0;
    int i = 0;
    for (std::vector<std::string>::iterator it = waypoints.begin() ; it != waypoints.end(); ++it){
        std::string ss = *it;
        if(i==0){
            if(ss == "v"){
                vigilancia = true;
                std::cout << "vigilancia" << std::endl;
            }else if(ss == "m"){
                monitor = true;
                std::cout << "monitoreo" << std::endl;
            }
            i++;
        }else{
            if(vigilancia){
                if(i==1){
                    size_t index = 0;
                    while (true) {
                        /* Locate the substring to replace. */
                        index = ss.find(",", index);
                        if (index == std::string::npos) break;

                        /* Make the replacement. */
                        ss.replace(index, 1, " ");

                        /* Advance index forward so the next iteration doesn't pick it up as well. */
                        index += 1;
                    }
                    std::vector<std::string> latlong;
                    std::istringstream isss(ss);
                    std::copy(std::istream_iterator<std::string>(isss),
                              std::istream_iterator<std::string>(),
                              back_inserter(latlong));        //isss >> latitude >> longitude;

                    double lati, longi;
                    std::string::size_type sz;     // alias of size_t
                    std::string::size_type sz_2;     // alias of size_t
                    lati = std::stod (latlong.at(0),&sz);
                    longi = std::stod (latlong.at(1),&sz_2);

                    waypoint_str wp(lati, longi, 0, true);
                    map.push_back(wp);
                    i++;
                }else{
                    radio = std::stoi(ss);
                    waypoint_str radiostr(radio,radio,radio,true);
                    map.push_back(radiostr);
                    printf("Radio %i\n", radio);
                }
            }else if(monitor){
                size_t index = 0;
                while (true) {
                    /* Locate the substring to replace. */
                    index = ss.find(",", index);
                    if (index == std::string::npos) break;

                    /* Make the replacement. */
                    ss.replace(index, 1, " ");

                    /* Advance index forward so the next iteration doesn't pick it up as well. */
                    index += 1;
                }
                std::vector<std::string> latlong;
                std::istringstream isss(ss);
                std::copy(std::istream_iterator<std::string>(isss),
                          std::istream_iterator<std::string>(),
                          back_inserter(latlong));        //isss >> latitude >> longitude;

                double lati, longi;
                std::string::size_type sz;     // alias of size_t
                std::string::size_type sz_2;     // alias of size_t
                lati = std::stod (latlong.at(0),&sz);
                longi = std::stod (latlong.at(1),&sz_2);

                waypoint_str wp(lati, longi, 0);
                map.push_back(wp);
            }
        }
    }

    if(vigilancia){
        std::cout << "Misión de vigilancia" << std::endl;
    }else if(monitor){
        for (std::vector<waypoint_str>::iterator it_w = map.begin() ; it_w != map.end(); ++it_w){
            waypoint_str wp = *it_w;
            std::cout << std::setprecision(10) << "lat : " << wp.latitude
                      << ", long : " << wp.longitude
                      << ", alt: " << wp.altitude
                      << std::endl;
        }

        std::cout << "map size " << map.size() << std::endl;
    }

    return map;
}

bool client_waypoints_fotos::validar_waypoints(std::istringstream waypoints_ss) {
    //método que valide que hemos recibido unos waypoints válidos

    //uno a uno validamos y si son buenos,
    // std::tuple<float,float> waypoint(lat,long)
    // this->waypoints.push (waypoint)
    return false;
}