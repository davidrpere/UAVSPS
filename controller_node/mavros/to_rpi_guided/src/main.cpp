#include <cstdlib>

#include <ros/ros.h>

#include <mavros_msgs/CommandBoolRequest.h>
#include <mavros_msgs/CommandBoolResponse.h>
#include <mavros_msgs/CommandCode.h>
#include <mavros_msgs/CommandBool.h>
#include <mavros_msgs/CommandTOL.h>
#include <mavros_msgs/CommandHome.h>

#include <mavros_msgs/ParamPull.h>
#include <mavros_msgs/ParamPush.h>
#include <mavros_msgs/ParamGet.h>
#include <mavros_msgs/ParamSet.h>

#include <mavros_msgs/SetMode.h>

#include <mavros_msgs/WaypointList.h>
#include <mavros_msgs/WaypointClear.h>
#include <mavros_msgs/WaypointPush.h>
#include <mavros_msgs/Waypoint.h>
#include <mavros_msgs/WaypointPushRequest.h>
#include <mavros_msgs/WaypointPushRequest.h>

#include <std_msgs/UInt16.h>
#include <std_msgs/Float64.h>

#include <sensor_msgs/NavSatFix.h>
#include <sensor_msgs/Imu.h>

//Nuestras clases
#include "client_waypoints_fotos.h"
#include "publisher_gps_fotos.h"
#include "apm_modes.h"
#include "structs.h"

int dron_id = 1;
int heading = 0;

double current_lat;
double current_long;
double current_alt;

std::string localhost_5557 = "tcp://*:5557";
publisher_gps_fotos publisher("Grillito", localhost_5557, 1);

std::string localhost_5560 = "tcp://*:5560";
publisher_gps_fotos publisher_heading("Grillito", localhost_5560, 2);

std::string puerto_waypoints = "tcp://*:5558";
client_waypoints_fotos cliente("Pepito", puerto_waypoints);

std::vector<std::string> modes;
std::vector<mavros_msgs::Waypoint> mission;

void gps_callback(const sensor_msgs::NavSatFix::ConstPtr& msg){
    ROS_INFO("POS : lat:%f, long:%f, alt:%f", msg->latitude, msg->longitude, msg->altitude);
    current_lat = msg->latitude;
    current_long = msg->longitude;
    current_alt = msg->altitude;
    publisher.publish(msg->latitude, msg->longitude, msg->altitude); //TODO implementar en zmq
    //publisher.publish(msg->latitude, msg->longitude, msg->altitude, heading);
}

void compass_callback(const std_msgs::Float64& msg){
    ROS_INFO("Heading : %f", msg.data);
    publisher_heading.publish((int)msg.data);
    heading = (int)msg.data;
    //publisher.publish_heading(msg.data); //TODO implementar en zmq
}

void waypointlist_callback(const mavros_msgs::WaypointList& msg){
    for(int i = 0; i<msg.waypoints.size(); i++){
        std::cout << msg.waypoints[i] << std::endl;
    }
}

void chatterCallback(const sensor_msgs::Imu::ConstPtr& msg){
    ROS_INFO("\nlinear acceleration\
                 \nx: [%f]\ny:[%f]\nz:[%f]", msg->linear_acceleration.x,
             msg->linear_acceleration.y, msg->linear_acceleration.z);
}

void wp_reached_callback(const std_msgs::UInt16& msg){
    std::cout << "evento wp reached " << std::endl;
    ROS_INFO("\nreached waypoint %f", msg.data);
    mavros_msgs::Waypoint wp = mission.at(msg.data);
    publisher.publish_foto(dron_id, wp.x_lat, wp.y_long, wp.z_alt);
}

int set_mode(ros::NodeHandle n, std::string modo){
    ros::ServiceClient cl = n.serviceClient<mavros_msgs::SetMode>("/mavros/set_mode");
    mavros_msgs::SetMode srv_setMode;
    srv_setMode.request.base_mode = 0;
    srv_setMode.request.custom_mode = modo;
    if(cl.call(srv_setMode)){
        ROS_INFO("setmode send ok %d value:", srv_setMode.response.mode_sent);
        return 0;
    }else{
        ROS_ERROR("Failed SetMode");
        return -1;
    }
}

