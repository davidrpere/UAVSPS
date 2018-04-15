#include <cstdlib>

#include <ros/ros.h>

#include <mavros_msgs/CommandBoolRequest.h>
#include <mavros_msgs/CommandBoolResponse.h>
#include <mavros_msgs/CommandCode.h>

#include <mavros_msgs/CommandBool.h>
#include <mavros_msgs/CommandTOL.h>
#include <mavros_msgs/SetMode.h>

#include <mavros_msgs/WaypointList.h>
#include <mavros_msgs/WaypointClear.h>
#include <mavros_msgs/WaypointPush.h>
#include <mavros_msgs/Waypoint.h>
#include <mavros_msgs/WaypointPushRequest.h>
#include <mavros_msgs/WaypointPushRequest.h>


#include <sensor_msgs/NavSatFix.h>
#include <std_msgs/Float64.h>
#include <sensor_msgs/Imu.h>

//Nuestras clases
#include "client_waypoints_fotos.h"
#include "publisher_gps_fotos.h"
#include "apm_modes.h"

std::string localhost_5557 = "tcp://*:5557";
publisher_gps_fotos publisher("Grillito", localhost_5557);

std::string ip_gcs = "tcp://192.168.4.16";
client_waypoints_fotos cliente("Pepito", ip_gcs);

std::vector<std::string> modes;

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

void gps_callback(const sensor_msgs::NavSatFix::ConstPtr& msg){
    ROS_INFO("POS : lat:%f, long:%f, alt:%f", msg->latitude, msg->longitude, msg->altitude);
    publisher.publish(msg->latitude, msg->longitude, msg->altitude); //TODO implementar en zmq
}

void compass_callback(const std_msgs::Float64& msg){
    ROS_INFO("Heading : %f", msg.data);
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

    //vector_wayp_str = client_waypoints_fotos.get_waypoints(); //TODO implementar en zmq
    for (std::vector<waypoint_str>::iterator it = vector_wayp_str.begin(); it != vector_wayp_str.end(); ++it) {
        waypoint_str wp = *it;
        mavros_msgs::Waypoint waypoint;
        waypoint.x_lat = wp.latitude;
        waypoint.y_long = wp.longitude;
        waypoint.z_alt = wp.altitude;
        waypoint.frame = mavros_msgs::Waypoint::FRAME_GLOBAL;
        waypoint.command = mavros_msgs::CommandCode::NAV_WAYPOINT;
        waypoint.is_current = false;
        waypoint.autocontinue = false;
        vector_waypoints_mavros.push_back(waypoint);
    }

    return vector_waypoints_mavros;
};

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

