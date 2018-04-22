//
// Created by David Rodriguez Pereira on 14/4/18.
//

#ifndef MAVROS_APM_MODES_H
#define MAVROS_APM_MODES_H

namespace uavsps{

        std::string modo_STABILIZE = "STABILIZE";
        std::string modo_ACRO = "ACRO";
        std::string modo_ALT_HOLD = "ALT_HOLD";
        std::string modo_AUTO = "AUTO";
        std::string modo_GUIDED = "GUIDED";
        std::string modo_LOITER = "LOITER";
        std::string modo_RTL = "RTL";
        std::string modo_CIRCLE = "CIRCLE";
        std::string modo_POSITION = "POSITION";
        std::string modo_LAND = "LAND";
        std::string modo_OF_LOITER = "OF_LOITER";
        std::string modo_DRIFT = "DRIFT";
        std::string modo_SPORT = "SPORT";
        std::string modo_FLIP = "FLIP";
        std::string modo_AUTOTUNE = "AUTOTUNE";
        std::string modo_POSHOLD = "POSHOLD";
        std::string modo_BRAKE = "BRAKE";
        std::string modo_THROW = "THROW";
        std::string modo_AVOID_ADSB = "AVOID_ADSB";
        std::string modo_GUIDED_NOGPS = "GUIDED_NOGPS";

        enum enum_modos{
            STABILIZE = 0,
            ACRO = 1,
            ALT_HOLD = 2,
            AUTO = 3,
            GUIDED = 4,
            LOITER = 5,
            RTL = 6,
            CIRCLE = 7,
            POSITION = 8,
            LAND = 9,
            OF_LOITER = 10,
            DRIFT = 11,
            SPORT = 12,
            FLIP = 13,
            AUTOTUNE = 14,
            POSHOLD = 15,
            BRAKE = 16,
            THROW = 17,
            AVOID_ADSB = 18,
            GUIDED_NOGPS = 19
        };

    std::vector<std::string> set_map_modes(){
            std::vector<std::string> modes;
            modes.push_back(modo_STABILIZE);
            modes.push_back(modo_ACRO);
            modes.push_back(modo_ALT_HOLD);
            modes.push_back(modo_AUTO);
            modes.push_back(modo_GUIDED);
            modes.push_back(modo_LOITER);
            modes.push_back(modo_RTL);
            modes.push_back(modo_CIRCLE);
            modes.push_back(modo_POSITION);
            modes.push_back(modo_LAND);
            modes.push_back(modo_OF_LOITER);
            modes.push_back(modo_DRIFT);
            modes.push_back(modo_SPORT);
            modes.push_back(modo_FLIP);
            modes.push_back(modo_AUTOTUNE);
            modes.push_back(modo_POSHOLD);
            modes.push_back(modo_BRAKE);
            modes.push_back(modo_THROW);
            modes.push_back(modo_AVOID_ADSB);
            modes.push_back(modo_GUIDED_NOGPS);
            return modes;
    };

};


#endif //MAVROS_APM_MODES_H