std::vector<mavros_msgs::Waypoint> get_waypoints(void)
{
    std::vector<mavros_msgs::Waypoint> vector_waypoints_mavros;
    std::vector<waypoint_str> vector_wayp_str;

    //As plantas video
    /*vector_wayp_str.push_back(waypoint_str(42.1692962646484375,-8.68889617919921875));
    vector_wayp_str.push_back(waypoint_str(42.1880607604980469,-8.66829776763916016));
    vector_wayp_str.push_back(waypoint_str(42.1880607604980469,-8.66848373413085938));
    vector_wayp_str.push_back(waypoint_str(42.1880607604980469,-8.668670654296875));
    vector_wayp_str.push_back(waypoint_str(42.1880607604980469,-8.66885662078857422));
    vector_wayp_str.push_back(waypoint_str(42.1879005432128906,-8.66885662078857422));
    vector_wayp_str.push_back(waypoint_str(42.1879005432128906,-8.668670654296875));*/


    //As plantas
    /*
    vector_wayp_str.push_back(waypoint_str(42.1882026360702653, -8.66902828216552734, 0));
    vector_wayp_str.push_back(waypoint_str(42.1882463580565101, -8.66884589195251465, 0));
    vector_wayp_str.push_back(waypoint_str(42.1882821305682256, -8.6686474084854126, 0));
    vector_wayp_str.push_back(waypoint_str(42.1883179030596907, -8.66844892501831055, 0));
    vector_wayp_str.push_back(waypoint_str(42.1881827624301735, -8.6683952808380127, 0));
    vector_wayp_str.push_back(waypoint_str(42.1880714699300938, -8.6683577299118042, 0));
    vector_wayp_str.push_back(waypoint_str(42.1879562024913213, -8.66832554340362549, 0));
    vector_wayp_str.push_back(waypoint_str(42.187852859091663, -8.66829872131347656, 0));
    vector_wayp_str.push_back(waypoint_str(42.1877654145446144, -8.66825580596923828, 0));
    vector_wayp_str.push_back(waypoint_str(42.1877137427099527, -8.66843819618225098, 0));
    vector_wayp_str.push_back(waypoint_str(42.187685919396877, -8.66863667964935303, 0));
    vector_wayp_str.push_back(waypoint_str(42.1876541213097909, -8.66882443428039551, 0));
    vector_wayp_str.push_back(waypoint_str(42.1877972125757168, -8.66888880729675293, 0));
    vector_wayp_str.push_back(waypoint_str(42.1879323540294706, -8.66894781589508057, 0));
    vector_wayp_str.push_back(waypoint_str(42.1880436467744531, -8.66900146007537842, 0));
    vector_wayp_str.push_back(waypoint_str(42.1880913436051941, -8.66877079010009766, 0));
    vector_wayp_str.push_back(waypoint_str(42.1881310909366434, -8.66856694221496582, 0));
    vector_wayp_str.push_back(waypoint_str(42.188015823606591, -8.66852939128875732, 0));
    vector_wayp_str.push_back(waypoint_str(42.1879045308126095, -8.6685025691986084, 0));
    vector_wayp_str.push_back(waypoint_str(42.1878727328354941, -8.66866350173950195, 0));
    vector_wayp_str.push_back(waypoint_str(42.1879760762026592, -8.66872251033782959, 0));
    vector_wayp_str.push_back(waypoint_str(42.1879760762026592, -8.66872251033782959, 0));

*/
    //Carregal
    /*
    vector_wayp_str.push_back(waypoint_str(41.9886834477315674,-8.70498061180114746,0));
    vector_wayp_str.push_back(waypoint_str(41.9875390971587592,-8.70479285717010498,0));
    vector_wayp_str.push_back(waypoint_str(41.9880853576637776,-8.70351612567901611,0));
    vector_wayp_str.push_back(waypoint_str(41.9885598429115419,-8.70369851589202881,0));
    vector_wayp_str.push_back(waypoint_str(41.9884003524665417,-8.70418131351470947,0));
    vector_wayp_str.push_back(waypoint_str(41.9884442123787593,-8.70455145835876465,0));
    vector_wayp_str.push_back(waypoint_str(41.9884442123787593,-8.70455145835876465,0));
    */
    //vector_wayp_str = client_waypoints_fotos.get_waypoints(); //TODO implementar en zmq
    int i = 0;
    for (std::vector<waypoint_str>::iterator it = vector_wayp_str.begin(); it != vector_wayp_str.end(); ++it) {
        waypoint_str wp = *it;
        mavros_msgs::Waypoint waypoint;
        waypoint.x_lat = wp.latitude;
        waypoint.y_long = wp.longitude;
        waypoint.z_alt = wp.altitude;
        waypoint.frame = mavros_msgs::Waypoint::FRAME_GLOBAL;
        waypoint.command = mavros_msgs::CommandCode::NAV_WAYPOINT;
        waypoint.is_current = false;
        waypoint.autocontinue = false;        if(i==0){
            waypoint.command = 82;
        }
        vector_waypoints_mavros.push_back(waypoint);
        i++;
    }

    return vector_waypoints_mavros;
};

