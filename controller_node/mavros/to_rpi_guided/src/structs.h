//
// Created by David Rodriguez Pereira on 17/4/18.
//

#ifndef MAVROS_STRUCTS_H
#define MAVROS_STRUCTS_H

struct waypoint_str{
public:
    waypoint_str(double p1, double p2, double p3){
        this->latitude = p1;
        this->longitude = p2;
        this->altitude = p3;
    }
    double latitude;
    double longitude;
    double altitude;
};

#endif //MAVROS_STRUCTS_H