void takeoff(ros::ServiceClient takeoff_cl, ros::NodeHandle n){
    mavros_msgs::CommandTOL srv_takeoff;
    srv_takeoff.request.altitude = 10;
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

int main(int argc, char **argv)
{
    ////////////////////////////////////
    ///////////INICIALIZACIÓN///////////
    ////////////////////////////////////

    ros::init(argc, argv, "uavsps_guided");
    ros::NodeHandle n;
    modes = uavsps::set_map_modes();

    /////////////SUBSCRIBERS/////////////
    //GPS
    ros::Subscriber sub_gps = n.subscribe("/mavros/global_position/global", 1, gps_callback);
    //COMPASS
    ros::Subscriber sub_compass = n.subscribe("/mavros/global_position/compass_hdg", 1, compass_callback);
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
    /////////////////////////////////////


    ///////////////COMANDOS///////////////
    ros::ServiceClient land_cl = n.serviceClient<mavros_msgs::CommandTOL>("/mavros/cmd/land");



    //////////////////////////////////////
    ///////////ESPERA_WAYPOINTS///////////
    //////////////////////////////////////

    ros::Rate r(1);
    ros::spinOnce();

    //Esperamos mientras no se limpie la lista de waypoints
    while(1){
        if(clear_waypoints(clear_wayps_cl, n)){
            break;
        }else{
            usleep(1000000);
            continue;
        }
    }

    ros::spinOnce();

    //Creamos request waypoints
    mavros_msgs::WaypointPush pushRequest;

    std::vector<mavros_msgs::Waypoint> vector_waypoints_mavros = get_waypoints(); //TODO implementar en el bucle tras init

    for(std::vector<mavros_msgs::Waypoint>::iterator it = vector_waypoints_mavros.begin();
        it != vector_waypoints_mavros.end(); ++it){
        ROS_INFO("Waypoint");
        mavros_msgs::Waypoint waypoint = *it;
        pushRequest.request.waypoints.push_back(waypoint);
    }

    usleep(10000000);

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

    //ARM
    arm(arming_cl, n);

    //AUTO
    set_mode(n, modes.at(uavsps::AUTO));

    while(ros::ok()){
        ros::spin();
    }

    //RTL

    /*usleep(5000000);
    set_mode(n, modes.at(uavsps::GUIDED));
    usleep(5000000);
    set_mode(n, modes.at(uavsps::AUTO));
    usleep(5000000);
    set_mode(n, modes.at(uavsps::STABILIZE));
     */

    /*
    ros::ServiceClient cl = n.serviceClient<mavros_msgs::SetMode>("/mavros/set_mode");
    mavros_msgs::SetMode srv_setMode;
    srv_setMode.request.base_mode = 0;
    srv_setMode.request.custom_mode = "GUIDED";
    srv_setMode.request.MAV_MODE_AUTO_ARMED
    if(cl.call(srv_setMode)){
        ROS_INFO("setmode send ok %d value:", srv_setMode.response.mode_sent);
    }else{
        ROS_ERROR("Failed SetMode");
        return -1;
    }
     */
    ros::spin();


    return 0;
    /*
    //Todo de aquí abajo es pseudocódigo

    bool obtenidos_waypoints = false;

    while(!obtenidos_waypoints)
    {

         * publisher.publish()
         *
         * if(cliente.waypoints_listos){
         *  std::vector<...> = cliente.getwaypoints
         *
         *  obtenidos_waypoints = true
         *  }
         *  else
         *  {
         *  sleep
         *  continue
         *  }
    }

    //cargo waypoints
    //armo sistema
    //activo modo guided
    //despego
    //while(1){
    // publisher.publishgps
    // if(waypoint_reached){
    //
    //  take_photo()
    //  publisher.publish_photo()
    //  if(next waypoint){}else return to home
    // }else{
    //   usleep 100 ms
    //  }
    //
    // }

    //Me suscribo a GPS y según o los obtengo llamo a publisher.publish en bucle
    //Espero a obtener mis waypoints mientras sigo publicando

    ////////////////////////////////////////////
    /////////////////GUIDED/////////////////////
    ////////////////////////////////////////////
    ros::ServiceClient cl = n.serviceClient<mavros_msgs::SetMode>("/mavros/set_mode");
    mavros_msgs::SetMode srv_setMode;
    srv_setMode.request.base_mode = 0;
    srv_setMode.request.custom_mode = "GUIDED";
    if(cl.call(srv_setMode)){
        ROS_ERROR("setmode send ok %d value:", srv_setMode.response.mode_sent);
    }else{
        ROS_ERROR("Failed SetMode");
        return -1;
    }

    ////////////////////////////////////////////
    ///////////////////ARM//////////////////////
    ////////////////////////////////////////////
    ros::ServiceClient arming_cl = n.serviceClient<mavros_msgs::CommandBool>("/mavros/cmd/arming");
    mavros_msgs::CommandBool srv;
    srv.request.value = true;
    if(arming_cl.call(srv)){
        ROS_ERROR("ARM send ok %d", srv.response.success);
    }else{
        ROS_ERROR("Failed arming or disarming");
    }

    ////////////////////////////////////////////
    /////////////////TAKEOFF////////////////////
    ////////////////////////////////////////////
    ros::ServiceClient takeoff_cl = n.serviceClient<mavros_msgs::CommandTOL>("/mavros/cmd/takeoff");
    mavros_msgs::CommandTOL srv_takeoff;
    srv_takeoff.request.altitude = 10;
    srv_takeoff.request.latitude = 0;
    srv_takeoff.request.longitude = 0;
    srv_takeoff.request.min_pitch = 0;
    srv_takeoff.request.yaw = 0;
    if(takeoff_cl.call(srv_takeoff)){
        ROS_ERROR("srv_takeoff send ok %d", srv_takeoff.response.success);
    }else{
        ROS_ERROR("Failed Takeoff");
    }

    ////////////////////////////////////////////
    /////////////////DO STUFF///////////////////
    ////////////////////////////////////////////
    sleep(10);

    ////////////////////////////////////////////
    ///////////////////LAND/////////////////////
    ////////////////////////////////////////////
    ros::ServiceClient land_cl = n.serviceClient<mavros_msgs::CommandTOL>("/mavros/cmd/land");
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

    while (n.ok())
    {
        ros::spinOnce();
        r.sleep();
    }

    return 0;*/
}