std::vector<mavros_msgs::Waypoint> convert_waypoints(std::vector<waypoint_str> waypoints_struct){
    std::vector<mavros_msgs::Waypoint> vector_waypoints_mavros;
    int i = 0;
    for (std::vector<waypoint_str>::iterator it = waypoints_struct.begin(); it != waypoints_struct.end(); ++it) {
        std::cout << "bucle convert_waypoints " << std::endl;
        waypoint_str wp = *it;
        mavros_msgs::Waypoint waypoint;
        waypoint.x_lat = wp.latitude;
        waypoint.y_long = wp.longitude;
        waypoint.z_alt = wp.altitude;
        waypoint.frame = mavros_msgs::Waypoint::FRAME_GLOBAL;
        /*
         * waypoint.z_alt = 0;
         * waypoint.frame = mavros_msgs::Waypoint::FRAME_GLOBAL_REL_ALT;
         * */
        waypoint.command = mavros_msgs::CommandCode::NAV_WAYPOINT;
        waypoint.is_current = false;
        waypoint.autocontinue = false;
        if(i==0){
            waypoint.command = 82;
        }
        vector_waypoints_mavros.push_back(waypoint);
        i++;
    }
    return vector_waypoints_mavros;
}

bool clear_waypoints(ros::ServiceClient clear_wayps, ros::NodeHandle n){
    mavros_msgs::WaypointClear clearRequest;
    if(clear_wayps.call(clearRequest)){
        ROS_INFO("Vaciada lista de waypoints.");
        return true;
    }else{
        ROS_INFO("No se pudo vaciar la lista de waypoints.");
        return false;
    }
};

void land(ros::ServiceClient land_cl, ros::NodeHandle n){
    mavros_msgs::CommandTOL srv_land;
    srv_land.request.altitude = 10;
    srv_land.request.latitude = 0;
    srv_land.request.longitude = 0;
    srv_land.request.min_pitch = 0;
    srv_land.request.yaw = 0;
    if(land_cl.call(srv_land)){
        ROS_INFO("srv_land send ok %d", srv_land.response.success);
    }else{
        ROS_ERROR("Failed Land");
    }
}

void arm(ros::ServiceClient arming_cl, ros::NodeHandle n){
    mavros_msgs::CommandBool srv;
    srv.request.value = true;
    if(arming_cl.call(srv)){
        ROS_ERROR("ARM send ok %d", srv.response.success);
    }else{
        ROS_ERROR("Failed arming or disarming");
    }
}

void takeoff(ros::ServiceClient takeoff_cl, ros::NodeHandle n, int altitud){
    mavros_msgs::CommandTOL srv_takeoff;
    srv_takeoff.request.altitude = altitud;
    srv_takeoff.request.latitude = 0;
    srv_takeoff.request.longitude = 0;
    srv_takeoff.request.min_pitch = 0;
    srv_takeoff.request.yaw = 0;
    if(takeoff_cl.call(srv_takeoff)){
        ROS_ERROR("srv_takeoff send ok %d", srv_takeoff.response.success);
    }else{
        ROS_ERROR("Failed Takeoff");
    }
}

void set_home(ros::ServiceClient sethome_cl){
    mavros_msgs::CommandHome sethome_cmd;
    sethome_cmd.request.current_gps = true;
    if (sethome_cl.call(sethome_cmd))
    {
        ROS_INFO("Home was set to new value");
    }
    else
    {
        ROS_ERROR("Home position couldn't been changed");
    }
}

void spin_for(int seconds){
    for(int i = 0; i<seconds; i++){
        usleep(1000000);
        ros::spinOnce();
    }
}

void set_circle_parameters(ros::ServiceClient param_get_cl, ros::ServiceClient param_set_cl, double radius, double rate){
    mavros_msgs::ParamGet pget;
    pget.request.param_id = "CIRCLE_RADIUS";
    if(param_get_cl.call(pget)){
        ROS_INFO("OK");
        mavros_msgs::ParamValue pvalget = pget.response.value;
        printf("Real %f integer %i", pvalget.real, pvalget.integer);
    }else{
        ROS_ERROR("NOP");
    }

    mavros_msgs::ParamSet pset;
    pset.request.param_id = "CIRCLE_RADIUS";
    pset.request.value.real = radius; // cm, entre 0 y 10000
    if(param_set_cl.call(pset)){
        ROS_INFO("SET CIRCLE RADIUS OK");
        mavros_msgs::ParamValue pvalset = pset.response.value;
        printf("Real %f integer %i", pvalset.real, pvalset.integer);
    }else{
        ROS_ERROR("SET CIRCLE RADIUS FAILURE");
    }

    pset.request.param_id = "CIRCLE_RATE";
    pset.request.value.real = rate; // deg/s, entre -90 y 90
    if(param_set_cl.call(pset)){
        ROS_INFO("SET CIRCLE RATE OK");
        mavros_msgs::ParamValue pvalset = pset.response.value;
        printf("Real %f integer %i", pvalset.real, pvalset.integer);
    }else{
        ROS_ERROR("SET CIRCLE RATE FAILURE");
    }
}

int main(int argc, char **argv)
{
    ////////////////////////////////////
    ///////////INICIALIZACIÓN///////////
    ////////////////////////////////////

    ros::init(argc, argv, "uavsps_guided", ros::init_options::AnonymousName);
    ros::NodeHandle n;

    modes = uavsps::set_map_modes();
    /////////////SUBSCRIBERS/////////////
    //GPS
    ros::Subscriber sub_gps = n.subscribe("/mavros/global_position/global", 1, gps_callback);
    //COMPASS
    ros::Subscriber sub_compass = n.subscribe("/mavros/global_position/compass_hdg", 1, compass_callback);
    //Waypoint reached
    ros::Subscriber sub_wp_reached = n.subscribe("/mavros/mission/reached", 1, wp_reached_callback);
    //IMU
    //ros::Subscriber sub_imu = n.subscribe("/mavros/imu/data", 1000, chatterCallback);
    //WAYPOINTS (No probado ?)
    //ros::Subscriber get_wayps = n.subscribe("/mavros/mission/waypoints", 1, waypointlist_callback);
    /////////////////////////////////////
    ///////////SERVICE CLIENTS///////////
    //Limpiar waypoints
    ros::ServiceClient clear_wayps_cl = n.serviceClient<mavros_msgs::WaypointClear>("/mavros/mission/clear");
    //Enviar waypoints
    ros::ServiceClient set_wayps_cl = n.serviceClient<mavros_msgs::WaypointPush>("/mavros/mission/push");
    //Armar
    ros::ServiceClient arming_cl = n.serviceClient<mavros_msgs::CommandBool>("/mavros/cmd/arming");
    //Despegar
    ros::ServiceClient takeoff_cl = n.serviceClient<mavros_msgs::CommandTOL>("/mavros/cmd/takeoff");
    //Set home
    ros::ServiceClient sethome_cl = n.serviceClient<mavros_msgs::CommandHome>("/mavros/cmd/set_home");
    /////////////////////////////////////
    ///////////////COMANDOS///////////////
    ros::ServiceClient land_cl = n.serviceClient<mavros_msgs::CommandTOL>("/mavros/cmd/land");

    ros::ServiceClient param_pull_cl = n.serviceClient<mavros_msgs::ParamPull>("/mavros/param/pull");
    ros::ServiceClient param_push_cl = n.serviceClient<mavros_msgs::ParamPush>("/mavros/param/push");

    ros::ServiceClient param_get_cl = n.serviceClient<mavros_msgs::ParamGet>("/mavros/param/get");
    ros::ServiceClient param_set_cl = n.serviceClient<mavros_msgs::ParamSet>("/mavros/param/set");


    //////////////////////////////////////
    ///////////ESPERA_WAYPOINTS///////////
    //////////////////////////////////////

    ros::Rate r(1);

    //SET MODE GUIDED
    set_mode(n, modes.at(uavsps::GUIDED));

    spin_for(30);

    //Esperamos mientras no se limpie la lista de waypoints
    while(1){
        if(clear_waypoints(clear_wayps_cl, n)){
            break;
        }else{
            spin_for(1);
            continue;
        }
    }

    set_home(sethome_cl);
    spin_for(10);

    //Creamos request waypoints
    mavros_msgs::WaypointPush pushRequest;

    std::vector<waypoint_str> vector_waypoints_custom;

    vector_waypoints_custom = cliente.get_waypoints(); //Bloqueante
    mavros_msgs::Waypoint mission_sethome;
    mission_sethome.command = mavros_msgs::CommandCode::CMD_DO_SET_HOME;
    pushRequest.request.waypoints.push_back(mission_sethome);

    //std::vector<mavros_msgs::Waypoint> vector_waypoints_mavros = convert_waypoints(vector_waypoints_custom);
    //std::vector<mavros_msgs::Waypoint> vector_waypoints_mavros = get_waypoints();

    std::vector<mavros_msgs::Waypoint> vector_waypoints_mavros;

    if(vector_waypoints_custom.at(0).vigilancia){
        int radio = vector_waypoints_custom.at(1).altitude;
        set_circle_parameters(param_get_cl, param_set_cl, radio, 20);
        mavros_msgs::Waypoint waypoint;
        waypoint.x_lat = vector_waypoints_custom.at(0).latitude;
        waypoint.y_long = vector_waypoints_custom.at(0).longitude;
        waypoint.z_alt = vector_waypoints_custom.at(0).altitude;
        waypoint.frame = mavros_msgs::Waypoint::FRAME_GLOBAL;
        waypoint.command = 201;
        waypoint.param1 = 10;
        waypoint.is_current = false;
        waypoint.autocontinue = false;
        vector_waypoints_mavros.push_back(waypoint);
        pushRequest.request.waypoints.push_back(waypoint);

        waypoint.command = mavros_msgs::CommandCode::NAV_LOITER_TURNS;
        vector_waypoints_mavros.push_back(waypoint);
        pushRequest.request.waypoints.push_back(waypoint);


    }else {
        vector_waypoints_mavros = convert_waypoints(vector_waypoints_custom);
        for(std::vector<mavros_msgs::Waypoint>::iterator it = vector_waypoints_mavros.begin();
            it != vector_waypoints_mavros.end(); ++it){
            ROS_INFO("Waypoint");
            mavros_msgs::Waypoint waypoint = *it;
            pushRequest.request.waypoints.push_back(waypoint);
        }
        mission = vector_waypoints_mavros;
    }

    mavros_msgs::Waypoint mission_rtl;
    mission_rtl.command = mavros_msgs::CommandCode::NAV_RETURN_TO_LAUNCH;
    pushRequest.request.waypoints.push_back(mission_rtl);

    spin_for(10);

    //usleep(1000);
    ////////////////////////////////////
    ///////////SET__WAYPOINTS///////////
    ////////////////////////////////////

    if(set_wayps_cl.call(pushRequest)){
        ROS_INFO("Waypoint cargado ");
    }else{
        ROS_INFO("NOOOOOO");
    }


    ////////////////////////////////////
    ///////////////MISIÓN///////////////
    ////////////////////////////////////

    //SET MODE GUIDED
    set_mode(n, modes.at(uavsps::GUIDED));

    std::cout << "En espera durante 3 minutos..." << std::endl;
    spin_for(180);

    //ARM
    std::cout << "vamos a aarmarla siuuu" << std::endl;
    arm(arming_cl, n);

    spin_for(1);

    int altitud = 10; //metros

    takeoff(takeoff_cl, n, altitud);

    spin_for(10);

    //AUTO
    set_mode(n, modes.at(uavsps::AUTO));

    int i = 0;
    while(ros::ok()){
        i++;
        spin_for(1);
        if(i==5){
            i=0;
            publisher.publish_foto(dron_id, current_lat, current_long, current_alt);
        }
    }

    ros::spin();
    return 0;
}


